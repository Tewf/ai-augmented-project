"""The checks of the brief: the cases it names, run against llms.py. Run with: python3 -m unittest discover -s checks"""
import importlib.util
import os
import unittest

spec = importlib.util.spec_from_file_location("candidate", os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "llms.py"))
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)

llms_links = candidate.llms_links

TEXT = """# Project

> A summary line.

## Docs

- [Standard](https://example.org/standard.md): the principles
- [Shapes](https://example.org/shapes.md): one file per genre
- [Bare](https://example.org/bare.md)

## Optional

- [Notes](https://example.org/notes.md): a note: with a colon
"""


class Llms(unittest.TestCase):
    def test_lists_links_in_order(self):
        self.assertEqual(llms_links(TEXT), [
            ("Standard", "https://example.org/standard.md", "the principles"),
            ("Shapes", "https://example.org/shapes.md", "one file per genre"),
            ("Bare", "https://example.org/bare.md", ""),
            ("Notes", "https://example.org/notes.md", "a note: with a colon"),
        ])

    def test_no_links(self):
        self.assertEqual(llms_links("# Project\n\nJust prose.\n"), [])

    def test_empty_text(self):
        self.assertEqual(llms_links(""), [])

    def test_no_description(self):
        self.assertEqual(llms_links("- [A](u)\n"), [("A", "u", "")])

    def test_other_bullets_ignored(self):
        self.assertEqual(llms_links("* [A](u): d\n  - [B](v): e\n- [C](w): f\n"), [("C", "w", "f")])

    def test_fenced_block_ignored(self):
        self.assertEqual(llms_links("```\n- [A](u): d\n```\n- [B](v): e\n"), [("B", "v", "e")])

    def test_colons_in_description(self):
        self.assertEqual(llms_links("- [A](u): one: two: three\n"), [("A", "u", "one: two: three")])

    def test_no_url_ignored(self):
        self.assertEqual(llms_links("- [text] no url\n- [A](u)\n"), [("A", "u", "")])

    def test_crlf_and_no_final_newline(self):
        self.assertEqual(llms_links("- [A](u): d\r\n- [B](v): e"), [("A", "u", "d"), ("B", "v", "e")])

    def test_returns_tuples_of_str(self):
        out = llms_links(TEXT)
        self.assertIsInstance(out, list)
        self.assertTrue(all(isinstance(x, tuple) and len(x) == 3 and all(isinstance(y, str) for y in x) for x in out))


if __name__ == "__main__":
    unittest.main()
