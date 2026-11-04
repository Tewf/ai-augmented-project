# Protocol: the person alone and the person with the method

Written on 2026-11-04, before any run of a person. It says what a participant does, how it is scored and what the
result cannot show. It is pre-registered: a change after the first run is a dated amendment at the end, never an edit.

The model arms of the same tasks are in [the protocol of the comparison](../protocol.md) and their numbers in
[results.md](../results.md). This page adds the two arms that wait for a person.

## Question

Take the three tasks of the comparison, scored by the same hidden tests. Does a person who is handed the method write
code that passes the hidden tests more often than a person who is handed the task sentence? How long does each take?

## Hypotheses

Written now, so the result can disagree with them.

| Id | Hypothesis | Kind |
|---|---|---|
| H1 | A participant passes more hidden tests of the three tasks with the method than alone. | primary, two-sided test |
| H2 | The median seconds per task differ between the arms. No direction is predicted: reading costs time, and fewer false starts save it. | secondary, described |
| H3 | Hidden pass without the name follows H1 with a smaller gap, since the method arm is told the function name. | secondary, described |

The model arms passed 0 of 15 alone and 15 of 15 with the method. That gap is mostly information: the method arm is
told the function, the module and the rules. A person can guess more from a sentence than a model can, so the gap
for a person is expected to be smaller than for the model.

## Arms

| Arm | Run here | The participant receives |
|---|---|---|
| person alone | yes | the task sentence and an empty folder |
| person with the method | yes | the files of the model's method arm: START.md, memory/INDEX.md with its two memory files, the brief and its checks, and the hand-over note |
| model alone, model with the method | yes, by a program | see [the comparison](../protocol.md) |
| person with the model | no | the decision's own test, the team against the better of its members, is still not made |

Both person arms use the three tasks (scope, changelog, llms), whose sentences, Decided lines and hidden tests are those
of the comparison. The files of the method arm are read from [fixtures/](../fixtures/) by path:
`fixtures/common/START.md`, `fixtures/common/memory/INDEX.md`, and `fixtures/<task>/brief.md`. The program copies them to
a scratch folder, so the participant works on a copy.

## What the participant may open

| | Alone | With the method |
|---|---|---|
| a text editor, a terminal, a Python 3 interpreter | yes | yes |
| the Python documentation | yes | yes |
| the task sentence | yes | yes |
| the files of the method, read in the order of the hand-over note | no | yes |
| a language model, a code assistant, or a search for the task itself | no | no |
| `hidden/`, `reference/`, `results.jsonl`, `results.md` and the other arm's work | no | no |

