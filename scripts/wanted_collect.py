#!/usr/bin/env python3
"""Daily Wanted (www.wanted.co.kr) job-posting collector for the portfolio project.

Pulls job postings matching the configured keywords into the staging inbox
docs/jd/_inbox/wanted/ so they can be mapped onto existing portfolio cases.
Also tracks a company watchlist (conglomerates that normally recruit through
their own portals) and shouts in the digest the day one of them posts on Wanted.

API behavior (verified 2026-08-18, plain HTTP, no auth):
  - Page 1:  GET /api/chaos/search/v1/results  (query, tab, limit) - serves the
    first page only; its `offset` param is IGNORED, so re-querying with a higher
    offset returns page 1 again.
  - Page 2+: follow `positions.links.next`, which points at
    GET /api/chaos/search/v1/position?...&offset=N&sort=... and returns a flat
    {"data": [...], "links": {...}, "total_count": N}. The server caps every
    page at 12 items regardless of the requested limit.
  - Detail:  GET /api/v4/jobs/{id} (chaos fallback on non-200).

Usage:
  python3 scripts/wanted_collect.py [--config PATH] [--dry-run] [--limit N]
                                    [--html] [--telegram [--env ENV_PATH]]
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.request
from datetime import date, datetime
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "wanted_targets.json"
INBOX_DIR = REPO_ROOT / "docs" / "jd" / "_inbox" / "wanted"
REPORT_DIR = INBOX_DIR / "report"
PM_ENV = Path("/home/window11/project-manager/.env")

BASE = "https://www.wanted.co.kr"
RESULTS_URL = BASE + "/api/chaos/search/v1/results"
JOB_URL = BASE + "/api/v4/jobs/{job_id}"
CHAOS_JOB_URL = BASE + "/api/chaos/jobs/v4/{job_id}/details"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.wanted.co.kr/search",
}
PAGE_SIZE = 12  # the server caps every search page at 12 items
HTTP_TIMEOUT = 20

# detail field -> markdown section heading
JD_SECTIONS = [
    ("intro", "소개"),
    ("main_tasks", "주요업무"),
    ("requirements", "자격요건"),
    ("preferred_points", "우대사항"),
    ("benefits", "혜택"),
    ("hire_rounds", "채용절차"),
]


def log(msg: str) -> None:
    print(msg, flush=True)


class PoliteSession:
    """Single-threaded HTTP wrapper sleeping `delay` between every call."""

    def __init__(self, delay: float) -> None:
        self._session = requests.Session()
        self._delay = delay
        self._first_call = True
        self.n_calls = 0

    def get_json(self, url: str, params: dict | None = None):
        """GET and parse JSON. Returns None on non-200 / parse error (logged, not fatal)."""
        if not self._first_call:
            time.sleep(self._delay)
        self._first_call = False
        self.n_calls += 1
        try:
            resp = self._session.get(url, params=params, headers=HEADERS, timeout=HTTP_TIMEOUT)
        except requests.RequestException as e:
            log(f"    [http] {url} -> ERROR {e}")
            return None
        if resp.status_code != 200:
            log(f"    [http] {url} -> HTTP {resp.status_code}")
            return None
        try:
            return resp.json()
        except ValueError as e:
            log(f"    [http] {url} -> bad JSON: {e}")
            return None


def search_positions(sess: PoliteSession, keyword: str, cap: int):
    """Collect up to `cap` postings for one keyword, following links.next.

    Returns (items, total_count), or (None, None) when the first page itself fails.
    """
    items: list[dict] = []
    total = None
    seen_ids: set[int] = set()
    next_url: str | None = None  # None -> first page via the results endpoint
    while len(items) < cap:
        if next_url is None:
            data = sess.get_json(RESULTS_URL, {"query": keyword, "tab": "position",
                                               "limit": PAGE_SIZE, "offset": 0})
            block = (data or {}).get("positions") or {}
            if data is None:
                if not items:
                    return None, None  # keyword search failed outright
                break  # first page failed after earlier pages; keep what we have
        else:
            data = sess.get_json(next_url)
            if data is None:
                break  # later page failed; keep what we have
            block = data
        if total is None:
            total = block.get("total_count")
            if total is not None:
                # total_count is the API's relevance-scoped count; deep pages
                # beyond it backfill loosely-matched jobs, so respect it.
                cap = min(cap, int(total))
        page = block.get("data") or []
        fresh = [it for it in page if it["id"] not in seen_ids]
        if not fresh:
            break  # repeated page (or empty) -> stop defensively
        seen_ids.update(it["id"] for it in fresh)
        items.extend(fresh)
        next_url = ((block.get("links") or {}).get("next")) or None
        if next_url:
            next_url = BASE + next_url
    return items[:cap], total


def fetch_detail(sess: PoliteSession, job_id: int):
    """Fetch the full JD payload for one posting. v4 first, chaos fallback on non-200."""
    data = sess.get_json(JOB_URL.format(job_id=job_id))
    if data is not None and data.get("job"):
        return data["job"]
    data = sess.get_json(CHAOS_JOB_URL.format(job_id=job_id))
    if data is None:
        return None
    # chaos shape: {"data": {"job": {...}}}
    job = (data.get("data") or {}).get("job")
    if not job:
        log(f"    [detail {job_id}] no job object in fallback response")
        return None
    return job


def check_watchlist(sess: PoliteSession, names: list[str]) -> dict[str, int | None]:
    """confirmed_position_count per watchlist company. None = no exact company match."""
    result: dict[str, int | None] = {}
    for name in names:
        data = sess.get_json(RESULTS_URL, {"query": name, "tab": "all",
                                          "limit": 20, "offset": 0})
        companies = ((data or {}).get("companies") or {}).get("data") or []
        match = next((c for c in companies if c.get("name") == name), None)
        result[name] = match.get("confirmed_position_count") if match else None
    return result


def slugify(name: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z가-힣]+", "-", name.strip()).strip("-")
    return slug or "unknown"


def yaml_value(value) -> str:
    """JSON is a YAML subset, so json.dumps is a safe way to quote scalars and lists."""
    return json.dumps(value, ensure_ascii=False)


def skill_tag_titles(skill_tags) -> list[str]:
    titles = []
    for tag in skill_tags or []:
        if isinstance(tag, dict):
            title = tag.get("title") or tag.get("name")
            if title:
                titles.append(str(title))
        elif tag:
            titles.append(str(tag))
    return titles


def render_hire_rounds(value) -> str | None:
    """hire_rounds is usually a list of round dicts; render whatever shape robustly."""
    if not value:
        return None
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, list):
        lines = []
        for i, item in enumerate(value, 1):
            if isinstance(item, dict):
                # keep the human-readable parts, drop ids
                parts = [str(v) for k, v in item.items()
                         if k in ("title", "name", "description", "step", "process")
                         and v not in (None, "")]
                line = " · ".join(parts) or json.dumps(item, ensure_ascii=False)
            else:
                line = str(item)
            lines.append(f"{i}. {line}")
        return "\n".join(lines) if lines else None
    return json.dumps(value, ensure_ascii=False)


def job_location(job: dict, fallback: str) -> str:
    address = job.get("address") or {}
    return address.get("full_location") or address.get("location") or fallback or ""


def render_markdown(job: dict, meta: dict) -> str:
    """One posting file: YAML frontmatter + JD sections (empty sections omitted)."""
    job_id = job.get("id", meta["id"])
    company = (job.get("company") or {}).get("name") or meta["company"]
    position = job.get("position") or meta["position"]
    detail = job.get("detail") or {}
    skills = skill_tag_titles(job.get("skill_tags"))

    lines = ["---"]
    lines.append(f"wanted_id: {yaml_value(job_id)}")
    lines.append(f"company: {yaml_value(company)}")
    lines.append(f"position: {yaml_value(position)}")
    lines.append(f"url: {yaml_value(f'https://www.wanted.co.kr/wd/{job_id}')}")
    lines.append(f"location: {yaml_value(job_location(job, meta.get('location', '')))}")
    lines.append(f"skill_tags: {yaml_value(skills)}")
    lines.append(f"due_time: {yaml_value(job.get('due_time'))}")
    lines.append(f"first_seen: {yaml_value(meta['first_seen'])}")
    lines.append(f"matched_keywords: {yaml_value(sorted(meta['matched_keywords']))}")
    lines.append("---")

    for field, heading in JD_SECTIONS:
        if field == "hire_rounds":
            body = render_hire_rounds(detail.get(field))
        else:
            body = (detail.get(field) or "").strip()
        if not body:
            continue
        lines.append("")
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(body)
    lines.append("")
    return "\n".join(lines)


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"seen": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        log(f"ERROR: {path} unreadable ({e}); refusing to overwrite the dedup ledger.")
        raise SystemExit(2)
    state.setdefault("seen", {})
    return state


def posting_file_location(jid: int) -> str:
    """Deep-page search results lack address.location, so recover the region
    from the posting file's frontmatter (written from the detail payload)."""
    for path in INBOX_DIR.glob(f"{jid}-*.md"):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        if not lines or lines[0].strip() != "---":
            continue
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.startswith("location:"):
                try:
                    value = json.loads(line.split(":", 1)[1].strip())
                    return value if isinstance(value, str) else ""
                except ValueError:
                    return ""
    return ""


