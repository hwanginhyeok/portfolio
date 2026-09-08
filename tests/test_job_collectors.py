import errno
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import global_collect
from scripts import state_utils
from scripts import wanted_collect
from scripts.shortlist import assess_shortlist, rank_actionable
from scripts.wanted_state_repair import (
    hydrate_zero_byte_files,
    read_frontmatter,
    reconstruct_wanted_state,
)


class AtomicStatePersistenceTests(unittest.TestCase):
    def test_enospc_during_replace_preserves_previous_ledger_and_cleans_temp(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            target = directory / "state.json"
            previous = '{"seen":{"old":{"first_seen":"2026-08-18"}}}\n'
            target.write_text(previous, encoding="utf-8")

            with patch.object(
                state_utils.os,
                "replace",
                side_effect=OSError(errno.ENOSPC, "No space left on device"),
            ):
                with self.assertRaises(OSError):
                    state_utils.atomic_write_json(target, {"seen": {"new": {}}})

            self.assertEqual(target.read_text(encoding="utf-8"), previous)
            self.assertEqual(list(directory.glob(".state.json.*.tmp")), [])

    def test_fsync_failure_preserves_previous_ledger(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "state.json"
            previous = '{"seen":{"old":{}}}\n'
            target.write_text(previous, encoding="utf-8")

            with patch.object(
                state_utils.os,
                "fsync",
                side_effect=OSError(errno.ENOSPC, "No space left on device"),
            ):
                with self.assertRaises(OSError):
                    state_utils.atomic_write_json(target, {"seen": {"new": {}}})

            self.assertEqual(target.read_text(encoding="utf-8"), previous)
            self.assertEqual(list(Path(temp_dir).glob(".state.json.*.tmp")), [])

    def test_atomic_text_write_preserves_previous_file_on_fsync_failure(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "posting.md"
            previous = "old posting\n"
            target.write_text(previous, encoding="utf-8")

            with patch.object(
                state_utils.os,
                "fsync",
                side_effect=OSError(errno.ENOSPC, "No space left on device"),
            ):
                with self.assertRaises(OSError):
                    state_utils.atomic_write_text(target, "new posting\n")

            self.assertEqual(target.read_text(encoding="utf-8"), previous)
            self.assertEqual(list(Path(temp_dir).glob(".posting.md.*.tmp")), [])


class WantedLedgerRepairTests(unittest.TestCase):
    def test_corrupt_ledger_reconstruction_merges_baseline_files_and_digest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            postings = root / "wanted"
            digest = postings / "digest"
            postings.mkdir()
            digest.mkdir()
            (postings / "2-acme.md").write_text(
                "---\n"
                "wanted_id: 2\n"
                'company: "Acme"\n'
                'position: "Supplier Quality Engineer"\n'
                'first_seen: "2026-08-22"\n'
                "---\n\n# body\n",
                encoding="utf-8",
            )
            (postings / "1-old.md").write_text(
                "---\n"
                "wanted_id: 1\n"
                'company: "Changed in file"\n'
                'position: "Changed in file"\n'
                'first_seen: "2026-08-24"\n'
                "---\n",
                encoding="utf-8",
            )
            (digest / "2026-08-23.md").write_text(
                "# 원티드 수집 다이제스트 — 2026-08-23\n\n"
                "| 회사 | 포지션 | 지역 | 링크 |\n"
                "|---|---|---|---|\n"
                "| Digest Co | Test Engineer | 서울 | [#3](https://www.wanted.co.kr/wd/3) |\n",
                encoding="utf-8",
            )

            baseline = {
                "seen": {
                    "1": {
                        "first_seen": "2026-08-18",
                        "company": "Original Co",
                        "position": "Original Position",
                    }
                }
            }
            repaired = reconstruct_wanted_state(baseline, postings, digest)

            self.assertEqual(set(repaired["seen"]), {"1", "2", "3"})
            self.assertEqual(repaired["seen"]["1"], baseline["seen"]["1"])
            self.assertEqual(repaired["seen"]["2"]["company"], "Acme")
            self.assertEqual(repaired["seen"]["2"]["first_seen"], "2026-08-22")
            self.assertEqual(repaired["seen"]["3"]["company"], "Digest Co")
            self.assertEqual(repaired["seen"]["3"]["first_seen"], "2026-08-23")
            self.assertTrue((postings / "2-acme.md").exists())

    def test_hydrate_mode_is_bounded_and_does_not_overwrite_nonzero_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            postings = Path(temp_dir)
            zero = postings / "42-acme.md"
            existing = postings / "43-existing.md"
            zero.write_bytes(b"")
            existing.write_text("keep this file\n", encoding="utf-8")
            calls = []

            def fake_detail(_session, posting_id):
                calls.append(posting_id)
                return {
                    "id": posting_id,
                    "position": "Manufacturing Test Engineer",
                    "company": {"name": "Acme"},
                    "detail": {"intro": "Build the test system."},
                }

            results = hydrate_zero_byte_files(
                postings,
                {"seen": {"42": {"company": "Acme", "position": ""}}},
                session=object(),
                detail_fetcher=fake_detail,
            )

            self.assertEqual(calls, [42])
            self.assertEqual([row["status"] for row in results], ["success"])
            self.assertIn("Manufacturing Test Engineer", zero.read_text(encoding="utf-8"))
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep this file\n")


class CollectorTrackTests(unittest.TestCase):
    def test_industrial_ai_solutions_architect_is_actionable_in_korea(self):
        result = assess_shortlist(
            {
                "title": "Industrial AI Solutions Architect",
                "department": "Manufacturing Transformation",
                "location_raw": "Seoul, South Korea",
                "eligibility": "korea",
                "body": "Deliver industrial AI systems to factory customers.",
            }
        )

        self.assertTrue(result["actionable"])
        self.assertEqual(result["track"], "engineering-consulting")
        self.assertIn("industrial-ai", result["technical_signal_evidence"])
        self.assertIn(
            "industrial-manufacturing-transformation",
            result["owner_domain_evidence"],
        )

    def test_forward_deployed_robotics_engineer_is_actionable_when_feasible(self):
        result = assess_shortlist(
            {
                "title": "Forward-Deployed Robotics Engineer",
                "location_raw": "Remote - worldwide",
                "eligibility": "remote",
                "remote_flag": True,
                "body": "This role is remote worldwide and deploys robots on customer sites.",
            }
        )

        self.assertTrue(result["actionable"])
        self.assertEqual(result["track"], "ai-native")
        self.assertEqual(result["feasibility"], "remote")
        self.assertIn("forward-deployed-engineering", result["technical_signal_evidence"])

    def test_industrial_ai_field_pm_is_actionable_with_owner_domain_evidence(self):
        result = assess_shortlist(
            {
                "title": "Industrial AI Field Product Manager",
                "department": "Factory Automation",
                "location_raw": "Seoul, South Korea",
                "eligibility": "korea",
                "body": "Lead technical deployments of AI systems at industrial customer sites.",
            }
        )

        self.assertTrue(result["actionable"])
        self.assertEqual(result["reason"], "actionable")
        self.assertIn("industrial-ai", result["technical_signal_evidence"])
        self.assertIn("robotics-industrial-automation", result["owner_domain_evidence"])

    def test_physical_ai_role_is_actionable_with_robotics_owner_domain(self):
        result = assess_shortlist(
            {
                "title": "Physical AI Product Manager",
                "department": "Robotics and Automation",
                "location_raw": "Seoul, South Korea",
                "eligibility": "korea",
                "body": "Own the technical roadmap for robot learning and deployment.",
            }
        )

        self.assertTrue(result["actionable"])
        self.assertEqual(result["reason"], "actionable")
        self.assertIn("industrial-ai", result["technical_signal_evidence"])
        self.assertIn("robotics-industrial-automation", result["owner_domain_evidence"])

    def test_generic_cloud_and_ai_product_roles_stay_informational(self):
        cloud = assess_shortlist(
            {
                "title": "Cloud Solutions Architect",
                "department": "Physical AI Cloud Platform",
                "location_raw": "Seoul, South Korea",
                "eligibility": "korea",
                "body": "Design cloud infrastructure and data services.",
            }
        )
        ai_product = assess_shortlist(
            {
                "title": "AI Product Manager",
                "department": "Software Product",
                "location_raw": "Seoul, South Korea",
                "eligibility": "korea",
                "body": "Own an AI product roadmap for a software platform.",
            }
        )

        self.assertFalse(cloud["actionable"])
        self.assertEqual(cloud["reason"], "generic-cloud-software")
        self.assertFalse(ai_product["actionable"])
        self.assertEqual(ai_product["reason"], "generic-ai-software")

    def test_track_metadata_is_preserved_in_search_and_written_frontmatter(self):
        config = json.loads(
            (Path(__file__).resolve().parents[1] / "config" / "wanted_targets.json")
            .read_text(encoding="utf-8")
        )
        lanes = wanted_collect.configured_search_lanes(config)
        self.assertIn(("engineering-consulting", "Solutions Architect"), lanes)

        wanted_content = wanted_collect.render_markdown(
            {
                "id": 7,
                "company": {"name": "Acme Robotics"},
                "position": "Industrial AI Solutions Architect",
                "address": {"location": "Seoul"},
                "detail": {"intro": "Build factory AI systems."},
            },
            {
                "id": 7,
                "company": "Acme Robotics",
                "position": "Industrial AI Solutions Architect",
                "first_seen": "2026-08-24",
                "matched_keywords": {"Solutions Architect"},
                "search_lanes": {"ai-native", "engineering-consulting"},
            },
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            wanted_path = Path(temp_dir) / "wanted.md"
            wanted_path.write_text(wanted_content, encoding="utf-8")
            frontmatter = read_frontmatter(wanted_path)

        self.assertEqual(frontmatter["track"], "engineering-consulting")
        self.assertEqual(frontmatter["search_lane"], "engineering-consulting")
        self.assertEqual(
            frontmatter["search_lanes"], ["ai-native", "engineering-consulting"]
        )

        global_posting = {
            "company": "Acme Robotics",
            "ats": "greenhouse",
            "job_id": "7",
            "title": "Forward-Deployed Robotics Engineer",
            "location_raw": "Seoul",
            "country": "South Korea",
            "region": "apac",
            "eligibility": "korea",
            "track": "ai-native",
            "search_lane": "ai-native",
            "search_lanes": ["ai-native"],
            "score": 30,
            "url": "https://example.test/jobs/7",
            "first_seen": "2026-08-24",
            "body": "Deploy robotics systems.",
        }
        global_content = global_collect.render_markdown(
            global_posting, ["forward-deployed engineering"]
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            global_path = Path(temp_dir) / "global.md"
            global_path.write_text(global_content, encoding="utf-8")
            frontmatter = read_frontmatter(global_path)

        self.assertEqual(frontmatter["track"], "ai-native")
        self.assertEqual(frontmatter["search_lanes"], ["ai-native"])

    def test_global_filter_assigns_lane_metadata_to_state_candidate(self):
        posting = {
            "title": "Industrial AI Solutions Architect",
            "department": "Manufacturing Transformation",
            "body": "Industrial AI for factories.",
            "location_raw": "Seoul, South Korea",
            "remote_flag": False,
            "company": "Acme Robotics",
        }
        kept, _, _ = global_collect.filter_and_score(
            [posting],
            [("solutions architect", re.compile(r"solutions?\s+architect", re.I), 5)],
            [],
            [],
            [],
            {"title": 3, "department": 2, "body": 1},
            15,
            {"solutions architect": "engineering-consulting"},
        )

        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]["track"], "engineering-consulting")
        self.assertEqual(kept[0]["search_lane"], "engineering-consulting")
        self.assertEqual(kept[0]["search_lanes"], ["engineering-consulting"])


class ShortlistTests(unittest.TestCase):
    def test_feasibility_gates_keep_korea_and_credible_sponsorship(self):
        korea = assess_shortlist(
            {
                "title": "Supplier Quality Engineer",
                "location_raw": "Seoul, South Korea",
                "eligibility": "korea",
                "body": "Supplier quality, APQP, PPAP and manufacturing test.",
            }
        )
        sponsored = assess_shortlist(
            {
                "title": "NPI Technical Program Manager",
                "location_raw": "Austin, United States",
                "eligibility": "sponsorship-likely",
                "body": "Visa sponsorship available for this role; own NPI and supplier quality.",
            }
        )
        global_remote = assess_shortlist(
            {
                "title": "Electrical Validation Engineer",
                "location_raw": "Remote - United States",
                "country": "United States",
                "eligibility": "remote",
                "remote_flag": True,
                "body": "This role is remote globally and owns validation infrastructure.",
            }
        )
        generic = assess_shortlist(
            {
                "title": "Technical Sales Manager",
                "location_raw": "Seoul, South Korea",
                "eligibility": "korea",
                "body": "Sell industrial products and manage accounts.",
            }
        )

        self.assertTrue(korea["actionable"])
        self.assertTrue(sponsored["actionable"])
        self.assertTrue(global_remote["actionable"])
        self.assertFalse(generic["actionable"])
        self.assertEqual(generic["reason"], "generic-sales-marketing-cx")

    def test_us_only_remote_is_not_actionable(self):
        result = assess_shortlist(
            {
                "title": "Reliability Engineer",
                "location_raw": "Remote - United States",
                "country": "United States",
                "eligibility": "remote",
                "remote_flag": True,
                "body": "Remote, U.S.-only. No international hiring.",
            }
        )

        self.assertFalse(result["actionable"])
        self.assertEqual(result["reason"], "us-only-remote")

    def test_remote_scope_is_required_and_explicit_negative_wins(self):
        unclear = assess_shortlist(
            {
                "title": "Reliability Engineer",
                "eligibility": "remote",
                "remote_flag": True,
                "body": "Remote position; location depends on the hiring team.",
            }
        )
        contradictory = assess_shortlist(
            {
                "title": "Reliability Engineer",
                "eligibility": "remote",
                "remote_flag": True,
                "body": "Remote globally, but this role hires in the United States only.",
            }
        )

        self.assertFalse(unclear["actionable"])
        self.assertEqual(unclear["reason"], "remote-scope-unclear")
        self.assertFalse(contradictory["actionable"])
        self.assertEqual(contradictory["reason"], "us-only-remote")

    def test_title_or_department_fit_is_required_not_body_only(self):
        body_only = assess_shortlist(
            {
                "title": "Project Coordinator",
                "department": "Operations",
                "eligibility": "korea",
                "body": "Own manufacturing, reliability, and supplier quality programs.",
            }
        )
        department_fit = assess_shortlist(
            {
                "title": "Program Manager",
                "department": "Hardware Systems",
                "eligibility": "korea",
                "body": "Coordinate the product launch.",
            }
        )

        self.assertFalse(body_only["actionable"])
        self.assertEqual(body_only["reason"], "outside-profile")
        self.assertTrue(department_fit["actionable"])
        self.assertIn("electrical-hardware", department_fit["fit_evidence"])

    def test_generic_role_families_cannot_surface_from_body_keywords(self):
        cases = (
            ("Order Management", "generic-order-management"),
            ("CX Manager", "generic-sales-marketing-cx"),
            ("Marketing Manager", "generic-sales-marketing-cx"),
            ("AI Agent TPM (Technical Project Manager)", "generic-ai-software"),
            ("Software Test Engineer", "generic-ai-software"),
            ("Operations Manager", "unrelated-manager"),
        )
        for title, expected_reason in cases:
            with self.subTest(title=title):
                result = assess_shortlist(
                    {
                        "title": title,
                        "eligibility": "korea",
                        "location_raw": "Seoul, South Korea",
                        "body": "Manufacturing hardware validation and supplier quality.",
                    }
                )
                self.assertFalse(result["actionable"])
                self.assertEqual(result["reason"], expected_reason)

    def test_sponsorship_needs_affirmative_text(self):
        h1b_only = assess_shortlist(
            {
                "title": "Manufacturing Test Engineer",
                "eligibility": "sponsorship-likely",
                "location_raw": "Austin, United States",
                "body": "H-1B transfer possible; relocation support may be available.",
            }
        )
        affirmative = assess_shortlist(
            {
                "title": "Manufacturing Test Engineer",
                "eligibility": "sponsorship-likely",
                "location_raw": "Austin, United States",
                "body": "Visa sponsorship is available for this role.",
            }
        )

        self.assertFalse(h1b_only["actionable"])
        self.assertEqual(h1b_only["reason"], "sponsorship-unconfirmed")
        self.assertTrue(affirmative["actionable"])

    def test_apac_without_sponsorship_stays_informational(self):
        result = assess_shortlist(
            {
                "title": "Manufacturing Test Engineer",
                "eligibility": "korea-apac",
                "location_raw": "Singapore",
                "country": "Singapore",
                "body": "Manufacturing test and validation responsibilities.",
            }
        )

        self.assertFalse(result["actionable"])
        self.assertEqual(result["reason"], "apac-work-authorization-unconfirmed")
        self.assertEqual(result["feasibility"], "korea-apac")

    def test_apac_with_explicit_sponsorship_is_actionable(self):
        result = assess_shortlist(
            {
                "title": "Manufacturing Test Engineer",
                "eligibility": "korea-apac",
                "location_raw": "Singapore",
                "country": "Singapore",
                "body": "The company sponsors work visas for this role.",
            }
        )

        self.assertTrue(result["actionable"])
        self.assertEqual(result["feasibility"], "sponsorship-likely")

        contradictory = assess_shortlist(
            {
                "title": "Manufacturing Test Engineer",
                "eligibility": "korea-apac",
                "location_raw": "Singapore",
                "country": "Singapore",
                "body": (
                    "The company sponsors work visas for this role, but no visa "
                    "sponsorship is available."
                ),
            }
        )

        self.assertFalse(contradictory["actionable"])
        self.assertEqual(
            contradictory["reason"], "apac-work-authorization-unconfirmed"
        )

    def test_korean_district_only_address_is_korea_feasible(self):
        wanted_result = assess_shortlist(
            {
                "title": "Supplier Quality Engineer",
                "location_raw": "금천구",
                "body": "Supplier quality, APQP and manufacturing test.",
            }
        )
        global_result = global_collect.eligibility(
            {
                "title": "Supplier Quality Engineer",
                "location_raw": "금천구",
                "country_hint": "",
                "body": "Supplier quality, APQP and manufacturing test.",
                "remote_flag": False,
            }
        )

        self.assertTrue(wanted_result["actionable"])
        self.assertEqual(wanted_result["feasibility"], "korea")
        self.assertEqual(global_result, ("korea", "South Korea", "apac"))

    def test_explicit_visa_needed_bucket_is_not_promoted_by_location(self):
        result = assess_shortlist(
            {
                "title": "Manufacturing Test Engineer",
                "eligibility": "visa-needed",
                "location_raw": "Seoul, South Korea",
                "body": "Manufacturing test and validation responsibilities.",
            }
        )

        self.assertFalse(result["actionable"])
        self.assertEqual(result["reason"], "visa-needed")

    def test_realistic_corpus_false_positives_stay_out(self):
        root = Path(__file__).resolve().parents[1]

        def corpus_row(relative_path: str, *, force_korea: bool = True):
            path = root / relative_path
            frontmatter = read_frontmatter(path)
            row = {
                "title": frontmatter.get("title") or frontmatter.get("position") or "",
                "department": frontmatter.get("department") or "",
                "company": frontmatter.get("company") or "",
                "location_raw": frontmatter.get("location") or "",
                "country": frontmatter.get("country") or "",
                "eligibility": frontmatter.get("eligibility") or "",
                "body": path.read_text(encoding="utf-8"),
            }
            if force_korea:
                row.update(eligibility="korea", location_raw="Seoul, South Korea")
            return row

        fixtures = (
            ("docs/jd/_inbox/global/amat-2625949.md", "generic-order-management"),
            ("docs/jd/_inbox/global/anthropic-5108695008.md", "unrelated-manager"),
            ("docs/jd/_inbox/wanted/319757-엣지크로스.md", "generic-ai-software"),
            ("docs/jd/_inbox/wanted/243828-팀에버플.md", "unrelated-manager"),
            (
                "docs/jd/_inbox/wanted/380480-동구밭.md",
                "consumer-sector",
            ),
            (
                "docs/jd/_inbox/wanted/370516-딥다이브.md",
                "generic-supply-chain",
            ),
            (
                "docs/jd/_inbox/wanted/377920-닷어스.md",
                "generic-supply-chain",
            ),
        )
        for relative_path, expected_reason in fixtures:
            with self.subTest(relative_path=relative_path):
                result = assess_shortlist(corpus_row(relative_path))
                self.assertFalse(result["actionable"])
                self.assertEqual(result["reason"], expected_reason)

        shield = assess_shortlist(
            corpus_row(
                "docs/jd/_inbox/global/shield-ai-9a9b8c07-1d96-4bcc-a29c-079b94516936.md",
                force_korea=False,
            )
        )
        self.assertFalse(shield["actionable"])
        self.assertEqual(shield["reason"], "visa-needed")

    def test_aptiv_automotive_manufacturing_and_test_roles_are_actionable(self):
        root = Path(__file__).resolve().parents[1]

        def corpus_row(relative_path: str):
            path = root / relative_path
            frontmatter = read_frontmatter(path)
            return {
                "title": frontmatter.get("title") or "",
                "department": frontmatter.get("department") or "",
                "location_raw": "Seoul, South Korea",
                "country": "South Korea",
                "eligibility": "korea",
                "body": path.read_text(encoding="utf-8"),
            }

        manufacturing = assess_shortlist(
            corpus_row("docs/jd/_inbox/global/aptiv-000666213.md")
        )
        test_lab = assess_shortlist(
            corpus_row("docs/jd/_inbox/global/aptiv-000657922.md")
        )

        self.assertTrue(manufacturing["actionable"])
        self.assertIn("technical-product-industrialization", manufacturing["owner_domain_evidence"])
        self.assertTrue(test_lab["actionable"])
        self.assertIn(
            "physical-product-test-validation-reliability-quality",
            test_lab["owner_domain_evidence"],
        )

    def test_motor_reliability_and_test_roles_have_owner_domain_connection(self):
        cases = (
            {
                "title": "Motor Control Test Engineer",
                "department": "Power Electronics",
                "expected_domain": "motor-power-electronics",
            },
            {
                "title": "Product Reliability Engineer",
                "department": "Physical Product Quality",
                "expected_domain": "physical-product-test-validation-reliability-quality",
            },
            {
                "title": "Hardware Validation Engineer",
                "department": "Embedded Electrical Systems",
                "expected_domain": "embedded-electrical-hardware",
            },
        )
        for case in cases:
            with self.subTest(title=case["title"]):
                result = assess_shortlist(
                    {
                        **case,
                        "eligibility": "korea",
                        "location_raw": "Seoul, South Korea",
                        "body": "Own physical product verification and reliability results.",
                    }
                )
                self.assertTrue(result["actionable"])
                self.assertIn(case["expected_domain"], result["owner_domain_evidence"])

    def test_blocked_itar_is_not_actionable(self):
        result = assess_shortlist(
            {
                "title": "Electrical Test Engineer",
                "location_raw": "California, United States",
                "eligibility": "blocked-itar",
                "body": "ITAR-controlled program; must be a US person.",
            }
        )

        self.assertFalse(result["actionable"])
        self.assertEqual(result["reason"], "blocked-itar")
        self.assertEqual(
            global_collect.eligibility(
                {
                    "title": "Electrical Test Engineer",
                    "location_raw": "Seoul, South Korea",
                    "country_hint": "",
                    "body": "ITAR-controlled program; must be a US person.",
                    "remote_flag": False,
                }
            )[0],
            "blocked-itar",
        )

        hyphenated = assess_shortlist(
            {
                "title": "Electrical Test Engineer",
                "location_raw": "Seoul, South Korea",
                "eligibility": "korea",
                "body": "Export-controlled program; U.S.-person requirement.",
            }
        )
        self.assertFalse(hyphenated["actionable"])
        self.assertEqual(hyphenated["reason"], "blocked-itar")

    def test_actionable_roles_are_ranked_by_fit(self):
        postings = [
            {
                "title": "Technical Program Manager, NPI",
                "company": "Low Fit",
                "eligibility": "korea",
                "location_raw": "Seoul",
                "body": "Coordinate a technical program.",
            },
            {
                "title": "Senior Manufacturing Test and Reliability Engineer, Electrical Hardware",
                "company": "High Fit",
                "eligibility": "korea",
                "location_raw": "Seoul",
                "body": "Own reliability, validation, quality, NPI and supplier test systems.",
            },
        ]

        ranked = rank_actionable(postings)

        self.assertEqual([p["company"] for p in ranked], ["High Fit", "Low Fit"])
        self.assertGreater(ranked[0]["fit_score"], ranked[1]["fit_score"])


if __name__ == "__main__":
    unittest.main()
