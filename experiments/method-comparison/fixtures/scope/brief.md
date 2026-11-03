# Brief: list the in rows of a scope table

## Task

Write a Python function that parses a Markdown scope table and lists its "in" rows, and tests for it.

## Decided

- The function is `scope_in_rows(markdown: str) -> list[str]`, in the module `scope.py` at the project root.
- The scope table is the table whose header row has "What" as its second cell. Other tables are ignored.
- A row counts as "in" when its first cell, with spaces stripped, is exactly `in`.
- The tests go in `checks/test_scope.py`. The file `checks/test_visible.py` is the brief's check and is not edited.

## To find

- The second cell ("What") of each "in" row, stripped, in order of appearance.
- The function and its tests, written to the two files above. No prose is needed.

## Checks

- `python3 -m unittest discover -s checks`: every test passes, the brief's own and yours.
