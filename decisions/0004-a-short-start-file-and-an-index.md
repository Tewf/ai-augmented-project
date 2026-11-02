# 0004: A short start file and a memory index

**Decision:** A session is handed a start file of at most 200 lines and a memory index of at most 200 lines, and nothing else; both bounds are provisional and set in configuration.

**Status:** proposed, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/b9732b9814c71768f722691f3c5049ec2b8ed378/shapes/decision-record.md).

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