def write_digest(digest_dir: Path, today: str, watchlist: dict, fresh: list[dict]) -> None:
    """Daily digest: non-zero watchlist alert at the very top, then watchlist + new postings."""
    alerts = [f"{name} → {count}건" for name, count in watchlist.items() if count]
    lines = []
    if alerts:
        lines.append(f"> 🚨 **대기업 와치리스트 공고 감지 ({today})**: " + " · ".join(alerts))
        lines.append("> **원티드에 직접 공고가 떴습니다. 즉시 확인 후 `docs/jd/{회사}/` 승격 검토.**")
        lines.append("")
    lines.append(f"# 원티드 수집 다이제스트 — {today}")
    lines.append("")
    lines.append("## 기업 와치리스트 상태 (원티드 내 공고 수)")
    lines.append("")
    lines.append("| 기업 | 공고 수 |")
    lines.append("|---|---:|")
    for name, count in watchlist.items():
        shown = f"{count}" if count is not None else "*(원티드 기업 매칭 없음)*"
        lines.append(f"| {name} | {shown} |")
    lines.append("")
    lines.append(f"## 신규 공고 ({len(fresh)}건)")
    lines.append("")
    if fresh:
        lines.append("| 회사 | 포지션 | 지역 | 링크 |")
        lines.append("|---|---|---|---|")
        for item in fresh:
            lines.append(
                f"| {item['company']} | {item['position']} | {item['location'] or '-'} "
                f"| [#{item['id']}](https://www.wanted.co.kr/wd/{item['id']}) |"
            )
    else:
        lines.append("오늘 새로 수집된 공고는 없습니다. (dedup 정상 동작)")
    lines.append("")
    digest_dir.mkdir(parents=True, exist_ok=True)
    (digest_dir / f"{today}.md").write_text("\n".join(lines), encoding="utf-8")


