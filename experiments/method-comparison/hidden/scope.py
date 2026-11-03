"""Hidden tests of the scope-table task: the judge. No arm is shown these cases; each follows from the Decided lines."""
import importlib.util
import os
import unittest

spec = importlib.util.spec_from_file_location("candidate", os.environ["CANDIDATE"])
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)

scope_in_rows = candidate.scope_in_rows

HEAD = "| | What | Why |\n|---|---|---|\n"


class ScopeHidden(unittest.TestCase):
    def test_what_must_be_the_second_cell(self):
        text = "| What | x | y |\n|---|---|---|\n| in | a | b |\n\n" + HEAD + "| in | real | z |\n"
        self.assertEqual(scope_in_rows(text), ["real"])

    def test_two_scope_tables(self):
        text = HEAD + "| in | a | x |\n\nProse.\n\n" + HEAD + "| in | b | x |\n| out | c | x |\n| in | d | x |\n"
        self.assertEqual(scope_in_rows(text), ["a", "b", "d"])

    def test_in_only_in_other_columns(self):
        text = HEAD + "| out | in | in |\n| in | a | in |\n"
        self.assertEqual(scope_in_rows(text), ["a"])

    def test_row_after_the_table_ended(self):
        text = HEAD + "| in | a | x |\n\n| in | stray | x |\n"
        self.assertEqual(scope_in_rows(text), ["a"])

    def test_padded_header(self):
        text = "|   |  What   |  Why  |\n|---|---|---|\n| in | a | x |\n"
        self.assertEqual(scope_in_rows(text), ["a"])

    def test_unicode_kept(self):
        text = HEAD + "| in | déléguer à l'agent — oui | x |\n"
        self.assertEqual(scope_in_rows(text), ["déléguer à l'agent — oui"])


if __name__ == "__main__":
    unittest.main()
