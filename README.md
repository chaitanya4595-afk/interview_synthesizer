# Interview Synthesizer

Turns a folder of interview transcripts into themes and a one-page partner memo in about 7 minutes, with every quote and number checked against the source.

Demo video: _link to come_

## The problem

Consultants synthesize interview transcripts by hand. It is slow, and quotes drift: they get paraphrased, tidied up or attached to the wrong person on the way into the deck.

## How it works

Run `/synthesize` in Claude Code. It runs five steps in order:

1. **Extract**: pulls claims, verbatim quotes and numbers from each transcript into `work/extracts/`.
2. **Themes**: groups the claims into 4 to 6 themes, counts who supports, is mixed on or is against each one, and lists where interviewees disagree (`work/themes.md`).
3. **Memo**: writes a one-page answer to the case question from the themes only (`output/memo.md`).
4. **check_quotes.py**: checks every quote word for word, and every number, against the transcripts (`output/quality_report.md`).
5. **Critic agent**: a separate reviewer scores each claim in the memo as Supported, Thin, Overstated or Unsupported (`output/critic_review.md`).

Each step writes a file so a person can check any stage, and each step can be rerun on its own.

## Results

Test case: 8 synthetic interviews for a fictional grocer deciding whether to double its private label share.

| | v1.0 (clean run) | v1.1 (partial rerun) |
|---|---|---|
| Run time | 6 min 50 s | not measured |
| Quotes verified | 101/101 | 105/105 |
| Numbers verified | 36/36 | 33/33 |
| Critic verdicts (Supported / Thin / Overstated / Unsupported) | 20 / 5 / 4 / 0 | 22 / 9 / 1 / 0 |

The v1.1 numbers come from a rerun from the themes step onward, not a clean `/synthesize` run.

Overstated claims in the memo went from 8 of 23 in the first memo, to 4 of 29 in v1.0, to 1 of 32 in v1.1.

Full history: [BUILD_LOG.md](BUILD_LOG.md).

## What I learned

* **The AI took shortcuts on stance.** The first themes run counted an interviewee as "against" because of the stance summary at the top of their extract, not anything they were quoted saying. Now support and against counts come only from quoted claims.
* **The checker needed checking too.** The number check read interview ids like INT08 as the number 08 and failed correct lines. It now skips ids.
* **A strict rule made the AI hide a disagreement.** A rule said every disagreement must show up as an "against" count. To follow it, the AI dropped a real disagreement it couldn't count. The rule now says to keep every real disagreement, even if it doesn't fit a count.

## Quickstart

1. Install [Claude Code](https://claude.com/claude-code) and Python 3.
2. Clone the repo:
   ```
   git clone https://github.com/chaitanya4595-afk/interview_synthesizer.git
   cd interview_synthesizer
   ```
3. Put your transcripts in `input/` as `.txt` files. Each one starts with a line like `Interview ID: INT01`.
4. Start Claude Code with `claude` and run `/synthesize`.

## Limitations

* All test data is synthetic. It has not been run on real interviews.
* Numbers can be real but misattributed. In v1.0 the memo presented a peer benchmark as one interviewee's recommended target.
* The memo does not yet make the case for growth or give a target number.
* No one other than the author has tested it yet.

## Adapting it

Edit the **Case** and **Topics** sections of [CLAUDE.md](CLAUDE.md) to set your client, case question and topic tags. The rules in CLAUDE.md (verbatim quotes, cite every claim, never invent a quote or number) apply to any case.
