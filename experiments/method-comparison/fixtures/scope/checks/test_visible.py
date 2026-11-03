"""The checks of the brief: the cases it names, run against scope.py. Run with: python3 -m unittest discover -s checks"""
import importlib.util
import os
import unittest

spec = importlib.util.spec_from_file_location("candidate", os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "scope.py"))
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)
scope_in_rows = candidate.scope_in_rows

SCOPE = """# Page

Some prose with a | pipe in it.

## Scope

| | What | Why |
|---|---|---|
| in | delegation | the rule needs a measure |
| in | coordination | six sessions, one day |
| out | the one-agent case | a neighbour holds it |
| in | incentives | economics has the models |
"""


class ScopeInRows(unittest.TestCase):
    def test_lists_in_rows_in_order(self):
        self.assertEqual(scope_in_rows(SCOPE), ["delegation", "coordination", "incentives"])

    def test_no_table(self):
        self.assertEqual(scope_in_rows("# Title\n\nNo table here.\n"), [])

    def test_empty_text(self):
        self.assertEqual(scope_in_rows(""), [])

    def test_only_out_rows(self):
        text = "| | What | Why |\n|---|---|---|\n| out | a | b |\n"
        self.assertEqual(scope_in_rows(text), [])

    def test_whitespace_around_cells(self):
        text = "|   | What | Why |\n|--|--|--|\n|in|tight|x|\n|  in  |  padded  |  y  |\n"
        self.assertEqual(scope_in_rows(text), ["tight", "padded"])

    def test_exact_match_only(self):
        text = "| | What | Why |\n|---|---|---|\n| In | upper | x |\n| inside | no | x |\n| index | no | x |\n| in | yes | x |\n"
        self.assertEqual(scope_in_rows(text), ["yes"])

    def test_other_tables_ignored(self):
        text = (
            "| Name | Value |\n|---|---|\n| in | trap |\n\n"
            "| | What | Why |\n|---|---|---|\n| in | real | x |\n"
        )
        self.assertEqual(scope_in_rows(text), ["real"])

    def test_markup_kept_verbatim(self):
        text = "| | What | Why |\n|---|---|---|\n| in | **bold** and [a link](http://x.y/z) | x |\n"
        self.assertEqual(scope_in_rows(text), ["**bold** and [a link](http://x.y/z)"])

    def test_alignment_separator_not_returned(self):
        text = "| | What | Why |\n|:--|:-:|--:|\n| in | a | b |\n"
        self.assertEqual(scope_in_rows(text), ["a"])

    def test_empty_what_cell_kept_as_empty_string(self):
        text = "| | What | Why |\n|---|---|---|\n| in |  | x |\n| in | b | y |\n"
        self.assertEqual(scope_in_rows(text), ["", "b"])

    def test_crlf_lines(self):
        text = "| | What | Why |\r\n|---|---|---|\r\n| in | a | b |\r\n| out | c | d |\r\n"
        self.assertEqual(scope_in_rows(text), ["a"])

    def test_no_trailing_newline(self):
        text = "| | What | Why |\n|---|---|---|\n| in | last | z |"
        self.assertEqual(scope_in_rows(text), ["last"])

    def test_returns_list_of_str(self):
        out = scope_in_rows(SCOPE)
        self.assertIsInstance(out, list)
        self.assertTrue(all(isinstance(x, str) for x in out))


if __name__ == "__main__":
    unittest.main()
