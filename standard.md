# The AI-augmented project standard

What setting up one project with a person, a model and a machine shares, as far as the evidence goes. The rules cover
who decides, what a session is handed, how memory is kept, and how a stale text is found. It extends
[reader-ergonomics](https://github.com/Tewf/reader-ergonomics/blob/2e5b6f0c3e67d2dc8195a63cf882d46170e79a5a/standard.md), the standard for any reader:
read that one first. This page adds only what the setup changes.

The evidence is a first-pass review of 39 sources, in [evidence/](evidence/README.md), ending on the baseline B1. The
design that turns it into files is [design/one-project.md](design/one-project.md).

## How to use it

1. **Pick the shape** from [shapes/](shapes/README.md): a [brief](shapes/brief.md) for each task, a
   [start file](shapes/start-file.md) for the project, a [memory index](shapes/memory-index.md) for the notes.
2. **Write to the principles** below, and to those of reader-ergonomics, which still hold.
3. **Check:** copy `checks/local/` into your project, set its tables in `checks/config.toml`, and run the standard's
   checks. The six local checks find each file by the names in that config.

Grades mean what they mean in [reader-ergonomics](https://github.com/Tewf/reader-ergonomics/blob/2e5b6f0c3e67d2dc8195a63cf882d46170e79a5a/standard.md#grades): measured, supported with caveat,
convention, not supported. Each principle states its grade and never claims more.

## Principles

<!-- principles:start -->

### Session: what the model decides and is handed

| Principle | Claim | Grade |
|---|---|---|
| [A task names its checks](principles/session/a-task-names-its-checks.md) | a task is handed to the model as a brief whose Checks part lists the commands that judge the result, each with what passing means. | measured for outside feedback over a model's own repair (Huang 2024; Olausson 2024). The brief with its four headings is descriptive, from two tiers and three tasks. That naming the checks raises the pass rate is not supported: round two found no gain once the tests were hidden. The Checks heading stays as the definition of the judge the runner needs |
| [The code takes precedence](principles/session/code-takes-precedence.md) | the start file says once that, when an instruction or a memory disagrees with the code, the code is followed and the disagreement is said. | measured (Xu 2026, secondary) |
| [The model decides nothing unchecked](principles/session/model-decides-nothing-unchecked.md) | a program decides what it can check, the person decides the rest, and the model drafts and proposes without deciding. | measured for tasks that decide, where a person with a model scored below the better of the two (Vaccaro 2024). The split of owners among the three parties is a convention |
| [Stale text is found by a program](principles/session/stale-text-found-by-a-program.md) | every path that an instruction names is looked up by a program on every commit, so a line that points at nothing is found, not trusted. | supported with caveat. Stale references appear in 23.0% of 356 repositories (Treude 2026, secondary). That a path lookup finds the stale lines that matter is untested |
| [The start file holds what the code cannot say](principles/session/start-file-holds-what-the-code-cannot-say.md) | the start file holds the commands, the non-standard conventions, the precedence sentence and one pointer per kind of task, within a bound of lines, and no overview of the repository. | supported with caveat. A generated overview did not help and cost over 20% more; a developer-written file helped by 2.4% on average, not significantly (Gloaguen 2026, measured). The bound of 200 lines is a convention, from vendors' practice |

### Memory: what is kept across sessions

| Principle | Claim | Grade |
|---|---|---|
| [A memory file has a source](principles/memory/memory-file-has-a-source.md) | each memory file records its date, its type and a source that a program can follow, and a rule is a proposal until the person accepts it. | convention, untested. No controlled study of notes that a model writes for a project was found |
| [The memory index has one line per file](principles/memory/memory-index-one-line-per-file.md) | the memory index holds one line per memory file, in one form and within a bound, so that a line is one fact's address and a program can count them. | convention, untested. One vendor caps the index of the notes a model writes (Anthropic 2026b) |

<!-- principles:end -->

## Where the evidence is

Every principle links its review in [evidence/](evidence/README.md), and every work cited is listed once in the
[bibliography](evidence/bibliography.md).
