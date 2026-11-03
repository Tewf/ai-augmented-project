"""The checks of the brief: the cases it names, run against changelog.py. Run with: python3 -m unittest discover -s checks"""
import importlib.util
import os
import unittest

spec = importlib.util.spec_from_file_location("candidate", os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "changelog.py"))
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)

changelog_releases = candidate.changelog_releases

LOG = """# Changelog

## [Unreleased]

- work in progress

## [1.2.0] - 2026-10-29

### Added

- a thing

## [1.1.0] - 2026-09-01

## [1.0.0] - 2026-08-15
"""


class Changelog(unittest.TestCase):
    def test_lists_releases_in_order(self):
        self.assertEqual(changelog_releases(LOG), [("1.2.0", "2026-10-29"), ("1.1.0", "2026-09-01"), ("1.0.0", "2026-08-15")])

    def test_no_heading(self):
        self.assertEqual(changelog_releases("# Changelog\n\nNothing yet.\n"), [])

    def test_empty_text(self):
        self.assertEqual(changelog_releases(""), [])

    def test_unreleased_skipped(self):
        self.assertEqual(changelog_releases("## [Unreleased]\n"), [])

    def test_no_date_skipped(self):
        self.assertEqual(changelog_releases("## [1.0.0]\n\n## [0.9.0] - 2026-01-02\n"), [("0.9.0", "2026-01-02")])

    def test_other_levels_ignored(self):
        text = "# [1.0.0] - 2026-01-01\n### [1.0.1] - 2026-01-02\n## [1.0.2] - 2026-01-03\n"
        self.assertEqual(changelog_releases(text), [("1.0.2", "2026-01-03")])

    def test_fenced_block_ignored(self):
        text = "```\n## [9.9.9] - 2026-01-01\n```\n## [1.0.0] - 2026-01-02\n"
        self.assertEqual(changelog_releases(text), [("1.0.0", "2026-01-02")])

    def test_prerelease_whole(self):
        self.assertEqual(changelog_releases("## [1.0.0-rc.1] - 2026-01-01\n"), [("1.0.0-rc.1", "2026-01-01")])

    def test_crlf_and_no_final_newline(self):
        text = "## [1.0.0] - 2026-01-01\r\n\r\n## [0.9.0] - 2025-12-31"
        self.assertEqual(changelog_releases(text), [("1.0.0", "2026-01-01"), ("0.9.0", "2025-12-31")])

    def test_returns_tuples_of_str(self):
        out = changelog_releases(LOG)
        self.assertIsInstance(out, list)
        self.assertTrue(all(isinstance(x, tuple) and len(x) == 2 and all(isinstance(y, str) for y in x) for x in out))


if __name__ == "__main__":
    unittest.main()
