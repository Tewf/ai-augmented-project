# Brief: the start-file check

**Shape:** [brief](../brief.md)

## Task

Write the check that decides whether a start file has its four parts and stays within its bound.
It runs on every commit.

## Decided

- The file is `START.md`. Its headings are Commands, Conventions, Precedence and Pointers, in that order.
- The bound is 200 lines. It is read from `checks/config.toml` and tagged PROVISIONAL there.
- The module is `checks/local/start_file.py`. No other module of `checks/local/` changes.

## To find

- The module, with a docstring that says what a clean run guarantees and what it does not.
- Unit tests that fail a file one line over the bound and pass a file at the bound.

## Checks

- `python3 -m unittest discover -s checks`: every test passes and none is skipped.
- `python3 checks/out/standard/checks/run.py . --tiers program,meaning --judge flag`: reports 0 errors.
