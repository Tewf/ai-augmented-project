"""Tests of checks/local/: each rule fails where it should and stays silent where it should not.

Run: python3 -m unittest discover -s checks
The standard's checks/ folder must be importable: set READER_ERGONOMICS_CHECKS to it, or check
reader-ergonomics out beside this repository (as CI does, under the name standard), or extract it
into checks/out/standard as AGENTS.md says.
"""
import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
REPOSITORY = HERE.parents[1]
CANDIDATES = [os.environ.get("READER_ERGONOMICS_CHECKS", ""), REPOSITORY.parent / "standard" / "checks",
              REPOSITORY / "checks" / "out" / "standard" / "checks", REPOSITORY.parent / "reader-ergonomics" / "checks"]
sys.path.insert(0, str(next(Path(c) for c in CANDIDATES if c and (Path(c) / "framework").is_dir())))


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"local_{name}", REPOSITORY / "checks" / "local" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


brief_checks, start_file = load("brief_checks"), load("start_file")
precedence, stale = load("start_file_precedence"), load("start_file_stale")
memory_index, memory_source = load("memory_index"), load("memory_source")

BRIEF = """# Brief: a task

## Task

Do the work.

## Decided

- The file is named x.

## To find

- A module and its tests.

## Checks

- `python3 -m unittest`: passes with no failure.
"""
START = """# Start

## Commands

- `python3 -m unittest discover -s checks`

## Conventions

- Prose has no em dash.

## Precedence

When a text disagrees with the code, follow the code and say so.

## Pointers

- A new check: read `checks/local/x.py`.
"""
INDEX = """# Memory

- [One](one.md): the first fact, in a sentence.
- [Two](two.md): the second fact, in a sentence.
"""
MEMORY = """# One

**Date:** 2026-11-03
**Type:** fact
**Source:** README.md

The fact.
"""


class Base(unittest.TestCase):
    """A temporary repository and a runner; no tests of its own."""
    module = None

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def write(self, path: str, text: str) -> None:
        (self.root / path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / path).write_text(text, encoding="utf-8")

    def run_check(self, config: dict | None = None) -> list[str]:
        return [finding.message for finding in self.module.check(self.root, config or {})]


class BriefTests(Base):
    module = brief_checks

    def test_a_complete_brief_passes(self):
        self.write("task/brief.md", BRIEF)
        self.assertEqual(self.run_check(), [])

    def test_an_empty_checks_part_is_refused(self):
        self.write("brief.md", BRIEF.split("- `python3")[0])
        self.assertTrue(any("no check is refused" in m for m in self.run_check()))

    def test_a_missing_part_is_found(self):
        self.write("brief.md", BRIEF.replace("## Decided", "## Notes"))
        messages = self.run_check()
        self.assertTrue(any("missing part 'Decided'" in m for m in messages))
        self.assertTrue(any("unexpected part 'Notes'" in m for m in messages))

    def test_parts_out_of_order_are_found(self):
        self.write("brief.md", BRIEF.replace("## To find", "## Checks2").replace("## Checks\n", "## To find\n").replace("## Checks2", "## Checks"))
        self.assertTrue(any("in the order" in m for m in self.run_check()))

    def test_a_check_without_a_command_is_found(self):
        self.write("brief.md", BRIEF.replace("`python3 -m unittest`: passes with no failure.", "It should work well."))
        self.assertTrue(any("command in backticks" in m for m in self.run_check()))

    def test_a_command_without_a_pass_condition_is_found(self):
        self.write("brief.md", BRIEF.replace(": passes with no failure.", ""))
        self.assertTrue(any("what passing means" in m for m in self.run_check()))

    def test_a_heading_in_a_code_block_is_not_a_part(self):
        self.write("brief.md", BRIEF + "\n```\n## Extra\n```\n")
        self.assertEqual(self.run_check(), [])

    def test_a_deeper_heading_is_content(self):
        self.write("brief.md", BRIEF.replace("Do the work.", "### Detail\n\nDo the work."))
        self.assertEqual(self.run_check(), [])


