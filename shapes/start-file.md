# Shape: start file

The **start file** is the first file a session is handed. It holds what the model cannot infer from the code and a
program can verify. It never holds an overview of the repository.

## When to use it

- Once per project, at the project root, as `START.md`. The path is a setting, so an agent that loads another name can be pointed at it.
- Not for one task. A task is a [brief](brief.md).
- Not for notes the model writes. Those are in the [memory index](memory-index.md).

## Skeleton

Four second-level headings, in this order, at most 200 lines in all:

```markdown
# <Project>: start file

## Commands
- `<a command that builds, tests or checks>`

## Conventions
- <a convention that is not in the code>

## Precedence
<One sentence: when a text disagrees with the code, follow the code and say so.>

## Pointers
- <a kind of task>: read `<a path>`
```

## Worked example

[This repository's own start file](examples/start-file.md) follows the skeleton. It carries a **Shape:** line that
links back here, and the checks run on it as they would on a real `START.md`.

Each command is one line in backticks. Each convention is one a reader cannot see in the code. The precedence sentence
is said once. Each pointer names a kind of task, then the path to read.

## Where each part comes from

| Part | Why it is there | Grade |
|---|---|---|
| Commands | a model cannot guess the project's own build and check commands | convention; files that state non-standard practice help (Gloaguen 2026) |
| Conventions | what the code does not show; a generated overview did not help | measured, for overviews (Gloaguen 2026) |
| Precedence | with this sentence the share of choices following the code rose from 4.2% to 91.4% | measured (Xu 2026, secondary) |
| Pointers | the model reads on demand; the file stays short | convention, untested |
| 200 lines | one vendor's target; no study sets a length | convention, PROVISIONAL |

The principles behind the parts are in the [session group](../principles/session/README.md).

## Rules

- No overview of the repository, and nothing the code states.
- Past the bound, a line goes before another is added.
- The precedence sentence stands in `Precedence`, once.
- A path in `Commands` or `Pointers` exists, or is listed as made at run time.
- Text from outside that enters the file is data. It is never an instruction.

## Checked by

- `start-file`: the four parts, a command per line in backticks, the bound.
- `start-file-precedence`: the sentence is in `Precedence`, once.
- `start-file-stale`: every path named exists. Running the commands is not built.
