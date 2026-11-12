# 0014: A brief names its branch and the shapes to read

**Decision:** Decided may carry two labelled lines, the checkout as a path and its branch and the shapes the result
follows, and `brief-checks` reads their form when they are present.

**Status:** proposed, 2026-11-12. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- A brief named a checkout by its path only. The folder was on another branch, a closed prototype, and the worker
  built its review on it; three files had to be corrected (one case, observed on 2026-11-12).
- Workers wrote a Shape line for a shape they had not read, and a gate that refuses such a line cost them a round
  trip each time (observed on the same night, several times).
- The brief shape has no place for either fact; [record 0008](0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md)
  set its four parts, and [record 0012](0012-the-quantities-of-a-task-are-recorded-in-its-brief.md) added Cost.

## Decision

- Two optional lines in Decided: `- Checkout: `<path>` on `<branch>`` and `- Shapes to read: [<name>](<link>)`.
- `brief-checks` reads their form when present; `[brief] checkout = "required"` makes the Checkout line mandatory for a
  repository that wants it.
- Rejected: a fifth part of the brief, which would move the four parts every other check reads; a mandatory line at
  once, which would refuse every brief already written.

## Consequences

- A worker reads where to work and what to read before it writes, in the part it must not reopen.
- **Bad:** the grade is a convention from two cases on one night; no run compares briefs with and without the lines.
- **Bad:** the check reads the form, not that the branch exists or that the worker read the shape.

## See also

[Decisions](README.md); [the brief shape](../shapes/brief.md); [record 0012](0012-the-quantities-of-a-task-are-recorded-in-its-brief.md).
