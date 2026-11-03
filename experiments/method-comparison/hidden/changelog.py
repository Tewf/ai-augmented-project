"""Hidden tests of the changelog task: the judge. No arm is shown these cases; each follows from the Decided lines."""
import importlib.util
import os
import unittest

spec = importlib.util.spec_from_file_location("candidate", os.environ["CANDIDATE"])
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)

changelog_releases = candidate.changelog_releases


class ChangelogHidden(unittest.TestCase):
    def test_text_after_the_date(self):
        self.assertEqual(changelog_releases("## [1.0.0] - 2026-01-01 [YANKED]\n"), [("1.0.0", "2026-01-01")])

    def test_malformed_date_skipped(self):
        text = "## [1.0.0] - 2026-1-5\n## [1.0.1] - 26-01-05\n## [1.0.2] - 2026-01-05\n"
        self.assertEqual(changelog_releases(text), [("1.0.2", "2026-01-05")])

    def test_fence_closes(self):
        text = "```\n## [9.9.9] - 2026-01-01\n```\n## [1.0.0] - 2026-01-02\n```\n## [8.8.8] - 2026-01-03\n```\n## [0.9.0] - 2026-01-04\n"
        self.assertEqual(changelog_releases(text), [("1.0.0", "2026-01-02"), ("0.9.0", "2026-01-04")])

    def test_link_reference_lines_ignored(self):
        text = "## [1.0.0] - 2026-01-01\n\n[1.0.0]: https://example.org/compare/0.9.0...1.0.0\n[Unreleased]: https://example.org\n"
        self.assertEqual(changelog_releases(text), [("1.0.0", "2026-01-01")])

    def test_same_version_twice_kept(self):
        text = "## [1.0.0] - 2026-01-01\n## [1.0.0] - 2026-01-02\n"
        self.assertEqual(changelog_releases(text), [("1.0.0", "2026-01-01"), ("1.0.0", "2026-01-02")])

    def test_version_kept_as_written(self):
        self.assertEqual(changelog_releases("## [v2.0.0+build.5] - 2026-02-02\n"), [("v2.0.0+build.5", "2026-02-02")])

    def test_heading_must_start_the_line(self):
        text = "see ## [1.0.0] - 2026-01-01 above\n## [1.0.1] - 2026-01-02\n"
        self.assertEqual(changelog_releases(text), [("1.0.1", "2026-01-02")])

    def test_unreleased_with_a_date_is_still_skipped(self):
        self.assertEqual(changelog_releases("## [Unreleased] - 2026-01-01\n## [1.0.0] - 2026-01-02\n"), [("1.0.0", "2026-01-02")])


if __name__ == "__main__":
    unittest.main()
