#!/usr/bin/env python3
"""Render the application ledger as a daily status report.

The ledger at docs/jd/applications.json is the SSOT for every role the user
applied to, is preparing, or parked. This script renders it two ways:

- docs/jd/APPLICATIONS.md — the human view, regenerated in place
- docs/jd/report/applications-YYYY-MM-DD.html — the Telegram attachment

It replaces the raw Wanted dump on the daily secretary-bot slot: what the user
needs every morning is which application is waiting on them, not 41 new
postings they will not read.

Usage:
    python3 scripts/applications_report.py                 # rewrite APPLICATIONS.md
    python3 scripts/applications_report.py --html          # + render the HTML
    python3 scripts/applications_report.py --html --telegram
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "docs" / "jd" / "applications.json"
MARKDOWN = REPO / "docs" / "jd" / "APPLICATIONS.md"
REPORT_DIR = REPO / "docs" / "jd" / "report"
DEFAULT_ENV = Path("/home/window11/project-manager/.env")  # same file wanted_collect.py reads
KST = timezone(timedelta(hours=9))

# Order the report by what the user has to do next, not alphabetically.
STATUS_ORDER = ("제출", "면접", "오퍼", "준비완료", "준비중", "미지원", "보류",
                "서류탈락", "마감")
STATUS_BADGE = {
    "제출": "📮", "면접": "🗣", "오퍼": "🎉", "준비완료": "✅", "준비중": "🛠",
    "미지원": "⬜", "보류": "⏸", "서류탈락": "❌", "마감": "🚫",
}
# Statuses that put the ball in the user's court.
NEEDS_ACTION = ("준비완료", "준비중", "미지원")
TOKEN_IN_URL = re.compile(r"bot\d+:[A-Za-z0-9_-]+")


def log(message: str) -> None:
    print(message, flush=True)


def load_ledger(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("applications") or []
    if not isinstance(rows, list):
        raise ValueError(f"{path}: 'applications' must be a list")
    return rows


def status_rank(row: dict) -> tuple[int, str]:
    status = str(row.get("status") or "")
    rank = STATUS_ORDER.index(status) if status in STATUS_ORDER else len(STATUS_ORDER)
    return (rank, str(row.get("company") or ""))


def sort_rows(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=status_rank)


def days_since(date_str: str | None, today: str) -> int | None:
    """Whole days between an ISO date and today; None when unparseable."""
    if not date_str:
        return None
    try:
        then = datetime.strptime(date_str, "%Y-%m-%d").date()
        now = datetime.strptime(today, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (now - then).days


def summary_counts(rows: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        status = str(row.get("status") or "미분류")
        counts[status] = counts.get(status, 0) + 1
    return counts


def render_markdown(rows: list[dict], today: str) -> str:
    ordered = sort_rows(rows)
    counts = summary_counts(rows)
    summary = " · ".join(f"{status} {counts[status]}"
                         for status in STATUS_ORDER if status in counts)
    lines = [
        "# 지원 이력 (APPLICATIONS)",
        "",
        f"> 생성: {today} · `scripts/applications_report.py` 자동 생성 — 직접 고치지 말 것.",
        "> SSOT: [`applications.json`](applications.json). 상태·날짜 수정은 그 파일에서.",
        "",
        f"**{len(rows)}건** — {summary}" if summary else f"**{len(rows)}건**",
        "",
        "## 전체",
        "",
        "| | 회사 | 포지션 | 채널 | 지원일 | 다음 행동 |",
        "|---|---|---|---|---|---|",
    ]
    for row in ordered:
        status = str(row.get("status") or "")
        badge = STATUS_BADGE.get(status, "")
        applied = row.get("applied_at") or "—"
        elapsed = days_since(row.get("applied_at"), today)
        if elapsed is not None:
            applied = f"{applied} (D+{elapsed})"
        position = row.get("position") or "—"
        url = row.get("url")
        if url:
            position = f"[{position}]({url})"
        lines.append(
            f"| {badge} {status} | {row.get('company') or '—'} | {position} | "
            f"{row.get('channel') or '—'} | {applied} | {row.get('next_action') or '—'} |"
        )

    pending = [row for row in ordered if str(row.get("status")) in NEEDS_ACTION]
    lines += ["", "## 대기 중인 결정", ""]
    if pending:
        for row in pending:
            lines.append(f"- **{row.get('company')} — {row.get('position')}**: "
                         f"{row.get('next_action') or '다음 행동 미정'}")
    else:
        lines.append("- 없음")

    lines += ["", "## 비고", ""]
    for row in ordered:
        note = row.get("notes")
        if note:
            lines.append(f"- **{row.get('company')} — {row.get('position')}**: {note}")
    lines.append("")
    return "\n".join(lines)


def render_html(rows: list[dict], today: str) -> str:
    ordered = sort_rows(rows)
    counts = summary_counts(rows)
    summary = " · ".join(f"{status} {counts[status]}"
                         for status in STATUS_ORDER if status in counts)
    pending = [row for row in ordered if str(row.get("status")) in NEEDS_ACTION]

    def esc(value: object) -> str:
        return html.escape(str(value if value not in (None, "") else "—"))

    parts = [
        "<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\">",
        f"<title>지원 현황 {esc(today)}</title>",
        "<style>",
        "body{font-family:-apple-system,'Malgun Gothic',sans-serif;margin:0;padding:20px;"
        "background:#f7f7f8;color:#1c1c1e;line-height:1.55}",
        "h1{font-size:20px;margin:0 0 4px}h2{font-size:15px;margin:24px 0 8px}",
        ".sub{color:#6b6b70;font-size:13px;margin-bottom:16px}",
        "table{border-collapse:collapse;width:100%;background:#fff;font-size:13px;"
        "box-shadow:0 1px 2px rgba(0,0,0,.06);border-radius:6px;overflow:hidden}",
        "th,td{padding:8px 10px;border-bottom:1px solid #ececee;text-align:left;"
        "vertical-align:top}",
        "th{background:#fafafa;font-weight:600;font-size:12px;color:#4a4a4f}",
        "tr:last-child td{border-bottom:none}",
        "a{color:#0b62d0;text-decoration:none}",
        "ul{margin:6px 0 0;padding-left:18px;font-size:13px}",
        ".note{color:#6b6b70;font-size:12px}",
        "</style></head><body>",
        f"<h1>지원 현황 · {esc(today)}</h1>",
        f"<div class=\"sub\">{esc(len(rows))}건 — {esc(summary)}</div>",
        "<h2>대기 중인 결정</h2>",
    ]
    if pending:
        parts.append("<ul>")
        for row in pending:
            parts.append(f"<li><b>{esc(row.get('company'))} — {esc(row.get('position'))}</b>: "
                         f"{esc(row.get('next_action'))}</li>")
        parts.append("</ul>")
    else:
        parts.append("<div class=\"note\">없음</div>")

    parts += ["<h2>전체</h2>", "<table><tr><th>상태</th><th>회사</th><th>포지션</th>"
              "<th>채널</th><th>지원일</th><th>다음 행동</th></tr>"]
    for row in ordered:
        status = str(row.get("status") or "")
        badge = STATUS_BADGE.get(status, "")
        applied = row.get("applied_at") or "—"
        elapsed = days_since(row.get("applied_at"), today)
        if elapsed is not None:
            applied = f"{applied} (D+{elapsed})"
        position = esc(row.get("position"))
        url = row.get("url")
        if url:
            position = f"<a href=\"{esc(url)}\">{position}</a>"
        parts.append(
            f"<tr><td>{esc(badge + ' ' + status)}</td><td>{esc(row.get('company'))}</td>"
            f"<td>{position}<div class=\"note\">{esc(row.get('notes'))}</div></td>"
            f"<td>{esc(row.get('channel'))}</td><td>{esc(applied)}</td>"
            f"<td>{esc(row.get('next_action'))}</td></tr>")
    parts += ["</table>", "</body></html>"]
    return "\n".join(parts)


def caption(rows: list[dict], today: str) -> str:
    counts = summary_counts(rows)
    pending = [row for row in rows if str(row.get("status")) in NEEDS_ACTION]
    lines = [f"🗂 지원 현황 {today}",
             f"총 {len(rows)}건 · 제출 {counts.get('제출', 0)}건 · 대기 {len(pending)}건"]
    for row in pending[:5]:
        lines.append(f"• {row.get('company')} — {row.get('next_action') or '다음 행동 미정'}")
    return "\n".join(lines)


def telegram_creds(env_path: Path) -> tuple[str, str] | None:
    """(token, chat_id) from KEY=VALUE lines; None when either key is missing.

    Same contract as wanted_collect.telegram_creds — values are never logged.
    """
    if not env_path.exists():
        return None
    token = chat = None
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("PM_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()
        elif line.startswith("PM_BOT_CHAT_ID="):
            chat = line.split("=", 1)[1].strip()
    return (token, chat) if token and chat else None


def send_report_via_telegram(path: Path, text: str, env_path: Path) -> bool:
    """sendDocument via stdlib urllib. Delivery failure never fails the run."""
    creds = telegram_creds(env_path)
    if creds is None:
        log(f"WARNING: Telegram credentials not found in {env_path}; report not sent")
        return False
    token, chat = creds
    boundary = "----apps" + datetime.now().strftime("%H%M%S%f")
    body = bytearray()
    for key, value in (("chat_id", chat), ("caption", text[:1000])):
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n"
                 f"{value}\r\n").encode("utf-8")
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"document\"; "
             f"filename=\"{path.name}\"\r\nContent-Type: text/html; charset=utf-8"
             "\r\n\r\n").encode()
    body += path.read_bytes() + b"\r\n" + f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendDocument", data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            ok = bool(json.loads(resp.read()).get("ok"))
    except Exception as exc:
        log(f"WARNING: telegram sendDocument failed: {TOKEN_IN_URL.sub('bot***', str(exc))}")
        return False
    if not ok:
        log("WARNING: telegram sendDocument returned ok=false; report not confirmed sent")
    return ok


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render the application ledger.")
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--html", action="store_true", help="also render the HTML report")
    parser.add_argument("--telegram", action="store_true",
                        help="send the HTML report to the PM bot (implies --html)")
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV,
                        help=f"env file with PM_BOT_TOKEN / PM_BOT_CHAT_ID (default: {DEFAULT_ENV})")
    args = parser.parse_args(argv)
    if args.telegram:
        args.html = True  # never send without a file

    if not args.ledger.exists():
        log(f"ERROR: ledger not found: {args.ledger}")
        return 1
    rows = load_ledger(args.ledger)
    today = datetime.now(KST).strftime("%Y-%m-%d")

    MARKDOWN.write_text(render_markdown(rows, today), encoding="utf-8")
    log(f"[markdown] {MARKDOWN.relative_to(REPO)} ({len(rows)} rows)")

    if args.html:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report = REPORT_DIR / f"applications-{today}.html"
        report.write_text(render_html(rows, today), encoding="utf-8")
        log(f"[report] {report.relative_to(REPO)} ({report.stat().st_size:,} bytes)")
        if args.telegram and send_report_via_telegram(report, caption(rows, today), args.env):
            log("[telegram] report delivered to the PM bot")
    return 0


if __name__ == "__main__":
    sys.exit(main())
