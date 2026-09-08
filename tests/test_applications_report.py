"""Focused tests for scripts/applications_report.py.

Covers what the daily report can get wrong without anyone noticing: the row
order the user reads first, the elapsed-days arithmetic, and the fact that a
row missing every optional field still renders.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import applications_report as ar  # noqa: E402


def row(**overrides):
    base = {
        "id": "x", "company": "C", "position": "P", "url": None,
        "channel": "ch", "status": "미지원", "applied_at": None,
        "next_action": "n", "notes": None,
    }
    base.update(overrides)
    return base


def test_submitted_rows_sort_above_unapplied():
    rows = [row(status="미지원", company="Z"), row(status="제출", company="A"),
            row(status="준비완료", company="M")]
    assert [r["status"] for r in ar.sort_rows(rows)] == ["제출", "준비완료", "미지원"]


def test_unknown_status_sorts_last_instead_of_raising():
    rows = [row(status="정체불명"), row(status="제출")]
    assert [r["status"] for r in ar.sort_rows(rows)] == ["제출", "정체불명"]


@pytest.mark.parametrize("applied,today,expected", [
    ("2026-05-15", "2026-09-06", 114),
    ("2026-09-06", "2026-09-06", 0),
    (None, "2026-09-06", None),
    ("not-a-date", "2026-09-06", None),
])
def test_days_since(applied, today, expected):
    assert ar.days_since(applied, today) == expected


def test_markdown_renders_a_row_with_no_url_or_notes():
    out = ar.render_markdown([row()], "2026-09-06")
    assert "| ⬜ 미지원 | C | P |" in out
    assert "](" not in out.split("## 전체")[1].split("## 대기")[0]


def test_html_escapes_a_hostile_position_title():
    out = ar.render_html([row(position="<script>alert(1)</script>")], "2026-09-06")
    assert "<script>alert(1)</script>" not in out
    assert "&lt;script&gt;" in out


def test_caption_lists_only_pending_rows():
    rows = [row(status="제출", company="Done", next_action="wait"),
            row(status="준비완료", company="Todo", next_action="submit")]
    text = ar.caption(rows, "2026-09-06")
    assert "• Todo — submit" in text
    assert "Done" not in text


def test_live_ledger_parses_and_renders():
    rows = ar.load_ledger(REPO / "docs" / "jd" / "applications.json")
    assert rows, "the shipped ledger must not be empty"
    for r in rows:
        assert r.get("company") and r.get("status"), f"incomplete row: {r.get('id')}"
    ar.render_markdown(rows, "2026-09-06")
    ar.render_html(rows, "2026-09-06")


def test_load_ledger_rejects_a_non_list(tmp_path):
    bad = tmp_path / "applications.json"
    bad.write_text(json.dumps({"applications": {"a": 1}}), encoding="utf-8")
    with pytest.raises(ValueError):
        ar.load_ledger(bad)
