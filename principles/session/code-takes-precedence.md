# The code takes precedence

**Claim:** the start file says once that, when an instruction or a memory disagrees with the code, the code is followed and the disagreement is said.

- **Grade:** measured (Xu 2026, secondary).
- **Evidence:** [review](../../evidence/human-ai-teaming/review.md), strand 2 (Xu 2026); [state of the art](../../evidence/human-ai-teaming/state-of-the-art.md), question 2; [design](../../design/one-project.md), decision 3; [record 0005](../../decisions/0005-memory-is-plain-files-with-a-source.md).
- **Check:** `start-file-precedence`: the sentence stands in the `Precedence` part, and nowhere else in the file.
- **Reader styles:** none.

## What it asks

- The `Precedence` part holds one sentence: when a text disagrees with the code, follow the code and say so.
- The sentence is said once. A second copy in another part is a second place to keep true.

## Why

- A stale instruction file won over the code in 90.1% of choices. With one sentence giving the code precedence, the share following the code rose from 4.2% to 91.4% (Xu 2026, secondary).
- The sentence costs one line and no upkeep.

## Limits

- Both figures are read from an abstract, so they are marked secondary. The study is a preprint.
- The sentence tells the model what to prefer. It does not find the stale line; [stale text is found by a program](stale-text-found-by-a-program.md) does.
- The program checks that the sentence is present. It does not check that a model obeys it.
