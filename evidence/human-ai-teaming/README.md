# Human-AI teaming: how one person, one model and one machine are set up on a project

A first-pass multivocal review, read on 2026-11-02. It asks what research and practice know about setting a person, a language model and a machine to work on one software project, and it ends on a named baseline.

- It holds 39 sources: 30 formal and 9 grey, plus the method paper.
- Grey: 6 tier 2 and 3 tier 3; one scores below the threshold and serves as an example only; no tier 1.
- Formal: 13 measured, 4 descriptive or supported with caveat, the rest convention, survey or located only. Most numbers are read from abstracts and marked (secondary).

## Files

| File | Role |
|---|---|
| [frame](frame.md) | step 1: the problem, the field's names beside the practitioners', and whether the repository's name matches |
| [protocol](protocol.md) | how the pool was searched, selected and scored |
| [sources](sources.md) | the flow, then each source with its grade or score |
| [review](review.md) | step 2: findings in five strands |
| [state of the art](state-of-the-art.md) | step 3: the best evidence per question, apart from the practice most adopted |
| [position](position.md) | step 4: what is known, what was not found, the four questions answered |
| [against](against.md) | null results, slowdowns and disagreements |
| [baseline](baseline.md) | step 5: B1, the maintainer's practice, written down for this review |
| [bibliography](../bibliography.md) | every work cited, once, with a stable link |

## Claims

| Claim | Grade | Where |
|---|---|---|
| A person with a model scored below the better of the two alone on average, g = -0.23; tasks that decide lost, tasks that create gained | measured | review.md Q1 |
| Complementary performance appears when person and model are about equally accurate; explanations raised acceptance whatever the model's correctness | measured | review.md Q1 |
| A context file does not raise success and costs about 20% more; developer-written files +2.4%, not significant | measured | review.md Q2 |
| A stale instruction file is obeyed over the code in 90.1% of choices | measured (secondary) | review.md Q2 |
| Experienced developers were 19% slower with AI tools in a trial of 16 people, while believing they were faster | measured | review.md Q4 |
| Other trials found 55.8% and about 21% faster | measured (secondary) | review.md Q4; against.md |
| A model repairs its output poorly without outside feedback | measured | review.md Q5 |
| No controlled study of a model-written project memory or of its audit was found | not found, in these searches | review.md Q3 |
| Vendor limits on instruction files (200 lines, 32 KiB) are settings, not findings | convention, untested | review.md Q2 |