class StartFileTests(Base):
    module = start_file

    def test_a_complete_start_file_passes(self):
        self.write("START.md", START)
        self.assertEqual(self.run_check(), [])

    def test_one_line_over_the_bound_fails_and_at_the_bound_passes(self):
        self.write("START.md", START)
        size = len(START.splitlines())
        self.assertEqual(self.run_check({"start_file": {"max_lines": size}}), [])
        self.assertTrue(any("past the bound" in m for m in self.run_check({"start_file": {"max_lines": size - 1}})))

    def test_a_part_out_of_order_is_found(self):
        self.write("START.md", START.replace("## Commands", "## Zed").replace("## Pointers", "## Commands").replace("## Zed", "## Pointers"))
        self.assertTrue(any("in the order" in m for m in self.run_check()))

    def test_an_overview_part_is_unexpected(self):
        self.write("START.md", START + "\n## Overview\n\nA tour.\n")
        self.assertTrue(any("unexpected part 'Overview'" in m for m in self.run_check()))

    def test_a_command_without_backticks_is_found(self):
        self.write("START.md", START.replace("- `python3 -m unittest discover -s checks`", "- run the tests"))
        self.assertTrue(any("backticks" in m for m in self.run_check()))

    def test_an_empty_part_is_found(self):
        self.write("START.md", START.replace("- Prose has no em dash.\n", ""))
        self.assertTrue(any("'Conventions' is empty" in m for m in self.run_check()))

    def test_a_pointer_must_be_a_list_item(self):
        self.write("START.md", START.replace("- A new check", "A new check"))
        self.assertTrue(any("list item" in m for m in self.run_check()))


class PrecedenceTests(Base):
    module = precedence

    def test_the_sentence_once_in_its_part_passes(self):
        self.write("START.md", START)
        self.assertEqual(self.run_check(), [])

    def test_a_missing_sentence_is_found(self):
        self.write("START.md", START.replace("follow the code", "do as you like"))
        self.assertTrue(any("no sentence" in m for m in self.run_check()))

    def test_the_sentence_elsewhere_is_found(self):
        self.write("START.md", START.replace("- Prose has no em dash.", "- Always follow the code."))
        self.assertTrue(any("said once" in m for m in self.run_check()))

    def test_the_sentence_twice_in_its_part_is_found(self):
        self.write("START.md", START.replace("and say so.", "and say so.\nFollow the code always."))
        self.assertTrue(any("said once" in m for m in self.run_check()))

    def test_the_phrase_is_configurable(self):
        self.write("START.md", START.replace("follow the code", "the code wins"))
        self.assertEqual(self.run_check({"start_file": {"precedence": "the code wins"}}), [])


class StaleTests(Base):
    module = stale

    def test_existing_paths_pass(self):
        self.write("START.md", START)
        self.write("checks/local/x.py", "")
        self.write("checks/hello.py", "")
        self.assertEqual(self.run_check(), [])

    def test_a_missing_path_in_pointers_is_stale(self):
        self.write("START.md", START)
        self.assertTrue(any("'checks/local/x.py' does not exist" in m for m in self.run_check()))

    def test_a_missing_path_in_a_command_is_stale(self):
        self.write("START.md", START.replace("discover -s checks", "tools/run.sh"))
        self.write("checks/local/x.py", "")
        self.assertTrue(any("'tools/run.sh' does not exist" in m for m in self.run_check()))

    def test_an_exempt_folder_is_skipped(self):
        self.write("START.md", START.replace("discover -s checks", "checks/out/standard/run.py"))
        self.write("checks/local/x.py", "")
        self.assertEqual(self.run_check({"start_file": {"exempt": ["checks/out/"]}}), [])

    def test_flags_and_urls_are_not_paths(self):
        self.write("START.md", START.replace("discover -s checks", "run --out=a/b https://x.org/y.md ~/z.md"))
        self.write("checks/local/x.py", "")
        self.assertEqual(self.run_check(), [])

    def test_a_path_in_conventions_is_not_looked_up(self):
        self.write("START.md", START.replace("- Prose has no em dash.", "- Never edit `gone/file.md`."))
        self.write("checks/local/x.py", "")
        self.assertEqual(self.run_check(), [])


