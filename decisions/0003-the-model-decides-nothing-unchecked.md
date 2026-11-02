# 0003: The model decides nothing unchecked

**Decision:** A program decides what a program can check, the person decides the rest, and the model drafts and proposes without deciding anything that no check or person has seen.

**Status:** proposed, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/b9732b9814c71768f722691f3c5049ec2b8ed378/shapes/decision-record.md).

## Context

- Human-AI teams scored below the better of person and model alone on average, and lost most on tasks that decide (Vaccaro 2024).
- A model repairs its own output poorly without outside feedback (Huang 2024; Olausson 2024).
- The blueprint already gives this answer for reasoning; the question was whether it holds for a whole project.

## Decision

- Three owners, in the table of [the design](../design/one-project.md): the person, the machine, the model.
- A draft is kept apart from a decision, and is accepted by a check or by the person.
- The model asks, with options, where no check covers a choice that is the person's.
- Rejected: the model decides low-risk choices; the model reviews its own output; the person decides everything; several models vote.

## Consequences

- The model's help is limited to drafting, proposing and repairing after a failed check.
- **Bad:** more questions reach the person than if the model decided small choices; the measure of decision 4 counts them.

## See also

[Decisions](README.md); [the design document](../design/one-project.md); [record 0002](0002-keep-the-name-and-take-the-practice-as-baseline.md).
