"""Report: rebuilds the tables of results.md from results.jsonl.

Usage: python3 report.py            (prints the tables; results.md embeds them)
A session counts once: the last record of a cell that is not an error. Wilson intervals at 95%.
Time O(records).
"""
from __future__ import annotations

import json
from math import sqrt
from pathlib import Path
from statistics import mean, median

from tasks import ARMS, TASKS

HERE = Path(__file__).resolve().parent


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def load() -> list[dict]:
    cells: dict[tuple, dict] = {}
    errors: list[dict] = []
    for ln in (HERE / "results.jsonl").read_text().splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        if r.get("error"):
            errors.append(r)
        else:
            cells[(r["task"], r["arm"], r["run"])] = r
    return list(cells.values()), errors


def rate(rs: list[dict], key: str) -> str:
    k = sum(1 for r in rs if r["verdict"][key])
    lo, hi = wilson(k, len(rs))
    return f"{k}/{len(rs)} ({100*k/len(rs):.0f}%, {100*lo:.0f}-{100*hi:.0f}%)" if rs else "none"


def tables() -> str:
    rs, errors = load()
    out = []
    names = {"alone": "model alone", "method": "model with the method"}
    out.append("| Arm | Sessions | Hidden pass | Hidden pass without the name | Visible pass |\n|---|---|---|---|---|")
    for a in ARMS:
        x = [r for r in rs if r["arm"] == a]
        out.append(f"| {names[a]} | {len(x)} | {rate(x, 'hidden')} | {rate(x, 'hidden_namefree')} | {rate(x, 'visible') if a == 'method' else 'not given'} |")
    out.append("\nHidden pass per task, passes out of sessions:\n\n| Task | model alone | model with the method |\n|---|---|---|")
    for t in TASKS:
        cols = []
        for a in ARMS:
            x = [r for r in rs if r["task"] == t and r["arm"] == a]
            cols.append(f"{sum(r['verdict']['hidden'] for r in x)}/{len(x)} ({sum(r['verdict']['hidden_namefree'] for r in x)}/{len(x)} without the name)")
        out.append(f"| {t} | {cols[0]} | {cols[1]} |")
    out.append("\nCounts per session, mean (median):\n\n| Count | model alone | model with the method |\n|---|---|---|")
    rows = [("total tokens (all five fields)", "tokens_total"), ("output tokens", "tokens_output"), ("fresh input tokens (input + cache write)", None),
            ("turns", "turns"), ("tool calls", "tool_calls"), ("questions asked", "questions"),
            ("files read before the first edit", "files_before_first_edit"), ("cost, dollars", "cost"), ("seconds", "seconds")]
    for label, key in rows:
        cells = []
        for a in ARMS:
            x = [r for r in rs if r["arm"] == a]
            vals = [r["tokens_input"] + r["tokens_cache_write"] for r in x] if key is None else [r[key] for r in x]
            fmt = "{:.4f}" if key == "cost" else "{:.0f}" if key in (None, "tokens_total", "tokens_output", "seconds") else "{:.1f}"
            cells.append(f"{fmt.format(mean(vals))} ({fmt.format(median(vals))})" if vals else "none")
        out.append(f"| {label} | {cells[0]} | {cells[1]} |")
    m = [r for r in rs if r["arm"] == "method"]
    s = sum(r["start_md_first"] for r in m)
    out.append(f"\nSTART.md opened by the first tool call: {s}/{len(m)} method sessions. In the alone arm the file does not exist.")
    total = sum(r["cost"] for r in rs)
    out.append(f"\nCost of the {len(rs)} counted sessions, by the agent's own figure: {total:.3f} dollars. Sessions that failed before a reply: {len(errors)}.")
    out.append("\nWhy hidden tests failed, by arm:\n\n| Arm | Task | Detail |\n|---|---|---|")
    for r in sorted(rs, key=lambda r: (r["arm"], r["task"], r["run"])):
        v = r["verdict"]
        if not v["hidden"]:
            out.append(f"| {r['arm']} | {r['task']} {r['run']} | {v['how']}: {v['detail'][:110].replace('|', '/')} |")
    return "\n".join(out)


if __name__ == "__main__":
    print(tables())
