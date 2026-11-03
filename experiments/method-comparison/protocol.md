# Protocol: the method against the model alone

Written on 2026-11-03, before any counted session. It says what is run, how it is judged and what the run cannot show.
The numbers are in [results.md](results.md).

## Question

On three small tasks with a program as judge, does handing a coding agent the method of this repository change how
often its code passes hidden tests, and what does it cost in tokens, turns and questions?

The method is a [start file](../../shapes/start-file.md), a [memory index](../../shapes/memory-index.md) and a
[brief](../../shapes/brief.md), handed over by a note. Design decision 6 of [the design](../../design/one-project.md)
asks for three arms: the person alone, the model alone, and both.

## Arms

| Arm | Run here | The agent receives |
|---|---|---|
| person alone | no | waits for the maintainer |
| person with model | no | waits for the maintainer |
| model alone | yes, **alone** | the task sentence, in an empty folder |
| model with the method | yes, **method** | a note, and a folder holding START.md, memory/INDEX.md with two memory files, the brief and its checks |

The person arms need a person. A program cannot play one, so the page says they wait. Nothing here says how a person
compares.

## Tasks

Three tasks of one kind: parse a small Markdown shape into a list. They are the tasks of the brief test in
`ai-augmented-agents` (round two): the scope table, the changelog and the `llms.txt` link list. Their sentences and
Decided lines are kept word for word.

| Task | Function | Module |
|---|---|---|
| scope | `scope_in_rows` | `scope.py` |
| changelog | `changelog_releases` | `changelog.py` |
| llms | `llms_links` | `llms.py` |

Each task has two test sets, in this folder.

- **Visible:** the cases the brief names as its checks, in `fixtures/<task>/checks/test_visible.py`. Only the method arm has them.
- **Hidden:** six to eight cases that no arm sees, in `hidden/<task>.py`. Each follows from the Decided lines alone.

The agent runs in a scratch folder under `/tmp`. The hidden tests never enter it.

## Runs

- The agent is Kilo Code 7.8.18, through its command-line tool, the baseline of [the IDE spike](https://github.com/Tewf/ai-augmented-ide). Its own prompt, tools and permissions are left at their defaults.
- The model is `claude-haiku-5-5`, called with the maintainer's key. The key is passed to the run as an environment variable and is never written, printed or put in a result file.
- Five sessions per task per arm: 3 tasks, 2 arms, 5 runs, **30 sessions**.
- The order is shuffled once with `random.Random(20261103)`, so drift in the service falls on all cells alike.
- Every session starts from a fresh folder and a fresh data directory. Sampling settings are the agent's defaults.
- The alone arm receives the task sentence as the message, and nothing else.
- The method arm receives the message `Start from the attached hand-over note.` and the file [note.md](fixtures/common/.handover/note.md).
- A session that exits with an error before any model reply is retried once. It is counted once, and the retry is logged. A session that fails twice is recorded as an error and left out of the rates.
- Results are appended to `results.jsonl` as each session ends.
- Network access is closed to everything but the model's host: a dead proxy and a one-host exception, as in the spike.

## Judge

A program, never the model: [judge.py](judge.py), tested in [test_judge.py](test_judge.py).

- **Primary: hidden pass.** The function that the task names exists in a Python file at the folder root, and it passes every hidden test within 20 seconds.
- **Secondary: hidden pass without the name.** When no file defines that name and the folder holds exactly one public function, it is judged under the name. The alone arm is not told the name, and this keeps a missing name from deciding the table. It is shown beside the primary, never in its place.
- **Secondary: visible pass,** where the folder has the brief's checks.
- A session that leaves no function, or one that does not import, fails.

## Counts

All from the agent's own database, read after the session: [extract.py](extract.py).

| Count | Definition |
|---|---|
| tokens | the session's five token fields: input, output, reasoning, cache read, cache write; the sum is also shown |
| cost | the agent's own figure in dollars |
| turns | assistant messages in the top-level session |
| questions asked | calls of the agent's question tool, plus lines of assistant text that end with a question mark |
| files read before the first edit | distinct paths opened by a read tool or a shell read (`cat`, `head`, `tail`, `sed`, `less`) before the first write or edit |
| START.md read first | the first tool call of the session opens a file named START.md |

## Predictions

Written now, so the result can disagree with them.

1. The method arm passes the hidden tests more often than the alone arm, mostly because it is told the function and its rules.
2. The method arm spends more tokens per session, since it reads four files first.
3. The agent reads START.md first in most method sessions, since the note names it. This says that the note works, not that the start file does.

## Harness check

Before the counted sessions, one session per arm on a fourth task, reversing a word order in a string, in another
folder. Its purpose is to see that the extract reads the database and that the judge sees the files. These two
sessions are discarded and not counted. Any change they force on the harness is written in `notes.md` of the job.

## What the run cannot say

- **Three tasks of one kind, one model, one agent, one day.** The size of the effect on another task is not measured.
- **The arms differ by more than the method.** The method arm is told the function name, the module, the rules and the checks. The alone arm is told a sentence. The gap measures the information as much as the shape of the files. This run cannot separate them.
- **The note names START.md.** That START.md is read first follows from the note, not from the start file.
- **The tasks are small.** A start file and a memory index exist for projects that a task of fifty lines does not need. A null result here is not a result for a real project.
- **The visible checks are given to one arm only.** A pass of the method arm on the visible tests says that it follows a list.
- **Five sessions per cell** give wide intervals. A gap of one or two sessions is noise. The page shows Wilson intervals.
- **A pass is not quality.** The tests check behaviour on small inputs, not style or robustness.
- **The person arms are not run.** The decision's test, the team against the better of its members, is not made.
- **No cost of writing the files.** The time to write a start file, an index and a brief is not counted.

## Reproduce

```sh
export ANTHROPIC_API_KEY=...   # the key, only in the environment of the run
./run.sh work/run-1            # a scratch folder; reads results.jsonl and resumes where it stopped
python3 -m unittest test_judge # the judge's tests
python3 report.py              # rebuilds results.md from results.jsonl
```
