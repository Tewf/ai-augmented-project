# The start file holds what the code cannot say

**Claim:** the start file holds the commands, the non-standard conventions, the precedence sentence and one pointer per kind of task, within a bound of lines, and no overview of the repository.

- **Grade:** supported with caveat. A generated overview did not help and cost over 20% more; a developer-written file helped by 2.4% on average, not significantly (Gloaguen 2026, measured). The bound of 200 lines is a convention, from vendors' practice.
- **Evidence:** [review](../../evidence/human-ai-teaming/review.md), strand 2; [state of the art](../../evidence/human-ai-teaming/state-of-the-art.md), question 2; [design](../../design/one-project.md), decision 2; [record 0004](../../decisions/0004-a-short-start-file-and-an-index.md).
- **Check:** `start-file`: four headings in order, none empty, at most the bound of lines, each command in backticks.
- **Reader styles:** none.

## What it asks

- The file is `START.md` at the project root. Its headings are `Commands`, `Conventions`, `Precedence` and `Pointers`, in that order.
- It states nothing the code states, and no tour of the repository.
- It stays within a bound, set in configuration and tagged PROVISIONAL. Past the bound, a line goes before another is added.

## Why

- Files help to state non-standard practice and are followed. Repository overviews did not help (Gloaguen 2026).
- A second ablation found no measurable move over 288 runs (Khatri 2026, secondary), so the file earns its place only by what the code cannot say.
- One vendor sets a target under 200 lines (Anthropic 2026b). No study sets a length.

## Limits

- The bound is a guess until measured. The check enforces the number, not the value of a line.
- Two studies of context files disagree on the size of the effect, and both are preprints.
- Whether a line states something the code does not is a judgment. The program cannot decide it.
