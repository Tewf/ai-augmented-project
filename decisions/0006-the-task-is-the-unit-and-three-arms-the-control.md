# 0006: The task is the unit, and three arms the control

**Decision:** The setup is measured per task by five counts read from logs, and a case must allow a comparison of the person alone, the model alone and both.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- Developers' own estimates of speed were wrong in sign (Becker 2025).
- The test of a team is whether it beats the better of its two members (Vaccaro 2024).
- No study was found that measures round trips or questions asked twice.

## Decision

- Counts: round trips, time, errors caught before a person saw them, questions (new and repeated), and errors that escaped.
- Arms are assigned in an order fixed by a seed; one check decides all three.
- Rejected: self-report; lines or commits; two arms; comparison with another whole setup.

## Consequences

- A claim that the setup works can fail.
- **Bad:** a case triples the work of each task, and one person gives an interval, not a test.

## See also

[Decisions](README.md); [the design document](../design/one-project.md); [record 0002](0002-keep-the-name-and-take-the-practice-as-baseline.md).
