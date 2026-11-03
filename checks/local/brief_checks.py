"""Brief checks: a brief has its four parts, in order, and its Checks part names commands that judge the result.

A brief is `brief.md` in a task's folder, with the headings Task, Decided, To find and Checks (design/one-project.md,
decision 2). `[brief] files` names the briefs, and `[brief] exempt` the files those patterns catch that are not briefs. Each of the four parts has at least one line. Each line of Checks
holds a command in backticks and, beside it, a few words saying what passing means. A brief with an empty Checks
part is refused, since the task would have no check.

What a run with no error guarantees: every brief named has the four parts once each, in order, none empty, and each
line of Checks is a command with a stated pass condition. What it does not: that the checks are good ones, that the
commands run, or that the task is well stated (the person's reading).
Time O(size of the briefs).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _parts import CODE, content, order_findings, parts, read, selected  # noqa: E402
from framework.check_api import Finding  # noqa: E402

NAME = "brief-checks"
EXACT = True
REQUIRED = ["Task", "Decided", "To find", "Checks"]
DEFAULT_FILES = ["brief.md", "*/brief.md"]


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("brief", {})
    required = settings.get("parts", REQUIRED)
    minimum = settings.get("pass_words", 2)
    findings: list[Finding] = []
    for path in selected(root, config, "brief", DEFAULT_FILES):
        text = read(root, path)
        findings += order_findings(NAME, path, text, required)
        for title, number, lines in parts(text):
            if title in required and not content(lines):
                findings.append(Finding(NAME, path, number, f"the part '{title}' is empty"
                                        + ("; a task with no check is refused" if title == "Checks" else "")))
            if title == "Checks":
                for line_number, line in content(lines):
                    commands = CODE.findall(line)
                    outside = CODE.sub(" ", line).replace("-", " ").replace("*", " ")
                    words = [word for word in outside.split() if any(char.isalnum() for char in word)]
                    if not commands:
                        findings.append(Finding(NAME, path, line_number, "a check is a command in backticks"))
                    elif len(words) < minimum:
                        findings.append(Finding(NAME, path, line_number, "say what passing means beside the command"))
    return findings
