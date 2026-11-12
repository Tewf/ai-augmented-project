# 0011: The method is compared with the model alone by a program

**Decision:** A program runs the two arms that need no person, the model alone and the model with the method, on tasks with hidden tests. The two arms that need a person wait for the maintainer.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- [Record 0006](0006-the-task-is-the-unit-and-three-arms-the-control.md) asks for three arms and a program as judge. No arm had been run.
- The brief test found that a brief with its checks lifted a small model's pass rate on cases it was shown, and left open cases it was not shown.
- A program can play the model arms. It cannot play a person, so the person arms need the maintainer.

## Decision

- The experiment is [method-comparison](../experiments/method-comparison/protocol.md): three tasks with hidden tests, two arms, five sessions each, 30 in all, with the protocol written before any session.
- The method arm is a start file, a memory index and a brief, handed over by a note. The alone arm is the task sentence.
- The counts are read from the agent's own database and the judge: pass rate, tokens, turns, questions, files read before the first edit, and whether the start file was read first.
- The person alone and the person with the model are not run, and the results page says so.
- Rejected: asking a model to play the person; judging by a model; a comparison of the model arms only by the brief's own checks.

## Consequences

- The first measure exists: 0 of 15 sessions pass alone and 15 of 15 with the method, on one model and three small tasks ([results](../experiments/method-comparison/results.md)).
- **Bad:** the two arms differ in the information they hold, not only in the shape of the files. The gap shows that a brief with decided facts works, not that the start file or the index helped.
- **Bad:** the design's own test, the team against the better of its members, is still not made.
- The next arms to run are the brief alone and the brief with the same facts in the message.

## See also

[Decisions](README.md); [the protocol](../experiments/method-comparison/protocol.md); [record 0008](0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md).
