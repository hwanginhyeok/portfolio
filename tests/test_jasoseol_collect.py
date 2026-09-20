#!/usr/bin/env python3
"""Offline unit tests for scripts/jasoseol_collect.py."""

from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import jasoseol_collect, state_utils

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "jasoseol"


def load_fixture(name: str) -> dict:
    path = FIXTURES_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


class JasoseolCollectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calendar_fixture = load_fixture("calendar_list.json")
        self.detail_2001 = load_fixture("detail_2001.json")
        self.detail_2005 = load_fixture("detail_2005.json")

    def test_mixed_announcement_recruiting_new_and_experienced_is_kept(self) -> None:
        ann_2001 = next(
            a for a in self.calendar_fixture["employment"] if a["id"] == 2001
        )
        # 2001 recruits both division 1 (신입) and division 2 (경력)
        divisions = [sub["division"] for sub in ann_2001["employments"]]
        self.assertIn(1, divisions)
        self.assertIn(2, divisions)
        self.assertTrue(jasoseol_collect.is_experienced_announcement(ann_2001))

        # Stage 1 filter over the fixture keeps 2001
        kept = [
            a
            for a in self.calendar_fixture["employment"]
            if jasoseol_collect.is_experienced_announcement(a)
        ]
        kept_ids = [a["id"] for a in kept]
        self.assertIn(2001, kept_ids)

    def test_announcement_with_only_division_1_or_3_is_dropped(self) -> None:
        ann_2002 = next(
            a for a in self.calendar_fixture["employment"] if a["id"] == 2002
        )
        ann_2003 = next(
            a for a in self.calendar_fixture["employment"] if a["id"] == 2003
        )
        # 2002 is 신입 only (1)
        self.assertFalse(jasoseol_collect.is_experienced_announcement(ann_2002))
        # 2003 is 인턴 only (3)
        self.assertFalse(jasoseol_collect.is_experienced_announcement(ann_2003))

        # Announcement with only 1 and 3 is also dropped
        mixed_non_exp = {
            "id": 9999,
            "title": "신입 및 인턴",
            "employments": [{"division": 1}, {"division": 3}],
        }
        self.assertFalse(
            jasoseol_collect.is_experienced_announcement(mixed_non_exp)
        )

        kept = [
            a
            for a in self.calendar_fixture["employment"]
            if jasoseol_collect.is_experienced_announcement(a)
        ]
        kept_ids = [a["id"] for a in kept]
        self.assertNotIn(2002, kept_ids)
        self.assertNotIn(2003, kept_ids)

    def test_sub_position_filtering_keeps_only_division_2_rows(self) -> None:
        # detail_2001 has division 1, 2, and 4
        sub_positions = jasoseol_collect.extract_experienced_sub_positions(
            self.detail_2001
        )
        self.assertEqual(
            sub_positions, ["Industrial AI Solutions Architect (경력)"]
        )
        self.assertNotIn("Industrial AI 신입", sub_positions)
        self.assertNotIn("계약직 테스터", sub_positions)

        # In rendered markdown, sub_positions in frontmatter only has division 2
        posting_record = {
            "id": 2001,
            "company": "Acme Industrial AI",
            "title": "Industrial AI Solutions Architect",
            "track": "engineering-consulting",
            "score": 30,
            "verdict": "actionable",
            "career_type": "경력",
            "start_time": "2026-09-01T09:00:00.000+09:00",
            "end_time": "2026-09-30T18:00:00.000+09:00",
            "url": "https://jasoseol.com/recruit/2001",
            "apply_url": "https://careers.acme.com/recruits/2001",
            "sub_positions": sub_positions,
        }
        rendered = jasoseol_collect.render_markdown(posting_record)
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "2001.md"
            file_path.write_text(rendered, encoding="utf-8")
            fm = jasoseol_collect.read_frontmatter(file_path)

        self.assertEqual(
            fm["sub_positions"], ["Industrial AI Solutions Architect (경력)"]
        )
        self.assertEqual(
            fm["experienced_positions"],
            ["Industrial AI Solutions Architect (경력)"],
        )

    def test_ledger_dedups_second_run_to_zero_new_postings(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir)
            config_file = inbox_dir / "config.json"
            config_file.write_text(
                json.dumps(
                    {
                        "lookahead_days": 60,
                        "score_threshold": 26,
                        "request_delay_seconds": 0.0,
                    }
                ),
                encoding="utf-8",
            )

            def fake_fetch_calendar(_sess, _start, _end):
                return copy.deepcopy(self.calendar_fixture["employment"]), None

            def fake_fetch_detail(_sess, ann_id):
                if ann_id == 2001:
                    return copy.deepcopy(self.detail_2001), None
                if ann_id == 2005:
                    return copy.deepcopy(self.detail_2005), None
                return None, f"Not found {ann_id}"

            with patch.object(
                jasoseol_collect, "fetch_calendar_list", side_effect=fake_fetch_calendar
            ), patch.object(
                jasoseol_collect, "fetch_detail", side_effect=fake_fetch_detail
            ):
                # First run
                stdout1 = io.StringIO()
                with patch("sys.stdout", stdout1):
                    code1 = jasoseol_collect.main(
                        [
                            "--config",
                            str(config_file),
                            "--inbox-dir",
                            str(inbox_dir),
                            "--json",
                        ]
                    )
                self.assertEqual(code1, 0)
                res1 = json.loads(stdout1.getvalue())
                self.assertEqual(res1["fetched"], 5)
                self.assertEqual(res1["experienced"], 3)  # 2001, 2004, 2005
                self.assertEqual(res1["actionable"], 2)  # 2001, 2005
                self.assertEqual(res1["new"], 2)

                self.assertTrue((inbox_dir / "2001.md").exists())
                self.assertTrue((inbox_dir / "2005.md").exists())
                state1 = json.loads(
                    (inbox_dir / "state.json").read_text(encoding="utf-8")
                )
                self.assertIn("2001", state1["seen"])
                self.assertIn("2005", state1["seen"])

                # Second run with identical data
                stdout2 = io.StringIO()
                with patch("sys.stdout", stdout2):
                    code2 = jasoseol_collect.main(
                        [
                            "--config",
                            str(config_file),
                            "--inbox-dir",
                            str(inbox_dir),
                            "--json",
                        ]
                    )
                self.assertEqual(code2, 0)
                res2 = json.loads(stdout2.getvalue())
                self.assertEqual(res2["new"], 0)
                self.assertEqual(res2["refreshed"], 0)

    def test_changed_end_time_refreshes_file_and_preserves_frontmatter(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir)
            config_file = inbox_dir / "config.json"
            config_file.write_text(
                json.dumps(
                    {
                        "lookahead_days": 60,
                        "score_threshold": 26,
                        "request_delay_seconds": 0.0,
                    }
                ),
                encoding="utf-8",
            )

            calendar_data = copy.deepcopy(self.calendar_fixture["employment"])

            def fake_fetch_calendar(_sess, _start, _end):
                return copy.deepcopy(calendar_data), None

            def fake_fetch_detail(_sess, ann_id):
                if ann_id == 2001:
                    return copy.deepcopy(self.detail_2001), None
                if ann_id == 2005:
                    return copy.deepcopy(self.detail_2005), None
                return None, f"Not found {ann_id}"

            with patch.object(
                jasoseol_collect, "fetch_calendar_list", side_effect=fake_fetch_calendar
            ), patch.object(
                jasoseol_collect, "fetch_detail", side_effect=fake_fetch_detail
            ):
                # First run
                jasoseol_collect.main(
                    [
                        "--config",
                        str(config_file),
                        "--inbox-dir",
                        str(inbox_dir),
                    ]
                )

            # Check initial end_time
            file_2001 = inbox_dir / "2001.md"
            fm_before = jasoseol_collect.read_frontmatter(file_2001)
            self.assertEqual(
                fm_before["end_time"], "2026-09-30T18:00:00.000+09:00"
            )

            # User added custom frontmatter field to 2001.md
            lines = file_2001.read_text(encoding="utf-8").splitlines()
            # Inject custom note in frontmatter
            lines.insert(1, 'custom_notes: "Operator review passed"')
            file_2001.write_text("\n".join(lines), encoding="utf-8")

            # Announcement 2001 changes deadline
            new_deadline = "2026-10-20T23:59:00.000+09:00"
            for a in calendar_data:
                if a["id"] == 2001:
                    a["end_time"] = new_deadline

            updated_detail_2001 = copy.deepcopy(self.detail_2001)
            updated_detail_2001["end_time"] = new_deadline

            def fake_fetch_detail_updated(_sess, ann_id):
                if ann_id == 2001:
                    return copy.deepcopy(updated_detail_2001), None
                if ann_id == 2005:
                    return copy.deepcopy(self.detail_2005), None
                return None, f"Not found {ann_id}"

            with patch.object(
                jasoseol_collect, "fetch_calendar_list", side_effect=fake_fetch_calendar
            ), patch.object(
                jasoseol_collect,
                "fetch_detail",
                side_effect=fake_fetch_detail_updated,
            ):
                stdout = io.StringIO()
                with patch("sys.stdout", stdout):
                    code = jasoseol_collect.main(
                        [
                            "--config",
                            str(config_file),
                            "--inbox-dir",
                            str(inbox_dir),
                            "--json",
                        ]
                    )

            self.assertEqual(code, 0)
            res = json.loads(stdout.getvalue())
            self.assertEqual(res["new"], 0)  # already in ledger, not new
            self.assertEqual(res["refreshed"], 1)

            # Check refreshed frontmatter
            fm_after = jasoseol_collect.read_frontmatter(file_2001)
            self.assertEqual(fm_after["end_time"], new_deadline)
            # Custom field is preserved!
            self.assertEqual(
                fm_after.get("custom_notes"), "Operator review passed"
            )

            # Check ledger state is also updated
            state = json.loads(
                (inbox_dir / "state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(state["seen"]["2001"]["end_time"], new_deadline)

    def test_malformed_or_empty_response_does_not_corrupt_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir)
            config_file = inbox_dir / "config.json"
            config_file.write_text("{}", encoding="utf-8")
            state_file = inbox_dir / "state.json"
            initial_state = {
                "seen": {
                    "999": {
                        "company": "Existing Corp",
                        "title": "Existing Role",
                        "end_time": "2026-09-01T00:00:00.000+09:00",
                    }
                }
            }
            state_file.write_text(json.dumps(initial_state), encoding="utf-8")

            # Case A: Calendar fetch returns None (network error or HTTP 500)
            with patch.object(
                jasoseol_collect,
                "fetch_calendar_list",
                return_value=(None, "HTTP 500 Server Error"),
            ):
                code = jasoseol_collect.main(
                    [
                        "--config",
                        str(config_file),
                        "--inbox-dir",
                        str(inbox_dir),
                    ]
                )
                self.assertNotEqual(code, 0)

            # State ledger remains intact
            current_state = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(current_state, initial_state)

            # Case B: Malformed response object
            with patch.object(
                jasoseol_collect.PoliteSession,
                "post_json",
                return_value=(None, "Bad JSON: Expecting value"),
            ):
                code = jasoseol_collect.main(
                    [
                        "--config",
                        str(config_file),
                        "--inbox-dir",
                        str(inbox_dir),
                    ]
                )
            # Case C: Empty or invalid JSON response (missing employment array)
            with patch.object(
                jasoseol_collect.PoliteSession,
                "post_json",
                return_value=({}, None),
            ):
                code = jasoseol_collect.main(
                    [
                        "--config",
                        str(config_file),
                        "--inbox-dir",
                        str(inbox_dir),
                    ]
                )
                self.assertNotEqual(code, 0)

            current_state = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(current_state, initial_state)

    def test_dry_run_does_not_write_files_or_mutate_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir)
            config_file = inbox_dir / "config.json"
            config_file.write_text("{}", encoding="utf-8")

            def fake_fetch_calendar(_sess, _start, _end):
                return copy.deepcopy(self.calendar_fixture["employment"]), None

            with patch.object(
                jasoseol_collect, "fetch_calendar_list", side_effect=fake_fetch_calendar
            ), patch.object(
                jasoseol_collect, "fetch_detail"
            ) as mock_detail:
                stdout = io.StringIO()
                with patch("sys.stdout", stdout):
                    code = jasoseol_collect.main(
                        [
                            "--config",
                            str(config_file),
                            "--inbox-dir",
                            str(inbox_dir),
                            "--dry-run",
                            "--json",
                        ]
                    )

                self.assertEqual(code, 0)
                mock_detail.assert_not_called()
                res = json.loads(stdout.getvalue())
                self.assertEqual(res["actionable"], 2)
                self.assertEqual(res["new"], 2)
                # No markdown files or state.json written
                self.assertEqual(list(inbox_dir.glob("*.md")), [])
                self.assertFalse((inbox_dir / "state.json").exists())

    def test_all_required_frontmatter_fields_present(self) -> None:
        posting = {
            "id": 12345,
            "company": "Test Co",
            "title": "Industrial AI Solutions Architect",
            "track": "engineering-consulting",
            "score": 30,
            "verdict": "actionable",
            "career_type": "경력",
            "start_time": "2026-09-01T09:00:00.000+09:00",
            "end_time": "2026-09-30T18:00:00.000+09:00",
            "apply_url": "https://example.com/apply",
            "sub_positions": ["Solutions Architect"],
        }
        rendered = jasoseol_collect.render_markdown(
            posting, content_body="Test content"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "12345.md"
            p.write_text(rendered, encoding="utf-8")
            fm = jasoseol_collect.read_frontmatter(p)

        required_fields = [
            "id",
            "company",
            "title",
            "track",
            "score",
            "verdict",
            "career_type",
            "start_time",
            "end_time",
            "url",
            "apply_url",
            "sub_positions",
            "experienced_positions",
        ]
        for field in required_fields:
            self.assertIn(
                field, fm, f"Required frontmatter field '{field}' missing"
            )
        self.assertEqual(fm["url"], "https://jasoseol.com/recruit/12345")

    def test_announcement_without_title_keywords_scores_on_sub_positions_and_passes(
        self,
    ) -> None:
        ann = {
            "id": 9101,
            "name": "현대모비스",
            "title": "2026 하반기 로보틱스 집중 채용",  # Title itself has score 0
        }
        detail = {
            "id": 9101,
            "name": "현대모비스",
            "title": "2026 하반기 로보틱스 집중 채용",
            "content": "",
            "employments": [
                {
                    "id": 1,
                    "division": 2,
                    "field": "연구직_로보틱스 모터 설계(경력)",
                },
                {
                    "id": 2,
                    "division": 2,
                    "field": "연구직_액추에이터 시스템/기구 설계(경력)",
                },
                {
                    "id": 3,
                    "division": 2,
                    "field": "관리직_로보틱스 생산기술(경력)",
                },
            ],
        }
        # Scored on announcement title alone: score is 0 and fails
        res_without_detail = jasoseol_collect.assess_announcement(
            ann, detail_data=None, score_threshold=28
        )
        self.assertFalse(res_without_detail["actionable"])
        self.assertEqual(res_without_detail["fit_score"], 0)

        # Scored with detail sub-positions: passes!
        res_with_detail = jasoseol_collect.assess_announcement(
            ann, detail_data=detail, score_threshold=28
        )
        self.assertTrue(res_with_detail["actionable"])
        self.assertGreaterEqual(res_with_detail["fit_score"], 28)
        self.assertIn(
            "연구직_로보틱스 모터 설계(경력)",
            res_with_detail["matched_sub_positions"],
        )

    def test_entry_level_only_sub_positions_do_not_contribute_to_score(
        self,
    ) -> None:
        ann = {
            "id": 9102,
            "name": "한국상사",
            "title": "2026년 하반기 채용",
        }
        # detail has high-keyword division 1 (신입) sub-position,
        # but only irrelevant division 2 (경력) sub-position
        detail = {
            "id": 9102,
            "name": "한국상사",
            "title": "2026년 하반기 채용",
            "content": "",
            "employments": [
                {
                    "id": 1,
                    "division": 1,  # 신입
                    "field": "연구직_로보틱스 모터 설계(신입)",
                },
                {
                    "id": 2,
                    "division": 2,  # 경력
                    "field": "7급_전국_경력경쟁채용_취업지원직",
                },
            ],
        }
        res = jasoseol_collect.assess_announcement(
            ann, detail_data=detail, score_threshold=28
        )
        self.assertFalse(res["actionable"])
        self.assertEqual(res["fit_score"], 0)
        self.assertEqual(res["matched_sub_positions"], [])

    def test_detail_cache_prevents_second_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / ".cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            cached_payload = {
                "id": 9103,
                "end_time": "2026-10-31T23:59:00.000+09:00",
                "detail": {
                    "id": 9103,
                    "name": "Cached Corp",
                    "title": "Cached Title",
                    "employments": [
                        {"division": 2, "field": "로봇 제어(경력)"}
                    ],
                },
            }
            (cache_dir / "9103.json").write_text(
                json.dumps(cached_payload), encoding="utf-8"
            )

            sess = jasoseol_collect.PoliteSession(delay=0.0)
            with patch.object(
                jasoseol_collect, "fetch_detail"
            ) as mock_fetch:
                detail, err, from_cache = jasoseol_collect.get_or_fetch_detail(
                    sess,
                    ann_id=9103,
                    end_time="2026-10-31T23:59:00.000+09:00",
                    cache_dir=cache_dir,
                )
                self.assertTrue(from_cache)
                self.assertIsNotNone(detail)
                self.assertIsNone(err)
                mock_fetch.assert_not_called()

    def test_detail_fetch_failure_skips_only_that_announcement(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir)
            config_file = inbox_dir / "config.json"
            config_file.write_text(
                json.dumps(
                    {
                        "lookahead_days": 60,
                        "score_threshold": 26,
                        "request_delay_seconds": 0.0,
                    }
                ),
                encoding="utf-8",
            )

            calendar_data = [
                {
                    "id": 3001,
                    "name": "Failing Corp",
                    "title": "Failing Role",
                    "start_time": "2026-09-01T09:00:00.000+09:00",
                    "end_time": "2026-09-30T18:00:00.000+09:00",
                    "employments": [{"id": 1, "division": 2}],
                },
                {
                    "id": 3002,
                    "name": "Success Corp",
                    "title": "Success Role",
                    "start_time": "2026-09-01T09:00:00.000+09:00",
                    "end_time": "2026-09-30T18:00:00.000+09:00",
                    "employments": [{"id": 2, "division": 2}],
                },
            ]

            success_detail = {
                "id": 3002,
                "name": "Success Corp",
                "title": "Success Role",
                "content": "",
                "employments": [
                    {
                        "id": 2,
                        "division": 2,
                        "field": "자율제조 로봇 제어 엔지니어(경력)",
                    }
                ],
            }

            def fake_fetch_calendar(_sess, _start, _end):
                return copy.deepcopy(calendar_data), None

            def fake_fetch_detail(_sess, ann_id):
                if ann_id == 3001:
                    return None, "HTTP 500 Internal Server Error"
                if ann_id == 3002:
                    return copy.deepcopy(success_detail), None
                return None, f"Not found {ann_id}"

            with patch.object(
                jasoseol_collect, "fetch_calendar_list", side_effect=fake_fetch_calendar
            ), patch.object(
                jasoseol_collect, "fetch_detail", side_effect=fake_fetch_detail
            ):
                stdout = io.StringIO()
                with patch("sys.stdout", stdout):
                    code = jasoseol_collect.main(
                        [
                            "--config",
                            str(config_file),
                            "--inbox-dir",
                            str(inbox_dir),
                            "--json",
                        ]
                    )

            self.assertEqual(code, 0)
            res = json.loads(stdout.getvalue())
            self.assertEqual(res["experienced"], 2)
            self.assertEqual(res["actionable"], 1)
            self.assertEqual(res["new"], 1)
            # Only announcement 3001 had detail failure
            self.assertEqual(len(res["failures"]), 1)
            self.assertIn("3001", res["failures"][0])
            # Only 3002.md was written
            self.assertTrue((inbox_dir / "3002.md").exists())
            self.assertFalse((inbox_dir / "3001.md").exists())


if __name__ == "__main__":
    unittest.main()
