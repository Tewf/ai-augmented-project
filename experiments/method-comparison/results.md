# Results: the method against the model alone

Thirty sessions of a coding agent on a small hosted model, five per task per arm, judged by hidden tests. What was run
and what it cannot say are in the [protocol](protocol.md). Written by [report.py](report.py) from
[results.jsonl](results.jsonl), then read.

## The headline

- **Hidden pass:** the model alone passed 0 of 15 sessions. The model with the method passed 15 of 15.
- **Tokens:** a session with the method used 263 thousand tokens on average, against 173 thousand alone: 52% more. Most of the difference is cache reads, since the method arm makes more turns on the same prompt.
- **Cost:** by the agent's own figure, 0.0084 dollars a session with the method and 0.0087 alone. Cached tokens are cheap, so more tokens did not cost more.
- **START.md** was opened by the first tool call in 15 of 15 method sessions. The note names it first, so this says that the note works.
- **Questions:** none in either arm. The agent's command-line mode cannot ask the person, so the count says nothing here.

## The tables

Model: `claude-haiku-5-5`. Intervals are Wilson, 95%.

| Arm | Sessions | Hidden pass | Hidden pass without the name | Visible pass |
|---|---|---|---|---|
| model alone | 15 | 0/15 (0%, 0-20%) | 0/15 (0%, 0-20%) | not given |
| model with the method | 15 | 15/15 (100%, 80-100%) | 15/15 (100%, 80-100%) | 15/15 (100%, 80-100%) |

Hidden pass per task, passes out of sessions:

| Task | model alone | model with the method |
|---|---|---|
| scope | 0/5 (0/5 without the name) | 5/5 (5/5 without the name) |
| changelog | 0/5 (0/5 without the name) | 5/5 (5/5 without the name) |
| llms | 0/5 (0/5 without the name) | 5/5 (5/5 without the name) |

Counts per session, mean (median):

| Count | model alone | model with the method |
|---|---|---|
| total tokens (all five fields) | 173156 (135088) | 262785 (274159) |
| output tokens | 3256 (3278) | 2120 (2104) |
| fresh input tokens (input + cache write) | 43610 (46145) | 37533 (47991) |
| turns | 3.9 (3.0) | 5.7 (6.0) |
| tool calls | 4.6 (4.0) | 9.7 (10.0) |
| questions asked | 0.0 (0.0) | 0.0 (0.0) |
| files read before the first edit | 1.2 (1.0) | 6.1 (6.0) |
| cost, dollars | 0.0087 (0.0089) | 0.0084 (0.0094) |
| seconds | 35 (26) | 40 (33) |

START.md opened by the first tool call: 15/15 method sessions. In the alone arm the file does not exist.

Cost of the 30 counted sessions, by the agent's own figure: 0.257 dollars. Sessions that failed before a reply: 0.

Why hidden tests failed, by arm:

| Arm | Task | Detail |
|---|---|---|
| alone | changelog 1 | none: no function |
| alone | changelog 2 | namefree: FAILED (failures=8) |
| alone | changelog 3 | namefree: FAILED (failures=8) |
| alone | changelog 4 | none: no function |
| alone | changelog 5 | none: no function |
| alone | llms 1 | namefree: FAILED (failures=8) |
| alone | llms 2 | namefree: FAILED (failures=8) |
| alone | llms 3 | namefree: FAILED (failures=8) |
| alone | llms 4 | namefree: FAILED (failures=2) |
| alone | llms 5 | namefree: FAILED (failures=8) |
| alone | scope 1 | none: no function |
| alone | scope 2 | namefree: FAILED (errors=6) |
| alone | scope 3 | none: no function |
| alone | scope 4 | none: no function |
| alone | scope 5 | none: no function |


## How to read it

- **The gap is large, and it is mostly information.** The hidden tests follow from the Decided lines of the brief. The alone arm never saw them. In the folders read, its code returned named tuples, dictionaries or classes where the tests expect pairs, triples and strings, and it chose its own names.
- **The name is not the whole gap.** When the one public function is judged under the task's name, the alone arm still passes 0 of 15. In 8 sessions a single function could be judged this way, and all 8 failed the hidden tests. In the other 7 sessions the folder held several public functions or none, so no name could be assumed.
- **The method did not make the agent slower or dearer.** Seconds, cost and output tokens are the same order. Turns and tool calls roughly double, since the agent reads the files and runs the checks.
- **The agent reads more before it edits.** 6.1 distinct files against 1.2.
- **The prediction held that the method arm passes more and spends more tokens.** It held that START.md is read first in most sessions. All three were written before the first counted session.

## What the comparison cannot say

- It cannot separate the shape of the three files from the information they carry. A brief with the function name and rules in a different shape, or the same facts in the message, is not an arm here. That arm is the next one to run.
- It cannot say the start file or the memory index helped. The two memory files hold nothing the task needs, and the brief alone carries the signature. A fourth arm with the brief only would show it.
- It says nothing about a real project, where the start file and the index exist for what a task of fifty lines does not need.
- It says nothing about the person. The person arms wait for the maintainer, so the design's test, whether the team beats the better of its members, is not made.
- Five sessions per cell give a lower bound of 80% for 15 of 15 and an upper bound of 20% for 0 of 15. Within a task, 5 of 5 against 0 of 5 is the only reading.
- One model, one agent, one day.

## Cost

- Counted sessions: 0.257 dollars by the agent's own figure, 30 sessions.
- All sessions run for this experiment, harness checks and discarded ones included: about 0.31 dollars.
- Time to write the three fixtures: not counted.

## What changed while it ran

- Two sessions needed a retry after a network drop (llms method 2 and 5). Both retries ended normally.
- Harness checks: four runs of two sessions on a fourth task, not counted. The first two ended at once on faults of the harness, which the job notes list.
- The method sessions made with the first fixture were discarded: a link in its start file led the agent outside its folder, and one session ended there. Three records were dropped and rerun with the link removed. The seven alone sessions already made stayed, since their folders held no such file.
- The runner retried on any non-zero exit, a little wider than the protocol's "error before any model reply". Two sessions used the retry.
- The judge was changed once after six sessions: its wrapper did not register the candidate's module, so a dataclass failed to import. Every session was judged again from its folder with the corrected judge.

## Reproduce

See the protocol. `python3 report.py` rebuilds the tables from `results.jsonl`.
