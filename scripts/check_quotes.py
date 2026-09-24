"""Check quotes and numbers in the extracts and memo against their sources.

Quote check:
  * work/extracts/*.md  - the "Exact quote" column, cited to the extract's interview id
  * output/memo.md      - every quote with an [INTxx] citation next to it
  Each quote must appear word for word in the transcript for that id, ignoring
  differences in whitespace, line breaks and curly vs straight quotes.

Number check:
  * every number in an extract claim must appear in that row's quote or Numbers column
  * every number in the memo must appear in some extract quote or claim

Results print to stdout and are written to output/quality_report.md, with quote
and number results in separate sections, failures first.
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_GLOB = os.path.join(ROOT, "input", "*.txt")
EXTRACT_GLOB = os.path.join(ROOT, "work", "extracts", "*.md")
MEMO_PATH = os.path.join(ROOT, "output", "memo.md")
REPORT_PATH = os.path.join(ROOT, "output", "quality_report.md")

CITE_RE = re.compile(r"\[(INT\d+(?:\s*[,–-]\s*INT\d+)*)\]")
ID_RE = re.compile(r"INT\d+")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


def normalize(text):
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    return re.sub(r"\s+", " ", text).strip()


def numbers_in(text):
    """Return the digit numbers in text, e.g. '$4,000 and 6.49%' -> ['4000', '6.49'].

    Interview ids are skipped, whether bracketed ([INT01-INT08]) or inline (INT08 says).
    """
    text = CITE_RE.sub(" ", text)
    text = re.sub(r"\bINT\d+\b", " ", text)
    text = re.sub(r"(?<=\d),(?=\d{3}\b)", "", text)
    return NUMBER_RE.findall(text)


def load_transcripts():
    transcripts = {}
    for path in sorted(glob.glob(INPUT_GLOB)):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        match = re.search(r"^Interview ID:\s*(INT\d+)", text, re.MULTILINE)
        if match:
            transcripts[match.group(1)] = normalize(text)
    return transcripts


def extract_rows():
    """Yield one dict per findings row: source, ids, claim, quote, numbers."""
    for path in sorted(glob.glob(EXTRACT_GLOB)):
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        header = next((l for l in lines if l.startswith("# Extract:")), "")
        ids = ID_RE.findall(header)[:1]
        cols = None
        for line in lines:
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cols is None:
                if "Exact quote" in cells:
                    cols = {name: i for i, name in enumerate(cells)}
                continue
            if set(cells[0]) <= set("-: "):
                continue
            quote = normalize(cells[cols["Exact quote"]])
            if len(quote) >= 2 and quote[0] == '"' and quote[-1] == '"':
                quote = quote[1:-1]
            claim_col = next(i for name, i in cols.items() if name.startswith("Claim"))
            yield {
                "source": f"{os.path.relpath(path, ROOT)} row {cells[0]}",
                "ids": ids,
                "claim": normalize(cells[claim_col]),
                "quote": quote,
                "numbers": cells[cols["Numbers"]] if "Numbers" in cols else "",
            }


def expand_ids(cite):
    """Turn 'INT01, INT03' or 'INT01–INT08' into a list of ids."""
    ids = []
    for part in re.split(r"\s*,\s*", cite):
        bounds = ID_RE.findall(part)
        if len(bounds) == 2:
            lo, hi = (int(b[3:]) for b in bounds)
            ids.extend(f"INT{n:02d}" for n in range(lo, hi + 1))
        else:
            ids.extend(bounds)
    return ids


def memo_quotes():
    """Yield (source, ids, quote) for memo quotes with an [INTxx] next to them.

    The citation is the one right after the quote (only spaces between). If there
    is none, a citation earlier on the same line counts when no other quote or
    sentence end sits between it and the quote.
    """
    with open(MEMO_PATH, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for lineno, raw in enumerate(lines, 1):
        line = normalize(raw)
        for m in re.finditer(r'"([^"]+)"', line):
            ids = []
            after = CITE_RE.match(line, m.end() + len(re.match(r"\s*", line[m.end():]).group()))
            if after:
                ids = expand_ids(after.group(1))
            else:
                before = [c for c in CITE_RE.finditer(line, 0, m.start())]
                if before:
                    gap = line[before[-1].end():m.start()]
                    if '"' not in gap and not re.search(r"[.;!?]\s", gap):
                        ids = expand_ids(before[-1].group(1))
            if ids:
                yield (f"output/memo.md line {lineno}", ids, m.group(1))


def check_quote(transcripts, ids, quote):
    missing = [i for i in ids if i not in transcripts]
    if missing:
        return False, f"no transcript for {', '.join(missing)}"
    if any(quote in transcripts[i] for i in ids):
        return True, ""
    return False, f"not found in {', '.join(ids)}"


def quote_results(transcripts, rows):
    """Return (ok, source, ids, quote, note) for every extract and memo quote."""
    items = [(r["source"], r["ids"], r["quote"]) for r in rows] + list(memo_quotes())
    results = []
    for source, ids, quote in items:
        if not ids:
            results.append((False, source, "?", quote, "no interview id"))
            continue
        ok, why = check_quote(transcripts, ids, quote)
        results.append((ok, source, ", ".join(ids), quote, why))
    return results


def number_results(rows):
    """Return (ok, source, number, context, note) for every number in claims and the memo."""
    results = []
    for r in rows:
        allowed = set(numbers_in(r["quote"])) | set(numbers_in(r["numbers"]))
        for n in numbers_in(r["claim"]):
            ok = n in allowed
            note = "" if ok else "not in this row's quote or Numbers column"
            results.append((ok, r["source"], n, r["claim"], note))

    pool = set()
    for r in rows:
        pool |= set(numbers_in(r["quote"])) | set(numbers_in(r["claim"]))
    with open(MEMO_PATH, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for lineno, raw in enumerate(lines, 1):
        line = normalize(raw)
        for n in numbers_in(line):
            ok = n in pool
            note = "" if ok else "not in any extract quote or claim"
            results.append((ok, f"output/memo.md line {lineno}", n, line, note))
    return results


def rate(results):
    passed = sum(1 for r in results if r[0])
    total = len(results)
    return passed, total, (100.0 * passed / total if total else 0.0)


def table(results, key_header, text_header, quote_text):
    ordered = [r for r in results if not r[0]] + [r for r in results if r[0]]
    out = [
        f"| Result | {key_header} | Source | {text_header} | Note |",
        "|---|---|---|---|---|",
    ]
    for ok, source, key, text, why in ordered:
        cell = text.replace("|", "\\|")
        if quote_text:
            cell = f'"{cell}"'
        out.append(f'| {"PASS" if ok else "FAIL"} | {key} | {source} | {cell} | {why} |')
    return out


def main():
    transcripts = load_transcripts()
    rows = list(extract_rows())
    quotes = quote_results(transcripts, rows)
    numbers = number_results(rows)

    print("Quote check")
    for ok, source, ids, quote, why in quotes:
        note = f"  ({why})" if why else ""
        print(f'{"PASS" if ok else "FAIL"}  [{ids}] {source}: "{quote}"{note}')
    print("\nNumber check")
    for ok, source, n, text, why in numbers:
        note = f"  ({why})" if why else ""
        print(f'{"PASS" if ok else "FAIL"}  {n} in {source}: {text}{note}')

    qp, qt, qr = rate(quotes)
    np_, nt, nr = rate(numbers)
    print(f"\nQuote pass rate:  {qp}/{qt} ({qr:.1f}%)")
    print(f"Number pass rate: {np_}/{nt} ({nr:.1f}%)")

    out = [
        "# Quality report",
        "",
        f"**Quote pass rate:** {qp}/{qt} ({qr:.1f}%)  ",
        f"**Number pass rate:** {np_}/{nt} ({nr:.1f}%)",
        "",
        "## Quote check",
        "",
        "Each quote is checked word for word against its transcript in input/, "
        "ignoring whitespace, line breaks and curly vs straight quotes. Failures first.",
        "",
        *table(quotes, "Interview", "Quote", True),
        "",
        "## Number check",
        "",
        "Every number in an extract claim must appear in that row's quote or Numbers column. "
        "Every number in the memo must appear in some extract quote or claim. Failures first.",
        "",
        *table(numbers, "Number", "Text", False),
    ]
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    return 0 if qp == qt and np_ == nt else 1


if __name__ == "__main__":
    sys.exit(main())
