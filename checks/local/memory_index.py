"""Memory index: one line per memory file, in one form, each link resolving, within a bound.

`[memory] indexes` names the index files (default memory/INDEX.md). Each entry is a list item
`- [title](file.md): the hook, on one line`; a dash (hyphen, en or em) with spaces may stand for the colon.
Before the first entry the index may hold prose (any line not starting "- "), an introduction that says how to use it. Between entries it may hold blank lines, heading lines that group them, and `**Shape:**` lines; none is
counted. The first form is the shape's; the second is what a maintainer's real index did before the shape existed. Each link resolves to a file beside the index; a file is listed once; when the index is named
INDEX.md, no other markdown file of its folder is left out. The hook is one physical line, of any number of sentences. The index has at most
`max_lines` lines; the bound is a guess no study sets, tagged PROVISIONAL in the configuration.

What a run with no error guarantees: every listed line has the form, every link resolves, no file is listed twice
or left out, and the bound holds. What it does not: that a hook says what its file holds (judgment).
Time O(size of the indexes + files in their folders).
"""
from __future__ import annotations

import posixpath
import re
from pathlib import Path

from framework.check_api import Finding, files_in_scope, matches_any

NAME = "memory-index"
EXACT = True
SEPARATOR = r"(?::| [\u2013\u2014-]) "  # a colon, or a dash with spaces: the two forms accepted
LINE = re.compile(r"^- \[([^\]]+)\]\(([^)\s]+\.md)\)" + SEPARATOR + r"(\S.*)$")
OPENING = re.compile(r"^(#{1,6} \S.*|\*\*Shape:\*\*.*)$")


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("memory", {})
    bound = settings.get("max_lines", 200)
    in_scope = files_in_scope(root, config)
    findings: list[Finding] = []
    for path in [p for p in in_scope if matches_any(p, settings.get("indexes", ["memory/INDEX.md"]))]:
        lines = (root / path).read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) > bound:
            findings.append(Finding(NAME, path, 0, f"{len(lines)} lines, past the bound of {bound}"))
        folder = posixpath.dirname(path)
        listed: dict[str, int] = {}
        for number, line in enumerate(lines, start=1):
            if not line.strip() or OPENING.match(line):
                continue
            match = LINE.match(line)
            if not match and not listed and not line.startswith("- "):
                continue  # an introduction: prose before the first entry
            if not match:
                findings.append(Finding(NAME, path, number, "a line is '- [title](file.md): the hook, on one line' (a dash may replace the colon)"))
                continue
            target = posixpath.normpath(posixpath.join(folder, match.group(2)))
            if not (root / target).is_file():
                findings.append(Finding(NAME, path, number, f"'{match.group(2)}' does not exist"))
            if target in listed:
                findings.append(Finding(NAME, path, number, f"'{match.group(2)}' is already listed on line {listed[target]}"))
            listed.setdefault(target, number)
        if posixpath.basename(path) == "INDEX.md":
            for other in in_scope:
                if other.endswith(".md") and posixpath.dirname(other) == folder and other != path and other not in listed:
                    findings.append(Finding(NAME, path, 0, f"'{posixpath.basename(other)}' is in the folder and not listed"))
    return findings
