# 0012: The quantities of a task are recorded in its brief

**Decision:** A brief closes with a Cost block that the owner fills when the task ends, and a memory file may carry an Estimate line with its uncertainty and date.

**Status:** accepted, 2026-11-04. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- Every practice of the method lacked the same thing: the tokens, dollars, minutes and output of a task were not recorded, so no choice between tiers, batches or caps could be weighed by cost.
- The brief is the one file that already exists for each task, so a second place for the quantities would break one place per fact.
- A number kept in memory for later use, such as how long a step takes, was written without its doubt or its age.

## Decision

- The brief gains a last part, Cost, with four lines in order: Tokens, Dollars, Minutes (the person's) and Produced.
- A value is a number with its unit, `pending` while the task is open, or `not measured`. It is never guessed.
- Cost is optional by default, since an open task has none; `[brief] cost = "required"` makes it mandatory for a repository that wants it.
- The memory shapes gain an optional `**Estimate:**` line: a number, its uncertainty in parentheses and a date. `memory-source` refuses one without them.
- Rejected: a separate cost file per task; making Cost mandatory at once, which would refuse every open brief.

## Consequences

- A program can sum the quantities of a set of tasks from their briefs alone.
- **Bad:** the numbers are written by the owner, so they are only as good as the owner's meter. The check reads the form, not the truth.
- No principle is added: the grade of recording costs is a convention until a use of the numbers is measured.

## See also

[Decisions](README.md); [record 0008](0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md), which this record extends; [the brief shape](../shapes/brief.md).
