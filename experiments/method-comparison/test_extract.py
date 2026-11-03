"""Tests of the extract and the report on a small database built here, in the shape of the agent's own."""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

import extract
import report


def database(parts: list[dict], assistants: int = 2) -> str:
    path = str(Path(tempfile.mkdtemp()) / "k.db")
    c = sqlite3.connect(path)
    c.execute("create table session (id text, parent_id text, cost real, tokens_input int, tokens_output int, tokens_reasoning int, "
              "tokens_cache_read int, tokens_cache_write int, time_created int)")
    c.execute("create table message (id text, session_id text, time_created int, data text)")
    c.execute("create table part (id text, message_id text, session_id text, time_created int, data text)")
    c.execute("insert into session values ('s', null, 0.5, 1, 2, 3, 4, 5, 0)")
    c.execute("insert into session values ('child', 's', 9, 9, 9, 9, 9, 9, 1)")
    c.execute("insert into message values ('u', 's', 0, ?)", (json.dumps({"role": "user"}),))
    for i in range(assistants):
        c.execute("insert into message values (?, 's', ?, ?)", (f"a{i}", i + 1, json.dumps({"role": "assistant"})))
    for n, p in enumerate(parts):
        c.execute("insert into part values (?, 'a0', 's', ?, ?)", (f"p{n}", n, json.dumps(p)))
    c.commit()
    return path


def tool(name: str, **inp) -> dict:
    return {"type": "tool", "tool": name, "state": {"input": inp}}


class ExtractTest(unittest.TestCase):
    def test_tokens_cost_turns_and_the_child_is_left_out(self):
        r = extract.counts(database([]))
        self.assertEqual((r["tokens_total"], r["cost"], r["turns"], r["session"]), (15, 0.5, 2, "s"))

    def test_start_md_first_and_files_before_first_edit(self):
        r = extract.counts(database([tool("read", filePath="/p/START.md"), tool("read", filePath="/p/brief.md"),
                                     tool("read", filePath="/p/brief.md"), tool("write", filePath="/p/a.py"),
                                     tool("read", filePath="/p/late.md")]))
        self.assertTrue(r["start_md_first"])
        self.assertEqual(r["files_before_first_edit"], 2)
        self.assertTrue(r["edited"])

    def test_another_file_first(self):
        r = extract.counts(database([tool("read", filePath="/p/brief.md"), tool("read", filePath="/p/START.md")]))
        self.assertFalse(r["start_md_first"])
        self.assertFalse(r["edited"])

    def test_shell_read_counts_as_a_file_read(self):
        r = extract.counts(database([tool("bash", command="cat START.md memory/INDEX.md"), tool("bash", command="python3 -m unittest")]))
        self.assertEqual(r["files_before_first_edit"], 2)

    def test_questions_are_question_tool_calls_and_lines_ending_in_a_mark(self):
        r = extract.counts(database([tool("question", question="which?"), {"type": "text", "text": "Done.\nShould I add more?\nNo."}]))
        self.assertEqual(r["questions"], 2)


class ReportTest(unittest.TestCase):
    def test_wilson_interval(self):
        lo, hi = report.wilson(0, 15)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.204, places=2)
        lo, hi = report.wilson(15, 15)
        self.assertAlmostEqual(lo, 0.796, places=2)
        self.assertEqual(hi, 1.0)
        self.assertEqual(report.wilson(0, 0), (0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
