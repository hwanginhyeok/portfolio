"""Tests for Jasoseol recruitment deadline calendar sync (scripts/jasoseol_calendar.py)."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

import scripts.jasoseol_calendar as jcal


def _write_posting_md(
    inbox_dir: Path,
    pid: str | int,
    *,
    company: str,
    title: str,
    end_time: str,
    score: int = 86,
    verdict: str = "actionable",
    actionable: bool = True,
    sub_positions: list[str] | None = None,
    matched_sub_positions: list[str] | None = None,
    track: str = "ai-native",
    scoring_version: int = 2,
    threshold: int = 28,
    url: str | None = None,
    apply_url: str | None = None,
) -> Path:
    subs = sub_positions or ["연구직_로보틱스 모터 설계(경력)"]
    matched = matched_sub_positions or ["연구직_로보틱스 모터 설계(경력)"]
    post_url = url or f"https://jasoseol.com/recruit/{pid}"
    app_url = apply_url or "https://apply.example.com/job"

    content = f"""---
id: {pid}
company: "{company}"
title: "{title}"
track: "{track}"
score: {score}
verdict: "{verdict}"
actionable: {str(actionable).lower()}
career_type: "경력"
start_time: "2026-09-01T09:00:00.000+09:00"
end_time: "{end_time}"
url: "{post_url}"
apply_url: "{app_url}"
sub_positions: {json.dumps(subs, ensure_ascii=False)}
matched_sub_positions: {json.dumps(matched, ensure_ascii=False)}
scoring_version: {scoring_version}
threshold: {threshold}
---

