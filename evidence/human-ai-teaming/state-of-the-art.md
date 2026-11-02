# State of the art

Step 3 of the review. For each question, the best evidence, kept apart from the practice most adopted. Upper bounds (what was achieved) are kept apart from limits (what was shown not to work). Sources are in [review](review.md).

## Q1 Decisions

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Vaccaro 2024 | the team is below the better of the two on average, g = -0.23; decision tasks lose, creating tasks gain | measured |
| Upper bound | Bansal 2021 | complementary performance appears on every task when person and model are about equally accurate | measured |
| Limit | Bansal 2021 | explanations raised acceptance whatever the model's correctness | measured |
| Most adopted | vendors' pages (Anthropic 2024) | an agent pauses for the person at checkpoints and blockers | convention, untested |
| Frameworks | Parasuraman 2000; Horvitz 1999 | choose a level of automation per stage; decide when to act and when to ask | convention, untested |

## Q2 Start of a session

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Most adopted | Agentic AI Foundation 2026 | a file of instructions in the repository, read by many tools | convention; the count is the owners' claim |
| Best evidence | Gloaguen 2026 | a context file does not raise success and raises cost by over 20% on average; it helps to state non-standard practice | measured |
| Upper bound | Gloaguen 2026 | developer-written files +2.4% on average, not significant | measured |
| Limit | Xu 2026 | a stale file overrides the code in 90.1% of choices (secondary) | measured |
| Size | vendors | under 200 lines, or a 32 KiB cap | convention, untested |

## Q3 Memory

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Most adopted | Anthropic 2026b | two stores, one written by the person, one by the model, both loaded; an audit command | convention, untested |
| Best evidence | none found | no controlled study of a model-written project memory | not found |
| Nearest | Treude 2026 | stale references in 23.0% of 356 repositories (secondary) | supported with caveat |

## Q4 Measure

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Upper bound | Peng 2023 | 55.8% faster on one task (secondary) | measured |
| Best evidence on experienced people | Becker 2025 | 19% slower; belief and result disagree | measured, 16 people |
| Most adopted | surveys (Stack Overflow 2025; DORA 2025b) | self-reported trust and use | measured, descriptive |

## Q5 Checks

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Huang 2024; Olausson 2024 | a model repairs poorly without outside feedback | measured |
| Most adopted | hooks and tests in the agent's loop (Anthropic 2024; Anthropic 2026b) | the environment gives ground truth | convention, untested |
