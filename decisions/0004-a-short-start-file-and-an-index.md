# 0004: A short start file and a memory index

**Decision:** A session is handed a start file, a memory index and the brief of its task, and nothing else. The file and the index have at most 200 lines each, a provisional bound set in configuration.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/shapes/decision-record.md).

**Amendment, 3 November:** the start file is `START.md` with four headings and the index is `memory/INDEX.md` with one line per file; the brief of the task is the third thing handed over ([0008](0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md)).

## Context

- A generated repository overview did not raise success and cost about 20% more (Gloaguen 2026).
- No study sets a length; a vendor gives under 200 lines as practice (Anthropic 2026b).

## Decision

- The start file holds commands, non-standard conventions, the precedence sentence and one pointer per task type.
- A program checks the bounds and runs each command and path the file names.
- Rejected: nothing; a generated overview; the whole memory; retrieval by similarity.

## Consequences

- A convention not in the code is stated once and checked.
- **Bad:** the bounds are guesses until measured, and the pointers need upkeep.

## See also

[Decisions](README.md); [the design document](../design/one-project.md); [record 0002](0002-keep-the-name-and-take-the-practice-as-baseline.md).
