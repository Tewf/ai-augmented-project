"""A reference solution of the changelog task, used only to check that the judge's tests accept a correct answer."""
import re

_RELEASE = re.compile(r"^## \[([^\]]*)\] - (\d{4}-\d{2}-\d{2})(?:\s.*)?$")


def changelog_releases(markdown):
    out = []
    fenced = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = _RELEASE.match(line)
        if m and m.group(1) != "Unreleased":
            out.append((m.group(1), m.group(2)))
    return out
