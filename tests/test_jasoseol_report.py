#!/usr/bin/env python3
"""Offline unit tests for scripts/jasoseol_report.py.

Covers:
  - Calendar bucketing of deadlines into the correct day cells
  - Urgent marking window (deadlines within the next 3 days)
  - HTML escaping of hostile strings (XSS prevention in company/title/sub-positions/URLs)
  - Sorting actionable postings by deadline ascending (with missing deadlines last)
  - The empty case that notifies a plain message through the harness ops bot
  - The non-empty case that writes HTML and notifies the caption
  - Accurate caption counts for actionable postings and urgent deadlines
  - Shortlist threshold filtering
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

import pytest

from scripts import jasoseol_report as jr


def make_posting(**overrides) -> dict:
    pid = str(overrides.get("id", "1001"))
    base = {
        "id": pid,
        "company": "테스트회사",
        "title": "임베디드 엔지니어",
        "track": "core",
        "score": 28,
        "verdict": "actionable",
        "actionable": True,
        "scoring_version": 2,
        "career_type": "경력",
        "start_time": "2026-09-01T00:00:00.000+09:00",
        "end_time": "2026-09-25T23:59:00.000+09:00",
        "url": f"https://jasoseol.com/recruit/{pid}",
        "apply_url": f"https://test.com/apply/{pid}",
        "sub_positions": ["모터제어", "전력전자"],
        "first_seen": "2026-09-20",
    }
    base.update(overrides)
    return base


# ── 1. Calendar bucketing ───────────────────────────────────────────────────

def test_calendar_bucketing_by_date():
    p1 = make_posting(id="1", end_time="2026-09-25T18:00:00.000+09:00")
    p2 = make_posting(id="2", end_time="2026-09-25T23:59:00.000+09:00")
    p3 = make_posting(id="3", end_time="2026-10-02T12:00:00.000+09:00")
    p4 = make_posting(id="4", end_time=None)

    buckets = jr.bucket_postings_by_date([p1, p2, p3, p4])

    assert "2026-09-25" in buckets
    assert len(buckets["2026-09-25"]) == 2
    assert {p["id"] for p in buckets["2026-09-25"]} == {"1", "2"}

    assert "2026-10-02" in buckets
    assert len(buckets["2026-10-02"]) == 1
    assert buckets["2026-10-02"][0]["id"] == "3"

    assert None not in buckets


def test_calendar_rendered_in_correct_day_cells():
    today = date(2026, 9, 20)  # Sunday
    p1 = make_posting(id="101", company="알파컴퍼니", title="HW엔지니어", end_time="2026-09-22T23:59:00.000+09:00")
    p2 = make_posting(id="102", company="베타테크", title="SW엔지니어", end_time="2026-09-25T18:00:00.000+09:00")

    html_out = jr.render_html([p1, p2], today=today)

    # Both companies and titles appear in the calendar
    assert "알파컴퍼니" in html_out
    assert "HW엔지니어" in html_out
    assert "베타테크" in html_out
    assert "SW엔지니어" in html_out

    # Both links to jasoseol recruitment are present
    assert "https://jasoseol.com/recruit/101" in html_out
    assert "https://jasoseol.com/recruit/102" in html_out

    # Day 09/22 has p1, Day 09/25 has p2
    assert "09/22" in html_out
    assert "09/25" in html_out


# ── 2. Urgent marking window ────────────────────────────────────────────────

@pytest.mark.parametrize("end_time,today,expected_urgent", [
    ("2026-09-20T23:59:00.000+09:00", date(2026, 9, 20), True),   # D-0 (today)
    ("2026-09-21T18:00:00.000+09:00", date(2026, 9, 20), True),   # D-1 (tomorrow)
    ("2026-09-22T23:59:00.000+09:00", date(2026, 9, 20), True),   # D-2
    ("2026-09-23T23:59:00.000+09:00", date(2026, 9, 20), True),   # D-3 (boundary: 3 days)
    ("2026-09-24T00:00:00.000+09:00", date(2026, 9, 20), False),  # D-4 (outside window)
    ("2026-10-10T23:59:00.000+09:00", date(2026, 9, 20), False),  # Far future
    ("2026-09-19T23:59:00.000+09:00", date(2026, 9, 20), False),  # Already passed
    (None, date(2026, 9, 20), False),                              # Missing deadline
    ("invalid-date", date(2026, 9, 20), False),                    # Unparseable deadline
])
def test_urgent_marking_window_logic(end_time, today, expected_urgent):
    assert jr.is_urgent(end_time, today=today, days_window=3) == expected_urgent


def test_urgent_marked_in_rendered_html():
    today = date(2026, 9, 20)
    urgent_p = make_posting(id="urg1", company="급한회사", title="긴급채용", end_time="2026-09-22T18:00:00.000+09:00")
    relaxed_p = make_posting(id="rel1", company="여유회사", title="상시채용", end_time="2026-10-15T23:59:00.000+09:00")

    html_out = jr.render_html([urgent_p, relaxed_p], today=today)

    # In calendar: urgent item has 'cal-item urgent' class
    assert "cal-item urgent" in html_out
    assert "급한회사" in html_out

    # In table: urgent row has 'urgent-row' class and pill
    assert "urgent-row" in html_out
    assert "🚨 D-2" in html_out

    # Relaxed posting row should not have urgent class
    assert "🚨 D-" not in html_out.split("여유회사")[0].split("<tr>")[-1]


# ── 3. HTML escaping of hostile strings ─────────────────────────────────────

def test_html_escaping_hostile_strings():
    today = date(2026, 9, 20)
    hostile = make_posting(
        company="<script>alert('xss-co')</script>",
        title="수석 엔지니어 <img src=x onerror=alert(1)> & \"quotes\"",
        sub_positions=["<b onmouseover='alert(2)'>해킹파트</b>", "정상파트 & <tag>"],
        track="core",
        score=30,
        url="https://jasoseol.com/recruit/999?q=<test>&evil=\"injection\"",
        apply_url="https://apply.com/job?a=1&b=2\" onfocus=\"alert(3)",
    )

    out = jr.render_html([hostile], today=today)

    # Raw script or img tags MUST NOT appear unescaped
    assert "<script>" not in out
    assert "</script>" not in out
    assert "<img src=x" not in out
    assert "<b onmouseover" not in out

    # Properly escaped versions must be present
    assert "&lt;script&gt;alert(&#x27;xss-co&#x27;)&lt;/script&gt;" in out
    assert "&lt;img src=x onerror=alert(1)&gt;" in out
    assert "&amp; &quot;quotes&quot;" in out
    assert "&lt;b onmouseover=&#x27;alert(2)&#x27;&gt;해킹파트&lt;/b&gt;" in out
    assert "&lt;tag&gt;" in out

    # URLs must be quoted/escaped in href attributes
    assert "&amp;evil=&quot;injection&quot;" in out
    assert "&amp;b=2&quot; onfocus=&quot;alert(3)" in out


# ── 4. Sorting by deadline ──────────────────────────────────────────────────

def test_sorting_by_deadline():
    p_nov = make_posting(id="nov", company="C_Nov", end_time="2026-11-01T23:59:00.000+09:00")
    p_sep_early = make_posting(id="sep_e", company="A_Early", end_time="2026-09-22T12:00:00.000+09:00")
    p_sep_late = make_posting(id="sep_l", company="B_Late", end_time="2026-09-22T18:00:00.000+09:00")
    p_oct = make_posting(id="oct", company="D_Oct", end_time="2026-10-10T00:00:00.000+09:00")
    p_no_dl = make_posting(id="none", company="E_None", end_time=None)

    sorted_list = jr.sort_by_deadline([p_nov, p_no_dl, p_sep_late, p_oct, p_sep_early])
    sorted_ids = [p["id"] for p in sorted_list]

    # Earlier deadline first; same day earlier time first; missing deadline last
    assert sorted_ids == ["sep_e", "sep_l", "oct", "nov", "none"]


def test_table_renders_rows_sorted_by_deadline():
    today = date(2026, 9, 20)
    p_late = make_posting(id="late", company="늦은회사", end_time="2026-10-20T00:00:00.000+09:00")
    p_early = make_posting(id="early", company="이른회사", end_time="2026-09-22T00:00:00.000+09:00")

    out = jr.render_html([p_late, p_early], today=today)

    early_idx = out.find("이른회사")
    late_idx = out.find("늦은회사")
    assert early_idx != -1 and late_idx != -1
    assert early_idx < late_idx, "Early deadline must appear before late deadline in table"


# ── 5. Ops notification modes ───────────────────────────────────────────────

def capture_notify(monkeypatch):
    calls = []

    def fake(text, **kwargs):
        calls.append((text, kwargs))
        return True

    monkeypatch.setattr(jr, "notify_send", fake)
    return calls


def test_empty_inbox_notifies_a_plain_message_without_html(tmp_path, monkeypatch):
    empty_inbox = tmp_path / "empty_inbox"
    empty_inbox.mkdir()
    report_dir = tmp_path / "report"
    calls = capture_notify(monkeypatch)

    exit_code = jr.main([
        "--inbox-dir", str(empty_inbox), "--report-dir", str(report_dir), "--telegram",
    ])

    assert exit_code == 0
    assert len(calls) == 1
    text, kwargs = calls[0]
    assert "오늘은 새로운 추천 공고가 없습니다." in text
    assert "경력 공고 0건을 검토했고 0건을 필터링했습니다." in text
    assert kwargs.get("title") == "portfolio jasoseol"
    assert not report_dir.exists()


def test_empty_inbox_message_includes_examined_and_filtered_counts(tmp_path, monkeypatch):
    inbox = tmp_path / "rejected_inbox"
    inbox.mkdir()
    calls = capture_notify(monkeypatch)

    for posting_id in ("101", "102"):
        (inbox / f"{posting_id}.md").write_text(
            """---
