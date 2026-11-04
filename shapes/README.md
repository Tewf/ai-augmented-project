# Shapes

A **shape** is the fixed skeleton of one kind of document: every document of that kind has the same parts in the same
order. These are the files that a session is handed or keeps, and the record that lists its jobs. The general shapes (note, folder README, report,
commit message, decision record) and the reasons for shapes are in
[reader-ergonomics](https://github.com/Tewf/reader-ergonomics/blob/2e5b6f0c3e67d2dc8195a63cf882d46170e79a5a/shapes/README.md).

## Contents

| Shape | For |
|---|---|
| [brief.md](brief.md) | one task handed to a model: the task, what is decided, what is to be found and the checks it is judged by; its worked example is [a brief for the start-file check](examples/brief.md) |
| [start-file.md](start-file.md) | the file a session is handed first: commands, conventions, the precedence sentence and pointers, within a bound; its worked example is [this repository's own](examples/start-file.md) |
| [job-record.md](job-record.md) | the jobs of a project in one TOML file, exported from their briefs and read by the scheduler, the guide's replay and the cases; its worked example is in the shape |
| [memory-index.md](memory-index.md) | the index of the notes a model keeps: one line per file; its worked example is [an index of two files](examples/memory/INDEX.md) |

## Choosing a shape

- One document, one shape. A text that needs two shapes is two documents.
- The brief is written per task. The start file and the memory index stay the same from task to task.
- Each shape names the principle behind each part and the check that reads it.
