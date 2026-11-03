# 0009: Which findings became principles

**Decision:** A finding becomes a principle when a registered check reads it and it is graded measured or supported with caveat, or enforced by a program here. Every other finding stays in the review.

**Status:** proposed, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/2e5b6f0c3e67d2dc8195a63cf882d46170e79a5a/shapes/decision-record.md).

## Context

- The standard's extension contract asks for a card and one file per principle. Its check `principle-coverage` fails a principle that names no registered check, so a rule with no program cannot be a principle yet.
- The review graded its findings in [state of the art](../evidence/human-ai-teaming/state-of-the-art.md). The design document turned five of them into files a session is handed.
- The three files are the start file, the memory index and the brief. A shape for each, and a check that reads it, were the next step.

## Decision

Seven findings became principles, in two groups. Each grade is the review's, never higher.

| Principle | Grade | Check |
|---|---|---|
| The model decides nothing unchecked | measured, for tasks that decide | `brief-checks` |
| A task names its checks | measured for outside feedback; convention for the brief | `brief-checks` |
| The start file holds what the code cannot say | supported with caveat | `start-file` |
| The code takes precedence | measured (secondary) | `start-file-precedence` |
| Stale text is found by a program | supported with caveat | `start-file-stale` |
| A memory file has a source | convention, untested | `memory-source` |
| The memory index has one line per file | convention, untested | `memory-index` |

Two of them are conventions. They became principles because the design makes a program enforce them, and a rule with a program is testable.

These findings stayed findings, each for the reason given:

- Explanations raised acceptance of wrong answers (Bansal 2021, measured). The rule it implies, to hand the model the check's reason and not an opinion, has no program yet.
- Speed results disagree (Becker 2025 measured; two trials secondary). The rule, to count time per task, needs the counts program, which is not built.
- Routing to the cheapest model that suffices (Chen 2023b, measured, secondary). It was shown in service settings, not for one person, and no program reads it.
- Context files may have no effect (Khatri 2026, secondary). It is evidence against a rule, so it stays in `against.md`.
- Frameworks for levels of automation and for asking (Parasuraman 2000; Horvitz 1999; Wu 2023). They are conventions, untested, and no program reads them.
- Memory architectures (Luo 2026; Packer 2023). They describe systems; this repository chose plain files.

The three shapes ask for the Shape line of an example in `shapes/examples/`. The memory index may open with a title and that line, which are not counted, so the index still holds one line per file.

## Consequences

- Each principle is run by a check in CI, and each check has unit tests.
- **Bad:** the checks read form, not meaning. The staleness check looks up paths and does not run the commands the design asks it to run.
- **Bad:** the generated `llms.txt` of the standard's builder replaces the hand-written index, so the design document is no longer listed there.
- A finding moves to a principle when a program is written for it, in a new record.

## See also

[Decisions](README.md); [the card](../standard.md); [the design document](../design/one-project.md); [record 0003](0003-the-model-decides-nothing-unchecked.md), [0004](0004-a-short-start-file-and-an-index.md), [0005](0005-memory-is-plain-files-with-a-source.md) and [0008](0008-a-task-is-handed-over-as-a-brief-that-names-its-checks.md), whose choices these principles carry.