id: %s
company: 탈락회사
title: 무관직무
score: 12
verdict: rejected
actionable: false
career_type: 경력
---
# 탈락공고
""" % posting_id,
            encoding="utf-8",
        )

    exit_code = jr.main(["--inbox-dir", str(inbox), "--telegram"])

    assert exit_code == 0
    assert len(calls) == 1
    assert "경력 공고 2건을 검토했고 2건을 필터링했습니다." in calls[0][0]


def test_non_empty_telegram_run_notifies_caption_and_writes_html(tmp_path, monkeypatch):
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    report_dir = tmp_path / "report"
    calls = capture_notify(monkeypatch)
    (inbox / "101.md").write_text(
        """---
id: 101
company: 추천회사
title: 임베디드 엔지니어
score: 30
verdict: actionable
actionable: true
career_type: 경력
scoring_version: 2
end_time: 2026-09-25T23:59:00.000+09:00
---
""",
        encoding="utf-8",
    )

    exit_code = jr.main([
        "--inbox-dir", str(inbox), "--report-dir", str(report_dir),
        "--telegram", "--date", "2026-09-25",
    ])

    assert exit_code == 0
    assert len(calls) == 1
    text, kwargs = calls[0]
    assert kwargs.get("title") == "portfolio jasoseol"
    assert "추천 공고" in text
    report = next(report_dir.glob("jasoseol-*.html"))
    assert report.name in text


def test_dry_run_does_not_notify(tmp_path, monkeypatch):
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    calls = capture_notify(monkeypatch)
    (inbox / "101.md").write_text(
        """---