The alone arm is not told the function name or the module. This is the same as the model alone, and it is why
[hidden pass without the name](#scoring) is shown beside.

## Order

- Each participant does both arms, on the same three tasks. The pairing removes the difference between people.
- **An order coin** decides which arm comes first. The program flips it at the first call, writes it in
  `runs/<id>-order.json` and in both records, and never lets the participant choose.
- The three tasks come in an order fixed by the id and the arm, shuffled once, so the program can replay it.
- A break of at least one hour separates the arms. A day is better. The program records the gap in seconds.

## Timing

- The clock starts when the participant presses Enter after the task is shown, and stops at the next Enter.
- Reading the method's files is inside the clock. This is the cost of the method on this task, and it is counted.
- The cap is 30 minutes a task. The participant stops at the cap, and the record says the task was over it. What is in
  the folder at the stop is scored.
- There are no pauses inside a task.

## What is recorded

One file per arm, `runs/<id>-<arm>.json`, written after every task, so a stopped session loses at most the task in progress.

- The anonymous id, the arm, whether the participant is a pilot, and the order coin.
- Per task: start and end in UTC, seconds, whether it was over the cap, the source files left at the folder root, the three verdicts.
- The commit of the repository, the Python version, the cap, and the gap after the first arm.

**No personal data enters the repository.** The id is letters and digits such as `P01`, and the program refuses a space.
The folder `runs/` ignores every file, so a record is committed only when the participant decides, with `git add -f`.
A record holds the participant's code, which the participant may not want to publish.

## Scoring

The program is [judge.py](../judge.py), imported, never copied, with the hidden tests of the model arms.

- **Primary: hidden pass.** The function the task names exists in a Python file at the folder root and passes every hidden test within 20 seconds. A participant scores 0 to 3 in each arm.
- **Secondary: hidden pass without the name.** When no file defines the name and the folder holds exactly one public function, it is judged under the name.
- **Secondary: visible pass,** in the method arm only, where the brief's checks exist.
- A task with no function, or one that does not import, scores 0.

**The test of H1** is on the participant's difference d, the hidden passes with the method minus those alone, an integer
from minus 3 to 3. It is an exact two-sided Wilcoxon signed-rank test, with alpha 0.05 and the zeros dropped. The unit is
the participant, not the task: the three tasks of one person are correlated. `run_person.py --summary` prints it.

Pilots are listed and left out of the test.

## Participants needed

**14 participants besides the pilot, planned as 16.** The reasoning:

1. **Design.** Paired, each participant in both arms, so the test is on d.
2. **Effect to detect.** The model arms differ by 3 of 3 tasks (15 of 15 against 0 of 15). That is mostly information, and a person alone can infer rules from a sentence. We assume a third of that gap: a person passes about 1 task alone and about 2 with the method, so the mean of d is 1.
3. **Spread.** If each arm count is binomial with probability 1/3 or 2/3 on 3 tasks, its variance is 0.67. Two arms with no correlation give a variance of d of 1.33, so a standard deviation of 1.2. The standardised effect is dz = 1 / 1.2 = 0.83.
4. **Sample size.** Alpha 0.05 two-sided, power 0.8. For a paired t test, n = ((1.96 + 0.84) / dz)^2 + 1.96^2 / 2 = 13.3. The signed-rank test needs 1 / 0.955 times as many, so 13.9. Round up: **14**.
5. **Spare.** An arm can be left unfinished, and an unfinished pair is dropped. Two spare gives **16**.

How it moves, for the same alpha and power: dz of 1.0 needs 10, dz of 0.7 needs 19, dz of 0.6 needs 25. If the real gap is half
of the assumed one, plan for 25. The assumption in step 2 is a guess, not a measurement. The pilot may refine it, and the
change is then an amendment.

**What no number of participants fixes.** The person who wrote the method is a participant.

- The maintainer wrote the start file, the memory files and the brief shape, chose the tasks and read the model results before running.
- He knows what the method says, so the method arm is faster for him than for anyone else.
- He knows what the hidden tests are likely to check.
- More participants dilute this in the test. They do not remove it from his record, which is why he is the pilot and is left out of the primary test.

Three more limits stay at any n:

- every participant is recruited by the maintainer, so they are a convenience sample;
- there are three tasks of one kind, so the result is about these tasks, not about tasks;
- nobody is blind to the arm.

## Stopping

- A participant stops an arm only at the end of a task. An arm with fewer than three tasks is incomplete, and its pair is dropped from the test and listed.
- The study stops when 14 complete pairs besides the pilot exist, or when 16 have started. It does not stop on a p value.
- A participant may withdraw at any time. Their records are deleted on request, since only the id links them.

## What the run cannot say

- **One participant is a pilot, not a result.** It tests the program and the instructions.
- **The second arm sees the same tasks.** The coin balances the order across participants. It does not remove the effect of having done the task once, and with 16 participants the balance is not exact.
- **The arms differ by more than the shape of the files.** The method arm is told the function, the module, the rules and the checks. The gap measures the information as much as the method, as in the model arms.
- **The tasks are small.** A start file and an index exist for projects that fifty lines of code do not need.
- **A pass is not quality.** The hidden tests check behaviour on small inputs.
- **The person with the model is not run.**

## Reproduce

```sh
cd experiments/method-comparison/person-arms
python3 run_person.py --self-test     # scores a known answer set, exits 0
python3 run_person.py P01             # the next arm of P01; run it again for the other arm
python3 run_person.py --summary       # the table and the paired test
```

## Amendments

None yet.
