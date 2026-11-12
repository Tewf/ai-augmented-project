"""Brief checks: a brief has its four parts, in order, and its Checks part names commands that judge the result.

A brief is `brief.md` in a task's folder, with the headings Task, Decided, To find and Checks (design/one-project.md,
decision 2). `[brief] files` names the briefs, and `[brief] exempt` the files those patterns catch that are not briefs. Each of the four parts has at least one line. Each line of Checks
holds a command in backticks and, beside it, a few words saying what passing means. A brief with an empty Checks
part is refused, since the task would have no check.

What a run with no error guarantees: every brief named has the four parts once each, in order, none empty, and each
line of Checks is a command with a stated pass condition. What it does not: that the checks are good ones, that the
commands run, or that the task is well stated (the person's reading).

A brief may close with a fifth part, Cost, which the owner fills when the task ends: four labelled lines, Tokens,
Dollars, Minutes (the person's) and Produced, in that order. A value is a number with its unit, or `pending` before
the task ends, or `not measured`; it is never guessed. Produced is any text. `[brief] cost = "required"` makes the
part mandatory; the default leaves it optional, since a brief is written before the task and an open one has no cost yet.
The check does not know that a number is true.

Decided may hold two labelled lines (record 0014). `- Checkout: `<path>` on `<branch>``: the folder the task works in
and the branch it must be on, since a path alone has sent a worker to the right repository on the wrong branch.
`- Shapes to read: [<name>](<link to a shape>)`: the shapes the result follows, to read before writing. When present,
each is checked for its form: a path and a branch in backticks, joined by "on"; at least one link to a `.md` file.
`[brief] checkout = "required"` makes the Checkout line mandatory. The check does not know that the branch exists.
Time O(size of the briefs).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _parts import CODE, content, order_findings, parts, read, selected  # noqa: E402
from framework.check_api import Finding  # noqa: E402

NAME = "brief-checks"
EXACT = True
REQUIRED = ["Task", "Decided", "To find", "Checks"]
DEFAULT_FILES = ["brief.md", "*/brief.md"]
COST_LABELS = ["Tokens", "Dollars", "Minutes", "Produced"]
COST_LINE = re.compile(r"^\s*[-*]\s*\**([A-Za-z]+):\**\s*(.*?)\s*$")
CHECKOUT = re.compile(r"^\s*[-*]\s*\**Checkout:\**\s*(.*)$")
CHECKOUT_FORM = re.compile(r"`[^`]+`\s+on\s+`[^`]+`")
SHAPES = re.compile(r"^\s*[-*]\s*\**Shapes to read:\**\s*(.*)$")
SHAPE_LINK = re.compile(r"\]\([^)\s]+\.md(?:#[^)]*)?\)")
COST_VALUE = re.compile(r"^(pending|not measured|\d[\d.,]*\s*\S+.*)$", re.IGNORECASE)


def cost_findings(path: str, lines: list[tuple[int, str]]) -> list[Finding]:
    """Findings for a Cost part: the four labels once each, in order, each with a value of the allowed form."""
    findings: list[Finding] = []
    found = []
    for number, line in content(lines):
        match = COST_LINE.match(line)
        if not match:
            findings.append(Finding(NAME, path, number, "a Cost line is '- Label: value'"))
            continue
        label, value = match.group(1), match.group(2)
        found.append(label)
        if label in COST_LABELS[:3] and not COST_VALUE.match(value):
            findings.append(Finding(NAME, path, number, f"{label} is a number with its unit, 'pending' or 'not measured'"))
        if label == "Produced" and not value:
            findings.append(Finding(NAME, path, number, "Produced says what the task made, or 'pending'"))
    if found != COST_LABELS:
        findings.append(Finding(NAME, path, lines[0][0] - 1 if lines else 0,
                                f"the Cost lines are {', '.join(COST_LABELS)}, once each, in that order"))
    return findings


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("brief", {})
    required = settings.get("parts", REQUIRED)
    minimum = settings.get("pass_words", 2)
    findings: list[Finding] = []
    for path in selected(root, config, "brief", DEFAULT_FILES):
        text = read(root, path)
        has_cost = any(title == "Cost" for title, _, _ in parts(text))
        if not has_cost and settings.get("cost") == "required":
            findings.append(Finding(NAME, path, 0, "missing part 'Cost': the owner fills it when the task ends"))
        findings += order_findings(NAME, path, text, required + (["Cost"] if has_cost else []))
        for title, number, lines in parts(text):
            if title == "Cost":
                findings += cost_findings(path, lines) if content(lines) else [
                    Finding(NAME, path, number, "the part 'Cost' is empty")]
            if title in required and not content(lines):
                findings.append(Finding(NAME, path, number, f"the part '{title}' is empty"
                                        + ("; a task with no check is refused" if title == "Checks" else "")))
            if title == "Decided":
                checkout = False
                for line_number, line in content(lines):
                    if (match := CHECKOUT.match(line)):
                        checkout = True
                        if not CHECKOUT_FORM.search(match.group(1)):
                            findings.append(Finding(NAME, path, line_number,
                                                    "a Checkout line is `<path>` on `<branch>`, both in backticks"))
                    if (match := SHAPES.match(line)) and not SHAPE_LINK.search(match.group(1)):
                        findings.append(Finding(NAME, path, line_number,
                                                "a Shapes to read line links at least one shape's .md file"))
                if not checkout and settings.get("checkout") == "required":
                    findings.append(Finding(NAME, path, number, "Decided has no Checkout line: name the path and its branch"))
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