id: 101
company: 추천회사
title: 임베디드 엔지니어
score: 30
verdict: actionable
actionable: true
career_type: 경력
scoring_version: 2
end_time: 2026-09-25T23:59:00.000+09:00
---
""",
        encoding="utf-8",
    )
    jr.main(["--inbox-dir", str(inbox), "--report-dir", str(tmp_path / "r"),
             "--telegram", "--dry-run", "--date", "2026-09-25"])
    assert calls == []


# ── 6. Caption counts ───────────────────────────────────────────────────────

def test_caption_counts_actionable_and_urgent():
    today = date(2026, 9, 20)
    p1 = make_posting(id="1", company="기업A", title="직무1", end_time="2026-09-21T18:00:00.000+09:00")  # Urgent (D-1)
    p2 = make_posting(id="2", company="기업B", title="직무2", end_time="2026-09-22T23:59:00.000+09:00")  # Urgent (D-2)
    p3 = make_posting(id="3", company="기업C", title="직무3", end_time="2026-10-05T23:59:00.000+09:00")  # Relaxed
    p4 = make_posting(id="4", company="기업D", title="직무4", end_time="2026-10-12T23:59:00.000+09:00")  # Relaxed

    caption = jr.make_caption([p1, p2, p3, p4], today=today)

    assert "추천 공고: 4건" in caption
    assert "긴급 마감(3일 이내): 2건" in caption
    assert "• 기업A" in caption
    assert "• 기업B" in caption
    assert "🚨 D-1" in caption
    assert "🚨 D-2" in caption


def test_caption_zero_urgent():
    today = date(2026, 9, 20)
    p1 = make_posting(id="1", company="기업A", title="직무1", end_time="2026-10-20T18:00:00.000+09:00")
    caption = jr.make_caption([p1], today=today)

    assert "추천 공고: 1건" in caption
    assert "긴급 마감(3일 이내): 0건" in caption
    assert "🚨" not in caption


# ── 7. Shortlist threshold filtering ────────────────────────────────────────

def test_load_postings_filters_by_threshold(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    # Actionable with score >= 26
    (inbox / "1.md").write_text(
        "---\n"
        "id: 1\n"
        "company: 합격사\n"
        "title: 모터제어\n"
        "score: 28\n"
        "verdict: actionable\n"
        "actionable: true\n"
        "scoring_version: 2\n"
        "---\n",
        encoding="utf-8",
    )
    # Actionable with score 26 (boundary)
    (inbox / "2.md").write_text(
        "---\n"
        "id: 2\n"
        "company: 경계사\n"
        "title: 전력전자\n"
        "score: 26\n"
        "verdict: actionable\n"
        "actionable: true\n"
        "scoring_version: 2\n"
        "---\n",
        encoding="utf-8",
    )
    # Low score below threshold (20) without actionable verdict
    (inbox / "3.md").write_text(
        "---\n"
        "id: 3\n"
        "company: 저점사\n"
        "title: 일반영업\n"
        "score: 18\n"
        "verdict: low-score\n"
        "actionable: false\n"
        "scoring_version: 2\n"
        "---\n",
        encoding="utf-8",
    )
    # Explicit rejected verdict
    (inbox / "4.md").write_text(
        "---\n"
        "id: 4\n"
        "company: 탈락사\n"
        "title: 경비직\n"
        "score: 30\n"
        "verdict: rejected\n"
        "actionable: false\n"
        "scoring_version: 2\n"
        "---\n",
        encoding="utf-8",
    )

    loaded = jr.load_postings(inbox, min_score=26)
    loaded_ids = {p["id"] for p in loaded}

    assert loaded_ids == {"1", "2"}


# ── 8. Live inbox and CLI integration ───────────────────────────────────────

def test_live_inbox_loads_and_renders():
    postings = jr.load_postings(jr.DEFAULT_INBOX_DIR)
    assert len(postings) >= 5, "Expected at least 5 actionable postings collected in Part 1"
    for p in postings:
        assert p["company"], f"Missing company in {p['id']}"
        assert p["title"], f"Missing title in {p['id']}"
        assert p["score"] >= 28, f"Posting {p['id']} score {p['score']} below threshold"

    html_out = jr.render_html(postings, today=date(2026, 9, 20))
    assert "<!doctype html>" in html_out
    assert "마감 캘린더" in html_out
    assert "추천 공고 목록" in html_out
    assert "현대모비스" in html_out
    assert "한국법무보호복지공단" not in html_out


def test_cli_html_and_dry_run(tmp_path):
    out_file = tmp_path / "test_report.html"
    ret = jr.main(["--output", str(out_file), "--dry-run"])
    assert ret == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "<!doctype html>" in content


# ── 9. New scoring version, demotion, and deadline filtering ─────────────────

def test_stale_record_with_old_scoring_version_is_skipped(tmp_path, capsys):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    # Posting with old scoring version (v1)
    (inbox / "101.md").write_text(
        "---\n"
        "id: 101\n"
        "company: 과거기업\n"
        "title: 과거직무\n"
        "score: 30\n"
        "verdict: actionable\n"
        "actionable: true\n"
        "scoring_version: 1\n"
        "---\n",
        encoding="utf-8",
    )
    # Posting with missing scoring version
    (inbox / "102.md").write_text(
        "---\n"
        "id: 102\n"
        "company: 구버전기업\n"
        "title: 구버전직무\n"
        "score: 30\n"
        "verdict: actionable\n"
        "actionable: true\n"
        "---\n",
        encoding="utf-8",
    )
    # Posting with current scoring version (v2)
    (inbox / "103.md").write_text(
        "---\n"
        "id: 103\n"
        "company: 현재기업\n"
        "title: 현재직무\n"
        "score: 30\n"
        "verdict: actionable\n"
        "actionable: true\n"
        "scoring_version: 2\n"
        "---\n",
        encoding="utf-8",
    )

    loaded = jr.load_postings(inbox, min_score=28)
    loaded_ids = {p["id"] for p in loaded}

    assert loaded_ids == {"103"}
    out = capsys.readouterr().out
    assert "WARNING: skipped 2 posting(s) evaluated under older scoring version" in out


def test_posting_demoted_below_threshold_is_excluded(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    # Posting demoted below threshold
    (inbox / "106243.md").write_text(
        "---\n"
        "id: 106243\n"
        "company: 한국법무보호복지공단\n"
        "title: 취업지원직\n"
        "score: 0\n"
        "verdict: not_actionable\n"
        "actionable: false\n"
        "scoring_version: 2\n"
        "dropped_out: 2026-09-20\n"
        "---\n",
        encoding="utf-8",
    )
    # Actionable posting
    (inbox / "106170.md").write_text(
        "---\n"
        "id: 106170\n"
        "company: 현대모비스\n"
        "title: 로보틱스\n"
        "score: 86\n"
        "verdict: actionable\n"
        "actionable: true\n"
        "scoring_version: 2\n"
        "---\n",
        encoding="utf-8",
    )

    loaded = jr.load_postings(inbox, min_score=28)
    loaded_ids = {p["id"] for p in loaded}

    assert loaded_ids == {"106170"}
    assert "106243" not in loaded_ids


def test_posting_whose_deadline_has_passed_is_excluded(tmp_path, capsys):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    today = date(2026, 9, 20)
    # Posting with deadline in the past
    (inbox / "201.md").write_text(
        "---\n"
        "id: 201\n"
        "company: 마감완료기업\n"
        "title: 마감직무\n"
        "score: 30\n"
        "verdict: actionable\n"
        "actionable: true\n"
        "scoring_version: 2\n"
        "end_time: 2026-09-19T23:59:00.000+09:00\n"
        "---\n",
        encoding="utf-8",
    )
    # Posting with future deadline
    (inbox / "202.md").write_text(
        "---\n"
        "id: 202\n"
        "company: 진행중기업\n"
        "title: 진행직무\n"
        "score: 30\n"
        "verdict: actionable\n"
        "actionable: true\n"
        "scoring_version: 2\n"
        "end_time: 2026-09-25T23:59:00.000+09:00\n"
        "---\n",
        encoding="utf-8",
    )

    loaded = jr.load_postings(inbox, min_score=28, today=today)
    loaded_ids = {p["id"] for p in loaded}

    assert loaded_ids == {"202"}
    assert "201" not in loaded_ids
    out = capsys.readouterr().out
    assert "skipped 1 posting(s) whose deadline has already passed" in out
