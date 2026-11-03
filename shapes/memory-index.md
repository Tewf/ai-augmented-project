# Shape: memory index

The **memory index** is the second file a session is handed, after the [start file](start-file.md). It lists the memory
files, one line each. A line is the address of one fact, so a program can count the lines and follow each link.

## When to use it

- Once per project, as `memory/INDEX.md`, beside the memory files it lists.
- Not for the facts themselves. Each fact is a file of its own.
- Not for a rule of the project. Rules the person wrote are in the start file.

## Skeleton

The index, then one memory file:

```markdown
# <Project>: memory

**Shape:** [memory index](<path to this shape>)

- [<title>](<file>.md): <the hook, in one sentence>
```

```markdown
# <title>

**Date:** <YYYY-MM-DD>
**Type:** <fact | rule | reference>
**Source:** <a path, a command in backticks, or an identifier>

<The fact, in a few lines.>
```

A file of type rule also has `**Status:** proposal` or `**Status:** accepted`.

The practice this shape was written for is older than it, and the checks accept its form too:

```markdown
# <Project>: memory

## <A heading that groups lines>
- [<title>](<file>.md) - <the hook, in one sentence>
```

```markdown
---
name: <file name>
description: "<the hook>"
metadata:
  type: <user | feedback | project | reference>
---

<The fact, with at least one date YYYY-MM-DD or one link in the body.>
```

## Worked example

[An index of two files](examples/memory/INDEX.md) is drawn from this repository's own review. It carries a **Shape:**
line that links back here. The two files it lists are beside it: a fact whose source is a path, and a rule that is
still a proposal.

## Where each part comes from

| Part | Why it is there | Grade |
|---|---|---|
| One line per file | a program counts the files and finds a broken link | convention, untested |
| Date | a program lists the files not checked for a set number of days | convention, untested |
| Type | a rule changes behaviour, so it waits for the person | convention, untested |
| Source | the audit follows it; a note without one cannot be audited | convention, untested |
| 200 lines | one vendor caps its index; no study sets a length | convention, PROVISIONAL |

The principles are [a memory file has a source](../principles/memory/memory-file-has-a-source.md) and
[the memory index has one line per file](../principles/memory/memory-index-one-line-per-file.md).

## Rules

- One fact per file. The model writes in this folder and in this form only.
- A rule is a proposal until the person accepts it.
- The index may hold a title, headings that group the lines, blank lines and **Shape:** lines. They are not counted.
- A line separates title from hook with a colon, or with a dash between spaces.
- A file has the three labelled lines, or a YAML header with `metadata.type` and a body that carries a date or a link.
  The header is not asked for the labelled lines, and the type is then one of user, feedback, project, reference.
- No memory file is left out of the index, and none is listed twice.
- A stale file is not deleted by the program. The person decides, or the model fixes it and the check passes.

## Checked by

- `memory-index`: the form of each line (either separator), each link, the bound, no file left out.
- `memory-source`: the three fields or the YAML header, the status of a rule, a source that is a path exists.
- The age of a file and the weekly list of files not checked are not built.
