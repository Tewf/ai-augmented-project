"""Run the method comparison: 30 sessions of the agent, each judged by a program.

Usage: ANTHROPIC_API_KEY=... python3 run.py SCRATCH [--only task:arm:i ...] [--harness]
The key is read from the environment of the run and handed on to the agent in that environment only. It is never
printed or written. Results are appended to results.jsonl as each session ends; a stopped run resumes.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

import extract
import judge
from tasks import ARMS, TASKS

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results.jsonl"
KILO = os.environ.get("KILO", str(Path.home() / ".vscode/extensions/kilocode.kilo-code-7.8.18-linux-x64/bin/kilo"))
MODEL = "anthropic/claude-haiku-5-5"
SEED = 20261103
RUNS = 5
SESSION_TIMEOUT = 900
HARNESS_SENTENCE = "Write a Python function that reverses the order of the words in a string, and tests for it."


def cells() -> list[tuple[str, str, int]]:
    order = [(t, a, i) for t in TASKS for a in ARMS for i in range(1, RUNS + 1)]
    random.Random(SEED).shuffle(order)
    return order


def prepare(scratch: Path, task: str, arm: str, i: int) -> Path:
    base = scratch / f"{task}-{arm}-{i}"
    shutil.rmtree(base, ignore_errors=True)
    project = base / "p"
    if arm == "method":
        shutil.copytree(HERE / "fixtures" / "common", project)
        (project / "memory").mkdir(exist_ok=True)
        if task in TASKS:
            for f in (HERE / "fixtures" / task).iterdir():
                (shutil.copytree if f.is_dir() else shutil.copy)(f, project / f.name)
        else:  # the harness check: a brief made from its sentence, with the same four parts
            (project / "brief.md").write_text(
                f"# Brief: reverse words\n\n## Task\n\n{HARNESS_SENTENCE}\n\n## Decided\n\n- The function is `reverse_words(text: str) -> str`, in `words.py` at the project root.\n\n"
                "## To find\n\n- The words in reverse order, joined by one space.\n\n## Checks\n\n- `python3 -m unittest discover -s checks`: every test passes.\n")
            (project / "checks").mkdir(exist_ok=True)
    else:
        project.mkdir(parents=True)
    for d in ("config/kilo", "data", "state", "cache"):
        (base / "xdg" / d).mkdir(parents=True, exist_ok=True)
    shutil.copy(HERE / "kilo.jsonc", base / "xdg/config/kilo/kilo.jsonc")
    cache = Path.home() / ".cache/kilo"
    if cache.is_dir():
        shutil.copytree(cache, base / "xdg/cache/kilo")
    return base


def environment(base: Path) -> dict:
    env = dict(os.environ)
    x = base / "xdg"
    env.update(XDG_CONFIG_HOME=str(x / "config"), XDG_DATA_HOME=str(x / "data"), XDG_STATE_HOME=str(x / "state"),
               XDG_CACHE_HOME=str(x / "cache"), KILO_TELEMETRY_LEVEL="off")
    dead = "http://127.0.0.1:9"
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        env[k] = dead
    env["NO_PROXY"] = env["no_proxy"] = "127.0.0.1,localhost,api.anthropic.com"
    return env


def session(base: Path, sentence: str, arm: str) -> dict:
    project = base / "p"
    cmd = [KILO, "run", "-m", MODEL]
    if arm == "method":  # -f takes a list, so it goes before another flag, and the message after that
        cmd += ["-f", str(project / ".handover/note.md"), "--format", "json", "Start from the attached hand-over note."]
    else:
        cmd += ["--format", "json", sentence]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=project, env=dict(environment(base), PWD=str(project)), capture_output=True, text=True,
                           timeout=SESSION_TIMEOUT, stdin=subprocess.DEVNULL)
        code, err = p.returncode, p.stderr
        (base / "run.json").write_text(p.stdout)
        (base / "run.err").write_text(err)
    except subprocess.TimeoutExpired:
        code, err = "timeout", ""
    out = {"exit": code, "seconds": round(time.time() - t0)}
    db = base / "xdg/data/kilo/kilo.db"
    out.update(extract.counts(str(db)) if db.exists() else {"session": None})
    return out


def one(scratch: Path, task: str, arm: str, i: int, sentence: str | None = None) -> dict:
    spec = TASKS.get(task)
    sentence = sentence or spec["sentence"]
    attempts = []
    for attempt in (1, 2):
        base = prepare(scratch, task, arm, i)
        rec = session(base, sentence, arm)
        attempts.append({"attempt": attempt, "exit": rec["exit"], "session": rec.get("session"), "turns": rec.get("turns", 0)})
        if rec.get("exit") == 0 and rec.get("session") and rec.get("turns", 0) > 0 and not rec.get("errors"):
            break
    rec.update(task=task, arm=arm, run=i, attempts=attempts)
    rec["error"] = not (rec.get("exit") == 0 and rec.get("session") and rec.get("turns", 0) > 0 and not rec.get("errors"))
    rec["verdict"] = judge.judge(base / "p", task, spec["function"]) if spec else None
    return rec


def done() -> set[tuple[str, str, int]]:
    if not RESULTS.exists():
        return set()
    recs = (json.loads(ln) for ln in RESULTS.read_text().splitlines() if ln.strip())
    return {(r["task"], r["arm"], r["run"]) for r in recs if not r.get("error")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scratch")
    ap.add_argument("--harness", action="store_true", help="one discarded session per arm on a fourth task")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--rejudge", action="store_true", help="judge again every recorded session from its folder")
    a = ap.parse_args()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set in the environment of the run")
    scratch = Path(a.scratch).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    if a.harness:
        for arm in ARMS:
            rec = one(scratch, "harness", arm, 1, HARNESS_SENTENCE)
            (scratch / f"harness-{arm}.json").write_text(json.dumps(rec, indent=1))
            print(arm, {k: rec.get(k) for k in ("exit", "turns", "tokens_total", "cost", "tool_names", "error")}, flush=True)
        return
    if a.rejudge:
        lines = [json.loads(ln) for ln in RESULTS.read_text().splitlines() if ln.strip()]
        for rec in lines:
            folder = scratch / f"{rec['task']}-{rec['arm']}-{rec['run']}" / "p"
            if not rec.get("error") and folder.is_dir():
                rec["verdict"] = judge.judge(folder, rec["task"], TASKS[rec["task"]]["function"])
        RESULTS.write_text("".join(json.dumps(x) + "\n" for x in lines))
        return
    finished = done()
    todo = [c for c in cells() if c not in finished]
    if a.limit:
        todo = todo[:a.limit]
    for n, (task, arm, i) in enumerate(todo, 1):
        rec = one(scratch, task, arm, i)
        with RESULTS.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        v = rec["verdict"]
        print(f"[{n}/{len(todo)}] {task} {arm} {i}: hidden={v['hidden']} namefree={v['hidden_namefree']} turns={rec.get('turns')} "
              f"tokens={rec.get('tokens_total')} cost={rec.get('cost')} error={rec['error']}", flush=True)


if __name__ == "__main__":
    main()
