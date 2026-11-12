# A brief names the state its task starts from

- **Decision asked.** Should a brief name its start as a repository and a commit, and its required reading as links,
  for the runner to prepare both before the worker starts? The maintainer decides. The brief-shape part can be
  accepted alone; the runner part waits for the tooling's owner.
- **Status.** Proposed, 2026-11-12.
- **Shape:** [design document](https://github.com/Tewf/reader-ergonomics-software-design/blob/e0bc14cdae3494513c3470b4faea7c2278829311/shapes/design-document.md)

**Summary.**

- A brief has postconditions, its Checks, and no precondition: nothing says what the task starts from.
- Two failures on one night came from that gap: a worker built on the wrong branch, and workers wrote to shapes they
  had not read.
- The field and this family both answer the first the same way: a task's code is named by a commit, never a branch,
  and the harness checks it out, not the worker.
- So a brief gains two optional lines in Decided, `Starts from` and `Shapes to read`, and the runner acts on them.

## Motivation

- Use case: a lead hands a review to a worker with a path. The folder was checked out on a closed prototype; the
  worker built on it, and three files had to be corrected (one case, 2026-11-12).
- Use case: workers name a Shape line for a shape they have not read; the shape gate refuses the write, and each
  refusal costs a read and a rewrite (several cases, 2026-11-12).
- The brief shape holds no place for either fact. Its four parts judge the result, never the start
  ([record 0008](../decisions/0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md)).

## Goals and non-goals

- Goal: the worker starts on the code the lead meant, whatever the folder held before.
- Goal: the worker has read the shapes its result follows before its first write.
- Goal: both are done by a program, at the start, not checked by a reader after the fact.
- Non-goal: proving the worker understood a shape; the shape's own checks judge the result.
- Non-goal: a new part of the brief; the four parts and every check that reads them stay as they are.
- Non-goal: changing the runner tonight; it is in use by other sessions.

## Design

Two optional lines in Decided:

```markdown
- Starts from: `<repository path or URL>` at `<commit>`
- Shapes to read: [<shape>](<link pinned by commit>), [<shape>](<link>)
```

- **Starts from** names a commit, seven to forty hexadecimal characters. A branch is where the result lands, written
  elsewhere in Decided as before; it is not the start, since a branch moves.
- **Shapes to read** links each shape the result follows, pinned by commit as every Shape line already is.
- `brief-checks` reads their form when present: a path and a commit, joined by "at"; at least one link to a `.md` file.
  `[brief] start = "required"` makes Starts from mandatory for a repository that wants it.
- The runner (here `agent-api`; in the workshop service, its dispatcher) acts on them, in a later change:
  - for Starts from, it makes a worktree at that commit and starts the worker there, and refuses to start when the
    commit is not found;
  - for Shapes to read, it tells the worker to read those files before its first write, as the
    [editor extension](../README.md) already does for the start file.

## Alternatives

| Option | Consequences | Why it lost |
|---|---|---|
| A. `Checkout: <path> on <branch>`, form checked (the first proposal, record 0014's first text) | names the branch the worker must be on | a branch moves, so the line does not fix the start; the family pins by commit, never by branch ([reader-ergonomics README](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/README.md), "Pin a release") |
| B. Starts from, form checked, no runner change | the brief says the commit; the worker must check it out | half the fix: a worker can still read the line and work in the folder as it is |
| C. A fifth part, Preconditions, with commands the runner runs | general: any start condition, not only the commit | moves the four parts every check reads; the one precondition seen is the commit, so a general part is not yet earned |
| D. The worker checks the commit itself, as a first Check | no new line | a Check judges the result; run first, it is a precondition in a postcondition's place, and nothing runs it before the work |
| E. Leave (b) to the gate, which already names the file to read | no change | each refusal costs a round trip; telling the worker first costs one sentence in the runner |
| F. The runner puts the shapes' text in the prompt | no read needed | the gate counts a shape as read only from a tool result, so text in the prompt would still be refused |

## Where the design comes from

| Part | Evidence | Grade |
|---|---|---|
| A start named by commit | SWE-bench names each task's codebase "by it's base commit" and its harness checks it out (Jimenez 2024, full text, pages 2 and 16); later benchmarks bind each instance to a base commit (Xie 2026, abstract) | convention of the field, adopted |
| The same in this family | pin by commit, never by branch ([reader-ergonomics README](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/README.md)); a precondition stated before the steps ([contract before steps](https://github.com/Tewf/reader-ergonomics-software-design/blob/e0bc14cdae3494513c3470b4faea7c2278829311/principles/specification/contract-before-steps.md)) | convention |
| The harness, not the worker, prepares the start | SWE-bench's harness; a project-owned agent regenerates code inside the receiving project's environment (Zhang 2026b, abstract) | convention |
| Reading handed over before the first turn | a retrieval-derived initial context gave higher file F1 with less exploration than random context (Qin 2026, abstract, a pilot); told to, the editor extension's model read the start file before its first text in 5 of 5 sessions for each of two models ([spike](https://github.com/Tewf/ai-augmented-ide/blob/master/spike/RESULTS.md)) | measured, small |

## Consequences

- Drawbacks: two more lines a lead may forget; the lines are optional, so the failure stays possible where they are
  absent.
- Risks: a commit named in a brief may be garbage-collected or never pushed; the runner's refusal makes that visible.
- Compatibility: every brief already written passes; `[brief] start = "required"` is off by default.
- Security: a worktree outside the user's folder reduces what the worker can reach by accident.

## Feasibility and plan

- Shown to work by: SWE-bench's harness for the start; the editor extension's spike for reading first.
- Tested by: four unit tests of `brief-checks` for the two lines' form.
- Rolled out by: the brief-shape part on its branch, then record 0014 accepted; the runner part as a change of its
  own, by the tooling's owner, after the night's lanes end.

## Open questions

- Whether a whole preconditions part (option C) earns its place once more than one kind of start condition is seen.
- Whether the runner should also refuse a worker whose first write comes before its reading.
