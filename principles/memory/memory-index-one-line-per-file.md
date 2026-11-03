# The memory index has one line per file

**Claim:** the memory index holds one line per memory file, in one form and within a bound, so that a line is one fact's address and a program can count them.

- **Grade:** convention, untested. One vendor caps the index of the notes a model writes (Anthropic 2026b).
- **Evidence:** [review](../../evidence/human-ai-teaming/review.md), strand 3 (Anthropic 2026b); [design](../../design/one-project.md), decision 2; [record 0004](../../decisions/0004-a-short-start-file-and-an-index.md).
- **Check:** `memory-index`: each line has the form, each link resolves, each file is listed once, and the lines stay within the bound.
- **Reader styles:** none.

## What it asks

- The index is `memory/INDEX.md`. Each line reads `- [title](file.md): the hook, in one sentence`.
- A title line and a `**Shape:**` line may open it. They are not counted.
- No memory file in the folder is left out, and none is listed twice.
- The bound is set in configuration and tagged PROVISIONAL.

## Why

- A session is handed the index with the start file. Past the bound the file is skimmed, not read.
- One line per file lets a program count the files and find a link that breaks.

## Limits

- The bound has no study behind it. The vendor value of 200 lines is a practice.
- The program checks the form of a hook, not whether it says what the file holds.
