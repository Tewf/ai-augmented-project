# Changelog

Every release of this repository, and the releases it pins, newest first, in the form of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
A pin move is recorded here, not in decisions/.

## [Unreleased]

### Added

- Two optional lines in a brief's Decided, Starts from (a repository and a commit) and Shapes to read, read by
  `brief-checks`; 4 tests, the design document [brief-start-state](design/brief-start-state.md) and
  [record 0014](decisions/0014-a-brief-names-its-start-commit-and-its-shapes.md), proposed.

- The job record: a shape ([job-record](shapes/job-record.md)) that extends the trace's `[[job]]` table with `depends_on`,
  `minutes`, `date`, `repo` and `outcome`, an exporter `checks/local/job_record.py` that writes it from a folder of briefs,
  15 tests, and [record 0013](decisions/0013-one-job-record-exported-from-the-briefs.md).

### Changed

- Pinned reader-ergonomics v1.24.2 (`65e4247`), from v1.21.0 (`2e5b6f0`): fixes that remove false findings in the sentence, term and figure checks, and `[defined_terms] cues`.

## [0.2.3] - 2026-11-04

### Fixed

- `CITATION.cff` still said 0.2.1 on the 0.2.2 tag; this release carries the matching version, and the pointers copy this one.

## [0.2.2] - 2026-11-04

### Added

- The person arms of the method comparison, in `experiments/method-comparison/person-arms/`: a pre-registered protocol that plans the number of
  participants.
- `run_person.py`, which times a person on the three tasks and scores them with the comparison's own judge.

### Changed

- Pinned reader-ergonomics v1.21.0 (`2e5b6f0`), from v1.20.0 (`4f99372`): duplication skips the lines a declared shape prescribes

## [0.2.1] - 2026-11-04

### Added

- A closing Cost block in the brief shape (tokens, dollars, the person's minutes, what was produced), read by `brief-checks`,
  and an optional Estimate line in the memory shapes, read by `memory-source`; both filled in the examples and tested
  ([record 0012](decisions/0012-the-quantities-of-a-task-are-recorded-in-its-brief.md)).

### Changed

- The principle "a task names its checks", the brief shape and the design: `Checks` stays as the judge's definition; the claim
  that listing the checks raises the pass rate is lowered to not supported (brief test, round two, 180 calls, hidden tests).
- Pinned reader-ergonomics v1.20.0 (`4f99372`), from v1.19.2 (`b9732b9`): the runner's verdicts file (`--out`), and hand-written llms.txt lines kept through a rebuild

### Changed

- `memory-index` accepts prose before the first entry, headings, blank lines and **Shape:** lines between entries,
  a dash as well as a colon between title and hook, and a hook judged by its line, not its sentence count.
- `memory-source` accepts a YAML header (`metadata.type` one of user, feedback, project, reference) with a date or a
  link in the body, beside the shape's three labelled lines.
- The memory-index shape and the source principle say both forms; [record 0010](decisions/0010-the-memory-shapes-meet-the-practice.md).

### Added

- Unit tests for both accepted forms.
- The first comparison, in `experiments/method-comparison/`: the model alone against the model with the method, 30
  sessions on three tasks with hidden tests, judged by a program ([record 0011](decisions/0011-the-method-is-compared-with-the-model-alone-by-a-program.md)).

## [0.1.0] - 2026-11-03

### Added

- The first release, at 0.x because the measure is not run: a first-pass review of human-AI teaming (39 sources) that
  names its baseline, B1, the maintainer's practice written down.
- A design document with a record per choice, and the card: seven principles in two groups, session and memory, each
  with its grade.
- Three shapes with a filled example each: the brief, the start file and the memory index.
- Six local checks in `checks/local/` with 43 unit tests, run in CI before the standard's checks.
- Take it, on the front page: the shapes to copy, the pin and the one command to run.

### Changed

- Pinned reader-ergonomics v1.19.2 (`b9732b9`), unchanged since the repository's start.

## 2026-11-03

### Added

- The card `standard.md`, seven principles, three shapes with a filled example each, and six local checks with unit
  tests that CI runs. The pin is unchanged (v1.19.2, `b9732b9`).

## 2026-11-02

### Added

- Pinned reader-ergonomics v1.19.2 (`b9732b9`), at the repository's start: the standard's pin, link, changelog and
  decision-record checks, which this skeleton is written to pass.

(0.2.0 was tagged one commit earlier, before this changelog entry; 0.2.1 is the same content with the entry and the citation in step.)
