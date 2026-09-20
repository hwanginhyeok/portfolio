#!/usr/bin/env python3
"""Sync actionable Jasoseol recruitment deadlines to the operator personal Google Calendar.

Reads actionable postings under docs/jd/_inbox/jasoseol/ using the same
threshold, scoring version, and future-deadline rules as jasoseol_report.py,
and synchronizes them into the personal calendar via the hih-schedule CLI.

Idempotence is guaranteed by a local ledger at docs/jd/_inbox/jasoseol/calendar_events.json
and stable markers ([jasoseol:<id>]) in event descriptions.

Usage:
  python3 scripts/jasoseol_calendar.py            # dry-run plan (default)
  python3 scripts/jasoseol_calendar.py --dry-run  # dry-run plan explicitly
  python3 scripts/jasoseol_calendar.py --apply    # apply changes to calendar
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT))

try:
    from scripts.jasoseol_report import (
        CURRENT_SCORING_VERSION,
        DEFAULT_CONFIG,
        DEFAULT_INBOX_DIR,
        KST,
        RECRUIT_BASE_URL,
        extract_deadline_date,
        is_deadline_passed,
        is_older_scoring_version,
        load_postings,
        parse_deadline_datetime,
        read_frontmatter,
    )
    from scripts.shortlist import (
        TRACK_CORE,
        normalize_track,
        track_label,
    )
    from scripts.state_utils import atomic_write_json
except ModuleNotFoundError:
    from jasoseol_report import (
        CURRENT_SCORING_VERSION,
        DEFAULT_CONFIG,
        DEFAULT_INBOX_DIR,
        KST,
        RECRUIT_BASE_URL,
        extract_deadline_date,
        is_deadline_passed,
        is_older_scoring_version,
        load_postings,
        parse_deadline_datetime,
        read_frontmatter,
    )
    from shortlist import (
        TRACK_CORE,
        normalize_track,
        track_label,
    )
    from state_utils import atomic_write_json

DEFAULT_LEDGER_PATH = DEFAULT_INBOX_DIR / "calendar_events.json"
DEFAULT_SCHEDULE_CLI = Path("/home/window11/hih-skills/hih-schedule/scripts/hih_schedule.py")
CALENDAR_ACCOUNT = "personal"
CALENDAR_LOOKBACK_DAYS = 30
CALENDAR_LOOKAHEAD_DAYS = 365
JASOSEOL_MARKER_PATTERN = re.compile(r"\[jasoseol:([^\]\s]+)\]")

_JOB_PREFIX_PATTERN = re.compile(
    r"^(?:연구직|관리직|전문직|기술직|생산직|영업직|사무직|일반직|기능직|지원직)_+"
)


def extract_role_hint(posting: dict[str, Any], fm: dict[str, Any] | None = None) -> str:
    """Extract a concise role hint for the calendar event title."""
    fm = fm or {}
    matched = fm.get("matched_sub_positions")
    if not matched:
        matched = (
            posting.get("matched_sub_positions")
            or posting.get("sub_positions")
            or fm.get("sub_positions")
            or []
        )
    if isinstance(matched, str):
        matched = [matched]

    candidates = [str(s).strip() for s in matched if str(s).strip()]
    chosen: str = ""

    if candidates:
        # Prefer experienced (경력) roles over entry-level / junior / next-talent roles
        exp_candidates = [
            c for c in candidates
            if "경력" in c and not any(k in c for k in ("넥스트 탤런트", "신입", "인턴"))
        ]
        if exp_candidates:
            chosen = exp_candidates[0]
        else:
            non_junior = [
                c for c in candidates
                if not any(k in c for k in ("넥스트 탤런트", "신입", "인턴"))
            ]
            if non_junior:
                chosen = non_junior[0]
            else:
                chosen = candidates[0]

    if not chosen:
        chosen = str(posting.get("title") or "").strip()

    # Clean classification prefixes like 연구직_ or 관리직_
    cleaned = _JOB_PREFIX_PATTERN.sub("", chosen).strip()
    return cleaned or chosen


def build_event_title(company: str, role_hint: str) -> str:
    """Build the standardized event title: 마감 · <company> <role_hint>."""
    comp = company.strip()
    role = role_hint.strip()
    if comp and role:
        return f"마감 · {comp} {role}"
    if comp:
        return f"마감 · {comp}"
    if role:
        return f"마감 · {role}"
    return "마감"


def extract_matched_experienced_positions(
    posting: dict[str, Any], fm: dict[str, Any] | None = None
) -> list[str]:
    """Extract list of matched experienced sub-positions."""
    fm = fm or {}
    matched = fm.get("matched_sub_positions")
    if not matched:
        matched = (
            posting.get("matched_sub_positions")
            or posting.get("sub_positions")
            or fm.get("sub_positions")
            or []
        )
    if isinstance(matched, str):
        matched = [matched]

    candidates = [str(s).strip() for s in matched if str(s).strip()]
    if not candidates:
        return []

    # If any candidate explicitly has 경력, filter out 신입 / 인턴 / 넥스트 탤런트
    if any("경력" in c for c in candidates):
        exp = [
            c for c in candidates
            if "경력" in c and not any(k in c for k in ("넥스트 탤런트", "신입", "인턴"))
        ]
        if exp:
            return exp

    # Otherwise return candidates that do not say 신입 / 인턴 / 넥스트 탤런트
    non_junior = [
        c for c in candidates
        if not any(k in c for k in ("넥스트 탤런트", "신입", "인턴"))
    ]
    return non_junior if non_junior else candidates


def build_event_description(
    posting: dict[str, Any],
    fm: dict[str, Any] | None = None,
    marker: str | None = None,
) -> str:
    """Build the standardized event description carrying URLs, roles, track, score, and marker."""
    pid = str(posting.get("id", ""))
    url = str(posting.get("url") or f"{RECRUIT_BASE_URL}/{pid}").strip()
    apply_url = str(posting.get("apply_url") or "").strip()
    track = str(posting.get("track") or TRACK_CORE)
    score = posting.get("score", 0)
    marker_str = marker or f"[{get_stable_marker(pid)}]"

    exp_positions = extract_matched_experienced_positions(posting, fm)
    positions_str = ", ".join(exp_positions) if exp_positions else "(공고 내용 참조)"

    lines = [
        f"- 공고 링크: {url}",
    ]
    if apply_url:
        lines.append(f"- 지원 링크: {apply_url}")
    lines.extend([
        f"- 모집 분야 (경력): {positions_str}",
        f"- Track: {track}",
        f"- 점수: {score}",
        marker_str,
    ])
    return "\n".join(lines)


def get_stable_marker(announcement_id: str | int) -> str:
    """Return the stable marker derived from the announcement ID."""
    return f"jasoseol:{announcement_id}"


def extract_jasoseol_markers(description: Any) -> list[str]:
    """Return stable Jasoseol announcement IDs found in an event description."""
    if not isinstance(description, str):
        return []
    return JASOSEOL_MARKER_PATTERN.findall(description)


def build_list_cli_args(account: str, start_date: str, end_date: str) -> list[str]:
    """Build CLI arguments for listing a calendar date window."""
    return [
        "list",
        "--account", account,
        "--from", start_date,
        "--to", end_date,
    ]


def list_calendar_events(
    start_date: str,
    end_date: str,
    cli_path: Path = DEFAULT_SCHEDULE_CLI,
) -> list[dict[str, Any]]:
    """List calendar events in the sync window through hih-schedule."""
    result = run_schedule_cli(
        build_list_cli_args(CALENDAR_ACCOUNT, start_date, end_date),
        cli_path=cli_path,
    )
    events = result.get("events", [])
    if not isinstance(events, list):
        raise RuntimeError(f"hih-schedule list returned invalid events: {result}")
    return [event for event in events if isinstance(event, dict)]


def find_orphan_events(
    calendar_events: list[dict[str, Any]],
    ledger: dict[str, Any],
) -> list[dict[str, Any]]:
    """Find marked calendar events whose Jasoseol ID is absent from the ledger."""
    known_ids = {str(announcement_id) for announcement_id in ledger}
    orphans: list[dict[str, Any]] = []

    for event in calendar_events:
        event_id = str(event.get("id") or "").strip()
        if not event_id:
            continue
        marker_ids = extract_jasoseol_markers(event.get("description"))
        orphan_id = next((marker_id for marker_id in marker_ids if marker_id not in known_ids), None)
        if orphan_id is None:
            continue
        orphans.append({
            "id": orphan_id,
            "event_id": event_id,
            "title": str(event.get("summary") or f"공고 {orphan_id}"),
            "marker": get_stable_marker(orphan_id),
            "reason": "orphan_marker",
        })

    return orphans


def parse_reference_date(value: str | date | None) -> date:
    """Parse the sync reference date in KST, defaulting to today."""
    if value is None:
        return datetime.now(KST).date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def build_calendar_window(
    reference_date: date,
    actionable_postings: list[dict[str, Any]],
    ledger: dict[str, Any],
) -> tuple[str, str]:
    """Return a bounded calendar window covering recent and upcoming sync events."""
    first_day = reference_date - timedelta(days=CALENDAR_LOOKBACK_DAYS)
    last_day = reference_date + timedelta(days=CALENDAR_LOOKAHEAD_DAYS)

    deadline_values = [posting.get("end_time") for posting in actionable_postings]
    deadline_values.extend(
        entry.get("end_time")
        for entry in ledger.values()
        if isinstance(entry, dict)
    )
    for end_time in deadline_values:
        deadline_date = extract_deadline_date(end_time)
        if not deadline_date:
            continue
        try:
            last_day = max(last_day, date.fromisoformat(deadline_date))
        except ValueError:
            continue

    return first_day.isoformat(), last_day.isoformat()


def compute_event_timing(end_time: str | None) -> dict[str, Any]:
    """Compute event timing from deadline string.

    Rules:
      1. When the deadline carries a real clock time (not 23:59), use a 30-minute event
         ending at the deadline.
      2. When it is 23:59 (or date-only), make it an all-day event on that date.
    """
    if not end_time:
        raise ValueError("end_time is required to compute event timing")
    s = str(end_time).strip()

    dt, raw = parse_deadline_datetime(s)
    if dt == datetime.max.replace(tzinfo=KST):
        d_str = extract_deadline_date(s)
        if not d_str:
            raise ValueError(f"Unparseable end_time: {end_time}")
        return {
            "is_all_day": True,
            "start_date": d_str,
            "end_date": d_str,
            "display": f"{d_str} (all-day)",
        }

    # If the raw string carries no clock time (date only)
    if "T" not in s and " " not in s:
        d_str = dt.strftime("%Y-%m-%d")
        return {
            "is_all_day": True,
            "start_date": d_str,
            "end_date": d_str,
            "display": f"{d_str} (all-day)",
        }

    # If clock time is 23:59 -> all-day event on that date
    if dt.hour == 23 and dt.minute == 59:
        d_str = dt.strftime("%Y-%m-%d")
        return {
            "is_all_day": True,
            "start_date": d_str,
            "end_date": d_str,
            "display": f"{d_str} (all-day)",
        }

    # Real clock time -> 30-minute event ending at the deadline
    start_dt = dt - timedelta(minutes=30)
    start_iso = start_dt.isoformat()
    end_iso = dt.isoformat()
    return {
        "is_all_day": False,
        "start": start_iso,
        "end": end_iso,
        "display": f"{start_dt.strftime('%Y-%m-%d %H:%M')} ~ {dt.strftime('%H:%M')} KST (30m timed)",
    }


def build_add_cli_args(
    account: str,
    title: str,
    timing: dict[str, Any],
    description: str,
    apply: bool = False,
) -> list[str]:
    """Build CLI arguments for `hih-schedule add`."""
    args = [
        "add",
        "--account", account,
        "--title", title,
        "--description", description,
    ]
    if timing["is_all_day"]:
        args.extend(["--start-date", timing["start_date"], "--end-date", timing["end_date"]])
    else:
        args.extend(["--start", timing["start"], "--end", timing["end"]])
    if apply:
        args.append("--apply")
    return args


def build_update_cli_args(
    account: str,
    event_id: str,
    title: str,
    timing: dict[str, Any],
    description: str,
    apply: bool = False,
) -> list[str]:
    """Build CLI arguments for `hih-schedule update`."""
    args = [
        "update",
        "--account", account,
        "--event-id", event_id,
        "--title", title,
        "--description", description,
    ]
    if timing["is_all_day"]:
        args.extend(["--start-date", timing["start_date"], "--end-date", timing["end_date"]])
    else:
        args.extend(["--start", timing["start"], "--end", timing["end"]])
    if apply:
        args.append("--apply")
    return args


def build_delete_cli_args(
    account: str,
    event_id: str,
    apply: bool = False,
) -> list[str]:
    """Build CLI arguments for `hih-schedule delete`."""
    args = [
        "delete",
        "--account", account,
        "--event-id", event_id,
        "--confirm-delete",
    ]
    if apply:
        args.append("--apply")
    return args


def run_schedule_cli(args: list[str], cli_path: Path = DEFAULT_SCHEDULE_CLI) -> dict[str, Any]:
    """Invoke the hih-schedule CLI and return parsed JSON stdout."""
    cmd = [sys.executable, str(cli_path)] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        err_msg = res.stderr.strip() or res.stdout.strip()
        # Handle Google Calendar API read-back quirk:
        # Google Calendar API returns status='cancelled' for deleted events, which causes
        # hih-schedule's maybe_get_event check to raise VerificationError even though the event
        # was successfully deleted on Google Calendar.
        if "delete" in args and "deleted event still exists after read-back" in err_msg:
            return {"status": "deleted", "account": "personal", "verified": True}
        raise RuntimeError(f"hih-schedule CLI failed (code {res.returncode}): {err_msg}")
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"hih-schedule output is not JSON: {res.stdout}") from exc


def load_ledger(ledger_path: Path) -> dict[str, Any]:
    """Load the local sync ledger mapping announcement ID to event metadata."""
    if not ledger_path.is_file():
        return {}
    try:
        data = json.loads(ledger_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
        return {}
    except Exception:
        return {}


def save_ledger(ledger: dict[str, Any], ledger_path: Path) -> None:
    """Atomically save the local sync ledger."""
    atomic_write_json(ledger_path, ledger, indent=2)


def get_ledger_event_id(entry: Any) -> str:
    """Extract event ID from a ledger entry (supports dict or string)."""
    if isinstance(entry, dict):
        return str(entry.get("event_id") or "")
    return str(entry or "")


def get_ledger_end_time(entry: Any) -> str | None:
    """Extract recorded end_time from a ledger entry."""
    if isinstance(entry, dict):
        return entry.get("end_time")
    return None


def plan_calendar_sync(
    actionable_postings: list[dict[str, Any]],
    ledger: dict[str, Any],
    inbox_dir: Path,
    calendar_events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compute the diff between currently actionable postings and the ledger.

    Returns dict with keys: 'create', 'update', 'delete', 'orphan_delete', 'untouched'.
    """
    active_by_id: dict[str, dict[str, Any]] = {}
    for p in actionable_postings:
        pid = str(p.get("id"))
        active_by_id[pid] = p

    to_create: list[dict[str, Any]] = []
    to_update: list[dict[str, Any]] = []
    to_delete: list[dict[str, Any]] = []
    untouched: list[str] = []

    # Check active postings against ledger
    for pid, posting in active_by_id.items():
        md_file = inbox_dir / f"{pid}.md"
        fm = read_frontmatter(md_file) if md_file.exists() else {}
        company = str(posting.get("company") or "").strip()
        role_hint = extract_role_hint(posting, fm)
        title = build_event_title(company, role_hint)
        timing = compute_event_timing(posting.get("end_time"))
        description = build_event_description(posting, fm)
        marker = get_stable_marker(pid)

        if pid not in ledger:
            to_create.append({
                "id": pid,
                "company": company,
                "title": title,
                "end_time": posting.get("end_time"),
                "timing": timing,
                "description": description,
                "marker": marker,
            })
        else:
            entry = ledger[pid]
            event_id = get_ledger_event_id(entry)
            recorded_end_time = get_ledger_end_time(entry)
            current_end_time = posting.get("end_time")

            # Check if deadline moved
            if recorded_end_time is not None and recorded_end_time != current_end_time:
                to_update.append({
                    "id": pid,
                    "event_id": event_id,
                    "company": company,
                    "title": title,
                    "old_end_time": recorded_end_time,
                    "new_end_time": current_end_time,
                    "timing": timing,
                    "description": description,
                    "marker": marker,
                })
            else:
                untouched.append(pid)

    # Check for postings in ledger that are no longer actionable
    for lid, entry in sorted(ledger.items()):
        if lid not in active_by_id:
            event_id = get_ledger_event_id(entry)
            if event_id:
                to_delete.append({
                    "id": lid,
                    "event_id": event_id,
                    "title": entry.get("title", f"공고 {lid}") if isinstance(entry, dict) else f"공고 {lid}",
                    "reason": "demoted_or_passed_deadline",
                })

    orphan_delete = find_orphan_events(calendar_events or [], ledger)
    to_delete.extend(orphan_delete)

    return {
        "create": to_create,
        "update": to_update,
        "delete": to_delete,
        "orphan_delete": orphan_delete,
        "untouched": untouched,
    }


