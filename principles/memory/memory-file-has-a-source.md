# A memory file has a source

**Claim:** each memory file records its date, its type and a source that a program can follow, and a rule is a proposal until the person accepts it.

- **Grade:** convention, untested. No controlled study of notes that a model writes for a project was found.
- **Evidence:** [review](../../evidence/human-ai-teaming/review.md), strand 3 (Anthropic 2026b; Treude 2026; Luo 2026); [state of the art](../../evidence/human-ai-teaming/state-of-the-art.md), question 3; [design](../../design/one-project.md), decision 3; [record 0005](../../decisions/0005-memory-is-plain-files-with-a-source.md).
- **Check:** `memory-source`: the three fields are present, the type is allowed, a rule has a status, and a source that is a path exists.
- **Reader styles:** none.

## What it asks

- One fact per file, in the memory folder only.
- Three labelled lines: `**Date:**`, `**Type:**` and `**Source:**`. The source is a path, a command in backticks, or an identifier.
- A file of type rule also has `**Status:**`, which is `proposal` or `accepted`. The person accepts it.

## Why

- Without a source, a note cannot be audited. A model that audits its own memory fails the rule that it decides nothing unchecked.
- The audit found in practice is a consistency check of text against the code (Treude 2026). It needs something to follow.
- One vendor keeps notes as plain local files that the person can edit (Anthropic 2026b).

## Limits

- The check follows a path. It does not run a command or look up an identifier, so those are checked for presence only.
- The age of a file, and the weekly list of files not checked, are not built.
- The evidence is a vendor's practice and a roadmap, not a measured effect.
