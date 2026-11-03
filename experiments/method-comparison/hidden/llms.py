"""Hidden tests of the llms.txt task: the judge. No arm is shown these cases; each follows from the Decided lines."""
import importlib.util
import os
import unittest

spec = importlib.util.spec_from_file_location("candidate", os.environ["CANDIDATE"])
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)

llms_links = candidate.llms_links


class LlmsHidden(unittest.TestCase):
    def test_description_stripped(self):
        self.assertEqual(llms_links("- [A](u):    spaced out   \n"), [("A", "u", "spaced out")])

    def test_empty_description_after_colon(self):
        self.assertEqual(llms_links("- [A](u):\n- [B](v): \n"), [("A", "u", ""), ("B", "v", "")])

    def test_text_without_colon_is_no_description(self):
        self.assertEqual(llms_links("- [A](u) not a description\n"), [("A", "u", "")])

    def test_title_must_be_followed_by_paren(self):
        self.assertEqual(llms_links("- [a [b]](u)\n- [c](w)\n"), [("c", "w", "")])

    def test_only_the_first_link_of_a_line(self):
        self.assertEqual(llms_links("- [A](u): see [B](v)\n"), [("A", "u", "see [B](v)")])

    def test_fence_closes(self):
        text = "```\n- [A](u)\n```\n- [B](v)\n```\n- [C](w)\n```\n- [D](x)\n"
        self.assertEqual(llms_links(text), [("B", "v", ""), ("D", "x", "")])

    def test_marker_needs_its_space(self):
        self.assertEqual(llms_links("-[A](u)\n- [B](v)\n"), [("B", "v", "")])

    def test_empty_title_and_unicode(self):
        self.assertEqual(llms_links("- [](u)\n- [Éléphant](https://é.example/x): à la carte\n"),
                         [("", "u", ""), ("Éléphant", "https://é.example/x", "à la carte")])


if __name__ == "__main__":
    unittest.main()
