# Brief: list the links of an llms.txt file

## Task

Write a Python function that parses the link list of an llms.txt file and returns each link with its description, and tests for it.

## Decided

- The function is `llms_links(text: str) -> list[tuple[str, str, str]]`, in the module `llms.py` at the project root.
- A link line starts, at the first character of the line, with `- [`. Its form is `- [title](url)`, optionally followed by `: description`. The `]` that ends the title must be followed at once by `(`, and the url ends at the first `)`.
- The description is the text after a colon that comes directly after the `)`, stripped. It is "" when there is no such colon.
- Lines of any other shape are ignored, and so are lines inside a fenced code block (``` fences). Only the first link of a line counts.
- The tests go in `checks/test_llms.py`. The file `checks/test_visible.py` is the brief's check and is not edited.

## To find

- The triple (title, url, description) of each link line, as three strings, in order of appearance.
- The function and its tests, written to the two files above. No prose is needed.

## Checks

- `python3 -m unittest discover -s checks`: every test passes, the brief's own and yours.
