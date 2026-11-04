# Shape: job record

A **job record** lists the jobs of a project, one table per job. A planner, a ranker and a counter all read the same
file. A job's numbers are written once, in its [brief](brief.md), and exported.

## When to use it

- For a set of jobs that were run, or are planned, each with a brief in a folder of its own.
- Not for one job: its brief already holds it.
- Not for the quantities of a single task. Those are the brief's Cost block.

## Skeleton

The file is TOML. Each job is a `[[job]]` table, and the fields below are the only ones. Every field except `id` may be
absent, and absent means unknown, never zero.

```toml
[[job]]
id = "<the folder name without its date>"
date = "<yyyy-mm-dd>"
wave = 0
kind = "<review>"
repo = "<the repository the job worked in>"
depends_on = ["<id of a job that must finish first>"]
agents = 1
tokens_k = 0
tokens_source = "recorded"
dollars = 0
minutes = 0
produced = "<what the job made, in a few words>"
outcome = "pass"
```

## Fields

| Field | Meaning | Where the exporter reads it |
|---|---|---|
| `id` | the job's name, unique in the file | the folder name, less its date |
| `date` | the day the job's folder opens | the folder name |
| `wave` | the launch cluster; jobs of one day share a wave | the rank of `date` among the dates of the folder, from 0 |
| `kind` | setup, review, audit, design, build, experiment or upkeep | the header line `**Kind:**` |
| `repo` | the repository the job worked in | the header line `**Repo:**` |
| `depends_on` | ids of the jobs that must finish first | the header line `**Depends on:**`, comma separated |
| `agents` | how many agent runs the row holds | the rule 1: a brief is one job |
| `tokens_k` | thousands of tokens of the job | the Cost line Tokens, when its unit is tokens |
| `tokens_source` | `recorded` when `tokens_k` is read from a Cost block, `estimate` when it is not | `recorded` with `tokens_k` |
| `dollars` | spend on a paid interface outside the subscription | the Cost line Dollars, when its unit is dollars |
| `minutes` | the person's minutes, or the worker's wall clock, as the Cost line says | the Cost line Minutes, when its unit is minutes |
| `produced` | what the job made | the Cost line Produced |
| `outcome` | `pass` or `fail`, from the brief's checks | the header line `**Outcome:**` |
| `changed`, `moved`, `kept`, `in_family` | the guide's readings of what a job changed and whether it stood | written by hand in the trace; the exporter never sets them |

The first group of fields extends the trace of the [foundations guide](https://github.com/Tewf/ai-augmented-foundations):
`depends_on`, `minutes`, `date`, `repo` and `outcome` are new, and every field it had is kept, with its meaning.

## Rules

- A value that is `pending`, `not measured`, absent or in another unit is left out of the table. It is never guessed.
- A header line sits between the title and the first part of the brief, as `**Label:** value`. The brief's own parts do not change.
- `depends_on` names only ids in the same file. A reader refuses an unknown id and a cycle.
- The exporter is [checks/local/job_record.py](../checks/local/job_record.py). It writes the tables by hand and reads a folder of `*/brief.md`.
- A reader ignores a field it does not know, so a file with more fields than the reader needs is still its input.

## Worked example

Two briefs, one folder each. The first is open, so only its date and header are known. The second is closed.

```markdown
<!-- 2026-11-04_second/brief.md -->
# Brief: the second job
**Depends on:** first
**Kind:** build
## Cost
- Tokens: 182384 tokens
- Dollars: not measured
- Minutes: 17 min
- Produced: one module and its tests
```

The exporter writes, for it:

```toml
[[job]]
id = "second"
date = "2026-11-04"
wave = 0
kind = "build"
depends_on = ["first"]
agents = 1
tokens_k = 182.384
tokens_source = "recorded"
minutes = 17
produced = "one module and its tests"
```

The scheduler reads `depends_on` as the wait and `minutes` as the length. The guide's replay reads `wave`, `kind`,
`agents` and `tokens_k`. The cases read `minutes`, `dollars` and `tokens_k` for the totals of a case.

## Checked by

- `checks/test_session.py`: the exporter's tests, which fix each rule above.
- Whether a brief's numbers are true is the owner's reading. A reader checks only that the file is well formed.
