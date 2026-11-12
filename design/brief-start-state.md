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
- Shapes to read: [<shape>](<link to the shape>), [<shape>](<link>)
```

- **Starts from** names a commit, seven to forty hexadecimal characters. A branch is where the result lands, written
  elsewhere in Decided as before; it is not the start, since a branch moves.
- **Shapes to read** links each shape the result follows. The check asks for a link to a `.md` file, not a pinned
  one; pinning the link by commit, as most Shape lines here are, is the lead's choice.
- `brief-checks` reads their form when present: a path and a commit, joined by "at"; at least one link to a `.md` file.
  `[brief] start = "required"` makes Starts from mandatory for a repository that wants it.
- The runner (here `agent-api`; in the workshop service, its dispatcher) acts on them, in a later change:
  - for Starts from, it makes a worktree at that commit and starts the worker there, and refuses to start when the
    commit is not found;
  - for Shapes to read, it tells the worker to read those files before its first write, as the
    [editor extension](../README.md) already does for the start file.

## Alternatives

The table holds the options in the order they were raised; H to K came from reviewers' passes.

| Option | Consequences | Why it lost |
|---|---|---|
| A. `Checkout: <path> on <branch>`, form checked (the first proposal, record 0014's first text) | names the branch the worker must be on | a branch moves, so the line does not fix the start; the family pins by commit, never by branch ([reader-ergonomics README](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/README.md), "Pin a release") |
| B. Starts from, form checked, no runner change | the brief says the commit; the worker must check it out | half the fix: a worker can still read the line and work in the folder as it is |
| C. A fifth part, Preconditions, with commands the runner runs | general: any start condition, not only the commit | moves the four parts every check reads; the one precondition seen is the commit, so a general part is not yet earned |
| D. The worker checks the commit itself, as a first Check | no new line | a Check judges the result; run first, it is a precondition in a postcondition's place, and nothing runs it before the work |
| E. Leave the reading to the shape gate, which already names the file to read | no change | each refusal costs a round trip; telling the worker first costs one sentence in the runner |
| F. The runner puts the shapes' text in the prompt | no read needed | the gate counts a shape as read only from a tool result, so text in the prompt would still be refused |
| G. `brief-checks` asks git whether the commit exists | a program checks the commit, as the family's oracle rule wants | the check runs in CI and on other machines, where the brief's repository is often not reachable; the runner, which has the path, is the program that can tell |
| H. The lead names a branch, and the runner resolves its head to a commit at dispatch and records it | the lead writes no hash; the start is still a commit | the brief is written before dispatch and the branch may move in between, so the worker starts from code the lead did not read; recording the commit afterwards documents the gap, it does not close it |
| I. A default start per repository in config | nothing to write in each brief | the failure seen was a folder on an unexpected branch; a default in config moves the question to config without naming what this task needs |
| J. A machine-readable field, a front-matter block or a TOML key, in place of a line of prose | the runner reads a key, not a pattern | a brief is a page read by a person and a model under four headings; a second format in one file splits it, and the line form is already read exactly by `brief-checks` |
| K. Starts from required by default for every new brief | the failure cannot recur where the line is required | a task with no repository, such as a review, has no start commit; a repository that wants it sets `[brief] start = "required"` |

## Where the design comes from

| Part | Evidence | Grade |
|---|---|---|
| A start named by commit | SWE-bench names each task's codebase "by it's base commit" and its harness checks it out (Jimenez 2024, full text, pages 2 and 16); a later benchmark, PonyEval, binds each instance to a base commit (Xie 2026, abstract) | convention of the field, adopted |
| The same in this family | pin by commit, never by branch ([reader-ergonomics README](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/README.md)); a precondition stated before the steps ([contract before steps](https://github.com/Tewf/reader-ergonomics-software-design/blob/e0bc14cdae3494513c3470b4faea7c2278829311/principles/specification/contract-before-steps.md)) | convention |
| The harness, not the worker, prepares the start | SWE-bench's harness clones the repository and checks out the base commit (Jimenez 2024, full text, page 16); no other source was found | convention, one benchmark |
| Context given before the first turn | a retrieval-derived initial context gave higher file F1 with less exploration than random context (Qin 2026, abstract, a pilot); it measures context handed over, not an instruction to read | measured, small |
| A worker told to read the start file first does | told to, two cloud models read the start file before their first text in 5 of 5 sessions each; two local models did in 0 of 5 and at best 2 of 5 ([spike](https://github.com/Tewf/ai-augmented-ide/blob/a939117921fc6b40af1e6ad6623d0c86967458f8/spike/RESULTS.md), measure 5); reading shapes first was not tested | measured, small, for the start file and the cloud models only |

## Consequences

- Drawbacks: two more lines a lead may forget; the lines are optional, so the failure stays possible where they are
  absent.
- Risks: a commit named in a brief may be garbage-collected or never pushed; the runner's refusal makes that visible.
- Compatibility: every brief already written passes; `[brief] start = "required"` is off by default.
- Security: none known; the runner's worktree is a convenience, not a confinement.

## Feasibility and plan

- Used by: SWE-bench's harness for the start; the editor extension's spike for reading first. No run has tested
  whether the lines prevent the failure; that is the open question below.
- Tested by: the unit tests of `brief-checks` for the two lines' form (class DecidedLinesTests).
- Rolled out by: the brief-shape part on its branch, then record 0014 accepted; the runner part as a change of its
  own, by the tooling's owner, after the night's lanes end.

## Open questions

- Whether briefs with the two lines fail less often than briefs without them, on the same tasks.
- Whether a whole preconditions part (option C) earns its place once more than one kind of start condition is seen.
- Whether the runner should also refuse a worker whose first write comes before its reading.
