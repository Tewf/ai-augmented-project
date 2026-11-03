# A task names its checks

**Claim:** a task is handed to the model as a brief whose Checks part lists the commands that judge the result, each with what passing means.

- **Grade:** measured for outside feedback over a model's own repair (Huang 2024; Olausson 2024). The brief with its four headings is descriptive, from two tiers and three tasks. That naming the checks raises the pass rate is not supported: round two found no gain once the tests were hidden. The Checks heading stays as the definition of the judge the runner needs.
- **Evidence:** [review](../../evidence/human-ai-teaming/review.md), strand 5; [state of the art](../../evidence/human-ai-teaming/state-of-the-art.md), question 5; [design](../../design/one-project.md), decision 2; [record 0008](../../decisions/0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md); [brief test, round two](https://github.com/Tewf/ai-augmented-agents/blob/master/experiments/brief-test/results-2.md).
- **Check:** `brief-checks`: the four parts in order, none empty, and each check a command in backticks with what passing means.
- **Reader styles:** none.

## What it asks

- The brief is `brief.md` in the task's folder, written before the task starts.
- Its parts are `Task`, `Decided`, `To find` and `Checks`, in that order.
- Each line of `Checks` holds one command in backticks and says what passing means.
- The person writes or accepts the brief. A model may draft it. When the checks cannot be written, the model asks and does not start.

## Why

- A model corrects its own reasoning poorly without outside feedback (Huang 2024). Self-repair gains are modest once cost is counted (Olausson 2024).
- Round two, 180 calls judged by hidden tests: 0 of 60 with no brief, 30 of 60 with the convention brief, 29 of 60 with the checks added. The brief halves the failures of a cheap model; naming the checks adds nothing measurable.
- Round one's 5 of 10 with the checks listed fell to 1 of 10 when rescored on hidden cases. It measured following a list.
- The checks in the brief are the task's check for the measure. They are listed once, because the runner needs the judge defined, not because listing them raises the pass rate.

## Limits

- Two tiers, three tasks, ten calls per cell; the hidden cases were written by the author of the visible ones, and the three tasks are of one kind.
- The arms differ in more than the Checks heading, so the convention's parts are not isolated.
- The program checks the form of the brief. It cannot tell whether the checks are good ones; that is the person's reading.
