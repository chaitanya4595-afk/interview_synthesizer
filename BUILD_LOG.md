# Build log

## 2026-09-23: themes v2
* Themes v1 counted INT02 as against Theme 1 using its stance line ("overdue"), not a quoted claim.
* Added a rule to the themes skill: support and against counts come only from quoted claims, never from the stance line.
* In v2, INT02's quotes actually support staging ("do it category by category", "let the stores that are ready go first"), so INT02 moved to support on Theme 1.

## 2026-09-23: number check false positives
* check_quotes.py read interview ids like INT08 as the number 08, which caused 11 false failures in the number check.
* The checker now skips interview ids, bracketed or inline, before checking numbers.

## 2026-09-23: v1.0
* v1.0 runs end to end with /synthesize in 6 min 50 s.
* Overstated claims fell from 8 of 23 to 4 of 29.
* Quotes 101/101 and numbers 36/36 verified.
* Known issues for v1.1:
  * Every theme shows "Against: 0".
  * The memo omits the disagreements in themes.md.
  * The 25% target is a judgment call flagged for human review.

## 2026-09-24: rule made the themes step drop a disagreement
* A themes rule said every disagreement must appear as an Against count in at least one theme.
* To satisfy it, the themes step dropped a real disagreement it could not count (what drives shoppers away).
* The rule now says to keep every real disagreement, even if it doesn't map to an Against count, and never to remove one to satisfy a counting rule.

## 2026-09-24: v1.1
* Note: These numbers come from a partial rerun (themes onward, same session as the previous critic review), not a clean /synthesize run. A clean timed run will be recorded with the demo video.
* Run finished 2026-09-24 12:39 EDT. Partial run: reused the v1.0 extracts and reran themes, memo, check_quotes.py and the critic. Run time was not measured, so it is not comparable to v1.0's 6 min 50 s.
* Themes skill fix: headlines are written before counting; each interview counts once per theme as Support, Mixed or Against; every real disagreement stays in the disagreements section.
* Themes now show dissent: Theme 2 Mixed [INT04], Theme 3 Against [INT02], Theme 5 Mixed [INT02].
* The memo names and quotes both sides on the pace of doubling and on what drives shoppers away.
* Quotes 105/105 and numbers 33/33 verified (v1.0: 101/101 and 36/36).
* Critic verdicts, v1.0 to v1.1:
  * Supported: 20 to 22
  * Thin: 5 to 9
  * Overstated: 4 to 1
  * Unsupported: 0 to 0
  * Total claims: 29 to 32
* Known issues for v1.2:
  * The critic says dissent is still undercounted, partly because each claim belongs to one theme only.
  * One Overstated claim: the memo says starting in frozen vegetables "clashes" with dairy and frozen capacity.
  * The answer gives no target number or time frame. The 25% target was dropped because it came from a peer benchmark.
  * themes.md leaves out the case for growing (19% against a peer average of about 25%, and a discounter taking about 9% of transactions), so the memo cannot use it.
