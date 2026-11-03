"""Judge: runs the hidden tests of a task against what a session left in its project folder.

A program decides, never the model. Three verdicts per session, all from the same folder:
- hidden: the module-level function the task names exists in some Python file of the project root and passes every
  hidden test. The folder is copied first, so the judge never changes the session's files.
- hidden_namefree: as above, but when no file defines that name, the one public function of the project's Python
  files (test files and the checks folder left out) is passed under the name. It exists because the bare sentence
  gives no name: the arm that is not told the name cannot be blamed for it. It is reported beside, never instead.
- visible: the same candidate against the checks of the brief (checks/test_visible.py of the task's fixture).

A candidate that does not import, or that runs past 20 seconds, fails. Time O(size of the code + the tests).
"""
from __future__ import annotations

import ast
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMEOUT = 20

WRAPPER = '''import importlib.util, sys
sys.path.insert(0, {root!r})
spec = importlib.util.spec_from_file_location("target", {target!r})
mod = importlib.util.module_from_spec(spec)
sys.modules["target"] = mod
spec.loader.exec_module(mod)
{name} = getattr(mod, {found!r})
'''


def source_files(root: Path) -> list[Path]:
    """Python files at the project root that are not tests."""
    return sorted(p for p in root.glob("*.py") if not p.name.startswith(("test_", "_judge")))


def top_level_functions(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return []
    return [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]


def locate(root: Path, name: str) -> tuple[Path | None, str | None, str]:
    """(file, function, how): how is 'named', 'namefree' or 'none'."""
    files = source_files(root)
    for p in files:
        if name in top_level_functions(p):
            return p, name, "named"
    public = [(p, f) for p in files for f in top_level_functions(p) if not f.startswith("_")]
    if len(public) == 1:
        return public[0][0], public[0][1], "namefree"
    return None, None, "none"


def run_tests(test_file: Path, candidate: Path, cwd: Path) -> tuple[bool, str]:
    env = dict(os.environ, CANDIDATE=str(candidate))
    try:
        p = subprocess.run([sys.executable, "-I", str(test_file)], env=env, cwd=cwd, capture_output=True, text=True,
                           timeout=TIMEOUT, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if p.returncode == 0:
        return True, "ok"
    last = [ln for ln in (p.stderr or p.stdout).strip().splitlines() if ln.strip()]
    return False, (last[-1] if last else f"exit {p.returncode}")[:200]


def judge(project: Path, task: str, function: str) -> dict:
    """Verdicts for one session folder. Never raises on a bad candidate."""
    out = {"hidden": False, "hidden_namefree": False, "visible": False, "how": "none", "detail": ""}
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "p"
        shutil.copytree(project, work, ignore=shutil.ignore_patterns("__pycache__", ".git", ".kilo", ".opencode"))
        target, found, how = locate(work, function)
        out["how"] = how
        if target is None:
            out["detail"] = "no function"
            return out
        wrapper = Path(tmp) / "_judge_candidate.py"
        wrapper.write_text(WRAPPER.format(root=str(work), target=str(target), name=function, found=found))
        ok, detail = run_tests(HERE / "hidden" / f"{task}.py", wrapper, work)
        out["detail"] = detail
        if how == "named":
            out["hidden"] = out["hidden_namefree"] = ok
        else:
            out["hidden_namefree"] = ok
        visible = work / "checks" / "test_visible.py"
        if visible.exists() and how == "named":
            out["visible"] = run_tests(visible, wrapper, work)[0]
    return out