class MemoryIndexTests(Base):
    module = memory_index

    def setUp(self) -> None:
        super().setUp()
        self.write("memory/one.md", MEMORY)
        self.write("memory/two.md", MEMORY.replace("# One", "# Two"))

    def test_a_complete_index_passes(self):
        self.write("memory/INDEX.md", INDEX)
        self.assertEqual(self.run_check(), [])

    def test_a_shape_line_is_allowed_and_not_counted(self):
        self.write("memory/INDEX.md", INDEX.replace("# Memory\n", "# Memory\n\n**Shape:** [x](x.md)\n"))
        self.assertEqual(self.run_check({"memory": {"max_lines": 7}}), [])

    def test_a_line_in_the_wrong_form_is_found(self):
        self.write("memory/INDEX.md", INDEX + "A note.\n")
        self.assertTrue(any("one sentence'" in m for m in self.run_check()))

    def test_a_broken_link_is_found(self):
        self.write("memory/INDEX.md", INDEX + "- [Three](three.md): a third fact.\n")
        self.assertTrue(any("'three.md' does not exist" in m for m in self.run_check()))

    def test_a_file_left_out_is_found(self):
        self.write("memory/INDEX.md", INDEX.splitlines()[0] + "\n\n- [One](one.md): the first fact.\n")
        self.assertTrue(any("'two.md' is in the folder and not listed" in m for m in self.run_check()))

    def test_a_file_listed_twice_is_found(self):
        self.write("memory/INDEX.md", INDEX + "- [One again](one.md): the same fact.\n")
        self.assertTrue(any("already listed" in m for m in self.run_check()))

    def test_a_hook_of_two_sentences_is_found(self):
        self.write("memory/INDEX.md", INDEX.replace("the first fact, in a sentence.", "The first fact. And a second."))
        self.assertTrue(any("the hook is one sentence" in m for m in self.run_check()))

    def test_one_line_over_the_bound_fails_and_at_the_bound_passes(self):
        self.write("memory/INDEX.md", INDEX)
        size = len(INDEX.splitlines())
        self.assertEqual(self.run_check({"memory": {"max_lines": size}}), [])
        self.assertTrue(any("past the bound" in m for m in self.run_check({"memory": {"max_lines": size - 1}})))


class MemorySourceTests(Base):
    module = memory_source

    def setUp(self) -> None:
        super().setUp()
        self.write("README.md", "# Root\n")
        self.write("memory/INDEX.md", "- [One](one.md): the first fact.\n")

    def test_a_complete_file_passes(self):
        self.write("memory/one.md", MEMORY)
        self.assertEqual(self.run_check(), [])

    def test_a_missing_source_is_found(self):
        self.write("memory/one.md", MEMORY.replace("**Source:** README.md\n", ""))
        self.assertTrue(any("**Source:**" in m for m in self.run_check()))

    def test_a_missing_date_and_a_bad_type_are_found(self):
        self.write("memory/one.md", MEMORY.replace("2026-11-03", "yesterday").replace("fact", "hunch"))
        messages = self.run_check()
        self.assertTrue(any("**Date:**" in m for m in messages))
        self.assertTrue(any("**Type:**" in m for m in messages))

    def test_a_source_path_that_does_not_exist_is_stale(self):
        self.write("memory/one.md", MEMORY.replace("README.md", "gone/file.md"))
        self.assertTrue(any("stale: the source 'gone/file.md'" in m for m in self.run_check()))

    def test_a_line_number_after_the_path_is_ignored(self):
        self.write("memory/one.md", MEMORY.replace("README.md", "README.md:3"))
        self.assertEqual(self.run_check(), [])

    def test_a_command_or_identifier_is_accepted(self):
        self.write("memory/one.md", MEMORY.replace("README.md", "`git log -1`"))
        self.assertEqual(self.run_check(), [])
        self.write("memory/one.md", MEMORY.replace("README.md", "arXiv 2610.30571"))
        self.assertEqual(self.run_check(), [])

    def test_a_url_is_not_looked_up(self):
        self.write("memory/one.md", MEMORY.replace("README.md", "https://example.org/a.md"))
        self.assertEqual(self.run_check(), [])

    def test_a_rule_needs_a_status(self):
        self.write("memory/one.md", MEMORY.replace("fact", "rule"))
        self.assertTrue(any("Status" in m for m in self.run_check()))
        self.write("memory/one.md", MEMORY.replace("The fact.", "**Status:** proposal").replace("fact", "rule"))
        self.assertEqual(self.run_check(), [])

    def test_a_file_the_index_does_not_list_is_not_read(self):
        self.write("memory/one.md", MEMORY)
        self.write("memory/stray.md", "no fields")
        self.assertEqual(self.run_check(), [])


if __name__ == "__main__":
    unittest.main()