# ── HTML daily report + Telegram delivery ───────────────────────────────────
# Rendered from the same `fresh_today` set the markdown digest lists, so the
# two never disagree. The page is self-contained (inline CSS only, no JS) and
# mobile-first: the PM reads it as a Telegram document on a phone.

# A posting is 핵심 when its title matches manufacturing / AI / PM / engineering
# intent. Substring match, case-insensitive: Korean titles glue Latin tokens to
# Hangul ("기술PM"), where a \b word boundary would never fire.
CORE_TITLE_PATTERN = re.compile("|".join(re.escape(k) for k in [
    "제조", "자율", "스마트팩토리", "생산", "공정", "설비", "PM",
    "프로젝트 매니저", "product manager", "프로덕트", "하드웨어", "전장",
    "임베디드", "기구", "로봇", "모빌리티", "technical project",
]), re.IGNORECASE)

MAX_MISC_CARDS = 100   # non-핵심 cards rendered; the rest are counted, not shown
MAX_SKILL_CHIPS = 8
EXCERPT_MAX_CHARS = 220

REPORT_CSS = """
:root{--bg:#f4f5f7;--panel:#ffffff;--panel2:#eef0f3;--ink:#1c212b;--dim:#59637a;
--faint:#8b94a8;--line:#e2e5eb;--accent:#2a63e7;--accent-ink:#ffffff;
--alert-bg:#fdecec;--alert-border:#f2b8b5;--alert-ink:#9c1c1c;--alert-dim:#8a3030;
--chip-bg:#eef0f4}
@media (prefers-color-scheme:dark){:root{--bg:#0f1319;--panel:#181d27;--panel2:#202634;
--ink:#e8ebf2;--dim:#a3adc2;--faint:#6e7890;--line:#2a3140;--accent:#5b8cff;
--accent-ink:#0d1220;--alert-bg:#3a1518;--alert-border:#7a2a2f;--alert-ink:#ff9d9d;
--alert-dim:#d98c8c;--chip-bg:#242b3a}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.6 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif}
.wrap{max-width:680px;margin:0 auto;padding:20px 16px 56px}
h1{font-size:22px;margin:0;letter-spacing:-.02em}
.sub{color:var(--dim);font-size:13.5px;margin:3px 0 0}
h2{font-size:17px;margin:30px 0 12px;letter-spacing:-.01em}
.group{font-size:13.5px;color:var(--dim);font-weight:700;margin:16px 0 10px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:16px 0 2px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.stat .k{display:block;font-size:11.5px;color:var(--faint);letter-spacing:.04em}
.stat .v{font-size:20px;font-weight:700}
.stat.core .v{color:var(--accent)}
.alert{background:var(--alert-bg);border-bottom:1px solid var(--alert-border);padding:14px 16px}
.alert .in{max-width:680px;margin:0 auto}
.alert-title{color:var(--alert-ink);font-weight:800;font-size:15.5px}
.alert-body{color:var(--alert-dim);font-size:13.5px;margin-top:3px}
.quiet{color:var(--faint);font-size:13.5px;background:var(--panel);
border:1px dashed var(--line);border-radius:10px;padding:12px 14px;margin:0}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{width:100%;border-collapse:collapse;font-size:14px;min-width:300px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}
thead th{color:var(--faint);font-size:11.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase}
tbody th{font-weight:500}
td.num,th.num{text-align:right}
td.hit{color:var(--alert-ink);font-weight:800}
td.zero{color:var(--faint)}
td.none{color:var(--faint);font-size:12.5px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:14px 16px;margin-bottom:12px}
.card.core{border-left:4px solid var(--accent)}
.card .pos{margin:0;font-size:16.5px;font-weight:700;line-height:1.4}
.card .co{margin:4px 0 0;color:var(--dim);font-size:13.5px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.chip{font-size:12px;padding:3px 9px;border-radius:999px;background:var(--chip-bg);
color:var(--dim);white-space:nowrap}
.chip-more{font-weight:700}
.card .req{margin:10px 0 0;color:var(--dim);font-size:13.5px;line-height:1.55}
.btn{display:block;margin:12px 0 0;padding:11px;border-radius:9px;background:var(--accent);
color:var(--accent-ink);text-align:center;text-decoration:none;font-weight:700;font-size:14.5px}
details.more{background:var(--panel);border:1px solid var(--line);border-radius:12px;
margin-top:14px;overflow:hidden}
details.more>summary{cursor:pointer;padding:14px 16px;font-weight:700;font-size:15px;
list-style:none;display:flex;justify-content:space-between;align-items:center;min-height:48px}
details.more>summary::-webkit-details-marker{display:none}
details.more>summary::after{content:"\\25BE";color:var(--faint);font-size:13px}
details.more[open]>summary::after{content:"\\25B4"}
details.more[open]>summary{border-bottom:1px solid var(--line)}
.details-body{padding:12px 12px 4px}
.foot{margin-top:40px;color:var(--faint);font-size:12px;text-align:center}
a{color:var(--accent)}
"""


