# Baseline

Step 5 of the review: the baseline the repository's rules are compared against. It is the maintainer's practice, written down for this review. It names no tool, no path and no private repository. Evidence is in [review](review.md).

**Shape:** [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/a7f405f26f14cd188291e2a86b630121c4302a94/shapes/baseline.md)

## B1: five practices

1. **Standing instructions.** A short file of instructions is loaded at the start of each session. It holds rules, the order of work and what to read for a task. Longer detail is read on demand and not copied into the file.
2. **One shared memory.** Notes are kept in one place read by every model the maintainer uses. Each note holds one fact, with an index. Models write notes in a fixed format; they do not write them anywhere else.
3. **Checks as the oracle.** What a program can check, a program checks, as a test, a hook or a CI job. Cost sets how often a check runs. A check that costs money stays off until the person turns it on. A model never reviews its own output in place of the checks. A rule written down gets a test.
4. **Delegation by cost.** A bulk or mechanical task goes first to a free local model. The next step is a cheaper hosted model, then a small cloud model with tools. The strongest model keeps judgment, code that will run and anything where a wrong answer would not be noticed.
5. **Questions to the person with options.** The model gives one recommendation, then acts. It asks when a choice is the person's, and it offers options with a default.

## Compared with what the review found

| Practice | Nearest finding | Fit |
|---|---|---|
| Standing instructions | short, verifiable files help to state non-standard practice (Gloaguen 2026; Anthropic 2026b) | matches; staleness is not tested by a program |
| One shared memory | a vendor's two stores with an index (Anthropic 2026b) | matches the form; no study of its effect |
| Checks as the oracle | outside feedback is what makes repair work (Huang 2024; Olausson 2024); hooks enforce, instructions do not (Anthropic 2026b) | matches the best evidence |
| Delegation by cost | cascades cut cost with little loss (Chen 2023b) | matches in service settings; not tested for one person |
| Questions with options | ask when a choice is the person's (Horvitz 1999; Wu 2023) | matches the design principle |

## What the baseline lacks

- A measure: none of the five has a count of its effect. The review shows self-report is unreliable (Becker 2025).
- A staleness test for instructions and memory, which Treude 2026 and Xu 2026 show to be needed.
- A control: no task has been run with and without a practice.

## How it would be measured

- Time per task against a control for the same task, not the person's estimate.
- Questions asked twice, counted from the session record.
- Errors a check caught before the person saw them, counted from the check logs.

## The review is finished

The baseline is named: B1. The design document is the next job; [position](position.md) lists what it must decide.
