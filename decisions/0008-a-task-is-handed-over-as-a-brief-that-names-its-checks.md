# 0008: A task is handed over as a brief that names its checks

**Decision:** Each task is handed to the model as a file of four parts, written before the task starts. The parts are the task, what is decided, what is to be found, and the checks it is judged by.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/shapes/decision-record.md).

## Context

- Decision 5 of the design has the extension hand a brief to the model, and the method had not defined one.
- The one small run that varied a brief found that adding the checks is what lifted a cheap model's pass rate; the figures are in [the design](../design/one-project.md).
- Decision 4 of the design needs a check written before each task, so the checks already exist when the brief is written.

## Decision

- The brief is `brief.md` in the task's folder, with the headings `Task`, `Decided`, `To find` and `Checks`.
- The checks in the brief are the task's check of decision 4, listed once.
- The person writes or accepts it; a brief with no checks is refused by a program.
- Rejected: a brief of objective, format, tools and limits only; the task typed in chat.

## Consequences

- The model is judged by what it was told, and the task is on disk for the counts.
- **Bad:** one more file per task, and the evidence for the checks part is one small run.

## See also

[Decisions](README.md); [the design document](../design/one-project.md); [record 0004](0004-a-short-start-file-and-an-index.md), which this record amends.
