"""Start file: START.md has its four parts in order, each command in backticks, and stays within its bound.

The start file is the first file a session is handed (design/one-project.md, decision 2). `[start_file] files` names
it (`exempt` removes files). Its level-2 headings are Commands, Conventions, Precedence and Pointers, once each, in that order, none empty.
Each line of Commands holds a command in backticks, and each line of Pointers a list item. The file has at most
`max_lines` lines; the bound is a guess no study sets, so it is tagged PROVISIONAL in the configuration.

What a run with no error guarantees: each start file named has the four parts, a command per line in backticks, and
no more lines than the bound. What it does not: that a line states what the code cannot (judgment), or that a
command runs.
Time O(size of the files).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _parts import CODE, content, order_findings, parts, read, selected  # noqa: E402
from framework.check_api import Finding  # noqa: E402

NAME = "start-file"
EXACT = True
REQUIRED = ["Commands", "Conventions", "Precedence", "Pointers"]
DEFAULT_FILES = ["START.md"]


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("start_file", {})
    bound = settings.get("max_lines", 200)
    findings: list[Finding] = []
    for path in selected(root, config, "start_file", DEFAULT_FILES):
        text = read(root, path)
        size = len(text.splitlines())
        if size > bound:
            findings.append(Finding(NAME, path, 0, f"{size} lines, past the bound of {bound}: a line goes before another is added"))
        findings += order_findings(NAME, path, text, REQUIRED)
        for title, number, lines in parts(text):
            if title in REQUIRED and not content(lines):
                findings.append(Finding(NAME, path, number, f"the part '{title}' is empty"))
            for line_number, line in content(lines):
                if title == "Commands" and not CODE.search(line):
                    findings.append(Finding(NAME, path, line_number, "a command is written in backticks, one per line"))
                if title == "Pointers" and not line.lstrip().startswith(("-", "*")):
                    findings.append(Finding(NAME, path, line_number, "a pointer is one list item: the task, then what to read"))
    return findings
