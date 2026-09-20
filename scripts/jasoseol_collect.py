#!/usr/bin/env python3
"""Daily Jasoseol (자소설닷컴) job-posting collector for the portfolio project.

Pulls experienced job postings matching the profile into docs/jd/_inbox/jasoseol/
and maintains a dedup ledger at docs/jd/_inbox/jasoseol/state.json.

Usage:
  python3 scripts/jasoseol_collect.py [--config PATH] [--inbox-dir PATH]
                                      [--start YYYY-MM-DD] [--days N]
                                      [--limit N] [--dry-run] [--json]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

try:  # package import when tested; direct import when run as a script
    from scripts.shortlist import (
        TRACK_CORE,
        assess_shortlist,
        normalize_track,
        track_label,
    )
    from scripts.state_utils import atomic_write_json, atomic_write_text
except ModuleNotFoundError:  # pragma: no cover - exercised by CLI execution
    from shortlist import (
        TRACK_CORE,
        assess_shortlist,
        normalize_track,
        track_label,
    )
    from state_utils import atomic_write_json, atomic_write_text

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "jasoseol_targets.json"
DEFAULT_INBOX_DIR = REPO_ROOT / "docs" / "jd" / "_inbox" / "jasoseol"

CALENDAR_URL = "https://jasoseol.com/employment/calendar_list.json"
DETAIL_URL = "https://jasoseol.com/employment/get.json"
RECRUIT_BASE_URL = "https://jasoseol.com/recruit"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Referer": "https://jasoseol.com/recruit",
}
HTTP_TIMEOUT = 20


def log(msg: str, to_stderr: bool = False) -> None:
    stream = sys.stderr if to_stderr else sys.stdout
    print(msg, file=stream, flush=True)


def yaml_value(value: Any) -> str:
    """JSON is a YAML subset, so json.dumps is a safe way to quote scalars and lists."""
    return json.dumps(value, ensure_ascii=False)


def read_frontmatter(path: Path) -> dict[str, Any]:
    """Read existing YAML frontmatter if file exists."""
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


def render_markdown(
    posting: dict[str, Any],
    content_body: str = "",
    existing_frontmatter: dict[str, Any] | None = None,
) -> str:
    """Render one posting file: YAML frontmatter + body sections.

    Preserves existing frontmatter fields on rewrite.
    """
    frontmatter = dict(existing_frontmatter or {})

    pid = posting["id"]
    company = posting.get("company", "")
    title = posting.get("title", "")
    track = normalize_track(posting.get("track", TRACK_CORE))
    score = int(posting.get("score", 0))
    verdict = str(posting.get("verdict", ""))
    career_type = str(posting.get("career_type", "경력"))
    start_time = posting.get("start_time")
    end_time = posting.get("end_time")
    url = f"{RECRUIT_BASE_URL}/{pid}"
    apply_url = posting.get("apply_url") or posting.get("employment_page_url") or ""
    sub_positions = (
        posting.get("sub_positions")
        or posting.get("experienced_positions")
        or []
    )
    matched_sub_positions = posting.get("matched_sub_positions") or []

    frontmatter["id"] = pid
    frontmatter["company"] = company
    frontmatter["title"] = title
    frontmatter["track"] = track
    frontmatter["score"] = score
    frontmatter["verdict"] = verdict
    frontmatter["career_type"] = career_type
    frontmatter["start_time"] = start_time
    frontmatter["end_time"] = end_time
    frontmatter["url"] = url
    frontmatter["apply_url"] = apply_url
    frontmatter["sub_positions"] = sub_positions
    frontmatter["experienced_positions"] = sub_positions
    if matched_sub_positions:
        frontmatter["matched_sub_positions"] = matched_sub_positions

    if "first_seen" not in frontmatter and "first_seen" in posting:
        frontmatter["first_seen"] = posting["first_seen"]

    key_order = [
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
        "matched_sub_positions",
        "first_seen",
    ]

    lines = ["---"]
    for k in key_order:
        if k in frontmatter:
            lines.append(f"{k}: {yaml_value(frontmatter[k])}")
    for k, v in frontmatter.items():
        if k not in key_order:
            lines.append(f"{k}: {yaml_value(v)}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title} — {company}")
    lines.append("")
    lines.append(f"- 채용 형태: **{career_type}**")
    lines.append(f"- Track: **{track_label(track)}** ({track})")
    lines.append(f"- 점수 / 판정: **{score}** · {verdict}")
    if end_time:
        lines.append(f"- 접수 마감: {end_time}")
    lines.append(f"- 공고 링크: [{url}]({url})")
    if apply_url:
        lines.append(f"- 접수 링크: [{apply_url}]({apply_url})")
    if matched_sub_positions and matched_sub_positions != sub_positions:
        lines.append(f"- 적합 모집 분야: {', '.join(matched_sub_positions)}")
    if sub_positions:
        lines.append(f"- 모집 분야 (경력): {', '.join(sub_positions)}")
    lines.append("")
    if content_body.strip():
        lines.append("## 상세 내용")
        lines.append("")
        lines.append(content_body.strip())
        lines.append("")
    return "\n".join(lines)


class PoliteSession:
    """Single-threaded HTTP wrapper sleeping delay between calls with bounded retries."""

    def __init__(self, delay: float = 1.0, max_retries: int = 3) -> None:
        self._session = requests.Session()
        self._delay = delay
        self._max_retries = max_retries
        self._first_call = True
        self.n_calls = 0

    def post_json(
        self,
        url: str,
        body: dict | None = None,
        headers: dict | None = None,
    ) -> tuple[dict | None, str | None]:
        """POST JSON body and parse JSON response.

        Returns (parsed_json, error_message).
        """
        hdrs = dict(HEADERS)
        if headers:
            hdrs.update(headers)

        for attempt in range(1, self._max_retries + 1):
            if not self._first_call and self._delay > 0:
                time.sleep(self._delay)
            self._first_call = False
            self.n_calls += 1

            try:
                resp = self._session.post(
                    url, json=body, headers=hdrs, timeout=HTTP_TIMEOUT
                )
            except requests.RequestException as exc:
                err = f"RequestException on {url} (attempt {attempt}/{self._max_retries}): {exc}"
                if attempt == self._max_retries:
                    log(f"    [http] {err}")
                    return None, err
                time.sleep(0.5 * attempt)
                continue

            if resp.status_code != 200:
                err = f"HTTP {resp.status_code} on {url} (attempt {attempt}/{self._max_retries})"
                if 500 <= resp.status_code < 600 and attempt < self._max_retries:
                    time.sleep(0.5 * attempt)
                    continue
                log(f"    [http] {err}")
                return None, err

            try:
                data = resp.json()
                return data, None
            except ValueError as exc:
                err = f"Bad JSON from {url}: {exc}"
                log(f"    [http] {err}")
                return None, err

        return None, "Max retries exceeded"


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"seen": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        log(f"ERROR: {path} unreadable ({exc}); refusing to overwrite the dedup ledger.")
        raise SystemExit(2)
    if not isinstance(state, dict) or not isinstance(state.get("seen"), dict):
        log(f"ERROR: {path} has no valid seen mapping; refusing to overwrite the dedup ledger.")
        raise SystemExit(2)
    return state


def calculate_window(
    start_arg: str | None, days_arg: int | None, default_days: int = 60
) -> tuple[str, str]:
    """Return (start_time_iso, end_time_iso) in 2026-09-01T00:00:00.000+09:00 format."""
    days = days_arg if days_arg is not None else default_days
    kst = timezone(timedelta(hours=9))

    if start_arg:
        if "T" in start_arg:
            try:
                start_dt = datetime.fromisoformat(start_arg)
            except ValueError:
                start_dt = datetime.strptime(start_arg.split("T")[0], "%Y-%m-%d")
        else:
            start_dt = datetime.strptime(start_arg, "%Y-%m-%d")
    else:
        now = datetime.now(kst)
        start_dt = datetime(now.year, now.month, now.day)

    end_dt = start_dt + timedelta(days=days)
    start_str = start_dt.strftime("%Y-%m-%dT00:00:00.000+09:00")
    end_str = end_dt.strftime("%Y-%m-%dT00:00:00.000+09:00")
    return start_str, end_str


def fetch_calendar_list(
    sess: PoliteSession, start_time: str, end_time: str
) -> tuple[list[dict[str, Any]] | None, str | None]:
    """Fetch calendar list from Jasoseol API. Returns (items, error_msg)."""
    body = {"start_time": start_time, "end_time": end_time}
    data, err = sess.post_json(CALENDAR_URL, body=body)
    if data is None:
        return None, err
    if not isinstance(data, dict):
        return None, f"Expected JSON object from {CALENDAR_URL}, got {type(data).__name__}"
    employments = data.get("employment")
    if employments is None or not isinstance(employments, list):
        return None, f"Missing or invalid 'employment' array in response from {CALENDAR_URL}"
    return employments, None


def is_experienced_announcement(announcement: dict[str, Any]) -> bool:
    """Filter stage 1: keep only announcements where any employments sub-item has division == 2."""
    sub_employments = announcement.get("employments") or []
    return any(
        isinstance(sub, dict) and sub.get("division") == 2
        for sub in sub_employments
    )


TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def strip_html(escaped_html: str | None) -> str:
    """Strip HTML tags and collapse whitespace."""
    if not escaped_html:
        return ""
    text = html.unescape(escaped_html)
    text = (
        text.replace("</li>", "\n")
        .replace("</p>", "\n")
        .replace("<br>", "\n")
        .replace("<br/>", "\n")
        .replace("<br />", "\n")
    )
    text = TAG_RE.sub(" ", text)
    return WS_RE.sub(" ", text).strip()


def extract_experienced_sub_positions(detail_data: dict[str, Any]) -> list[str]:
    """Keep only the sub-positions whose division is 2 and return their titles."""
    sub_employments = detail_data.get("employments") or []
    titles: list[str] = []
    for sub in sub_employments:
        if isinstance(sub, dict) and sub.get("division") == 2:
            title = sub.get("field") or sub.get("title") or ""
            title = str(title).strip()
            if title and title not in titles:
                titles.append(title)
    return titles


def fetch_detail(
    sess: PoliteSession, announcement_id: int
) -> tuple[dict[str, Any] | None, str | None]:
    """Fetch announcement detail from Jasoseol get.json endpoint."""
    body = {"employment_company_id": announcement_id}
    data, err = sess.post_json(DETAIL_URL, body=body)
    if data is None:
        return None, err
    if not isinstance(data, dict):
        return None, f"Expected JSON object from {DETAIL_URL} for id {announcement_id}"
    return data, None


def get_or_fetch_detail(
    sess: PoliteSession,
    ann_id: int,
    end_time: str | None,
    cache_dir: Path,
) -> tuple[dict[str, Any] | None, str | None, bool]:
    """Load detail from disk cache if valid, otherwise fetch via PoliteSession and cache on disk.

    Returns (detail_data, error_message, from_cache).
    """
    cache_file = cache_dir / f"{ann_id}.json"
    if cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            if isinstance(cached, dict) and cached.get("end_time") == end_time:
                detail = cached.get("detail")
                if isinstance(detail, dict):
                    return detail, None, True
        except (ValueError, OSError):
            pass

    data, err = fetch_detail(sess, ann_id)
    if data is None:
        return None, err, False

    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        payload = {"id": ann_id, "end_time": end_time, "detail": data}
        atomic_write_json(cache_file, payload)
    except OSError as exc:
        log(f"    [cache {ann_id}] Warning: failed to write cache: {exc}")

    return data, None, False


def assess_announcement(
    announcement: dict[str, Any],
    detail_data: dict[str, Any] | None = None,
    exclude_patterns: list[re.Pattern[str]] | None = None,
    score_threshold: int = 28,
) -> dict[str, Any]:
    """Score announcement using assess_shortlist on experienced sub-positions, body, and company.

    Returns assessment dict with actionable, reason, fit_score, track, and matched_sub_positions.
    """
    title = str(
        (detail_data.get("title") if detail_data else None)
        or announcement.get("title")
        or ""
    )
    company = str(
        (detail_data.get("name") if detail_data else None)
        or announcement.get("name")
        or ""
    )

    if exclude_patterns:
        for pat in exclude_patterns:
            if pat.search(title):
                return {
                    "actionable": False,
                    "reason": "excluded-by-title-pattern",
                    "fit_score": 0,
                    "track": TRACK_CORE,
                    "matched_sub_positions": [],
                }

    if not detail_data:
        # Fallback when detail is not available (e.g. offline dry-run test)
        posting_for_shortlist = {
            "title": title,
            "company": company,
            "department": "",
            "location_raw": "한국",
            "eligibility": "korea",
            "country": "South Korea",
            "body": "",
        }
        shortlist_result = assess_shortlist(posting_for_shortlist)
        fit_score = int(shortlist_result.get("fit_score", 0))
        actionable = bool(shortlist_result.get("actionable")) and (
            fit_score >= score_threshold
        )
        return {
            "actionable": actionable,
            "reason": str(shortlist_result.get("reason", "")),
            "fit_score": fit_score,
            "track": normalize_track(shortlist_result.get("track", TRACK_CORE)),
            "matched_sub_positions": [],
        }

    experienced_subs = extract_experienced_sub_positions(detail_data)
    if not experienced_subs:
        return {
            "actionable": False,
            "reason": "no-experienced-positions",
            "fit_score": 0,
            "track": TRACK_CORE,
            "matched_sub_positions": [],
        }

    body_text = strip_html(detail_data.get("content"))

    # Stage A: Check joined experienced sub-positions
    posting_all = {
        "title": ", ".join(experienced_subs),
        "company": company,
        "department": f"{body_text} {company}".strip(),
        "body": title,
        "location_raw": "한국",
        "eligibility": "korea",
        "country": "South Korea",
    }
    r_all = assess_shortlist(posting_all)

    # Stage B: Check each sub-position individually to isolate matched roles
    matched_subs: list[str] = []
    for sub in experienced_subs:
        r_sub = assess_shortlist({
            "title": sub,
            "company": company,
            "department": f"{body_text} {company}".strip(),
            "body": title,
            "location_raw": "한국",
            "eligibility": "korea",
            "country": "South Korea",
        })
        if r_sub["actionable"]:
            matched_subs.append(sub)

    if r_all["actionable"] and int(r_all.get("fit_score", 0)) >= score_threshold:
        return {
            "actionable": True,
            "reason": str(r_all.get("reason", "actionable")),
            "fit_score": int(r_all.get("fit_score", 0)),
            "track": normalize_track(r_all.get("track", TRACK_CORE)),
            "matched_sub_positions": matched_subs if matched_subs else experienced_subs,
        }

    if matched_subs:
        # Score joined matched sub-positions to avoid generic role interference (e.g. sales in mixed campaign)
        posting_matched = {
            "title": ", ".join(matched_subs),
            "company": company,
            "department": f"{body_text} {company}".strip(),
            "body": title,
            "location_raw": "한국",
            "eligibility": "korea",
            "country": "South Korea",
        }
        r_matched = assess_shortlist(posting_matched)
        fit_score = int(r_matched.get("fit_score", 0))
        actionable = bool(r_matched.get("actionable")) and (
            fit_score >= score_threshold
        )
        return {
            "actionable": actionable,
            "reason": str(r_matched.get("reason", "")),
            "fit_score": fit_score,
            "track": normalize_track(r_matched.get("track", TRACK_CORE)),
            "matched_sub_positions": matched_subs,
        }

    return {
        "actionable": False,
        "reason": str(r_all.get("reason", "")),
        "fit_score": int(r_all.get("fit_score", 0)),
        "track": normalize_track(r_all.get("track", TRACK_CORE)),
        "matched_sub_positions": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect Jasoseol job postings into inbox.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG,
                        help=f"targets config (default: {DEFAULT_CONFIG})")
    parser.add_argument("--inbox-dir", type=Path, default=DEFAULT_INBOX_DIR,
                        help=f"inbox directory (default: {DEFAULT_INBOX_DIR})")
    parser.add_argument("--start", type=str, default=None,
                        help="window start date (YYYY-MM-DD or ISO string, default: today)")
    parser.add_argument("--days", type=int, default=None,
                        help="window lookahead days (default from config or 60)")
    parser.add_argument("--limit", type=int, default=None,
                        help="cap detail fetches (smoke test)")
    parser.add_argument("--dry-run", action="store_true",
                        help="summary only; no detail fetches, no files written")
    parser.add_argument("--json", action="store_true",
                        help="print run summary as JSON")
    args = parser.parse_args(argv)
    emit = lambda msg: log(msg, to_stderr=args.json)

    config_path = args.config
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            emit(f"ERROR: failed to load config {config_path}: {exc}")
            return 1
    else:
        config = {}

    lookahead_days = int(config.get("lookahead_days", config.get("days", 60)))
    score_threshold = int(config.get("score_threshold", config.get("min_score", 28)))
    exclude_patterns = [
        re.compile(p, re.IGNORECASE) for p in config.get("exclude_title_patterns", [])
    ]
    watchlist_companies = set(config.get("company_watchlist", []))
    delay = float(config.get("request_delay_seconds", 1.0))

    inbox_dir = args.inbox_dir
    state_path = inbox_dir / "state.json"
    state = load_state(state_path)
    seen = state["seen"]

    start_time, end_time = calculate_window(args.start, args.days, lookahead_days)
    sess = PoliteSession(delay=delay)
    failures: list[str] = []

    # ---- Phase 1: Fetch calendar list ---------------------------------------
    emit(f"[fetch] querying Jasoseol calendar from {start_time} to {end_time}...")
    calendar_items, fetch_err = fetch_calendar_list(sess, start_time, end_time)
    if calendar_items is None:
        failures.append(f"Calendar fetch failed: {fetch_err}")
        emit(f"ERROR: calendar fetch failed: {fetch_err}")
        summary = {
            "fetched": 0,
            "experienced": 0,
            "actionable": 0,
            "new": 0,
            "refreshed": 0,
            "failures": failures,
        }
        if args.json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            emit(f"[summary] fetched=0 experienced=0 actionable=0 new=0 failures={len(failures)}")
        return 1

    n_fetched = len(calendar_items)

    # ---- Phase 2: Stage 1 filter (division == 2) -----------------------------
    experienced_items = [
        item for item in calendar_items if is_experienced_announcement(item)
    ]
    n_experienced = len(experienced_items)

    # ---- Phase 3: Detail fetch & disk cache ----------------------------------
    cache_dir = inbox_dir / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    announcements_with_detail: list[tuple[dict[str, Any], dict[str, Any]]] = []
    n_cached = 0
    n_fetched_detail = 0

    emit(f"[detail] gathering details for {n_experienced} experienced announcements...")
    for idx, item in enumerate(experienced_items, 1):
        ann_id = int(item["id"])
        item_end_time = item.get("end_time")

        if args.dry_run and not (cache_dir / f"{ann_id}.json").exists():
            continue

        detail_data, err, from_cache = get_or_fetch_detail(
            sess, ann_id, item_end_time, cache_dir
        )
        if detail_data is None:
            err_msg = f"Detail fetch failed for {ann_id}: {err}"
            failures.append(err_msg)
            emit(f"    [detail {idx}/{n_experienced}] id={ann_id} WARNING: {err} (skipped)")
            continue

        if from_cache:
            n_cached += 1
        else:
            n_fetched_detail += 1
            emit(f"    [detail {idx}/{n_experienced}] id={ann_id} ({item.get('name')}) fetched")

        announcements_with_detail.append((item, detail_data))

    emit(
        f"[detail] completed: {len(announcements_with_detail)}/{n_experienced} ready "
        f"({n_cached} cached, {n_fetched_detail} fetched, {len(failures)} skipped)"
    )

    # ---- Phase 4: Stage 2 filter & scoring (assess_shortlist) ----------------
    actionable_candidates: list[
        tuple[dict[str, Any], dict[str, Any], dict[str, Any]]
    ] = []

    if announcements_with_detail:
        for item, detail_data in announcements_with_detail:
            assessment = assess_announcement(
                item, detail_data, exclude_patterns, score_threshold
            )
            if assessment["actionable"]:
                actionable_candidates.append((item, detail_data, assessment))
    elif args.dry_run:
        for item in experienced_items:
            assessment = assess_announcement(
                item, None, exclude_patterns, score_threshold
            )
            if assessment["actionable"]:
                actionable_candidates.append((item, {}, assessment))

    n_actionable = len(actionable_candidates)
    emit(f"[filter] fetched={n_fetched} experienced={n_experienced} actionable={n_actionable}")

    # Watchlist check
    for item, _, _ in actionable_candidates:
        co = str(item.get("name") or "")
        if co in watchlist_companies:
            emit(f"  [watchlist] 🚨 Watchlist company announcement detected: {co} - {item.get('title')}")

    # Identify which actionable postings need fetching / updating
    today_str = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    todo: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any], bool]] = []  # (item, detail, assess, is_new)

    for item, detail_data, assess in actionable_candidates:
        jid = str(item["id"])
        item_end_time = item.get("end_time")
        if jid not in seen:
            todo.append((item, detail_data, assess, True))
        else:
            prev_end_time = seen[jid].get("end_time")
            if item_end_time != prev_end_time:
                todo.append((item, detail_data, assess, False))

    if args.limit is not None:
        todo = todo[: args.limit]

    n_new = 0
    n_refreshed = 0

    write_failures: list[str] = []
    if args.dry_run:
        n_new = sum(1 for _, _, _, is_new in todo if is_new)
        n_refreshed = sum(1 for _, _, _, is_new in todo if not is_new)
        emit(
            f"[dry-run] actionable={n_actionable} would_write_or_update={len(todo)} "
            f"(new={n_new}, refreshed={n_refreshed}); no files written."
        )
    else:
        for item, detail_data, assess, is_new in todo:
            ann_id = int(item["id"])
            jid_str = str(ann_id)

            sub_titles = extract_experienced_sub_positions(detail_data)
            matched_subs = assess.get("matched_sub_positions") or sub_titles
            content_body = str(detail_data.get("content") or "")
            apply_url = str(detail_data.get("employment_page_url") or "")

            posting_record = {
                "id": ann_id,
                "company": str(detail_data.get("name") or item.get("name") or ""),
                "title": str(detail_data.get("title") or item.get("title") or ""),
                "track": assess["track"],
                "score": assess["fit_score"],
                "verdict": assess["reason"],
                "career_type": "경력",
                "start_time": item.get("start_time") or detail_data.get("start_time"),
                "end_time": item.get("end_time") or detail_data.get("end_time"),
                "apply_url": apply_url,
                "sub_positions": sub_titles,
                "experienced_positions": sub_titles,
                "matched_sub_positions": matched_subs,
                "first_seen": seen.get(jid_str, {}).get("first_seen", today_str),
            }

            md_path = inbox_dir / f"{ann_id}.md"
            existing_frontmatter = read_frontmatter(md_path)
            md_content = render_markdown(
                posting_record,
                content_body=content_body,
                existing_frontmatter=existing_frontmatter,
            )

            try:
                atomic_write_text(md_path, md_content)
            except OSError as exc:
                err_msg = f"Failed writing {md_path}: {exc}"
                emit(f"    [write {ann_id}] ERROR: {exc}")
                write_failures.append(err_msg)
                failures.append(err_msg)
                continue

            seen[jid_str] = {
                "first_seen": posting_record["first_seen"],
                "company": posting_record["company"],
                "title": posting_record["title"],
                "end_time": posting_record["end_time"],
                "track": posting_record["track"],
                "score": posting_record["score"],
                "verdict": posting_record["verdict"],
                "sub_positions": sub_titles,
                "matched_sub_positions": matched_subs,
            }

            if is_new:
                n_new += 1
                emit(f"[write:new] {ann_id}.md — {posting_record['title']} @ {posting_record['company']}")
            else:
                n_refreshed += 1
                emit(f"[write:refreshed] {ann_id}.md (end_time updated) — {posting_record['title']} @ {posting_record['company']}")

        try:
            atomic_write_json(state_path, state)
        except OSError as exc:
            err_msg = f"Failed writing ledger {state_path}: {exc}"
            emit(f"ERROR: {err_msg}")
            failures.append(err_msg)
            return 1

    summary = {
        "fetched": n_fetched,
        "experienced": n_experienced,
        "actionable": n_actionable,
        "new": n_new,
        "refreshed": n_refreshed,
        "failures": failures,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        emit(f"[summary] fetched={n_fetched} experienced={n_experienced} actionable={n_actionable} new={n_new} refreshed={n_refreshed}")
        if failures:
            emit(f"[summary] failures encountered ({len(failures)}):")
            for f in failures:
                emit(f"  - {f}")
        if actionable_candidates:
            emit("[actionable postings]")
            for item, detail_data, assess in actionable_candidates:
                co = str(detail_data.get("name") or item.get("name") or "")
                ti = str(detail_data.get("title") or item.get("title") or "")
                sc = assess["fit_score"]
                dl = item.get("end_time") or detail_data.get("end_time") or ""
                m_subs = assess.get("matched_sub_positions") or []
                emit(f"  - [{item['id']}] {co} | {ti} | score={sc} | deadline={dl}")
                if m_subs:
                    emit(f"      matched: {', '.join(m_subs)}")

    if write_failures and len(write_failures) == len(todo) and len(todo) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