# {title} — {company}
"""
    file_path = inbox_dir / f"{pid}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_all_day_versus_timed_event_decision():
    """Verify timing computation: 23:59 -> all-day, clock time -> 30m timed."""
    # 1. End time at 23:59:00 -> all-day event
    t_allday = jcal.compute_event_timing("2026-09-20T23:59:00.000+09:00")
    assert t_allday["is_all_day"] is True
    assert t_allday["start_date"] == "2026-09-20"
    assert t_allday["end_date"] == "2026-09-20"

    args_allday = jcal.build_add_cli_args(
        account="personal",
        title="마감 · 현대로템 생산기지 시스템 설계 총괄",
        timing=t_allday,
        description="test",
        apply=True,
    )
    assert "--start-date" in args_allday
    assert "2026-09-20" in args_allday
    assert "--end-date" in args_allday
    assert "--start" not in args_allday

    # 2. End time at 10:00:00 -> 30-minute timed event ending at 10:00
    t_timed = jcal.compute_event_timing("2026-09-29T10:00:00.000+09:00")
    assert t_timed["is_all_day"] is False
    assert t_timed["start"] == "2026-09-29T09:30:00+09:00"
    assert t_timed["end"] == "2026-09-29T10:00:00+09:00"

    args_timed = jcal.build_add_cli_args(
        account="personal",
        title="마감 · 현대모비스 로보틱스 모터 설계(경력)",
        timing=t_timed,
        description="test",
        apply=True,
    )
    assert "--start" in args_timed
    assert "2026-09-29T09:30:00+09:00" in args_timed
    assert "--end" in args_timed
    assert "2026-09-29T10:00:00+09:00" in args_timed
    assert "--start-date" not in args_timed

    # 3. End time at 17:00:00 -> 30-minute timed event ending at 17:00
    t_timed2 = jcal.compute_event_timing("2026-09-28T17:00:00.000+09:00")
    assert t_timed2["is_all_day"] is False
    assert t_timed2["start"] == "2026-09-28T16:30:00+09:00"
    assert t_timed2["end"] == "2026-09-28T17:00:00+09:00"

    # 4. Date-only string -> all-day event
    t_dateonly = jcal.compute_event_timing("2026-10-05")
    assert t_dateonly["is_all_day"] is True
    assert t_dateonly["start_date"] == "2026-10-05"
    assert t_dateonly["end_date"] == "2026-10-05"


def test_stable_marker_and_ledger_preventing_duplicates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Verify stable marker generation and ledger idempotence preventing duplicate event creation."""
    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    ledger_path = inbox_dir / "calendar_events.json"

    _write_posting_md(
        inbox_dir,
        "106170",
        company="현대모비스",
        title="2026 하반기 로보틱스 집중 채용",
        end_time="2026-09-29T10:00:00.000+09:00",
        matched_sub_positions=[
            "연구직_로보틱스 모터 설계(넥스트 탤런트)",
            "연구직_로보틱스 모터 설계(경력)",
        ],
    )

    cli_calls: list[list[str]] = []

    def fake_run_schedule_cli(args: list[str], cli_path: Path = jcal.DEFAULT_SCHEDULE_CLI) -> dict[str, Any]:
        cli_calls.append(args)
        if args[0] == "add":
            return {
                "account": "personal",
                "status": "created",
                "event": {
                    "id": "cal_evt_106170",
                    "summary": args[args.index("--title") + 1],
                },
            }
        raise AssertionError(f"Unexpected CLI invocation: {args}")

    monkeypatch.setattr(jcal, "run_schedule_cli", fake_run_schedule_cli)

    # First run with --apply
    postings = jcal.load_postings(inbox_dir, today="2026-09-20")
    assert len(postings) == 1
    ledger = jcal.load_ledger(ledger_path)
    plan = jcal.plan_calendar_sync(postings, ledger, inbox_dir)
    assert len(plan["create"]) == 1
    assert plan["create"][0]["marker"] == "jasoseol:106170"
    assert "[jasoseol:106170]" in plan["create"][0]["description"]

    result1 = jcal.execute_sync(plan, ledger, ledger_path, apply=True)
    assert result1["created"] == 1
    assert result1["created_event_ids"] == ["cal_evt_106170"]
    assert len(cli_calls) == 1
    assert cli_calls[0][0] == "add"
    assert "--apply" in cli_calls[0]

    # Verify ledger was written
    saved_ledger = jcal.load_ledger(ledger_path)
    assert "106170" in saved_ledger
    assert saved_ledger["106170"]["event_id"] == "cal_evt_106170"
    assert saved_ledger["106170"]["marker"] == "jasoseol:106170"

    # Second run with --apply (must be idempotent: 0 created, 0 CLI calls)
    cli_calls.clear()
    postings2 = jcal.load_postings(inbox_dir, today="2026-09-20")
    plan2 = jcal.plan_calendar_sync(postings2, saved_ledger, inbox_dir)
    assert len(plan2["create"]) == 0
    assert len(plan2["update"]) == 0
    assert len(plan2["delete"]) == 0
    assert plan2["untouched"] == ["106170"]

    result2 = jcal.execute_sync(plan2, saved_ledger, ledger_path, apply=True)
    assert result2["created"] == 0
    assert result2["updated"] == 0
    assert result2["deleted"] == 0
    assert len(cli_calls) == 0  # No calendar API called!


