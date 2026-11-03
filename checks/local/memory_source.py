"""Memory source: each memory file records a date, a type and a source, and a rule has a status.

A memory file is a markdown file listed on a line of a memory index (`[memory] indexes`). It takes one of two forms.
The shape's form holds the lines `**Date:**` (YYYY-MM-DD), `**Type:**` (one of `[memory] types`, default fact, rule,
reference) and `**Source:**`. The practice's form, older than the shape, opens with a YAML header whose
`metadata: type:` is one of `[memory] yaml_types` (default user, feedback, project, reference); its source is
the body: at least one date YYYY-MM-DD or one link, `[text](target)` or `[[name]]`. A file with the header is read as the
practice's form, and the shape's lines are not asked of it. A source in
backticks is a command, an identifier is any other text; neither is run or looked up. A source that is a single
path-like word must exist, looked up from the project root, with a ":line" or "#anchor" ignored. A file of type
rule also has `**Status:**`, which is proposal or accepted (design/one-project.md, decision 3).

What a run with no error guarantees: each memory file named has the three fields, an allowed type, a status when
it is a rule, and a source that is an existing path when it looks like one. What it does not: that a command still
gives the recorded result, that an identifier exists, or how long ago a file was last checked.

A file may also carry one `**Estimate:**` line, in either form: a number, its uncertainty in parentheses (`+- x` written
`±x`, or `a to b`), a comma and the date, as in `12 minutes (8 to 20), 2026-11-03`. Without all three it is refused: an
estimate with no stated doubt or no date cannot be told from a fact. The program does not know that the number is right.
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
HEADER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)(.*)", re.DOTALL)
BODY_DATE = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")
BODY_LINK = re.compile(r"\[[^\]\n]+\]\([^)\s]+\)|\[\[[^\]\n]+\]\]")
YAML_TYPES = ["user", "feedback", "project", "reference"]
SUFFIXES = (".md", ".py", ".toml", ".yml", ".yaml", ".json", ".sh", ".qmd", ".txt", ".cff")


def field(text: str, label: str) -> str | None:
    found = re.search(rf"^\*\*{label}:\*\*[ \t]*(.*)$", text, re.MULTILINE)
    return found.group(1).strip() if found else None


ESTIMATE = re.compile(r"^\d[\d.,]*[^(]*\(\s*(?:±\s*\d[\d.,]*|\d[\d.,]*\s+to\s+\d[\d.,]*)[^)]*\)\s*,\s*\d{4}-\d{2}-\d{2}$")


def estimate_findings(path: str, text: str) -> list[Finding]:
    """Findings for the `**Estimate:**` lines of a file: each is a number, its uncertainty and a date."""
    return [Finding(NAME, path, 0, "an **Estimate:** is a number, its uncertainty in parentheses (±x or a to b), a comma and a date")
            for value in re.findall(r"^\*\*Estimate:\*\*[ \t]*(.*)$", text, re.MULTILINE) if not ESTIMATE.match(value.strip())]


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


def header_type(header: str) -> str | None:
    """The `type:` under `metadata:` in a YAML header, read line by line (no YAML library); quotes are dropped."""
    inside = False
    for line in header.splitlines():
        if re.match(r"^metadata:\s*$", line):
            inside = True
        elif inside and line.strip() and not line[0].isspace():
            inside = False
        elif inside:
            found = re.match(r"^\s+type:\s*(.*?)\s*$", line)
            if found:
                return found.group(1).strip("\"'")
    return None


def check_header(path: str, header: str, body: str, allowed: list[str]) -> list[Finding]:
    """Findings for a file in the practice's form: a type among the allowed, and a date or a link in the body."""
    findings = []
    kind = header_type(header)
    if kind is None or kind not in allowed:
        findings.append(Finding(NAME, path, 0, f"the header's metadata type is one of {', '.join(allowed)}"))
    if not (BODY_DATE.search(body) or BODY_LINK.search(body)):
        findings.append(Finding(NAME, path, 0, "the body records its source: a date YYYY-MM-DD or a link"))
    return findings


def check(root: Path, config: dict) -> list[Finding]:
    types = config.get("memory", {}).get("types", ["fact", "rule", "reference"])
    yaml_types = config.get("memory", {}).get("yaml_types", YAML_TYPES)
    findings: list[Finding] = []
    for path in memory_files(root, config):
        text = (root / path).read_text(encoding="utf-8", errors="replace")
        findings += estimate_findings(path, text)
        header = HEADER.match(text)
        if header:
            findings += check_header(path, header.group(1), header.group(2), yaml_types)
            continue
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
