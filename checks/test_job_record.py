"""Tests of checks/local/job_record.py: each field is read from where the shape says, and nothing is guessed.

Run: python3 -m unittest discover -s checks
It reuses the temporary repository and the sample briefs of test_session.py.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_session as session  # noqa: E402

job_record = session.load("job_record")


CLOSED = """# Brief: a closed job

**Shape:** [brief](../brief.md)
**Depends on:** first, second
**Repo:** project
**Kind:** build
**Outcome:** pass

## Task

Do the work.
""" + session.COST.replace("182000 tokens", "182384 tokens")


class JobRecordTests(session.Base):
    module = job_record

    def jobs(self, **briefs: str) -> list[dict]:
        for folder, text in briefs.items():
            self.write(f"{folder}/brief.md", text)
        return job_record.export(self.root)

    def test_a_closed_brief_exports_every_field_it_states(self):
        job = self.jobs(**{"2026-11-04_closed": CLOSED})[0]
        self.assertEqual(job, {"id": "closed", "date": "2026-11-04", "kind": "build", "repo": "project",
                               "depends_on": ["first", "second"], "agents": 1, "tokens_k": 182.384,
                               "tokens_source": "recorded", "dollars": 1.4, "minutes": 25.0,
                               "produced": "one module and its tests", "outcome": "pass", "wave": 0})

    def test_pending_and_not_measured_are_left_out_not_guessed(self):
        text = session.BRIEF + session.COST.replace("182000 tokens", "pending").replace("25 minutes", "not measured")
        job = self.jobs(**{"2026-11-04_open": text})[0]
        for key in ("tokens_k", "tokens_source", "minutes"):
            self.assertNotIn(key, job)
        self.assertEqual(job["dollars"], 1.4)

    def test_a_pending_produced_is_left_out(self):
        job = self.jobs(**{"2026-11-04_open": session.BRIEF + session.COST.replace("one module and its tests", "pending")})[0]
        self.assertNotIn("produced", job)

    def test_a_brief_without_cost_or_header_has_only_its_id_date_and_rules(self):
        self.assertEqual(self.jobs(**{"2026-11-04_bare": session.BRIEF})[0],
                         {"id": "bare", "date": "2026-11-04", "agents": 1, "wave": 0})

    def test_a_number_in_another_unit_is_left_out(self):
        text = session.BRIEF + session.COST.replace("182000 tokens", "9 meter points").replace("25 minutes", "3 hours")
        job = self.jobs(**{"2026-11-04_units": text})[0]
        self.assertNotIn("tokens_k", job)
        self.assertNotIn("minutes", job)

    def test_a_minutes_line_with_a_note_after_the_unit_is_read(self):
        text = session.BRIEF + session.COST.replace("25 minutes", "17 min (wall clock of the worker)")
        self.assertEqual(self.jobs(**{"2026-11-04_note": text})[0]["minutes"], 17.0)

    def test_an_unknown_kind_or_outcome_is_left_out(self):
        text = CLOSED.replace("**Kind:** build", "**Kind:** chores").replace("**Outcome:** pass", "**Outcome:** maybe")
        job = self.jobs(**{"2026-11-04_odd": text})[0]
        self.assertNotIn("kind", job)
        self.assertNotIn("outcome", job)

    def test_a_header_line_below_the_first_part_is_not_a_header(self):
        job = self.jobs(**{"2026-11-04_late": session.BRIEF.replace("Do the work.", "**Kind:** build")})[0]
        self.assertNotIn("kind", job)

    def test_waves_rank_the_dates(self):
        jobs = self.jobs(**{"2026-11-02_a": session.BRIEF, "2026-11-04_b": session.BRIEF, "2026-11-04_c": session.BRIEF, "2026-11-03_d": session.BRIEF})
        self.assertEqual({j["id"]: j["wave"] for j in jobs}, {"a": 0, "d": 1, "b": 2, "c": 2})

    def test_a_folder_without_a_date_keeps_its_name_and_has_no_wave(self):
        job = self.jobs(plain=session.BRIEF)[0]
        self.assertEqual(job["id"], "plain")
        self.assertNotIn("wave", job)

    def test_match_picks_folders(self):
        self.write("2026-11-04_a/brief.md", session.BRIEF)
        self.write("2026-11-03_b/brief.md", session.BRIEF)
        self.assertEqual([j["id"] for j in job_record.export(self.root, "2026-11-04_*")], ["a"])

    def test_the_toml_reads_back_to_the_same_jobs(self):
        import tomllib
        jobs = self.jobs(**{"2026-11-04_closed": CLOSED, "2026-11-04_bare": session.BRIEF})
        self.assertEqual(tomllib.loads(job_record.to_toml(jobs))["job"], jobs)

    def test_a_quote_a_backslash_and_a_tab_in_produced_survive(self):
        import tomllib
        text = session.BRIEF + session.COST.replace("one module and its tests", 'says "a" \\ b\tc')
        jobs = self.jobs(**{"2026-11-04_q": text})
        self.assertEqual(tomllib.loads(job_record.to_toml(jobs))["job"][0]["produced"], 'says "a" \\ b\tc')

    def test_main_writes_the_file_and_refuses_an_empty_folder(self):
        self.write("2026-11-04_a/brief.md", session.BRIEF + session.COST)
        out = self.root / "out" / "jobs.toml"
        self.assertEqual(job_record.main([str(self.root), "--out", str(out)]), 0)
        self.assertIn('id = "a"', out.read_text())
        self.assertEqual(job_record.main([str(self.root / "out")]), 2)

    def test_a_cost_block_the_brief_check_accepts_is_one_the_exporter_reads(self):
        self.write("2026-11-04_a/brief.md", session.BRIEF + session.COST)
        self.assertEqual([m for m in brief_checks_messages(self.root)], [])
        self.assertEqual(job_record.export(self.root)[0]["tokens_k"], 182.0)


def brief_checks_messages(root: Path) -> list[str]:
    return [finding.message for finding in session.brief_checks.check(root, {})]


if __name__ == "__main__":
    unittest.main()
