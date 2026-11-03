"""Memory source: each memory file records a date, a type and a source, and a rule has a status.

A memory file is a markdown file listed on a line of a memory index (`[memory] indexes`). It holds the lines `**Date:**`
(YYYY-MM-DD), `**Type:**` (one of `[memory] types`, default fact, rule, reference) and `**Source:**`. A source in
backticks is a command, an identifier is any other text; neither is run or looked up. A source that is a single
path-like word must exist, looked up from the project root, with a ":line" or "#anchor" ignored. A file of type
rule also has `**Status:**`, which is proposal or accepted (design/one-project.md, decision 3).

What a run with no error guarantees: each memory file named has the three fields, an allowed type, a status when
it is a rule, and a source that is an existing path when it looks like one. What it does not: that a command still
gives the recorded result, that an identifier exists, or how long ago a file was last checked.
Time O(size of the files).
"""
from __future__ import annotations

import posixpath
import re
from pathlib import Path

from framework.check_api import Finding, files_in_scope, matches_any

NAME = "memory-source"
EXACT = True
LISTED = re.compile(r"^- \[[^\]]+\]\(([^)\s]+\.md)\)", re.MULTILINE)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SUFFIXES = (".md", ".py", ".toml", ".yml", ".yaml", ".json", ".sh", ".qmd", ".txt", ".cff")


def field(text: str, label: str) -> str | None:
    found = re.search(rf"^\*\*{label}:\*\*[ \t]*(.*)$", text, re.MULTILINE)
    return found.group(1).strip() if found else None


def memory_files(root: Path, config: dict) -> list[str]:
    patterns = config.get("memory", {}).get("indexes", ["memory/INDEX.md"])
    listed: list[str] = []
    for index in [p for p in files_in_scope(root, config) if matches_any(p, patterns)]:
        text = (root / index).read_text(encoding="utf-8", errors="replace")
        for target in LISTED.findall(text):
            path = posixpath.normpath(posixpath.join(posixpath.dirname(index), target))
            if (root / path).is_file() and path not in listed:
                listed.append(path)
    return listed


def check(root: Path, config: dict) -> list[Finding]:
    types = config.get("memory", {}).get("types", ["fact", "rule", "reference"])
    findings: list[Finding] = []
    for path in memory_files(root, config):
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        date, kind, source = field(text, "Date"), field(text, "Type"), field(text, "Source")
        if date is None or not DATE.match(date):
            findings.append(Finding(NAME, path, 0, "a memory file records its **Date:** as YYYY-MM-DD"))
        if kind is None or kind not in types:
            findings.append(Finding(NAME, path, 0, f"a memory file records its **Type:**, one of {', '.join(types)}"))
        if kind == "rule" and field(text, "Status") not in ("proposal", "accepted"):
            findings.append(Finding(NAME, path, 0, "a rule has **Status:** proposal or accepted"))
        if not source:
            findings.append(Finding(NAME, path, 0, "a memory file records the **Source:** that proves it"))
        elif " " not in source and not source.startswith("`"):
            target = re.split(r"[:#]", source)[0]
            if (target.endswith(SUFFIXES) or "/" in target) and "://" not in source and not (root / target).exists():
                findings.append(Finding(NAME, path, 0, f"stale: the source '{target}' does not exist"))
    return findings
