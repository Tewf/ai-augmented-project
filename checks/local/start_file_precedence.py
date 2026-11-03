"""Start file precedence: the sentence that gives the code precedence stands once, in the Precedence part.

`[start_file] precedence` is the phrase the sentence must hold (default "follow the code"), matched without regard
to case. The phrase must appear in the Precedence part of each start file named, and nowhere else in the file, so
the sentence has one place (design/one-project.md, decision 3).

What a run with no error guarantees: the phrase is in the Precedence part and in no other line. What it does not: that
the sentence is well put, or that a model obeys it.
Time O(size of the files).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _parts import blanked, parts, read, selected  # noqa: E402
from framework.check_api import Finding  # noqa: E402

NAME = "start-file-precedence"
EXACT = True
DEFAULT_FILES = ["START.md"]


def check(root: Path, config: dict) -> list[Finding]:
    phrase = config.get("start_file", {}).get("precedence", "follow the code").lower()
    findings: list[Finding] = []
    for path in selected(root, config, "start_file", DEFAULT_FILES):
        text = read(root, path)
        where = [number for number, line in enumerate(blanked(text).splitlines(), start=1) if phrase in line.lower()]
        inside = {number for title, _, lines in parts(text) if title == "Precedence" for number, line in lines if phrase in line.lower()}
        if not inside:
            findings.append(Finding(NAME, path, 0, f"the Precedence part has no sentence with '{phrase}'"))
        for number in where:
            if number not in inside:
                findings.append(Finding(NAME, path, number, "the precedence sentence is said once, in the Precedence part"))
        if len(inside) > 1:
            findings.append(Finding(NAME, path, min(inside), "the precedence sentence is said once"))
    return findings
