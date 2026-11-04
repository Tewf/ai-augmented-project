"""Run one participant through the two person arms of the method comparison, and score them with the experiment's judge.

Usage (standard library only):
    python3 run_person.py P01              # the next arm of participant P01; the first call flips the order coin
    python3 run_person.py P01 --pilot      # the same, and the record says the participant is a pilot
    python3 run_person.py --summary        # the table of every complete run, and the paired test
    python3 run_person.py --self-test      # scores a known answer set and exits 0 when the program works

The id is anonymous: letters and digits, at most 12. One record per arm is written to runs/<id>-<arm>.json after every
task. The tasks, the hidden tests and the scoring are those of the model arms (judge.py, tasks.py, one folder up).
Time O(tasks + size of the answers); the clock is the wall clock of the person.
"""
from __future__ import annotations

import argparse
import datetime
import json
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))
import judge  # noqa: E402  the experiment's own judge, never a copy
from tasks import ARMS, TASKS  # noqa: E402

RUNS = HERE / "runs"
CAP_SECONDS = 30 * 60  # a task is stopped at 30 minutes; protocol.md, Timing
ID_PATTERN = re.compile(r"^[A-Za-z0-9]{1,12}$")
ARM_NAME = {"alone": "person alone", "method": "person with the method"}
METHOD_FILES = ["START.md", "memory/INDEX.md", "brief.md"]  # read in this order, as the hand-over note says


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)  # the file on disk is always whole


