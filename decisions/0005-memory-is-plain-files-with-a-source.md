# 0005: Memory is plain files, each with a source

**Decision:** Memory is one fact per file in one folder, written by the model in a fixed format, audited by a program that follows each file's source, with one sentence giving the code precedence.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- A stale file was followed in 90.1% of choices; one sentence giving the code precedence raised the share following the code to 91.4% (Xu 2026, secondary).
- Stale references appear in 23.0% of 356 repositories (Treude 2026, secondary).
- No controlled study of a model-written memory or of its audit was found.

## Decision

- The model writes facts in that folder only; a rule that changes behaviour is a proposal until the person accepts it.
- The audit marks a file stale or unchecked and never deletes.
- Rejected: no memory; free writing anywhere; the person only; the model auditing itself; a similarity store.

## Consequences

- A stale memory is found by a program before it is obeyed.
- **Bad:** a fact without a checkable source, such as one about the person, cannot be audited; it is an open question in the design.

## See also

[Decisions](README.md); [the design document](../design/one-project.md); [record 0002](0002-keep-the-name-and-take-the-practice-as-baseline.md).