def is_core_position(title: str) -> bool:
    return bool(CORE_TITLE_PATTERN.search(title or ""))


def shorten_location(loc: str) -> str:
    """'서울 강남구 테헤란로 317, 18층' -> '서울 강남구'. Street detail is noise on a phone."""
    tokens = (loc or "").strip().split()
    if not tokens:
        return ""
    if len(tokens) > 1 and re.fullmatch(r"[가-힣]+[시군구]", tokens[1]):
        return f"{tokens[0]} {tokens[1]}"
    return tokens[0]


def read_posting_extras(jid: int) -> tuple[list[str], str]:
    """(skill_tags, 자격요건 excerpt) for one posting, read back from its file.

    The state ledger keeps only id/company/position/location; what the HTML
    card shows beyond that lives in the posting markdown the detail phase
    wrote. Best effort: a missing/unreadable file yields empty extras, and the
    card still renders from ledger data.
    """
    for path in INBOX_DIR.glob(f"{jid}-*.md"):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        skills: list[str] = []
        if lines and lines[0].strip() == "---":
            for line in lines[1:]:
                if line.strip() == "---":
                    break
                if line.startswith("skill_tags:"):
                    try:
                        value = json.loads(line.split(":", 1)[1])
                        if isinstance(value, list):
                            skills = [str(t) for t in value]
                    except ValueError:
                        pass
        excerpt: list[str] = []
        in_requirements = False
        for line in lines:
            if line.startswith("## "):
                if in_requirements:
                    break
                in_requirements = line[3:].strip() == "자격요건"
                continue
            if in_requirements and line.strip():
                excerpt.append(line.strip())
                if len(excerpt) == 3:
                    break
        text = " ".join(excerpt)
        if len(text) > EXCERPT_MAX_CHARS:
            text = text[: EXCERPT_MAX_CHARS - 1].rstrip() + "…"
        return skills, text
    return [], ""


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def skill_chips(skills: list[str]) -> str:
    if not skills:
        return ""
    chips = [f'<span class="chip">{esc(t)}</span>' for t in skills[:MAX_SKILL_CHIPS]]
    hidden = len(skills) - MAX_SKILL_CHIPS
    if hidden > 0:
        chips.append(f'<span class="chip chip-more">+{hidden}</span>')
    return f'<div class="chips">{"".join(chips)}</div>'


