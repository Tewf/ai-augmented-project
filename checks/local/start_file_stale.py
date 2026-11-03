"""Start file stale: each path the Commands and Pointers parts name in backticks exists.

A word in backticks counts as a path when it holds a "/" or ends in a known extension (`[start_file] suffixes`),
and does not begin with "-", "~", "$", "<" or "http", nor hold "*", "=" or ":". Paths are looked up from the
project root. A path under a folder that `[start_file] exempt` lists, such as one made at run time, is skipped.
A line whose path does not exist is stale (design/one-project.md, decision 3).

What a run with no error guarantees: every path-like word in the commands and pointers of each start file exists
now. What it does not: that a command runs, or that an existing path still holds what the line says.
Time O(size of the files + paths looked up).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _parts import CODE, content, parts, read, selected  # noqa: E402
from framework.check_api import Finding, matches_any  # noqa: E402

NAME = "start-file-stale"
EXACT = True
DEFAULT_FILES = ["START.md"]
SUFFIXES = (".md", ".py", ".toml", ".yml", ".yaml", ".json", ".sh", ".qmd", ".txt", ".cff")
SKIP_START = ("-", "~", "$", "<", "http")


def path_like(word: str, suffixes: tuple[str, ...]) -> bool:
    if word.startswith(SKIP_START) or any(char in word for char in "*=:"):
        return False
    return "/" in word or word.endswith(suffixes)


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("start_file", {})
    exempt = settings.get("exempt", [])
    suffixes = tuple(settings.get("suffixes", SUFFIXES))
    findings: list[Finding] = []
    for path in selected(root, config, "start_file", DEFAULT_FILES):
        for title, _, lines in parts(read(root, path)):
            if title not in ("Commands", "Pointers"):
                continue
            for number, line in content(lines):
                for span in CODE.findall(line):
                    for word in span.split():
                        word = word.strip(".,;)")
                        if not path_like(word, suffixes) or matches_any(word.removeprefix("./"), exempt):
                            continue
                        if not (root / word).exists():
                            findings.append(Finding(NAME, path, number, f"stale: '{word}' does not exist"))
    return findings
