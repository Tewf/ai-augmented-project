# 0010: The memory shapes meet the practice

**Decision:** The memory checks accept the form the maintainer's memory already has, beside the shape's own, because the practice is older than the shape.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/b9732b9814c71768f722691f3c5049ec2b8ed378/shapes/decision-record.md).

## Context

- The shape was written from a review, before it met the memory it describes: the maintainer's own memory of 164 files.
- `memory-index` refused that index. It groups its lines under headings and separates title from hook with a dash.
- `memory-source` refused the files 492 times. They carry a YAML header (`name`, `description`, `metadata.type`) and dates in the body, not the lines **Date:**, **Type:** and **Source:**.
- The family's rule is that the repository wins over a stale instruction. Here the stale instruction is the shape.

## Decision

- `memory-index` accepts prose before the first entry, heading lines, blank lines and **Shape:** lines between entries, a hook of several sentences on one line, and a colon or a dash between title and hook.
- `memory-source` accepts a YAML header whose `metadata.type` is user, feedback, project or reference, and whose body holds a date YYYY-MM-DD or a link as its source.
- The shape's **Source:** line stays the other accepted form. Both forms are in the shape and tested.
- Rejected: asking 164 files to be rewritten; keeping the refusal and exempting the memory.

## Consequences

- Run on those 164 files, the widened checks leave 3 files without a date or a link, and 4 findings on the index: two lines not in the entry form and two files not listed. Those are findings, not refusals of the form.
- **Bad:** a date or a link is a weaker source than a path or a command. The check cannot follow it; it only sees that one is there.
- The type vocabulary now has two sets, one per form.

## See also

[Decisions](README.md); [record 0005](0005-memory-is-plain-files-with-a-source.md); [the memory index shape](../shapes/memory-index.md).
