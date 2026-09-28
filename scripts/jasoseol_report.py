#!/usr/bin/env python3
"""Daily Jasoseol (자소설닷컴) job report generator and Telegram notifier.

Reads collected postings under docs/jd/_inbox/jasoseol/ and renders one
self-contained HTML report with:
  1. A deadline calendar month grid covering this week and the next 4 weeks
     (with urgent deadlines inside the next 3 days distinctly marked).
  2. A table of actionable postings sorted by deadline ascending.

Optionally sends the HTML report as a document attachment to the operator
Telegram bot via sendDocument with a curated caption.

Usage:
  python3 scripts/jasoseol_report.py                  # render only (default)
  python3 scripts/jasoseol_report.py --html           # write report HTML to docs/jd/report/
  python3 scripts/jasoseol_report.py --html --dry-run # render without Telegram send
  python3 scripts/jasoseol_report.py --telegram       # write HTML and send to Telegram bot
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

try:
    from scripts.shortlist import (
        TRACK_CORE,
        normalize_track,
        track_label,
    )
except ModuleNotFoundError:
    try:
        from shortlist import (
            TRACK_CORE,
            normalize_track,
            track_label,
        )
    except ModuleNotFoundError:
        TRACK_CORE = "core"
        normalize_track = lambda t: t or "core"
        track_label = lambda t: t or "core"

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "jasoseol_targets.json"
DEFAULT_INBOX_DIR = REPO_ROOT / "docs" / "jd" / "_inbox" / "jasoseol"
DEFAULT_REPORT_DIR = REPO_ROOT / "docs" / "jd" / "report"
DEFAULT_ENV = Path(os.environ.get("PORTFOLIO_PM_ENV", os.environ.get("PM_ENV_PATH", "/home/window11/project-manager/.env")))
RECRUIT_BASE_URL = "https://jasoseol.com/recruit"
CURRENT_SCORING_VERSION = 2
KST = timezone(timedelta(hours=9))
TOKEN_IN_URL = re.compile(r"bot\d+:[A-Za-z0-9_-]+")

REPORT_CSS = """
:root {
  --bg: #f4f5f7;
  --panel: #ffffff;
  --panel2: #eef0f3;
  --ink: #1c212b;
  --dim: #59637a;
  --faint: #8b94a8;
  --line: #e2e5eb;
  --accent: #2a63e7;
  --accent-ink: #ffffff;
  --alert-bg: #fdecec;
  --alert-border: #f2b8b5;
  --alert-ink: #9c1c1c;
  --alert-dim: #8a3030;
  --chip-bg: #eef0f4;
  --ok: #1c7c4a;
  --ok-bg: #e3f3ea;
  --urgent-bg: #fff1f0;
  --urgent-border: #ffa39e;
  --urgent-ink: #cf1322;
  --cal-today-bg: #edf3ff;
  --cal-today-border: #2a63e7;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1319;
    --panel: #181d27;
    --panel2: #202634;
    --ink: #e8ebf2;
    --dim: #a3adc2;
    --faint: #6e7880;
    --line: #2a3140;
    --accent: #5b8cff;
    --accent-ink: #0d1220;
    --alert-bg: #3a1518;
    --alert-border: #7a2a2f;
    --alert-ink: #ff9d9d;
    --alert-dim: #d98c8c;
    --chip-bg: #242b3a;
    --ok: #5fd39a;
    --ok-bg: #15301f;
    --urgent-bg: #3c1618;
    --urgent-border: #822227;
    --urgent-ink: #ff8585;
    --cal-today-bg: #16243d;
    --cal-today-border: #5b8cff;
  }
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 14px/1.55 -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif;
}
.wrap {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 20px 48px;
}
header {
  margin-bottom: 24px;
}
h1 {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 6px;
  letter-spacing: -0.02em;
}
.sub {
  color: var(--dim);
  font-size: 13.5px;
}
h2 {
  font-size: 16px;
  font-weight: 700;
  margin: 28px 0 12px;
  letter-spacing: -0.01em;
  display: flex;
  align-items: center;
  gap: 8px;
}
.badge-count {
  font-size: 12px;
  background: var(--panel2);
  color: var(--dim);
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 600;
}
.table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin-bottom: 16px;
}
/* Calendar grid styles */
.cal-grid {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
}
.cal-grid th {
  background: var(--panel2);
  color: var(--dim);
  padding: 8px 6px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  border-bottom: 1px solid var(--line);
  border-right: 1px solid var(--line);
}
.cal-grid th:last-child {
  border-right: none;
}
.cal-grid td {
  height: 96px;
  vertical-align: top;
  padding: 6px;
  border-bottom: 1px solid var(--line);
  border-right: 1px solid var(--line);
  background: var(--panel);
}
.cal-grid td:last-child {
  border-right: none;
}
.cal-grid tr:last-child td {
  border-bottom: none;
}
.cal-grid td.today-cell {
  background: var(--cal-today-bg);
  box-shadow: inset 0 0 0 1.5px var(--cal-today-border);
}
.cal-grid td.empty-cell {
  background: var(--bg);
  opacity: 0.65;
}
.cal-day-hdr {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}
.cal-day-num {
  font-size: 11px;
  font-weight: 700;
  color: var(--faint);
}
.today-cell .cal-day-num {
  color: var(--accent);
}
.today-badge {
  font-size: 10px;
  background: var(--accent);
  color: var(--accent-ink);
  padding: 1px 4px;
  border-radius: 3px;
  font-weight: 600;
}
.cal-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.cal-item {
  display: block;
  background: var(--panel2);
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 3px 5px;
  font-size: 11px;
  line-height: 1.3;
  text-decoration: none;
  color: var(--ink);
  transition: opacity 0.15s;
}
.cal-item:hover {
  opacity: 0.85;
}
.cal-item.urgent {
  background: var(--urgent-bg);
  border-color: var(--urgent-border);
  color: var(--urgent-ink);
}
.cal-co {
  font-weight: 700;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.cal-title {
  display: block;
  color: var(--dim);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 10.5px;
}
.cal-item.urgent .cal-title {
  color: var(--urgent-ink);
}
/* Actionable table styles */
.act-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
  font-size: 13px;
}
.act-table th {
  background: var(--panel2);
  color: var(--dim);
  font-weight: 600;
  font-size: 12px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  text-align: left;
  white-space: nowrap;
}
.act-table td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
.act-table tr:last-child td {
  border-bottom: none;
}
.act-table tr.urgent-row {
  background: var(--urgent-bg);
}
.act-table tr.urgent-row td {
  border-bottom-color: var(--urgent-border);
}
.co-name {
  font-weight: 700;
  white-space: nowrap;
}
.job-title {
  font-weight: 600;
  color: var(--ink);
  text-decoration: none;
}
.job-title:hover {
  text-decoration: underline;
  color: var(--accent);
}
.dl-wrap {
  white-space: nowrap;
  font-size: 12.5px;
}
.urgent-pill {
  display: inline-block;
  background: var(--urgent-border);
  color: var(--urgent-ink);
  font-size: 10.5px;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 4px;
  margin-left: 4px;
  white-space: nowrap;
}
@media (prefers-color-scheme: dark) {
  .urgent-pill {
    background: #6a1a1e;
    color: #ffb4b4;
  }
}
.sub-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 2px;
}
.sub-chip {
  background: var(--chip-bg);
  color: var(--dim);
  font-size: 11.5px;
  padding: 2px 7px;
  border-radius: 4px;
  white-space: nowrap;
}
.score-badge {
  display: inline-block;
  font-weight: 700;
  font-size: 12px;
  background: var(--panel2);
  padding: 2px 6px;
  border-radius: 4px;
  text-align: center;
}
.score-badge.high {
  background: var(--ok-bg);
  color: var(--ok);
}
.apply-btn {
  display: inline-block;
  background: var(--accent);
  color: var(--accent-ink) !important;
  font-size: 12px;
  font-weight: 600;
  padding: 5px 10px;
  border-radius: 6px;
  text-decoration: none;
  white-space: nowrap;
}
.apply-btn:hover {
  opacity: 0.9;
}
.footer {
  margin-top: 36px;
  color: var(--faint);
  font-size: 12px;
  text-align: center;
  border-top: 1px solid var(--line);
  padding-top: 16px;
}
"""


def log(msg: str, to_stderr: bool = False) -> None:
    stream = sys.stderr if to_stderr else sys.stdout
    print(msg, file=stream, flush=True)


def read_frontmatter(path: Path) -> dict[str, Any]:
    """Parse YAML frontmatter from a markdown file."""
    if not path.exists():
        return {}
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not content.startswith("---"):
        return {}
    lines = content.splitlines()
    values: dict[str, Any] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        raw = raw.strip()
        try:
            values[key.strip()] = json.loads(raw)
        except (TypeError, ValueError):
            values[key.strip()] = raw.strip('"\'')
    return values


def extract_deadline_date(end_time: str | None) -> str | None:
    """Extract YYYY-MM-DD string from an end_time string."""
    if not end_time:
        return None
    s = str(end_time).strip()
    if not s:
        return None
    try:
        if "T" in s:
            dt = datetime.fromisoformat(s)
            return dt.strftime("%Y-%m-%d")
        return datetime.strptime(s[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
    except Exception:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
        if m:
            return m.group(1)
        return None


def format_deadline(end_time: str | None) -> str:
    """Format end_time for display, e.g. 2026-09-30 23:59 or 2026-09-30."""
    if not end_time:
        return "—"
    s = str(end_time).strip()
    try:
        if "T" in s:
            dt = datetime.fromisoformat(s)
            return dt.strftime("%Y-%m-%d %H:%M")
        return s[:10]
    except Exception:
        return s[:16]


def parse_deadline_datetime(end_time: str | None) -> tuple[datetime, str]:
    """Parse end_time into a sortable datetime, placing empty/unparseable values last."""
    if not end_time:
        return datetime.max.replace(tzinfo=KST), ""
    s = str(end_time).strip()
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=KST)
        else:
            dt = dt.astimezone(KST)
        return dt, s
    except Exception:
        try:
            dt = datetime.strptime(s[:10], "%Y-%m-%d").replace(tzinfo=KST)
            return dt, s
        except Exception:
            return datetime.max.replace(tzinfo=KST), s


def is_older_scoring_version(
    version: Any, current_version: int = CURRENT_SCORING_VERSION
) -> bool:
    """Return True if version is missing or older than current_version."""
    if version is None:
        return True
    try:
        if isinstance(version, str) and version.lower().startswith("v"):
            version = version[1:]
        return int(version) < current_version
    except (ValueError, TypeError):
        return True


def is_deadline_passed(
    end_time: str | None,
    now_or_today: datetime | date | None = None,
) -> bool:
    """Return True if deadline has already passed."""
    if not end_time:
        return False
    dt, _ = parse_deadline_datetime(end_time)
    if dt == datetime.max.replace(tzinfo=KST):
        return False
    if now_or_today is None:
        ref_dt = datetime.now(KST)
    elif isinstance(now_or_today, datetime):
        ref_dt = now_or_today if now_or_today.tzinfo else now_or_today.replace(tzinfo=KST)
    elif isinstance(now_or_today, date):
        d_str = extract_deadline_date(end_time)
        if d_str:
            try:
                d = datetime.strptime(d_str, "%Y-%m-%d").date()
                if d < now_or_today:
                    return True
                if d > now_or_today:
                    return False
            except Exception:
                pass
        now_kst = datetime.now(KST)
        if now_kst.date() == now_or_today:
            return dt < now_kst
        return False
    else:
        ref_dt = datetime.now(KST)
    return dt < ref_dt


def is_experienced_hire(frontmatter: dict[str, Any]) -> bool:
    """Return whether a posting is marked as an experienced-hire announcement."""
    career_type = str(frontmatter.get("career_type") or "").strip().lower()
    return career_type in {"경력", "experienced", "experienced hire", "experienced_hire"}


def load_postings(
    inbox_dir: Path,
    min_score: int | None = None,
    config_path: Path | None = None,
    today: date | str | None = None,
    current_scoring_version: int = CURRENT_SCORING_VERSION,
    stats: dict[str, int] | None = None,
) -> list[dict[str, Any]]:
    """Load actionable postings from inbox directory.

    Only postings that passed the shortlist threshold with a future deadline
    and evaluated under the current scoring version appear in the report.
    When ``stats`` is provided, it receives experienced-hire examined and
    filtered counts for the run.
    """
    if stats is not None:
        stats.clear()
        stats.update({"examined": 0, "filtered": 0})

    if not inbox_dir.exists():
        return []

    if min_score is None:
        cfg_file = config_path or DEFAULT_CONFIG
        if cfg_file.exists():
            try:
                cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
                min_score = int(cfg.get("score_threshold", 28))
            except Exception:
                min_score = 28
        else:
            min_score = 28

    if today is None:
        today_d = datetime.now(KST).date()
    elif isinstance(today, str):
        today_d = datetime.strptime(today[:10], "%Y-%m-%d").date()
    else:
        today_d = today

    postings: list[dict[str, Any]] = []
    stale_version_count = 0
    passed_deadline_count = 0

    for md_file in sorted(inbox_dir.glob("*.md")):
        fm = read_frontmatter(md_file)
        if not fm:
            continue
        experienced_hire = is_experienced_hire(fm)
        if stats is not None and experienced_hire:
            stats["examined"] += 1

        # Check scoring version
        version = fm.get("scoring_version")
        if is_older_scoring_version(version, current_scoring_version):
            stale_version_count += 1
            if stats is not None and experienced_hire:
                stats["filtered"] += 1
            continue

        score = int(fm.get("score", 0) or 0)
        verdict = str(fm.get("verdict", "")).strip().lower()
        actionable_flag = fm.get("actionable")

        if actionable_flag is False or verdict in ("rejected", "not_actionable"):
            if stats is not None and experienced_hire:
                stats["filtered"] += 1
            continue
        if score < min_score:
            if stats is not None and experienced_hire:
                stats["filtered"] += 1
            continue
        if actionable_flag is not True and verdict != "actionable":
            if stats is not None and experienced_hire:
                stats["filtered"] += 1
            continue

        end_time = fm.get("end_time")
        if is_deadline_passed(end_time, now_or_today=today_d):
            passed_deadline_count += 1
            if stats is not None and experienced_hire:
                stats["filtered"] += 1
            continue

        pid = str(fm.get("id") if fm.get("id") is not None else md_file.stem)
        company = str(fm.get("company") or "").strip()
        title = str(fm.get("title") or "").strip()
        track = normalize_track(str(fm.get("track") or TRACK_CORE))
        start_time = fm.get("start_time")
        url = str(fm.get("url") or f"{RECRUIT_BASE_URL}/{pid}").strip()
        apply_url = str(fm.get("apply_url") or "").strip()

        sub_positions = (
            fm.get("sub_positions")
            or fm.get("experienced_positions")
            or []
        )
        if isinstance(sub_positions, str):
            sub_positions = [sub_positions]
        sub_positions = [str(s).strip() for s in sub_positions if str(s).strip()]

        postings.append({
            "id": pid,
            "company": company,
            "title": title,
            "track": track,
            "score": score,
            "verdict": verdict,
            "career_type": fm.get("career_type", "경력"),
            "start_time": start_time,
            "end_time": end_time,
            "url": url,
            "apply_url": apply_url,
            "sub_positions": sub_positions,
            "experienced_positions": sub_positions,
            "first_seen": fm.get("first_seen"),
        })

    if stale_version_count > 0:
        log(f"WARNING: skipped {stale_version_count} posting(s) evaluated under older scoring version (< {current_scoring_version})")
    log(f"[filter] skipped {passed_deadline_count} posting(s) whose deadline has already passed")

    return postings


def sort_by_deadline(postings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort postings ascending by deadline, secondary key company name."""
    return sorted(
        postings,
        key=lambda p: (
            parse_deadline_datetime(p.get("end_time"))[0],
            p.get("company", ""),
            p.get("title", ""),
        ),
    )