def read_json(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def repository_commit() -> str:
    try:
        p = subprocess.run(["git", "-C", str(HERE), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10)
        return p.stdout.strip() if p.returncode == 0 else "unknown"
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"


def prepare_folder(folder: Path, task: str, arm: str) -> None:
    """The alone arm gets an empty folder; the method arm gets the files of the model arm, copied from the fixtures."""
    shutil.rmtree(folder, ignore_errors=True)
    if arm == "alone":
        folder.mkdir(parents=True)
        return
    shutil.copytree(PARENT / "fixtures" / "common", folder)
    for f in (PARENT / "fixtures" / task).iterdir():
        (shutil.copytree if f.is_dir() else shutil.copy)(f, folder / f.name)


def collect(folder: Path) -> dict[str, str]:
    """The person's source files at the folder root, as text: what the judge reads."""
    return {p.name: p.read_text(encoding="utf-8", errors="replace") for p in judge.source_files(folder)}


def score_folder(folder: Path, task: str) -> dict:
    return judge.judge(folder, task, TASKS[task]["function"])


def task_order(participant: str, arm: str) -> list[str]:
    order = list(TASKS)
    random.Random(f"{participant}-{arm}").shuffle(order)
    return order


def passes(record: dict, key: str = "hidden") -> int:
    return sum(1 for t in record["tasks"].values() if t["verdict"][key])


def run_task(record: dict, task: str, folder: Path, wait) -> None:
    """One task: show it, time it, collect and score the answer. wait(kind, folder) blocks until the person presses Enter."""
    arm = record["arm"]
    prepare_folder(folder, task, arm)
    wait("start", folder)
    t0, started = time.monotonic(), now()
    wait("finish", folder)
    seconds = round(time.monotonic() - t0)
    record["tasks"][task] = {
        "start": started, "end": now(), "seconds": seconds, "over_cap": seconds > CAP_SECONDS,
        "files": collect(folder), "verdict": score_folder(folder, task),
    }


def interactive_wait(record: dict, index: int, total: int):
    def wait(kind: str, folder: Path) -> None:
        task = record["current"]
        if kind == "start":
            print(f"\n=== Task {index} of {total}, {ARM_NAME[record['arm']]} ===\n")
            print(TASKS[task]["sentence"], "\n")
            print(f"Work folder: {folder}")
            if record["arm"] == "alone":
                print("You may open nothing from the repository. Write your code in a .py file at the root of that folder.")
            else:
                print("Read these files first, in this order, in full (their copies are in the work folder):")
                for name in METHOD_FILES:
                    src = "fixtures/common/" + name if name != "brief.md" else f"fixtures/{task}/brief.md"
                    print(f"  {name}    (in the repository: experiments/method-comparison/{src})")
                print("Then do what brief.md says and run its checks. Your code goes where the brief says.")
            print(f"\nThe clock includes reading. The cap is {CAP_SECONDS // 60} minutes.")
            input("Press Enter to start the clock. ")
        else:
            input("Press Enter when you stop (done, stuck or at the cap). ")
    return wait


def table(record: dict) -> str:
    rows = ["| Task | Hidden | Without the name | Visible | Seconds | Over the cap |", "|---|---|---|---|---|---|"]
    for task, t in record["tasks"].items():
        v = t["verdict"]
        vis = ("yes" if v["visible"] else "no") if record["arm"] == "method" else "not given"
        rows.append(f"| {task} | {'pass' if v['hidden'] else 'fail'} | {'pass' if v['hidden_namefree'] else 'fail'} | {vis} | "
                    f"{t['seconds']} | {'yes' if t['over_cap'] else 'no'} |")
    return "\n".join(rows)


def run_arm(participant: str, arm: str, order: dict, pilot: bool, work_root: Path, wait_factory=interactive_wait,
            runs: Path = RUNS) -> dict:
    path = runs / f"{participant}-{arm}.json"
    record = read_json(path) or {
        "schema": 1, "participant": participant, "arm": arm, "pilot": pilot, "order": order,
        "protocol": "experiments/method-comparison/person-arms/protocol.md", "repository_commit": repository_commit(),
        "python": sys.version.split()[0], "cap_seconds": CAP_SECONDS, "started": now(),
        "task_order": task_order(participant, arm), "tasks": {}, "complete": False,
    }
    first = order["first"]
    if arm != first:
        other = read_json(runs / f"{participant}-{first}.json")
        if other and other.get("ended"):
            record.setdefault("seconds_since_first_arm",
                              round((datetime.datetime.fromisoformat(now()) - datetime.datetime.fromisoformat(other["ended"])).total_seconds()))
    todo = [t for t in record["task_order"] if t not in record["tasks"]]
    total = len(record["task_order"])
    for task in todo:
        record["current"] = task
        index = total - len(todo) + todo.index(task) + 1
        run_task(record, task, work_root / f"{participant}-{arm}" / task, wait_factory(record, index, total))
        record.pop("current", None)
        write_json(path, record)  # saved after every task
    record["complete"] = True
    record["ended"] = now()
    write_json(path, record)
    return record


def load_order(participant: str, runs: Path = RUNS) -> dict:
    path = runs / f"{participant}-order.json"
    order = read_json(path)
    if order is None:
        heads = secrets.randbelow(2) == 0  # heads: alone first; the coin is recorded, not chosen
        order = {"coin": "heads" if heads else "tails", "first": "alone" if heads else "method", "flipped": now()}
        write_json(path, order)
        print(f"Order coin: {order['coin']}. First arm: {ARM_NAME[order['first']]}.")
    return order


def next_arm(participant: str, order: dict, runs: Path = RUNS) -> str | None:
    sequence = [order["first"]] + [a for a in ARMS if a != order["first"]]
    for arm in sequence:
        rec = read_json(runs / f"{participant}-{arm}.json")
        if not rec or not rec.get("complete"):
            return arm
    return None


# ---- the paired test: exact two-sided Wilcoxon signed-rank, standard library only ----

def wilcoxon_p(diffs: list[int]) -> float:
    d = [x for x in diffs if x != 0]
    n = len(d)
    if n == 0:
        return 1.0
    mags = sorted(abs(x) for x in d)
    doubled = {}
    i = 0
    while i < n:  # average rank of a run of ties, doubled so that it is an integer
        j = i
        while j + 1 < n and mags[j + 1] == mags[i]:
            j += 1
        doubled[mags[i]] = (i + 1) + (j + 1)
        i = j + 1
    ranks = [doubled[abs(x)] for x in d]
    total, w_plus = sum(ranks), sum(doubled[abs(x)] for x in d if x > 0)
    counts = {0: 1}
    for r in ranks:
        nxt = dict(counts)
        for s, c in counts.items():
            nxt[s + r] = nxt.get(s + r, 0) + c
        counts = nxt
    low = min(w_plus, total - w_plus)
    return min(1.0, 2 * sum(c for s, c in counts.items() if s <= low) / 2 ** n)


def summary(runs: Path = RUNS) -> str:
    people: dict[str, dict] = {}
    for f in sorted(runs.glob("*-*.json")):
        rec = read_json(f)
        if rec and rec.get("complete") and rec.get("arm") in ARMS:
            people.setdefault(rec["participant"], {})[rec["arm"]] = rec
    lines = ["| Participant | Pilot | Alone (hidden of 3) | Method (hidden of 3) | Difference | Median seconds alone | Median seconds method |",
             "|---|---|---|---|---|---|---|"]
    diffs = []
    for pid, arms in people.items():
        if set(arms) != set(ARMS):
            lines.append(f"| {pid} | {'yes' if next(iter(arms.values()))['pilot'] else 'no'} | one arm only | | | | |")
            continue
        a, m = passes(arms["alone"]), passes(arms["method"])
        med = lambda r: sorted(t["seconds"] for t in r["tasks"].values())[len(r["tasks"]) // 2]
        pilot = arms["alone"]["pilot"] or arms["method"]["pilot"]
        lines.append(f"| {pid} | {'yes' if pilot else 'no'} | {a} | {m} | {m - a:+d} | {med(arms['alone'])} | {med(arms['method'])} |")
        if not pilot:
            diffs.append(m - a)
    lines.append("")
    lines.append(f"Complete pairs, pilot excluded: {len(diffs)} (planned: 14, with two spare; protocol.md).")
    if diffs:
        lines.append(f"Mean difference in hidden passes of 3: {sum(diffs) / len(diffs):+.2f}. "
                     f"Exact two-sided Wilcoxon signed-rank p = {wilcoxon_p(diffs):.4f} (zeros dropped).")
    return "\n".join(lines)


# ---- self-test ----

def self_test() -> int:
    """Score the reference answers (all must pass), a wrong answer (must fail), a full scripted arm, and the paired test."""
    failures = []

    def check(ok: bool, what: str) -> None:
        print(("ok    " if ok else "FAIL  ") + what)
        if not ok:
            failures.append(what)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for task, spec in TASKS.items():
            good = tmp / f"good-{task}"
            good.mkdir()
            shutil.copy(PARENT / "reference" / f"{task}.py", good / f"{task}.py")
            v = score_folder(good, task)
            check(v["hidden"] and v["hidden_namefree"], f"reference answer for {task} passes the hidden tests")
            bad = tmp / f"bad-{task}"
            bad.mkdir()
            (bad / f"{task}.py").write_text(f"def {spec['function']}(markdown):\n    return []\n")
            check(not score_folder(bad, task)["hidden"], f"a wrong answer for {task} fails")

        runs = tmp / "runs"

        def scripted(record, index, total):
            def wait(kind, folder):
                if kind == "finish":
                    ref = PARENT / "reference" / f"{record['current']}.py"
                    shutil.copy(ref, folder / ref.name)
            return wait

        rec = run_arm("T01", "method", {"coin": "heads", "first": "method", "flipped": now()}, True, tmp / "work",
                      wait_factory=scripted, runs=runs)
        check(rec["complete"] and passes(rec) == 3, "a scripted arm is saved whole and scores 3 of 3")
        saved = read_json(runs / "T01-method.json")
        check(saved is not None and set(saved["tasks"]) == set(TASKS) and "files" in saved["tasks"]["scope"], "the record holds every task with its files")
        check(all(t["verdict"]["visible"] for t in saved["tasks"].values()), "the brief's visible checks run in the method arm")
        rec2 = run_arm("T01", "alone", {"coin": "heads", "first": "method", "flipped": now()}, True, tmp / "work",
                       wait_factory=scripted, runs=runs)
        check(passes(rec2) == 3 and "seconds_since_first_arm" in rec2, "the second arm records the gap after the first")
        check("T01" in summary(runs), "the summary lists the participant")

    check(abs(wilcoxon_p([1, 2, 3, 4, 5]) - 2 / 32) < 1e-12, "Wilcoxon: five positive differences give p = 0.0625")
    check(wilcoxon_p([0, 0]) == 1.0, "Wilcoxon: no difference gives p = 1")
    check(ID_PATTERN.match("P01") is not None and ID_PATTERN.match("Jean Dupont") is None, "an id with a space is refused")
    print("self-test:", "FAILED" if failures else "passed")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("participant", nargs="?", help="anonymous id, such as P01")
    ap.add_argument("--pilot", action="store_true", help="record that this participant is a pilot")
    ap.add_argument("--summary", action="store_true", help="print the table of complete runs and the paired test")
    ap.add_argument("--self-test", action="store_true", help="score a known answer set and exit 0 when it works")
    ap.add_argument("--work", default=str(Path(tempfile.gettempdir()) / "method-comparison-person"),
                    help="scratch folder for the work (default: in the system temporary folder)")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.summary:
        print(summary())
        return 0
    if not args.participant or not ID_PATTERN.match(args.participant):
        ap.error("give an anonymous id of letters and digits, at most 12, such as P01; never a name")
    (RUNS).mkdir(exist_ok=True)
    order = load_order(args.participant)
    arm = next_arm(args.participant, order)
    if arm is None:
        print("Both arms are complete.")
        print(summary())
        return 0
    print(f"Next arm for {args.participant}: {ARM_NAME[arm]}. Three tasks, in an order fixed by the id and the arm.")
    record = run_arm(args.participant, arm, order, args.pilot, Path(args.work))
    print("\n" + table(record))
    print(f"\nHidden passes: {passes(record)} of {len(record['tasks'])}. Saved: runs/{args.participant}-{arm}.json")
    nxt = next_arm(args.participant, order)
    print("Next: run the same command again for the other arm." if nxt else "Both arms are complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
