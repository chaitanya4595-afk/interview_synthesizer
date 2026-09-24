---
name: synthesize
description: Runs the full interview synthesis pipeline end to end.
disable-model-invocation: true
---

# Run the full pipeline

1. List every .txt file in input/. If there are none, stop and tell the user to add transcripts to input/.
2. Use the extract skill on each file, one at a time.
3. Use the themes skill.
4. Use the memo skill.
5. Run: python scripts/check_quotes.py
6. If any quote or number fails, fix the step that produced it and rerun from that step. Try this once. If it still fails, stop and show the user the failures.
7. Use the critic agent to review output/memo.md.
8. Tell the user, in 6 lines at most: where the memo is, the quote and number pass rates, the critic's verdict counts, and the single most important thing to review by hand.