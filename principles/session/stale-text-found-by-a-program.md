# Stale text is found by a program

**Claim:** every path that an instruction names is looked up by a program on every commit, so a line that points at nothing is found, not trusted.

- **Grade:** supported with caveat. Stale references appear in 23.0% of 356 repositories (Treude 2026, secondary). That a path lookup finds the stale lines that matter is untested.
- **Evidence:** [review](../../evidence/human-ai-teaming/review.md), strands 2 and 3 (Treude 2026; Xu 2026); [state of the art](../../evidence/human-ai-teaming/state-of-the-art.md), question 3; [design](../../design/one-project.md), decision 2.
- **Check:** `start-file-stale`: each path in the `Commands` and `Pointers` parts exists.
- **Reader styles:** none.

## What it asks

- A path in backticks, in the commands or the pointers of the start file, names a file or folder that exists.
- A path that is made at run time, such as a folder the checks extract into, is listed in configuration as exempt.
- A line that fails is stale. The person decides, or the model fixes it and the check passes. The program deletes nothing.

## Why

- A model obeys a stale file over the code (Xu 2026). Finding the stale line costs a lookup.
- The audit that exists in practice is a consistency check of the file against the code (Treude 2026).

## Limits

- The check looks up paths only. It does not run the commands, which the design asks for and which is not built.
- A path that exists can still describe the wrong thing. The lookup finds absence, not error.
- The rate of 23.0% is for documentation of agent configuration in one sample of repositories.
