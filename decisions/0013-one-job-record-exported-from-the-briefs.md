# 0013: One job record, exported from the briefs

**Decision:** The jobs of a project are listed in one TOML file, the trace's `[[job]]` table extended, and an exporter writes it from the briefs.

**Status:** accepted, 2026-11-04. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- Three programs read jobs, each from a file written by hand: the scheduler reads a table of waits and weights, the guide's replay reads a trace, and the cases count from the repositories' history.
- A job's minutes, tokens and dependencies are already in its brief and its Cost block, as [record 0012](0012-the-quantities-of-a-task-are-recorded-in-its-brief.md) decided. Retyping them into three files breaks one place per fact.
- The guide's trace already has a `[[job]]` table with the fields the replay needs. A fourth format would be a second place for them.

## Decision

- The record is the trace's `[[job]]` table, with five new fields: `depends_on`, `minutes`, `date`, `repo` and `outcome`. Every field the trace had is kept, with its meaning.
- This repository owns the format, since it owns the brief: [shapes/job-record.md](../shapes/job-record.md) has the field table, and `checks/local/job_record.py` writes the file from a folder of `*/brief.md`.
- The exporter reads the Cost block and optional header lines of the brief (`**Depends on:**`, `**Repo:**`, `**Kind:**`, `**Outcome:**`). A value that is pending, not measured, absent or in another unit is left out, never guessed.
- Two fields are rules and not readings: `agents` is 1, and `wave` is the rank of the date.
- Each consumer reads what it needs and ignores the rest. The scheduler takes `depends_on` and `minutes` through `--jobs`, the replay reads the extended trace unchanged, and the cases read the file in their shared module.
- Rejected: a new format for the scheduler.
- Rejected: a field for the person's judgment of a job, which stays in the trace by hand.
- Rejected: filling a missing number from a default, which would hide what was not measured.

## Consequences

- A real job's numbers flow from its brief to the plan, the ranking and the count without being retyped.
- **Bad:** the exporter leaves out what the brief does not state.
- A record built from briefs without header lines has no `kind`, and the replay cannot use such a row until the owner adds the line.
- **Bad:** a job with no minutes keeps the scheduler's default weight of 1, so a path mixes minutes and unmeasured jobs. The scheduler's output says how many.
- The grade of recording jobs this way stays a convention until a use of the numbers is measured.

## See also

[Decisions](README.md); [record 0012](0012-the-quantities-of-a-task-are-recorded-in-its-brief.md), which this record builds on; [the job-record shape](../shapes/job-record.md); [the brief shape](../shapes/brief.md).