def test_moved_deadline_updating_rather_than_duplicating(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Verify that when a posting deadline moves, sync issues an update rather than creating a duplicate."""
    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    ledger_path = inbox_dir / "calendar_events.json"

    # Initial posting and ledger with deadline at 2026-09-29T10:00:00
    initial_end = "2026-09-29T10:00:00.000+09:00"
    _write_posting_md(
        inbox_dir,
        "106170",
        company="현대모비스",
        title="2026 하반기 로보틱스 집중 채용",
        end_time=initial_end,
    )
    initial_ledger = {
        "106170": {
            "event_id": "cal_evt_106170",
            "end_time": initial_end,
            "title": "마감 · 현대모비스 로보틱스 모터 설계(경력)",
            "marker": "jasoseol:106170",
        }
    }
    jcal.save_ledger(initial_ledger, ledger_path)

    # Now deadline moves to 2026-09-30T15:00:00
    new_end = "2026-09-30T15:00:00.000+09:00"
    _write_posting_md(
        inbox_dir,
        "106170",
        company="현대모비스",
        title="2026 하반기 로보틱스 집중 채용",
        end_time=new_end,
    )

    cli_calls: list[list[str]] = []

    def fake_run_schedule_cli(args: list[str], cli_path: Path = jcal.DEFAULT_SCHEDULE_CLI) -> dict[str, Any]:
        cli_calls.append(args)
        if args[0] == "update":
            return {
                "account": "personal",
                "status": "updated",
                "event": {
                    "id": args[args.index("--event-id") + 1],
                },
            }
        raise AssertionError(f"Expected update, got: {args}")

    monkeypatch.setattr(jcal, "run_schedule_cli", fake_run_schedule_cli)

    postings = jcal.load_postings(inbox_dir, today="2026-09-20")
    plan = jcal.plan_calendar_sync(postings, initial_ledger, inbox_dir)
    assert len(plan["create"]) == 0
    assert len(plan["update"]) == 1
    assert plan["update"][0]["id"] == "106170"
    assert plan["update"][0]["event_id"] == "cal_evt_106170"
    assert plan["update"][0]["old_end_time"] == initial_end
    assert plan["update"][0]["new_end_time"] == new_end

    result = jcal.execute_sync(plan, initial_ledger, ledger_path, apply=True)
    assert result["updated"] == 1
    assert len(cli_calls) == 1
    assert cli_calls[0][0] == "update"
    assert "--event-id" in cli_calls[0]
    assert "cal_evt_106170" in cli_calls[0]
    assert "--start" in cli_calls[0]
    assert "2026-09-30T14:30:00+09:00" in cli_calls[0]
    assert "2026-09-30T15:00:00+09:00" in cli_calls[0]

    # Verify ledger updated with the new deadline
    updated_ledger = jcal.load_ledger(ledger_path)
    assert updated_ledger["106170"]["end_time"] == new_end


def test_demoted_posting_removes_event(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Verify that an event whose posting was demoted or excluded is removed from the calendar and ledger."""
    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    ledger_path = inbox_dir / "calendar_events.json"

    # Pre-existing event in ledger
    existing_ledger = {
        "106063": {
            "event_id": "cal_evt_106063",
            "end_time": "2026-09-20T23:59:00.000+09:00",
            "title": "마감 · TKG태광 품질 (QA)",
            "marker": "jasoseol:106063",
        }
    }
    jcal.save_ledger(existing_ledger, ledger_path)

    # The posting has been demoted (e.g. verdict is now rejected, score 15 < 28)
    _write_posting_md(
        inbox_dir,
        "106063",
        company="TKG태광",
        title="2026년 3분기 수시채용",
        end_time="2026-09-20T23:59:00.000+09:00",
        score=15,
        verdict="rejected",
        actionable=False,
    )

    cli_calls: list[list[str]] = []

    def fake_run_schedule_cli(args: list[str], cli_path: Path = jcal.DEFAULT_SCHEDULE_CLI) -> dict[str, Any]:
        cli_calls.append(args)
        if args[0] == "delete":
            return {
                "account": "personal",
                "status": "deleted",
                "eventId": args[args.index("--event-id") + 1],
            }
        raise AssertionError(f"Expected delete, got: {args}")

    monkeypatch.setattr(jcal, "run_schedule_cli", fake_run_schedule_cli)

    postings = jcal.load_postings(inbox_dir, today="2026-09-20")
    assert len(postings) == 0  # Demoted posting is not actionable

    plan = jcal.plan_calendar_sync(postings, existing_ledger, inbox_dir)
    assert len(plan["create"]) == 0
    assert len(plan["update"]) == 0
    assert len(plan["delete"]) == 1
    assert plan["delete"][0]["id"] == "106063"
    assert plan["delete"][0]["event_id"] == "cal_evt_106063"

    result = jcal.execute_sync(plan, existing_ledger, ledger_path, apply=True)
    assert result["deleted"] == 1
    assert len(cli_calls) == 1
    assert cli_calls[0][0] == "delete"
    assert "--confirm-delete" in cli_calls[0]
    assert "cal_evt_106063" in cli_calls[0]

    # Verify event removed from ledger
    updated_ledger = jcal.load_ledger(ledger_path)
    assert "106063" not in updated_ledger


def test_past_deadline_never_created(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Verify that postings whose deadlines have passed are never created."""
    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    ledger_path = inbox_dir / "calendar_events.json"

    # Posting with deadline in the past relative to today=2026-09-20
    _write_posting_md(
        inbox_dir,
        "105001",
        company="과거기업",
        title="과거 채용 공고",
        end_time="2026-09-10T18:00:00.000+09:00",
        score=90,
        verdict="actionable",
        actionable=True,
    )

    cli_calls: list[list[str]] = []

    def fake_run_schedule_cli(args: list[str], cli_path: Path = jcal.DEFAULT_SCHEDULE_CLI) -> dict[str, Any]:
        cli_calls.append(args)
        return {}

    monkeypatch.setattr(jcal, "run_schedule_cli", fake_run_schedule_cli)

    postings = jcal.load_postings(inbox_dir, today="2026-09-20")
    assert len(postings) == 0  # Skipped because deadline passed

    plan = jcal.plan_calendar_sync(postings, {}, inbox_dir)
    assert len(plan["create"]) == 0
    assert len(plan["update"]) == 0
    assert len(plan["delete"]) == 0

    result = jcal.execute_sync(plan, {}, ledger_path, apply=True)
    assert result["created"] == 0
    assert len(cli_calls) == 0


def test_role_hint_and_event_shape():
    """Verify role hint extraction and event title/description format."""
    posting = {
        "id": "106170",
        "company": "현대모비스",
        "title": "2026 하반기 로보틱스 집중 채용",
        "track": "ai-native",
        "score": 86,
        "url": "https://jasoseol.com/recruit/106170",
        "apply_url": "https://mobisrobotics-recruit.com/",
    }
    fm = {
        "matched_sub_positions": [
            "연구직_로보틱스 모터 설계(넥스트 탤런트)",
            "연구직_로보틱스 모터 설계(경력)",
            "연구직_로봇 핸즈 SW 설계(경력)",
        ]
    }

    hint = jcal.extract_role_hint(posting, fm)
    assert hint == "로보틱스 모터 설계(경력)"

    title = jcal.build_event_title("현대모비스", hint)
    assert title == "마감 · 현대모비스 로보틱스 모터 설계(경력)"

    desc = jcal.build_event_description(posting, fm)
    assert "https://jasoseol.com/recruit/106170" in desc
    assert "https://mobisrobotics-recruit.com/" in desc
    assert "연구직_로보틱스 모터 설계(경력)" in desc
    assert "Track: ai-native" in desc
    assert "점수: 86" in desc
    assert "[jasoseol:106170]" in desc


def test_dry_run_does_not_call_cli_or_modify_ledger(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Verify that --dry-run prints plan without calling calendar CLI or creating ledger."""
    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    ledger_path = inbox_dir / "calendar_events.json"

    _write_posting_md(
        inbox_dir,
        "106170",
        company="현대모비스",
        title="2026 하반기 로보틱스 집중 채용",
        end_time="2026-09-29T10:00:00.000+09:00",
    )

    cli_calls: list[list[str]] = []

    def fake_run_schedule_cli(args: list[str], cli_path: Path = jcal.DEFAULT_SCHEDULE_CLI) -> dict[str, Any]:
        cli_calls.append(args)
        return {}

    monkeypatch.setattr(jcal, "run_schedule_cli", fake_run_schedule_cli)

    postings = jcal.load_postings(inbox_dir, today="2026-09-20")
    ledger = jcal.load_ledger(ledger_path)
    plan = jcal.plan_calendar_sync(postings, ledger, inbox_dir)
    assert len(plan["create"]) == 1

    # Run with apply=False (dry-run)
    result = jcal.execute_sync(plan, ledger, ledger_path, apply=False)
    assert result["status"] == "dry-run"
    assert len(cli_calls) == 0
    assert not ledger_path.exists()


def test_orphan_marker_sweep_deletes_only_unknown_marked_events(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Marked events absent from the ledger are deleted; unmarked operator events survive."""
    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    ledger_path = inbox_dir / "calendar_events.json"
    calendar_events = [
        {
            "id": "orphan-event",
            "summary": "마감 · 삭제된 공고",
            "description": "- 공고 링크: https://jasoseol.com/recruit/999999\n[jasoseol:999999]",
        },
        {
            "id": "operator-event",
            "summary": "운영자 개인 일정",
            "description": "채용과 무관한 개인 메모",
        },
    ]

    plan = jcal.plan_calendar_sync([], {}, inbox_dir, calendar_events=calendar_events)
    assert len(plan["delete"]) == 1
    assert plan["orphan_delete"] == [
        {
            "id": "999999",
            "event_id": "orphan-event",
            "title": "마감 · 삭제된 공고",
            "marker": "jasoseol:999999",
            "reason": "orphan_marker",
        }
    ]
    assert all(item["event_id"] != "operator-event" for item in plan["delete"])

    cli_calls: list[list[str]] = []

    def fake_run_schedule_cli(args: list[str], cli_path: Path = jcal.DEFAULT_SCHEDULE_CLI) -> dict[str, Any]:
        cli_calls.append(args)
        if args[0] == "delete":
            return {"status": "deleted", "eventId": "orphan-event"}
        raise AssertionError(f"Unexpected CLI invocation: {args}")

    monkeypatch.setattr(jcal, "run_schedule_cli", fake_run_schedule_cli)

    dry_run_result = jcal.execute_sync(plan, {}, ledger_path, apply=False)
    assert dry_run_result["orphan_deleted"] == 0
    assert cli_calls == []

    apply_result = jcal.execute_sync(plan, {}, ledger_path, apply=True)
    assert apply_result["deleted"] == 1
    assert apply_result["orphan_deleted"] == 1
    assert len(cli_calls) == 1
    assert cli_calls[0][0] == "delete"
    assert "orphan-event" in cli_calls[0]
    assert "operator-event" not in cli_calls[0]


def test_orphan_sweep_lists_calendar_window_in_dry_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Dry-run performs the read-only list sweep but never calls delete."""
    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    ledger_path = inbox_dir / "calendar_events.json"
    cli_calls: list[list[str]] = []

    def fake_run_schedule_cli(args: list[str], cli_path: Path = jcal.DEFAULT_SCHEDULE_CLI) -> dict[str, Any]:
        cli_calls.append(args)
        if args[0] == "list":
            return {"events": []}
        raise AssertionError(f"Dry-run must not mutate the calendar: {args}")

    monkeypatch.setattr(jcal, "run_schedule_cli", fake_run_schedule_cli)

    assert jcal.main([
        "--dry-run",
        "--today", "2026-09-20",
        "--inbox", str(inbox_dir),
        "--ledger", str(ledger_path),
    ]) == 0

    assert len(cli_calls) == 1
    assert cli_calls[0][:5] == [
        "list", "--account", "personal", "--from", "2026-08-21",
    ]
    assert cli_calls[0][-2:] == ["--to", "2027-09-20"]


def test_run_schedule_cli_execs_the_cli_directly(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout='{"events": []}', stderr="")

    monkeypatch.setattr(jcal.subprocess, "run", fake_run)
    cli = tmp_path / "hih-schedule"
    result = jcal.run_schedule_cli(["list", "--account", "personal"], cli_path=cli)

    assert result == {"events": []}
    assert calls[0][0] == str(cli)
    assert calls[0][1:] == ["list", "--account", "personal"]


def test_run_schedule_cli_raises_on_failure(monkeypatch, tmp_path):
    def fake_run(cmd, **kwargs):
        return SimpleNamespace(returncode=2, stdout="", stderr="boom")

    monkeypatch.setattr(jcal.subprocess, "run", fake_run)
    with pytest.raises(RuntimeError, match="boom"):
        jcal.run_schedule_cli(["list"], cli_path=tmp_path / "hih-schedule")


def test_default_schedule_cli_is_a_mac_path():
    assert str(jcal.DEFAULT_SCHEDULE_CLI).startswith("/")
    assert "window11" not in str(jcal.DEFAULT_SCHEDULE_CLI)
