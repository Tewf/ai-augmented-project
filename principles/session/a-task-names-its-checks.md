# A task names its checks

**Claim:** a task is handed to the model as a brief whose Checks part lists the commands that judge the result, each with what passing means.

- **Grade:** measured for outside feedback over a model's own repair (Huang 2024; Olausson 2024). The brief with its checks is a convention, with one run of one task and one model in its favour.
- **Evidence:** [review](../../evidence/human-ai-teaming/review.md), strand 5; [state of the art](../../evidence/human-ai-teaming/state-of-the-art.md), question 5; [design](../../design/one-project.md), decision 2; [record 0008](../../decisions/0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md); [brief test](https://github.com/Tewf/ai-augmented-agents/blob/master/experiments/brief-test/results.md).
- **Check:** `brief-checks`: the four parts in order, none empty, and each check a command in backticks with what passing means.
- **Reader styles:** none.

## What it asks

- The brief is `brief.md` in the task's folder, written before the task starts.
- Its parts are `Task`, `Decided`, `To find` and `Checks`, in that order.
- Each line of `Checks` holds one command in backticks and says what passing means.
- The person writes or accepts the brief. A model may draft it. When the checks cannot be written, the model asks and does not start.

## Why

- A model corrects its own reasoning poorly without outside feedback (Huang 2024). Self-repair gains are modest once cost is counted (Olausson 2024).
- In one small run, a cheap model passed 0 of 10 with no brief and 0 of 10 with the usual fields. It passed 5 of 10 when the checks were added.
- The checks in the brief are the task's check for the measure. They are listed once, so the model is judged by what it was told.

## Limits

- The run is one task and one model, and that arm was shown the cases it is judged by. It is a first data point, not a result.
- The program checks the form of the brief. It cannot tell whether the checks are good ones; that is the person's reading.