def report_card(posting: dict, core: bool) -> str:
    loc = shorten_location(posting.get("location", ""))
    meta = esc(posting["company"]) + (f" · {esc(loc)}" if loc else "")
    parts = [f'<article class="card{" core" if core else ""}">']
    parts.append(f'<h3 class="pos">{esc(posting["position"])}</h3>')
    parts.append(f'<p class="co">{meta}</p>')
    parts.append(skill_chips(posting.get("skills") or []))
    if posting.get("excerpt"):
        parts.append(f'<p class="req">{esc(posting["excerpt"])}</p>')
    parts.append(f'<a class="btn" href="https://www.wanted.co.kr/wd/{posting["id"]}">'
                 "원티드에서 보기</a>")
    parts.append("</article>")
    return "".join(parts)


def render_html_report(today: str, watchlist: dict, fresh: list[dict],
                       total_seen: int) -> str:
    """Self-contained daily report page: watchlist first, then core-first cards.

    The same `fresh` set the markdown digest lists — on a quiet day it is empty
    and the page still renders, watchlist included.
    """
    posts = []
    for p in fresh:
        skills, excerpt = read_posting_extras(p["id"])
        posts.append({**p, "skills": skills, "excerpt": excerpt})
    core = [p for p in posts if is_core_position(p["position"])]
    total_misc = sum(1 for p in posts if not is_core_position(p["position"]))
    omitted = max(0, total_misc - MAX_MISC_CARDS)
    misc = [p for p in posts if not is_core_position(p["position"])][:MAX_MISC_CARDS]
    alerts = [(name, count) for name, count in watchlist.items() if count]

    body: list[str] = []
    if alerts:
        alert_names = " · ".join(f"{esc(name)} {count}건" for name, count in alerts)
        body.append(
            '<div class="alert" role="alert"><div class="in">'
            '<div class="alert-title">🚨 대기업 와치리스트 공고 감지</div>'
            f'<div class="alert-body">{alert_names} — 원티드에 대기업 공고가 직접 떴습니다. '
            "즉시 확인 후 docs/jd/{회사}/ 승격을 검토하세요.</div></div></div>")
    body.append('<main class="wrap">')
    body.append("<h1>원티드 채용 리포트</h1>")
    body.append(f'<p class="sub">{esc(today)} · 오늘의 신규 공고</p>')
    body.append(
        '<div class="stats">'
        f'<div class="stat"><span class="k">신규</span><span class="v">{len(posts)}건</span></div>'
        f'<div class="stat core"><span class="k">핵심</span>'
        f'<span class="v">{len(core)}건</span></div>'
        f'<div class="stat"><span class="k">누적</span>'
        f'<span class="v">{total_seen}건</span></div>'
        "</div>")

    body.append("<h2>기업 와치리스트</h2>")
    if alerts:
        rows = []
        for name, count in watchlist.items():
            if count:
                cell = f'<td class="num hit">{count}건 🚨</td>'
            elif count == 0:
                cell = '<td class="num zero">0건</td>'
            else:
                cell = '<td class="num none">집계 안 됨</td>'
            rows.append(f'<tr><th scope="row">{esc(name)}</th>{cell}</tr>')
        body.append('<div class="scroll"><table><thead><tr><th>기업</th>'
                    f'<th class="num">원티드 공고</th></tr></thead><tbody>{"".join(rows)}'
                    "</tbody></table></div>")
    else:
        zeros = sum(1 for c in watchlist.values() if c == 0)
        unmatched = sum(1 for c in watchlist.values() if c is None)
        quiet = (f"와치리스트 비제로 기업 없음 — 대기업 신규 없음 ({zeros}개 기업 0건"
                 + (f" · {unmatched}개 기업 원티드 매칭 없음" if unmatched else "")
                 + ").")
        body.append(f'<p class="quiet">{quiet}</p>')

    body.append("<h2>신규 공고</h2>")
    if not posts:
        body.append('<p class="quiet">오늘 새로 수집된 공고는 없습니다. (dedup 정상 동작)</p>')
    else:
        if core:
            body.append(f'<h3 class="group">핵심 {len(core)}건</h3>')
            body.extend(report_card(p, True) for p in core)
        if misc:
            omitted_note = f" · {omitted}건 생략" if omitted else ""
            body.append(f"<details class=\"more\"><summary>기타 신규 공고 "
                        f"{total_misc}건{omitted_note}</summary><div class=\"details-body\">")
            body.extend(report_card(p, False) for p in misc)
            if omitted:
                body.append(f'<p class="quiet">리포트 크기 상한(기타 {MAX_MISC_CARDS}건)으로 '
                            f"{omitted}건은 표시에서 뺐습니다. 전체 목록은 digest를 참고하세요.</p>")
            body.append("</div></details>")
    body.append(f'<footer class="foot">scripts/wanted_collect.py 자동 생성 · '
                f"누적 {total_seen}공고 추적 중 · {datetime.now().strftime('%H:%M')} 생성</footer>")
    body.append("</main>")

    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>원티드 채용 리포트 {esc(today)}</title>"
        f"<style>{REPORT_CSS}</style></head><body>{''.join(body)}</body></html>")


