"""Shared reading of a markdown file by headings; no check lives here, so the runner skips it.

A part is the text under one heading of a given level, up to the next heading of that level or a shallower one.
Fenced code blocks are blanked first, so a heading inside one is not a heading. Line numbers are preserved.
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import FENCED_BLOCK, Finding, files_in_scope, matches_any

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
CODE = re.compile(r"`([^`\n]+)`")


def blanked(text: str) -> str:
    """The text with fenced blocks emptied, line count kept."""
    return FENCED_BLOCK.sub(lambda match: "\n" * match.group(0).count("\n"), text)


def parts(text: str, level: int = 2) -> list[tuple[str, int, list[tuple[int, str]]]]:
    """(title, line of the heading, [(line number, line text)]) for each heading of the level, in order."""
    found: list[tuple[str, int, list[tuple[int, str]]]] = []
    for number, line in enumerate(blanked(text).splitlines(), start=1):
        heading = HEADING.match(line)
        if heading and len(heading.group(1)) <= level:
            if len(heading.group(1)) == level:
                found.append((heading.group(2), number, []))
            else:
                found.append(("", number, []))  # a shallower heading closes the part and owns no part
            continue
        if found:
            found[-1][2].append((number, line))
    return [part for part in found if part[0]]


def content(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """The non-blank lines of a part."""
    return [(number, line) for number, line in lines if line.strip()]


def selected(root: Path, config: dict, table: str, default: list[str]) -> list[str]:
    """The markdown files in scope that the table's `files` patterns name, less those its `exempt` names."""
    settings = config.get(table, {})
    patterns = settings.get("files", default)
    return [path for path in files_in_scope(root, config)
            if matches_any(path, patterns) and not matches_any(path, settings.get("exempt", []))]


def read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8", errors="replace")


def order_findings(name: str, path: str, text: str, required: list[str]) -> list[Finding]:
    """Findings when the level-2 headings are not exactly the required ones, in order."""
    titles = parts(text)
    found = [title for title, _, _ in titles]
    findings = []
    for title, number, _ in titles:
        if title not in required:
            findings.append(Finding(name, path, number, f"unexpected part '{title}': the parts are {', '.join(required)}"))
    wanted = [title for title in required if title in found]
    if [title for title in found if title in required] != wanted or len(set(found)) != len(found):
        findings.append(Finding(name, path, 0, f"the parts must come once each, in the order {', '.join(required)}"))
    for title in required:
        if title not in found:
            findings.append(Finding(name, path, 0, f"missing part '{title}'"))
    return findings