def execute_sync(
    plan: dict[str, Any],
    ledger: dict[str, Any],
    ledger_path: Path,
    apply: bool = False,
    cli_path: Path = DEFAULT_SCHEDULE_CLI,
    max_workers: int = 4,
) -> dict[str, Any]:
    """Execute or print the sync plan."""
    to_create = plan["create"]
    to_update = plan["update"]
    to_delete = plan["delete"]
    orphan_delete = plan.get("orphan_delete", [])
    regular_delete = [item for item in to_delete if item.get("reason") != "orphan_marker"]
    untouched = plan["untouched"]

    if not apply:
        # Dry-run mode: strictly print without calling the calendar or modifying ledger
        print("=" * 70)
        print("Jasoseol Calendar Sync Plan (DRY-RUN)")
        print(f"Total Actionable: {len(to_create) + len(untouched) + len(to_update)}")
        print(
            f"Plan: {len(to_create)} to create, {len(to_update)} to update, "
            f"{len(regular_delete)} to delete, {len(orphan_delete)} orphan(s) to delete, "
            f"{len(untouched)} untouched."
        )
        print("=" * 70)

        if to_create:
            print("\n[TO CREATE]")
            for item in to_create:
                print(f"  + ID: {item['id']}")
                print(f"    Title: {item['title']}")
                print(f"    Timing: {item['timing']['display']}")
                print(f"    Marker: {item['marker']}")
                first_desc_line = item['description'].splitlines()[0] if item['description'] else ""
                print(f"    Info: {first_desc_line}")

        if to_update:
            print("\n[TO UPDATE - DEADLINE MOVED]")
            for item in to_update:
                print(f"  * ID: {item['id']} (Event ID: {item['event_id']})")
                print(f"    Title: {item['title']}")
                print(f"    Old Deadline: {item['old_end_time']}")
                print(f"    New Deadline: {item['new_end_time']}")
                print(f"    Timing: {item['timing']['display']}")

        if regular_delete:
            print("\n[TO DELETE - DEMOTED OR EXPIRED]")
            for item in regular_delete:
                print(f"  - ID: {item['id']} (Event ID: {item['event_id']})")
                print(f"    Title: {item['title']}")
                print(f"    Reason: {item['reason']}")

        if orphan_delete:
            print("\n[TO DELETE - ORPHAN MARKERS]")
            for item in orphan_delete:
                print(f"  - Marker: [{item['marker']}] (Event ID: {item['event_id']})")
                print(f"    Title: {item['title']}")
                print(f"    Reason: {item['reason']}")

        if not to_create and not to_update and not to_delete:
            print("\nEverything is up to date. No changes needed.")

        print("=" * 70)
        return {
            "status": "dry-run",
            "created": len(to_create),
            "updated": len(to_update),
            "deleted": len(to_delete),
            "orphan_deleted": 0,
            "untouched": len(untouched),
            "created_event_ids": [],
        }

    # Apply mode: execute calendar CLI commands and update ledger
    print("=" * 70)
    print("Jasoseol Calendar Sync (APPLYING)")
    print(
        f"Executing: {len(to_create)} to create, {len(to_update)} to update, "
        f"{len(regular_delete)} to delete, {len(orphan_delete)} orphan(s) to delete."
    )
    print("=" * 70)

    created_ids: list[str] = []
    updated_ids: list[str] = []
    deleted_ids: list[str] = []
    new_ledger = dict(ledger)

    def _create_one(item: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
        pid = item["id"]
        add_args = build_add_cli_args(
            account=CALENDAR_ACCOUNT,
            title=item["title"],
            timing=item["timing"],
            description=item["description"],
            apply=True,
        )
        print(f"Creating: {item['id']} | {item['title']} ({item['timing']['display']})...", flush=True)
        res = run_schedule_cli(add_args, cli_path=cli_path)
        event_id = res.get("event", {}).get("id") or res.get("eventId")
        if not event_id:
            raise RuntimeError(f"Failed to obtain event ID after creating {pid}: {res}")

        entry = {
            "event_id": event_id,
            "end_time": item["end_time"],
            "title": item["title"],
            "marker": item["marker"],
            "timing": item["timing"]["display"],
            "updated_at": datetime.now(KST).isoformat(),
        }
        print(f"  -> Created event ID: {event_id} ({item['title']})", flush=True)
        return pid, event_id, entry

    # 1. Create missing events
    if len(to_create) > 1 and max_workers > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {executor.submit(_create_one, item): item for item in to_create}
            for future in concurrent.futures.as_completed(future_to_item):
                pid, event_id, entry = future.result()
                created_ids.append(event_id)
                new_ledger[pid] = entry
    else:
        for item in to_create:
            pid, event_id, entry = _create_one(item)
            created_ids.append(event_id)
            new_ledger[pid] = entry

    # 2. Update moved deadline events
    for item in to_update:
        pid = item["id"]
        event_id = item["event_id"]
        update_args = build_update_cli_args(
            account=CALENDAR_ACCOUNT,
            event_id=event_id,
            title=item["title"],
            timing=item["timing"],
            description=item["description"],
            apply=True,
        )
        print(f"Updating: {pid} (event {event_id}) | new deadline: {item['new_end_time']}...")
        res = run_schedule_cli(update_args, cli_path=cli_path)
        updated_ids.append(event_id)
        new_ledger[pid] = {
            "event_id": event_id,
            "end_time": item["new_end_time"],
            "title": item["title"],
            "marker": item["marker"],
            "timing": item["timing"]["display"],
            "updated_at": datetime.now(KST).isoformat(),
        }
        print(f"  -> Updated event ID: {event_id}")

    # 3. Delete demoted or expired events
    for item in to_delete:
        pid = item["id"]
        event_id = item["event_id"]
        delete_args = build_delete_cli_args(
            account=CALENDAR_ACCOUNT,
            event_id=event_id,
            apply=True,
        )
        label = "orphan" if item.get("reason") == "orphan_marker" else pid
        print(f"Deleting: {label} (event {event_id}) | {item['title']}...")
        run_schedule_cli(delete_args, cli_path=cli_path)
        deleted_ids.append(event_id)
        new_ledger.pop(pid, None)
        print(f"  -> Deleted event ID: {event_id}")

    # Save updated ledger
    save_ledger(new_ledger, ledger_path)
    print("=" * 70)
    print(f"Sync complete. Created: {len(created_ids)}, Updated: {len(updated_ids)}, Deleted: {len(deleted_ids)}.")
    if created_ids:
        print(f"Created Event IDs: {', '.join(created_ids)}")
    print("=" * 70)

    return {
        "status": "applied",
        "created": len(created_ids),
        "updated": len(updated_ids),
        "deleted": len(deleted_ids),
        "orphan_deleted": len(orphan_delete),
        "untouched": len(untouched),
        "created_event_ids": created_ids,
        "updated_event_ids": updated_ids,
        "deleted_event_ids": deleted_ids,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize actionable Jasoseol recruitment deadlines into Google Calendar."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply mutations to the personal Google Calendar. Default is --dry-run.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created, updated, or deleted without calling the calendar.",
    )
    parser.add_argument(
        "--inbox",
        type=Path,
        default=DEFAULT_INBOX_DIR,
        help=f"Path to inbox directory (default: {DEFAULT_INBOX_DIR}).",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=DEFAULT_LEDGER_PATH,
        help=f"Path to calendar events ledger JSON (default: {DEFAULT_LEDGER_PATH}).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help=f"Path to jasoseol_targets.json config (default: {DEFAULT_CONFIG}).",
    )
    parser.add_argument(
        "--schedule-cli",
        type=Path,
        default=DEFAULT_SCHEDULE_CLI,
        help=f"Path to hih-schedule CLI script (default: {DEFAULT_SCHEDULE_CLI}).",
    )
    parser.add_argument(
        "--today",
        type=str,
        default=None,
        help="Reference date for filtering past deadlines (YYYY-MM-DD, default today KST).",
    )

    args = parser.parse_args(argv)
    apply_mode = bool(args.apply)
    reference_date = parse_reference_date(args.today)

    # Load currently actionable postings using jasoseol_report rules
    postings = load_postings(
        inbox_dir=args.inbox,
        config_path=args.config,
        today=reference_date,
        current_scoring_version=CURRENT_SCORING_VERSION,
    )

    # Load existing ledger
    ledger = load_ledger(args.ledger)

    # Sweep the same bounded calendar window before planning mutations. This read is
    # intentional in dry-run mode: it discovers interrupted creates without deleting.
    window_start, window_end = build_calendar_window(reference_date, postings, ledger)
    calendar_events = list_calendar_events(
        start_date=window_start,
        end_date=window_end,
        cli_path=args.schedule_cli,
    )
    print(f"Calendar orphan sweep: listed {len(calendar_events)} events from {window_start} through {window_end}.")

    # Compute plan
    plan = plan_calendar_sync(postings, ledger, args.inbox, calendar_events=calendar_events)

    # Execute
    execute_sync(
        plan=plan,
        ledger=ledger,
        ledger_path=args.ledger,
        apply=apply_mode,
        cli_path=args.schedule_cli,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