def is_urgent(
    end_time: str | None,
    today: date | str | None = None,
    days_window: int = 3,
) -> bool:
    """Return True if deadline falls within the next `days_window` days (inclusive).

    Deadlines in the past or missing return False.
    """
    date_str = extract_deadline_date(end_time)
    if not date_str:
        return False

    if today is None:
        today_d = datetime.now(KST).date()
    elif isinstance(today, str):
        today_d = datetime.strptime(today[:10], "%Y-%m-%d").date()
    else:
        today_d = today

    try:
        deadline_d = datetime.strptime(date_str, "%Y-%m-%d").date()
        diff = (deadline_d - today_d).days
        return 0 <= diff <= days_window
    except Exception:
        return False


def days_until_deadline(
    end_time: str | None,
    today: date | str | None = None,
) -> int | None:
    """Return whole days remaining until deadline, or None if unparseable."""
    date_str = extract_deadline_date(end_time)
    if not date_str:
        return None

    if today is None:
        today_d = datetime.now(KST).date()
    elif isinstance(today, str):
        today_d = datetime.strptime(today[:10], "%Y-%m-%d").date()
    else:
        today_d = today

    try:
        deadline_d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (deadline_d - today_d).days
    except Exception:
        return None


def bucket_postings_by_date(
    postings: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Bucket postings by their YYYY-MM-DD deadline date."""
    buckets: dict[str, list[dict[str, Any]]] = {}
    for p in postings:
        d = extract_deadline_date(p.get("end_time"))
        if d:
            buckets.setdefault(d, []).append(p)
    return buckets


def build_calendar_weeks(
    today: date,
    num_weeks: int = 5,
) -> list[list[date]]:
    """Build a month grid covering this week (starting Monday) and next (num_weeks - 1) weeks."""
    # Monday is weekday 0 in Python datetime
    start_of_week = today - timedelta(days=today.weekday())
    weeks: list[list[date]] = []
    for w in range(num_weeks):
        week_days = [start_of_week + timedelta(days=w * 7 + d) for d in range(7)]
        weeks.append(week_days)
    return weeks


def make_caption(
    postings: list[dict[str, Any]],
    today: date | str | None = None,
) -> str:
    """Generate a concise Telegram caption stating actionable & urgent counts."""
    if today is None:
        today_d = datetime.now(KST).date()
    elif isinstance(today, str):
        today_d = datetime.strptime(today[:10], "%Y-%m-%d").date()
    else:
        today_d = today

    today_str = today_d.strftime("%Y-%m-%d")
    n_actionable = len(postings)
    urgent_postings = [p for p in postings if is_urgent(p.get("end_time"), today=today_d)]
    n_urgent = len(urgent_postings)

    lines = [
        f"📋 자소설닷컴 추천 채용 리포트 · {today_str}",
        f"추천 공고: {n_actionable}건 · 긴급 마감(3일 이내): {n_urgent}건",
    ]

    ordered = sort_by_deadline(postings)
    if ordered:
        lines.append("")
        for p in ordered[:5]:
            co = p.get("company") or "—"
            ti = p.get("title") or "—"
            dl = format_deadline(p.get("end_time"))
            d_left = days_until_deadline(p.get("end_time"), today=today_d)
            if d_left is not None and 0 <= d_left <= 3:
                urg = f" 🚨 D-{d_left}" if d_left > 0 else " 🚨 오늘 마감"
            else:
                urg = ""
            lines.append(f"• {co} — {ti} (~{dl}){urg}")
        if len(ordered) > 5:
            lines.append(f"  … 외 {len(ordered) - 5}건")

    return "\n".join(lines)


def make_empty_message(examined_count: int, filtered_count: int) -> str:
    """Generate the short Telegram message for a quiet recommendation day."""
    return (
        "오늘은 새로운 추천 공고가 없습니다. "
        f"경력 공고 {examined_count}건을 검토했고 {filtered_count}건을 필터링했습니다."
    )


def render_html(
    postings: list[dict[str, Any]],
    today: date | str | None = None,
    num_weeks: int = 5,
) -> str:
    """Render the self-contained HTML report."""
    if today is None:
        today_d = datetime.now(KST).date()
    elif isinstance(today, str):
        today_d = datetime.strptime(today[:10], "%Y-%m-%d").date()
    else:
        today_d = today

    today_str = today_d.strftime("%Y-%m-%d")
    n_actionable = len(postings)
    urgent_postings = [p for p in postings if is_urgent(p.get("end_time"), today=today_d)]
    n_urgent = len(urgent_postings)

    esc = lambda v: html.escape(str(v if v is not None else ""), quote=True)

    date_buckets = bucket_postings_by_date(postings)
    weeks = build_calendar_weeks(today_d, num_weeks=num_weeks)
    sorted_postings = sort_by_deadline(postings)

    parts: list[str] = [
        "<!doctype html>",
        "<html lang=\"ko\">",
        "<head>",
        "<meta charset=\"utf-8\">",
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        f"<title>자소설닷컴 추천 공고 · {esc(today_str)}</title>",
        f"<style>{REPORT_CSS}</style>",
        "</head>",
        "<body>",
        "<div class=\"wrap\">",
        "<header>",
        f"<h1>자소설닷컴 경력 추천 공고</h1>",
        f"<div class=\"sub\">기준일: {esc(today_str)} · 추천 공고 <b>{n_actionable}건</b> · 긴급 마감 <b>{n_urgent}건</b></div>",
        "</header>",
    ]

    # Section 1: Deadline Calendar Grid (This week + next 4 weeks = 5 weeks)
    parts.append("<h2>마감 캘린더 (이번 주 ~ 향후 4주)</h2>")
    parts.append("<div class=\"table-wrap\">")
    parts.append("<table class=\"cal-grid\">")
    parts.append("<thead><tr>")
    for day_name in ("월 (Mon)", "화 (Tue)", "수 (Wed)", "목 (Thu)", "금 (Fri)", "토 (Sat)", "일 (Sun)"):
        parts.append(f"<th>{esc(day_name)}</th>")
    parts.append("</tr></thead>")
    parts.append("<tbody>")

    grid_end_date = weeks[-1][-1]
    outside_grid_postings: list[dict[str, Any]] = []

    for week in weeks:
        parts.append("<tr>")
        for day_dt in week:
            day_str = day_dt.strftime("%Y-%m-%d")
            day_postings = date_buckets.get(day_str, [])
            is_today_cell = (day_dt == today_d)
            is_empty_cell = (len(day_postings) == 0)

            classes = []
            if is_today_cell:
                classes.append("today-cell")
            if is_empty_cell:
                classes.append("empty-cell")

            cls_attr = f" class=\"{' '.join(classes)}\"" if classes else ""
            parts.append(f"<td{cls_attr}>")
            parts.append("<div class=\"cal-day-hdr\">")
            parts.append(f"<span class=\"cal-day-num\">{day_dt.strftime('%m/%d')}</span>")
            if is_today_cell:
                parts.append("<span class=\"today-badge\">오늘</span>")
            parts.append("</div>")

            if day_postings:
                parts.append("<div class=\"cal-items\">")
                for p in day_postings:
                    urg = is_urgent(p.get("end_time"), today=today_d)
                    urg_cls = " urgent" if urg else ""
                    p_url = p.get("url") or f"{RECRUIT_BASE_URL}/{p.get('id', '')}"
                    p_co = p.get("company", "")
                    p_ti = p.get("title", "")
                    parts.append(
                        f"<a href=\"{esc(p_url)}\" target=\"_blank\" rel=\"noopener noreferrer\" "
                        f"class=\"cal-item{urg_cls}\" title=\"{esc(p_co)} - {esc(p_ti)}\">"
                        f"<span class=\"cal-co\">{esc(p_co)}</span>"
                        f"<span class=\"cal-title\">{esc(p_ti)}</span>"
                        f"</a>"
                    )
                parts.append("</div>")

            parts.append("</td>")
        parts.append("</tr>")
    parts.append("</tbody></table></div>")

    # Check for postings outside the calendar window
    for p in sorted_postings:
        p_d = extract_deadline_date(p.get("end_time"))
        if p_d and p_d > grid_end_date.strftime("%Y-%m-%d"):
            outside_grid_postings.append(p)

    if outside_grid_postings:
        parts.append(
            f"<div class=\"sub\" style=\"margin-top:-8px; margin-bottom:20px;\">"
            f"* 5주 이후 마감 공고 ({len(outside_grid_postings)}건): "
            + ", ".join(
                f"{esc(p.get('company'))} ({esc(extract_deadline_date(p.get('end_time')))})"
                for p in outside_grid_postings
            )
            + "</div>"
        )

    # Section 2: Table of Actionable Postings
    parts.append("<h2>추천 공고 목록 <span class=\"badge-count\">마감순 정렬</span></h2>")
    parts.append("<div class=\"table-wrap\">")
    parts.append("<table class=\"act-table\">")
    parts.append(
        "<thead><tr>"
        "<th>마감일</th>"
        "<th>회사</th>"
        "<th>공고명</th>"
        "<th>모집 분야 (경력)</th>"
        "<th>Track</th>"
        "<th>점수</th>"
        "<th>지원</th>"
        "</tr></thead>"
    )
    parts.append("<tbody>")

    for p in sorted_postings:
        urg = is_urgent(p.get("end_time"), today=today_d)
        row_cls = " class=\"urgent-row\"" if urg else ""
        dl_text = format_deadline(p.get("end_time"))
        d_left = days_until_deadline(p.get("end_time"), today=today_d)

        urg_pill = ""
        if urg and d_left is not None:
            if d_left == 0:
                urg_pill = "<span class=\"urgent-pill\">🚨 오늘 마감</span>"
            else:
                urg_pill = f"<span class=\"urgent-pill\">🚨 D-{d_left}</span>"

        p_url = p.get("url") or f"{RECRUIT_BASE_URL}/{p.get('id', '')}"
        p_apply = p.get("apply_url") or p_url
        p_co = p.get("company", "—")
        p_ti = p.get("title", "—")
        p_tr = p.get("track", "core")
        p_sc = p.get("score", 0)

        subs = p.get("sub_positions") or []
        if subs:
            subs_html = "<div class=\"sub-chips\">" + "".join(
                f"<span class=\"sub-chip\">{esc(s)}</span>" for s in subs
            ) + "</div>"
        else:
            subs_html = "—"

        score_cls = "score-badge high" if p_sc >= 30 else "score-badge"

        parts.append(
            f"<tr{row_cls}>"
            f"<td class=\"dl-wrap\">{esc(dl_text)}{urg_pill}</td>"
            f"<td class=\"co-name\">{esc(p_co)}</td>"
            f"<td><a href=\"{esc(p_url)}\" target=\"_blank\" rel=\"noopener noreferrer\" class=\"job-title\">{esc(p_ti)}</a></td>"
            f"<td>{subs_html}</td>"
            f"<td>{esc(track_label(p_tr))} ({esc(p_tr)})</td>"
            f"<td><span class=\"{score_cls}\">{esc(p_sc)}</span></td>"
            f"<td><a href=\"{esc(p_apply)}\" target=\"_blank\" rel=\"noopener noreferrer\" class=\"apply-btn\">지원하기</a></td>"
            f"</tr>"
        )

    parts.append("</tbody></table></div>")

    parts.append("<div class=\"footer\">")
    parts.append(f"자동 생성: {esc(today_str)} · SSOT: docs/jd/_inbox/jasoseol/ · scripts/jasoseol_report.py")
    parts.append("</div>")

    parts.append("</div>")  # .wrap
    parts.append("</body></html>")

    return "\n".join(parts)


def telegram_creds(env_path: Path) -> tuple[str, str] | None:
    """(token, chat_id) from KEY=VALUE lines; None when either key is missing."""
    if not env_path.exists():
        return None
    token = chat = None
    try:
        text = env_path.read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.splitlines():
        if line.startswith("PM_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()
        elif line.startswith("PM_BOT_CHAT_ID="):
            chat = line.split("=", 1)[1].strip()
    return (token, chat) if token and chat else None


def send_report_via_telegram(path: Path, caption_text: str, env_path: Path) -> bool:
    """Send document to operator Telegram bot via sendDocument."""
    creds = telegram_creds(env_path)
    if creds is None:
        log(f"WARNING: Telegram credentials not found in {env_path}; report not sent")
        return False
    token, chat = creds
    boundary = "----jasoseol" + datetime.now().strftime("%H%M%S%f")
    body = bytearray()
    for key, value in (("chat_id", chat), ("caption", caption_text[:1000])):
        body += (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n"
            f"{value}\r\n"
        ).encode("utf-8")
    body += (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"document\"; "
        f"filename=\"{path.name}\"\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    ).encode()
    body += path.read_bytes() + b"\r\n" + f"--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendDocument",
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            ok = bool(result.get("ok"))
            http_status = getattr(resp, "status", None)
            status_text = str(http_status) if isinstance(http_status, int) else "unknown"
            log(f"[telegram] sendDocument API response: HTTP {status_text}, ok={'true' if ok else 'false'}")
    except Exception as exc:
        log(f"WARNING: telegram sendDocument failed: {TOKEN_IN_URL.sub('bot***', str(exc))}")
        return False
    if not ok:
        log("WARNING: telegram sendDocument returned ok=false; report not confirmed sent")
    return ok


def send_message_via_telegram(message_text: str, env_path: Path) -> bool:
    """Send a plain text message to the operator Telegram bot via sendMessage."""
    creds = telegram_creds(env_path)
    if creds is None:
        log(f"WARNING: Telegram credentials not found in {env_path}; message not sent")
        return False
    token, chat = creds
    body = urlencode({"chat_id": chat, "text": message_text}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            ok = bool(result.get("ok"))
            http_status = getattr(resp, "status", None)
            status_text = str(http_status) if isinstance(http_status, int) else "unknown"
            log(f"[telegram] sendMessage API response: HTTP {status_text}, ok={'true' if ok else 'false'}")
    except Exception as exc:
        log(f"WARNING: telegram sendMessage failed: {TOKEN_IN_URL.sub('bot***', str(exc))}")
        return False
    if not ok:
        log("WARNING: telegram sendMessage returned ok=false; message not confirmed sent")
    return ok


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Jasoseol actionable job postings report.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG,
                        help=f"targets config (default: {DEFAULT_CONFIG})")
    parser.add_argument("--inbox-dir", type=Path, default=DEFAULT_INBOX_DIR,
                        help=f"inbox directory (default: {DEFAULT_INBOX_DIR})")
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR,
                        help=f"report output directory (default: {DEFAULT_REPORT_DIR})")
    parser.add_argument("--output", type=Path, default=None,
                        help="explicit output HTML path")
    parser.add_argument("--html", action="store_true",
                        help="write report to docs/jd/report/jasoseol-YYYY-MM-DD.html")
    parser.add_argument("--telegram", action="store_true",
                        help="send report via Telegram bot (implies writing HTML)")
    parser.add_argument("--dry-run", action="store_true",
                        help="render report without sending Telegram message")
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV,
                        help=f"env file for Telegram credentials (default: {DEFAULT_ENV})")
    parser.add_argument("--date", type=str, default=None,
                        help="override today's date (YYYY-MM-DD)")
    parser.add_argument("--min-score", type=int, default=None,
                        help="minimum score threshold (default: from config or 28)")

    args = parser.parse_args(argv)

    if args.telegram:
        args.html = True  # sending requires writing the report file

    if args.date:
        today = datetime.strptime(args.date[:10], "%Y-%m-%d").date()
    else:
        today = datetime.now(KST).date()
    today_str = today.strftime("%Y-%m-%d")

    load_stats: dict[str, int] = {}
    postings = load_postings(
        args.inbox_dir,
        min_score=args.min_score,
        config_path=args.config,
        today=today,
        stats=load_stats,
    )

    if not postings:
        log(
            f"[jasoseol_report] no actionable postings found in {args.inbox_dir}; "
            "report will not be generated."
        )
        if args.telegram:
            empty_message = make_empty_message(
                load_stats.get("examined", 0), load_stats.get("filtered", 0)
            )
            if args.dry_run:
                log(f"[dry-run] telegram send skipped (--dry-run). Message: {empty_message}")
            elif send_message_via_telegram(empty_message, args.env):
                log("[telegram] empty-result message delivered to PM bot")
            else:
                log("[telegram] empty-result message delivery failed or not attempted")
        return 0

    html_content = render_html(postings, today=today)
    caption_text = make_caption(postings, today=today)
    urgent_count = sum(1 for p in postings if is_urgent(p.get("end_time"), today=today))

    report_path = args.output
    if report_path is None and args.html:
        args.report_dir.mkdir(parents=True, exist_ok=True)
        report_path = args.report_dir / f"jasoseol-{today_str}.html"

    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(html_content, encoding="utf-8")
        try:
            rel_path = report_path.relative_to(REPO_ROOT)
        except ValueError:
            rel_path = report_path
        log(f"[report] {rel_path} ({len(html_content):,} bytes, {len(postings)} actionable, {urgent_count} urgent)")
    else:
        log(f"[jasoseol_report] rendered HTML in memory ({len(html_content):,} bytes, {len(postings)} actionable, {urgent_count} urgent). (Use --html to save)")

    if args.telegram:
        if args.dry_run:
            log(f"[dry-run] telegram send skipped (--dry-run). Caption:\n{caption_text}")
        else:
            if report_path and send_report_via_telegram(report_path, caption_text, args.env):
                log("[telegram] report delivered to PM bot")
            else:
                log("[telegram] report delivery failed or not attempted")
    elif args.dry_run:
        log(f"[dry-run] render completed. Caption preview:\n{caption_text}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
