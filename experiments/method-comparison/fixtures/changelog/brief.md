# Brief: list the released versions of a changelog

## Task

Write a Python function that parses a Markdown changelog and lists its released versions with their dates, and tests for it.

## Decided

- The function is `changelog_releases(markdown: str) -> list[tuple[str, str]]`, in the module `changelog.py` at the project root.
- A release is a line that starts with `## [`, then the version up to the next `]`, then ` - `, then a date written YYYY-MM-DD. Text may follow the date.
- A `## [Unreleased]` line is not a release. A `## [x]` line with no such date is not a release.
- Headings of other levels are ignored. Lines inside a fenced code block (``` fences) are ignored.
- The tests go in `checks/test_changelog.py`. The file `checks/test_visible.py` is the brief's check and is not edited.

## To find

- The pair (version, date) of each release, as two strings, in order of appearance.
- The function and its tests, written to the two files above. No prose is needed.

## Checks

- `python3 -m unittest discover -s checks`: every test passes, the brief's own and yours.
