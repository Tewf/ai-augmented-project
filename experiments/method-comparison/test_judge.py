"""Tests of the judge: a reference passes, and empty, wrong, misnamed and hanging code fail as they should."""
import tempfile
import unittest
from pathlib import Path

import judge
from tasks import TASKS

HERE = Path(__file__).resolve().parent


def project(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp())
    for name, body in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(body)
    return root


class JudgeTest(unittest.TestCase):
    def test_reference_passes_hidden(self):
        for task, spec in TASKS.items():
            src = (HERE / "reference" / f"{task}.py").read_text()
            v = judge.judge(project({f"{task}.py": src}), task, spec["function"])
            self.assertTrue(v["hidden"], (task, v))
            self.assertEqual(v["how"], "named")

    def test_reference_passes_visible(self):
        for task, spec in TASKS.items():
            src = (HERE / "reference" / f"{task}.py").read_text()
            vis = (HERE / "fixtures" / task / "checks" / "test_visible.py").read_text()
            v = judge.judge(project({f"{task}.py": src, "checks/test_visible.py": vis}), task, spec["function"])
            self.assertTrue(v["visible"], (task, v))

    def test_empty_folder_fails(self):
        v = judge.judge(project({"notes.txt": "x"}), "scope", "scope_in_rows")
        self.assertFalse(v["hidden"] or v["hidden_namefree"])
        self.assertEqual(v["how"], "none")

    def test_wrong_code_fails(self):
        v = judge.judge(project({"scope.py": "def scope_in_rows(markdown):\n    return []\n"}), "scope", "scope_in_rows")
        self.assertFalse(v["hidden"])

    def test_syntax_error_fails(self):
        v = judge.judge(project({"scope.py": "def scope_in_rows(:\n"}), "scope", "scope_in_rows")
        self.assertFalse(v["hidden"])

    def test_misnamed_passes_only_namefree(self):
        src = (HERE / "reference" / "scope.py").read_text().replace("scope_in_rows", "parse_scope")
        src = "\n".join(l for l in src.splitlines())  # helper _cells is private, so one public function remains
        v = judge.judge(project({"table.py": src}), "scope", "scope_in_rows")
        self.assertFalse(v["hidden"])
        self.assertTrue(v["hidden_namefree"], v)
        self.assertEqual(v["how"], "namefree")

    def test_two_public_functions_without_the_name_is_none(self):
        v = judge.judge(project({"a.py": "def f(x):\n    return []\n\ndef g(x):\n    return []\n"}), "scope", "scope_in_rows")
        self.assertEqual(v["how"], "none")

    def test_hang_fails(self):
        old = judge.TIMEOUT
        judge.TIMEOUT = 2
        try:
            v = judge.judge(project({"scope.py": "def scope_in_rows(m):\n    while True:\n        pass\n"}), "scope", "scope_in_rows")
        finally:
            judge.TIMEOUT = old
        self.assertFalse(v["hidden"])
        self.assertEqual(v["detail"], "timeout")

    def test_judge_does_not_change_the_folder(self):
        root = project({"scope.py": "def scope_in_rows(m):\n    return []\n"})
        before = sorted(p.name for p in root.rglob("*"))
        judge.judge(root, "scope", "scope_in_rows")
        self.assertEqual(before, sorted(p.name for p in root.rglob("*")))


if __name__ == "__main__":
    unittest.main()
