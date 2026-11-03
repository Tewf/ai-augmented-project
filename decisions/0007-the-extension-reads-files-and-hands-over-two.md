# 0007: The extension reads files and hands over two

**Decision:** The editor extension keeps no state of its own: it shows the files of the design and hands the model the start file, the memory index and the brief of the task.

**Status:** accepted, 2026-11-03, on the maintainer's word to finish, not read line by line. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/b9732b9814c71768f722691f3c5049ec2b8ed378/shapes/decision-record.md).

**Amendment, 3 November:** the interface is ten kinds of file, not six: the topic files, the brief, the judgment answers file and the audit report are added. The title keeps its two, the start file and the index; the brief is the task, not context ([0008](0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md)).

## Context

- A fact kept in two places drifts; the extension is one of two places unless it keeps none.
- The extension is a viewer; routing and memory are decisions of the setup.

## Decision

- The interface is ten kinds of file, with a writer and a reader each ([design](../design/one-project.md)).
- It shows owners, verdicts, bounds, the audit and the counts; it hands over the start file, the index, the brief, a failed check's reason and the log line.
- Rejected: its own store; routing between models; calling a model itself.

## Consequences

- Any other editor can read the same files.
- **Bad:** files are less convenient than a store for the extension's author.

## See also

[Decisions](README.md); [the design document](../design/one-project.md); [record 0002](0002-keep-the-name-and-take-the-practice-as-baseline.md).
