---
name: extract
description: Extracts structured findings from one interview transcript in input/. Use when asked to process, extract or code an interview.
argument-hint: "[transcript file name]"
---

# Extract findings from one interview

## Input
Read input/$ARGUMENTS. If no file name was given, list the files in input/ and ask which one to process.

## Steps
1. Read the whole transcript before writing anything.
2. Note the interview id and role from the header.
3. Find the claims that matter to the case question in CLAUDE.md. Skip small talk and off topic stories, even vivid ones.
4. For each claim, copy one supporting quote exactly as written. Do not fix grammar, cut words from the middle, or join sentences. A script will later search for each quote word for word.
5. Tag each claim with one topic from CLAUDE.md.
6. Copy any number exactly as said.

## Output
Write work/extracts/<same name as input>.md in this format:

# Extract: INTxx, <role>
Stance on the case question: Supportive | Mixed | Skeptical
Reason for stance: <one sentence>

| # | Claim (one line, your words) | Exact quote | Topic | Numbers |
|---|---|---|---|---|

## Rules
* No quote, no claim.
* 12 claims at most. Pick the ones a partner would care about.