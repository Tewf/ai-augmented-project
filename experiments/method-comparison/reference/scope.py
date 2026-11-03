"""A reference solution, used only to check that the judge's tests accept a correct answer."""


def _cells(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def scope_in_rows(markdown):
    rows = []
    in_scope = False
    for line in markdown.splitlines():
        if not line.strip().startswith("|"):
            in_scope = False
            continue
        cells = _cells(line)
        if len(cells) >= 2 and cells[1] == "What":
            in_scope = True
            continue
        if in_scope and len(cells) >= 2 and cells[0] == "in":
            rows.append(cells[1])
    return rows
