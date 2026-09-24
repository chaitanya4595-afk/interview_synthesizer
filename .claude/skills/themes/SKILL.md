---
name: themes
description: Groups findings from all interview extracts into themes. Use after the extract skill has run on every transcript.
---

# Find themes across all interviews

## Input
Read every file in work/extracts/. Do not read the raw transcripts; work only from the extracts.

## Steps
1. List every claim from every extract, keeping its interview id and quote.
2. Group the claims into 4 to 6 themes that do not overlap. Each claim belongs to one theme only.
3. For each theme, count how many interviews support it and how many push against it.
4. Pick the 2 or 3 strongest quotes per theme, copied exactly from the extracts.
5. Find where interviewees clearly disagree with each other.

## Output
Write work/themes.md in this format:

# Themes
## Theme 1: <headline as a full sentence stating the insight>
Support: N interviews [INTxx, INTxx] | Against: N [INTxx]
Key quotes:
* "<exact quote>" [INTxx]
Why it matters for the case question: <one sentence>

(repeat for each theme)

## Conditions for success
List every condition any interviewee says must be true for the plan to work.
* <condition>: raised by [INTxx, INTxx]. "<exact quote>" [INTxx]. Numbers: <any figures given>


## Where interviewees disagree
* <topic>: [INTxx] says ..., while [INTxx] says ...

## Rules
* Themes are ranked by how much they matter to the case question, not by count alone.
* A theme supported by only one interview must be labeled "Single source".
* Never add quotes or numbers that are not in the extracts.
* Support and against counts come only from quoted claims, never from the stance line.