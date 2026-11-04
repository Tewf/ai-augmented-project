"""Job record: read a folder of briefs and write the jobs as TOML, one `[[job]]` table per brief.

The format is shapes/job-record.md. A job is a folder `<date>_<name>/` holding a `brief.md`. The exporter takes
- the id and the date from the folder name;
- depends_on, repo, kind and outcome from optional lines in the brief's header, the lines between the title and the first part:
  `**Depends on:** a, b`, `**Repo:** name`, `**Kind:** review`, `**Outcome:** pass`;
- tokens_k, dollars and minutes from the Cost block, and produced from its Produced line.
A value that is `pending`, `not measured`, absent, or in another unit than tokens, dollars or minutes is left out of
the table. It is never guessed. Two fields are rules, not readings: `agents` is 1, since a brief is one job, and `wave`
is the rank of the job's date among the dates of the folder, from 0, so briefs of one day share a wave.
This module has no NAME, so the runner loads it and skips it. Run: python3 job_record.py FOLDER [--match GLOB] [--out FILE]
What a run guarantees: every table has an id; every number comes from a Cost line in the allowed form. What it does
not: that the brief's numbers are true.
Standard library only. Time O(size of the briefs).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FOLDER_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})[_-]+(.+)$")
HEADER_LINE = re.compile(r"^\*\*([A-Za-z ]+):\*\*\s*(.*?)\s*$")
COST_LINE = re.compile(r"^\s*[-*]\s*\**(Tokens|Dollars|Minutes|Produced):\**\s*(.*?)\s*$")
NUMBER_UNIT = re.compile(r"^(\d[\d,]*(?:\.\d+)?)\s*([A-Za-z$]+)")
KINDS = ("setup", "review", "audit", "design", "build", "experiment", "upkeep")
OUTCOMES = ("pass", "fail")
UNITS = {"tokens": ("tokens", "token"), "dollars": ("dollars", "dollar", "usd", "$"),
         "minutes": ("minutes", "minute", "min", "mins")}
BLANK = ("pending", "not measured", "")


def measured(value: str, quantity: str) -> float | None:
    """The number of a Cost value when its unit is the quantity's own; None for pending, not measured or another unit."""
    if value.strip().lower() in BLANK:
        return None
    found = NUMBER_UNIT.match(value.strip())
    if not found or found.group(2).lower() not in UNITS[quantity]:
        return None
    return float(found.group(1).replace(",", ""))


def header_of(text: str) -> dict[str, str]:
    """The `**Label:** value` lines between the title and the first second-level heading, by lower-case label."""
    found: dict[str, str] = {}
    for line in text.splitlines()[1:]:
        if line.startswith("## "):
            break
        match = HEADER_LINE.match(line)
        if match:
            found[match.group(1).strip().lower()] = match.group(2)
    return found


def cost_of(text: str) -> dict[str, str]:
    """The four lines of the Cost part by label, empty when the brief has none."""
    found: dict[str, str] = {}
    inside = False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip() == "Cost"
            continue
        match = COST_LINE.match(line) if inside else None
        if match:
            found[match.group(1)] = match.group(2)
    return found


def identity(folder: str) -> tuple[str, str]:
    """(id, date) from a folder name; a name without a date prefix has an empty date."""
    match = FOLDER_NAME.match(folder)
    return (match.group(2), match.group(1)) if match else (folder, "")


def job_of(folder: str, text: str) -> dict:
    """The record of one brief: only the fields the brief states."""
    name, date = identity(folder)
    header, cost = header_of(text), cost_of(text)
    job: dict = {"id": name}
    if date:
        job["date"] = date
    if header.get("kind", "") in KINDS:
        job["kind"] = header["kind"]
    if header.get("repo"):
        job["repo"] = header["repo"]
    needs = [item.strip() for item in header.get("depends on", "").split(",") if item.strip()]
    if needs:
        job["depends_on"] = needs
    job["agents"] = 1
    tokens, dollars, minutes = (measured(cost.get(label, ""), quantity)
                                for label, quantity in (("Tokens", "tokens"), ("Dollars", "dollars"), ("Minutes", "minutes")))
    if tokens is not None:
        job["tokens_k"] = round(tokens / 1000, 3)
        job["tokens_source"] = "recorded"
    if dollars is not None:
        job["dollars"] = dollars
    if minutes is not None:
        job["minutes"] = minutes
    produced = cost.get("Produced", "")
    if produced.strip().lower() not in BLANK:
        job["produced"] = produced
    if header.get("outcome", "").lower() in OUTCOMES:
        job["outcome"] = header["outcome"].lower()
    return job


def export(root: Path, match: str = "*") -> list[dict]:
    """The jobs of every `<match>/brief.md` under root, in folder order, with each job's wave from the rank of its date."""
    jobs = [job_of(path.parent.name, path.read_text(encoding="utf-8", errors="replace"))
            for path in sorted(root.glob(f"{match}/brief.md"))]
    dates = sorted({job["date"] for job in jobs if "date" in job})
    for job in jobs:
        if "date" in job:
            job["wave"] = dates.index(job["date"])
    return jobs


def quoted(text: str) -> str:
    """A TOML basic string."""
    out = text.replace("\\", "\\\\").replace('"', '\\"')
    return '"' + "".join(f"\\u{ord(c):04x}" if ord(c) < 32 or ord(c) == 127 else c for c in out) + '"'


def value(item) -> str:
    if isinstance(item, list):
        return "[" + ", ".join(quoted(x) for x in item) + "]"
    if isinstance(item, str):
        return quoted(item)
    return f"{item:g}" if isinstance(item, float) else str(item)


ORDER = ("id", "date", "wave", "kind", "repo", "depends_on", "agents", "tokens_k", "tokens_source", "dollars",
         "minutes", "produced", "outcome")


def to_toml(jobs: list[dict]) -> str:
    """The jobs as `[[job]]` tables, fields in a fixed order."""
    blocks = []
    for job in jobs:
        lines = ["[[job]]"] + [f"{key} = {value(job[key])}" for key in ORDER if key in job]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", type=Path, help="a folder of <date>_<name>/brief.md")
    parser.add_argument("--match", default="*", help="only the subfolders whose name matches, such as '2026-11-04_*'")
    parser.add_argument("--out", type=Path, help="write the TOML here instead of to the output")
    args = parser.parse_args(argv)
    jobs = export(args.folder, args.match)
    if not jobs:
        print(f"error: no */brief.md under {args.folder}", file=sys.stderr)
        return 2
    text = to_toml(jobs)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
