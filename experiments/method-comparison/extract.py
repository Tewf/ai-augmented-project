"""Extract: the counts of one session, read from the agent's own database after the session.

Usage: extract.py DB      (prints the counts as JSON)

Definitions are those of protocol.md, fixed before the counted sessions. Only the top-level session counts; a
subagent session opened for a task is a child and is left out of the turns but its tokens are in the parent's totals
as the agent reports them. Time O(messages + parts).
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys

READ_TOOLS = {"read", "view", "cat"}
WRITE_TOOLS = {"write", "edit", "multiedit", "patch", "apply_patch", "str_replace_editor"}
SHELL_READ = re.compile(r"\b(cat|head|tail|sed|less|nl|bat)\b")
PATH = re.compile(r"[\w./-]+\.\w+|[\w./-]*/[\w./-]+")


def tool_paths(name: str, inp: dict) -> list[str]:
    """Paths a tool call opens for reading; shell reads are found by the command's words."""
    if name in READ_TOOLS:
        p = inp.get("filePath") or inp.get("file_path") or inp.get("path") or ""
        return [p] if p else []
    if name == "bash":
        cmd = inp.get("command", "")
        if SHELL_READ.search(cmd):
            return [w for w in PATH.findall(cmd) if not w.startswith("-")]
    return []


def counts(db: str) -> dict:
    c = sqlite3.connect(db)
    row = c.execute("select id, cost, tokens_input, tokens_output, tokens_reasoning, tokens_cache_read, tokens_cache_write "
                    "from session where parent_id is null order by time_created limit 1").fetchone()
    if row is None:
        return {"session": None}
    sid, cost, t_in, t_out, t_rea, t_cr, t_cw = row
    messages = [(r[0], json.loads(r[1])) for r in c.execute("select id, data from message where session_id=? order by time_created, id", (sid,))]
    parts: dict[str, list[dict]] = {}
    for mid, data in c.execute("select message_id, data from part where session_id=? order by time_created, id", (sid,)):
        parts.setdefault(mid, []).append(json.loads(data))
    turns, questions, tools = 0, 0, []
    errors = []
    for mid, d in messages:
        if d.get("role") != "assistant":
            continue
        turns += 1
        if d.get("error"):
            errors.append(str(d["error"])[:200])
        for p in parts.get(mid, []):
            if p.get("type") == "text":
                questions += sum(1 for ln in p.get("text", "").splitlines() if ln.rstrip().rstrip("*_)\"'").endswith("?"))
            elif p.get("type") == "tool":
                name = p.get("tool", "")
                inp = p.get("state", {}).get("input", {}) or {}
                if name == "question":
                    questions += 1
                tools.append((name, inp))
    first_edit = next((i for i, (n, _) in enumerate(tools) if n in WRITE_TOOLS), len(tools))
    opened: list[str] = []
    for n, inp in tools[:first_edit]:
        for p in tool_paths(n, inp):
            if p not in opened:
                opened.append(p)
    first_paths = tool_paths(*tools[0]) if tools else []
    return {
        "session": sid, "cost": cost, "tokens_input": t_in, "tokens_output": t_out, "tokens_reasoning": t_rea,
        "tokens_cache_read": t_cr, "tokens_cache_write": t_cw, "tokens_total": t_in + t_out + t_rea + t_cr + t_cw,
        "turns": turns, "tool_calls": len(tools), "questions": questions, "files_before_first_edit": len(opened),
        "start_md_first": bool(first_paths) and first_paths[0].endswith("START.md"),
        "edited": first_edit < len(tools), "tool_names": sorted({n for n, _ in tools}), "errors": errors,
    }


if __name__ == "__main__":
    print(json.dumps(counts(sys.argv[1]), indent=1))
