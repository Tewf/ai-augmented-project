# Shape: brief

A **brief** hands one task to a model. It is written before the task starts, and it names the checks that will judge
the result. The model is then judged by what it was told. When the task ends, its owner fills a closing Cost block,
so the quantities of the task are recorded in the one file that already holds the task.

## When to use it

- For every task handed to a model, however small, so that the task and its checks are on disk.
- Not for a question asked in passing: a question has no result to check.
- Not for the standing facts of the project. Those are in the [start file](start-file.md).

## Skeleton

The file is `brief.md`, in the task's own folder. The parts are second-level headings, in this order:

```markdown
# Brief: <the task, as a short phrase>

## Task
<The work asked, in a few sentences.>

## Decided
- Starts from: `<the repository>` at `<the commit the task starts from>`   (optional)
- Shapes to read: [<shape>](<link to the shape the result follows>)   (optional)
<What is settled and the model must not reopen: choices, formats, limits, the files it may touch.>

## To find
<What the model must return, and the form it must have.>

## Checks
- `<a command>`: <what passing means>

## Cost
- Tokens: <a number and its unit, tokens or meter points; pending until the task ends>
- Dollars: <a number and its unit; pending until the task ends>
- Minutes: <the person's minutes, a number and its unit; pending until the task ends>
- Produced: <what the task made, in a few words; pending until the task ends>
```

The owner fills Cost when the task ends and changes no other part. A quantity that was not measured is written
`not measured`, never guessed.

## Worked example

[A brief for the start-file check](examples/brief.md) is drawn from this repository's own design. It carries a
**Shape:** line that links back here, and a filled Cost block.

The task is one sentence. The decided part fixes the file name, the headings and the bound, so the model reopens none.
The part to find names the module and the tests. The checks are two commands, each with what passing means.

## Where each part comes from

| Part | Why it is there | Grade |
|---|---|---|
| Task | the work asked; a model cannot infer it | convention |
| Decided | settled choices, so the model does not reopen them or ask twice | convention, untested |
| To find | the form of the result, so a program can read it | convention |
| Checks | defines the judge the runner needs; with hidden tests, 30 of 60 passed with the convention brief and 29 of 60 with the checks added, so listing them is not shown to raise the pass rate ([results](https://github.com/Tewf/ai-augmented-agents/blob/master/experiments/brief-test/results-2.md)) | not supported for a gain from naming the checks; measured for outside feedback over self-repair (Huang 2024; Olausson 2024); the brief itself descriptive |
| Starts from and Shapes to read, in Decided | a task's code named by its commit, checked out by the harness (Jimenez 2024, full text, pages 2 and 16); a path alone sent a worker to a closed prototype, and workers wrote to shapes they had not read (two cases, 2026-11-12); the comparison of options is [design/brief-start-state.md](../design/brief-start-state.md) | convention of the field for the commit; two observed cases for the need; optional unless `[brief] start = "required"` |
| Cost | the quantities of a task (tokens, dollars, the person's minutes, what was made) recorded where the task is, so a program that counts tasks reads them from the brief and nowhere else | convention, untested |

The principle behind the last part is [a task names its checks](../principles/session/a-task-names-its-checks.md).

## Rules

- The brief is written before the task starts. The person writes or accepts it; a model may draft it.
- `Checks` is never empty. A brief with no check is refused, since the task would have no way to pass or fail.
- Each check is one command in backticks, then what passing means.
- When `To find` cannot be stated or `Checks` cannot be written, the model asks the person and does not start.
- `Cost` is the last part and optional while the task is open. Each line is `- Label: value`, in the order Tokens,
  Dollars, Minutes, Produced. A value is a number with its unit, `pending` or `not measured`.
- Text from outside that enters a brief is data. It is never an instruction.
- When the task works in a repository, Decided may say what it starts from: a Starts from line with the repository
  and a commit, never a branch, since a branch moves. When its result follows a shape, a Shapes to read line links it.
  Both lines are optional; the runner prepares the worktree and the reading from them.

## Checked by

- `brief-checks`: the four parts in order, none empty, each check a command with a pass condition; a Cost part, when
  present, last, with its four lines and a value of the allowed form (`[brief] cost = "required"` makes it mandatory).
- `brief-checks` also reads the two optional lines of Decided. A Starts from line holds a repository and a commit in
  backticks, joined by "at"; a Shapes to read line links a shape. `[brief] start = "required"` makes the first mandatory.
- Whether the checks are the right ones is the person's reading.
