# 0014: A brief names the commit it starts from and the shapes to read

**Decision:** Decided may carry two optional lines: the repository and commit the task starts from, and the shapes its
result follows. Their form is read by `brief-checks`, and the runner prepares the worktree and the reading.

**Status:** accepted as a temporary decision, 2026-11-12: used as final until confirmed or replaced, as
[issue 2](https://github.com/Tewf/ai-augmented-project/issues/2) says. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- A brief named a folder by its path only; the folder was on a closed prototype, and the worker built on it. Workers
  also wrote to shapes they had not read, and each refusal of the gate cost a round trip (2026-11-12).
- A brief has postconditions, its Checks, and no precondition.
- The comparison of six options, with the evidence, is the design document
  [A brief names the state its task starts from](../design/brief-start-state.md).

## Decision

- Two optional lines in Decided, a Starts from line and a Shapes to read line, written as the shape's skeleton shows.
- The start is a commit, never a branch: the family pins by commit, and the field names a task's code by its base
  commit (Jimenez 2024).
- `brief-checks` reads their form; `[brief] start = "required"` makes Starts from mandatory for a repository that
  wants it.
- The runner's part is made in the runner, outside this repository (12 Nov.): a worktree at the commit, on a new
  branch, and the reading told before the first write. The design document says how.
- Rejected, each with its reason in the design document:
  - a branch in place of the commit, the first text of this record (12 Nov.);
  - the Starts from line with no runner change, which states the start and does not make it;
  - git asked by `brief-checks` whether the commit exists, where the repository is often not reachable;
  - a fifth part for preconditions, and the commit checked as a first Check;
  - leaving the reading to the gate, and the shapes' text put in the prompt.
  - a branch resolved to a commit by the runner at dispatch, and a default start per repository in config.
  - a machine-readable field in place of the line, and the line required by default for every brief.

## Consequences

- The worker is started at the named commit and told to read its shapes before writing; what
  it does in the worktree afterwards is not constrained.
- **Bad:** a runner that does not read the lines only states them, and its worker may still work in the folder as it is.
- **Bad:** the need rests on what one night showed: one worker built on the wrong branch, and several were refused by the shape gate, on one night (2026-11-12). No run compares briefs with and without the lines.
- **Bad:** the check reads the form, not that the commit exists; the runner finds a missing commit only at launch.
- **Bad:** temporary: the reasons and what would close the question are in [issue 2](https://github.com/Tewf/ai-augmented-project/issues/2).

## See also

[Decisions](README.md); [the design document](../design/brief-start-state.md); [the brief shape](../shapes/brief.md);
[record 0012](0012-the-quantities-of-a-task-are-recorded-in-its-brief.md).