def build_caption(today: str, watchlist: dict, n_new: int, n_core: int,
                  total_seen: int) -> str:
    alerts = " · ".join(f"{name} {count}건" for name, count in watchlist.items() if count)
    return (f"📋 원티드 채용 리포트 {today}\n"
            f"신규 {n_new}건 (핵심 {n_core}건) · 누적 {total_seen}건\n"
            f"⚠️ 워치리스트: {alerts if alerts else '대기업 신규 없음'}")


def telegram_creds(env_path: Path) -> tuple[str, str] | None:
    """(token, chat_id) from KEY=VALUE lines; None when either key is missing.

    The values are never logged, printed, or written anywhere.
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


# telegram error strings can embed the request URL, which embeds the bot token
TOKEN_IN_URL = re.compile(r"bot\d+:[A-Za-z0-9_-]+")


def send_report_via_telegram(path: Path, caption: str, env_path: Path) -> bool:
    """sendDocument via stdlib urllib — the same multipart construction as
    sns-studio's studio_dashboard.send_document. `chat_id` rides in the form
    body as a string, which is what sendDocument expects.

    Returns False on any failure. The collection run has already succeeded by
    the time this is called, so a delivery problem must never fail the run.
    """
    creds = telegram_creds(env_path)
    if creds is None:
        log(f"WARNING: Telegram credentials not found in {env_path}; report not sent "
            "(the collection run itself succeeded)")
        return False
    token, chat = creds
    boundary = "----wanted" + datetime.now().strftime("%H%M%S%f")
    body = bytearray()
    for key, value in (("chat_id", chat), ("caption", caption[:1000])):
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect Wanted job postings into the staging inbox.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG,
                        help=f"targets config (default: {DEFAULT_CONFIG})")
    parser.add_argument("--dry-run", action="store_true",
                        help="search-level summary only; no detail fetches, no files")
    parser.add_argument("--limit", type=int, default=None,
                        help="cap detail fetches (smoke test)")
    parser.add_argument("--html", action="store_true",
                        help="also render report/YYYY-MM-DD.html for today's new postings")
    parser.add_argument("--telegram", action="store_true",
                        help="render the report (implies --html) and send it to the PM bot")
    parser.add_argument("--env", type=Path, default=PM_ENV,
                        help=f"env file with PM_BOT_TOKEN / PM_BOT_CHAT_ID "
                             f"(default: {PM_ENV})")
    args = parser.parse_args()
    if args.telegram:
        args.html = True  # --telegram implies --html; never send without a file

    config = json.loads(args.config.read_text(encoding="utf-8"))
    keywords = config["keywords"]
    watchlist_names = config["company_watchlist"]
    exclude_patterns = [re.compile(p) for p in config["exclude_title_patterns"]]
    cap = int(config["per_keyword_cap"])
    delay = float(config["request_delay_seconds"])

    state_path = INBOX_DIR / "state.json"
    digest_dir = INBOX_DIR / "digest"
    postings_dir = INBOX_DIR
    state = load_state(state_path)

    sess = PoliteSession(delay)
    today = date.today().isoformat()

    # ---- phase 1: keyword searches -> union by job id -----------------------
    union: dict[int, dict] = {}
    failed_keywords: list[str] = []
    for kw in keywords:
        items, total = search_positions(sess, kw, cap)
        if items is None:
            failed_keywords.append(kw)
            log(f"[search] {kw!r}: FAILED")
            continue
        for item in items:
            jid = item["id"]
            entry = union.setdefault(jid, {
                "id": jid,
                "position": item.get("position", ""),
                "company": (item.get("company") or {}).get("name", ""),
                "location": (item.get("address") or {}).get("location", ""),
                "matched_keywords": set(),
            })
            entry["matched_keywords"].add(kw)
        log(f"[search] {kw!r}: total={total} fetched={len(items)} "
            f"(union now {len(union)})")

    if len(failed_keywords) == len(keywords):
        log("ERROR: every keyword search failed - API down or response shape changed.")
        return 1
    if failed_keywords:
        log(f"NOTE: searches failed for keywords (skipped): {failed_keywords}")

    # ---- filter: already seen, then excluded titles --------------------------
    seen = state["seen"]
    fresh_ids = [jid for jid in union if str(jid) not in seen]
    excluded = {jid: entry for jid, entry in union.items()
                if any(p.search(entry["position"] or "") for p in exclude_patterns)}
    todo = [jid for jid in fresh_ids if jid not in excluded]
    log(f"[filter] union={len(union)} already_seen={len(union) - len(fresh_ids)} "
        f"excluded_by_title={len(excluded)} new_to_fetch={len(todo)}")

    if args.limit is not None:
        todo = todo[: args.limit]
        log(f"[limit] detail fetches capped to {len(todo)}")

    written: list[dict] = []
    failures: list[int] = []

    # ---- phase 2: detail fetch + write posting files (skipped on dry-run) ----
    if not args.dry_run:
        for jid in todo:
            entry = union[jid]
            job = fetch_detail(sess, jid)
            if job is None:
                failures.append(jid)
                continue
            meta = {**entry, "first_seen": today}
            filename = f"{jid}-{slugify(entry['company'])}.md"
            try:
                content = render_markdown(job, meta)
                postings_dir.mkdir(parents=True, exist_ok=True)
                (postings_dir / filename).write_text(content, encoding="utf-8")
            except OSError as e:
                failures.append(jid)
                log(f"    [write {jid}] ERROR {e}")
                continue
            written.append({
                "id": jid,
                "company": (job.get("company") or {}).get("name") or entry["company"],
                "position": job.get("position") or entry["position"],
                "location": job_location(job, entry.get("location", "")),
            })
            # only mark seen once the file exists, so failed ids retry next run
            seen[str(jid)] = {
                "first_seen": today,
                "company": written[-1]["company"],
                "position": written[-1]["position"],
            }
            log(f"[write] {filename} — {written[-1]['position']} @ {written[-1]['company']}")

        if failures:
            log(f"NOTE: {len(failures)} detail fetches failed (left unseen for retry): {failures}")

    # ---- phase 3: watchlist ---------------------------------------------------
    log("[watchlist] checking company posting counts on Wanted...")
    watch_counts = check_watchlist(sess, watchlist_names)
    for name in watchlist_names:
        count = watch_counts[name]
        shown = f"{count}건" if count is not None else "기업 매칭 없음"
        marker = " 🚨 NON-ZERO" if count else ""
        log(f"  {name}: {shown}{marker}")

    # ---- phase 4: persist state + digest --------------------------------------
    if not args.dry_run:
        postings_dir.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
        # postings first seen today (covers re-runs within the same day)
        fresh_today = []
        for k, v in seen.items():
            if v["first_seen"] != today:
                continue
            jid = int(k)
            location = (union.get(jid) or {}).get("location") or posting_file_location(jid)
            fresh_today.append({"id": jid, **v, "location": location})
        fresh_today.sort(key=lambda p: p["id"])
        write_digest(digest_dir, today, watch_counts, fresh_today)
        log(f"[done] files written: {len(written)} | digest: digest/{today}.md | "
            f"state: {len(seen)} ids seen")

        # ---- phase 5: HTML report + optional Telegram delivery ---------------
        report_path: Path | None = None
        if args.html:
            REPORT_DIR.mkdir(parents=True, exist_ok=True)
            report_path = REPORT_DIR / f"{today}.html"
            report_path.write_text(
                render_html_report(today, watch_counts, fresh_today, len(seen)),
                encoding="utf-8")
            log(f"[report] {report_path.relative_to(REPO_ROOT)} "
                f"({report_path.stat().st_size:,} bytes)")
        if args.telegram:
            if report_path is None or not report_path.exists():
                log("WARNING: --telegram requested but no rendered report exists; "
                    "nothing sent.")
            else:
                n_core = sum(1 for p in fresh_today if is_core_position(p["position"]))
                caption = build_caption(today, watch_counts, len(fresh_today),
                                        n_core, len(seen))
                if send_report_via_telegram(report_path, caption, args.env):
                    log("[telegram] report delivered to the PM bot")
    else:
        log(f"[dry-run] would fetch details for {len(todo)} new postings; "
            f"no files written.")

    log(f"[stats] http calls: {sess.n_calls}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
