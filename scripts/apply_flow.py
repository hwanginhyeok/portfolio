#!/usr/bin/env python3
"""From a collected job posting to a ready-to-submit application (t265).

Three offline steps plus one network check, all deterministic (no model call):

- ``shortlist``: rank every collected posting (wanted / global / jasoseol) by
  fit and feasibility, drop what the ledger already holds, optionally verify
  each top row is still open on its ATS.
- ``kit KEY``: write a tailored kit for one posting into
  ``docs/jd/<company>/``: resume variant, cover letter KR/EN, form answers,
  portfolio links. Every claim is a verbatim line from the profile files
  (RESUME.md master, apple/materials/resume_en.md); nothing is invented and
  anything the profile does not hold stays a ``[TODO]`` for the operator.
- ``track KEY STATUS``: move the posting's row in ``docs/jd/applications.json``
  (applied / response / interview) and regenerate APPLICATIONS.md.

Usage:
    python3 scripts/apply_flow.py shortlist [--top 10] [--check-open] [--out PATH]
    python3 scripts/apply_flow.py kit KEY [--questions FILE.json]
    python3 scripts/apply_flow.py track KEY STATUS [--note TEXT]
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Iterable

try:  # package import when tested; direct import when run as a script
    from scripts import applications_report as ledger_report
    from scripts.shortlist import assess_shortlist
    from scripts.state_utils import atomic_write_json
except ModuleNotFoundError:  # pragma: no cover - exercised by CLI execution
    import applications_report as ledger_report
    from shortlist import assess_shortlist
    from state_utils import atomic_write_json

REPO = Path(__file__).resolve().parent.parent
INBOX = REPO / "docs" / "jd" / "_inbox"
LEDGER = REPO / "docs" / "jd" / "applications.json"
RESUME_KO = REPO / "docs" / "blocks" / "05-extra" / "RESUME.md"
RESUME_EN = REPO / "docs" / "jd" / "apple" / "materials" / "resume_en.md"
KST = timezone(timedelta(hours=9))

SITE_URL = "https://hwanginhyeok.github.io/portfolio"
GITHUB_URL = "https://github.com/hwanginhyeok"
# Case pages are the portfolio's own published cases (cases/*.md -> site).
VALID_STATUSES = ("미지원", "준비중", "준비완료", "제출", "서류탈락", "면접", "오퍼", "보류", "마감")

# Hosts whose application form opens without an account (verified per ATS).
NO_LOGIN_HOSTS = ("jobs.ashbyhq.com", "job-boards.greenhouse.io", "boards.greenhouse.io",
                  "jobs.lever.co")


def log(message: str) -> None:
    print(message, flush=True)


# ── posting loading ──────────────────────────────────────────────────────────

_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n?(.*)\Z", re.S)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a collector markdown file into (frontmatter dict, body)."""
    match = _FRONTMATTER.match(text)
    if not match:
        return {}, text
    values: dict = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        raw = raw.strip()
        try:
            values[key.strip()] = json.loads(raw)
        except ValueError:
            values[key.strip()] = raw.strip("\"'")
    return values, match.group(2)


def _kst_today() -> date:
    return datetime.now(KST).date()


def _deadline(value: object) -> date | None:
    text = str(value or "")[:10]
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def form_kind(url: str) -> str:
    """`open` = the form needs no account, `login` = account/login first."""
    return "open" if any(host in (url or "") for host in NO_LOGIN_HOSTS) else "login"


def _from_markdown(path: Path, source: str) -> dict | None:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    if not meta:
        return None
    posting = dict(meta)
    posting["body"] = body
    posting["source"] = source
    if source == "wanted":
        posting["title"] = meta.get("position") or ""
        posting["eligibility"] = "korea"
        posting["location"] = meta.get("location") or "대한민국"
        posting["job_id"] = str(meta.get("wanted_id"))
        posting["deadline"] = meta.get("due_time")
    else:
        posting["job_id"] = str(meta.get("job_id"))
        posting["deadline"] = None
    posting["key"] = f"{source}:{posting['job_id']}"
    posting["form"] = form_kind(str(posting.get("url") or ""))
    return posting


def load_candidates(inbox: Path = INBOX) -> list[dict]:
    """All collected postings across sources, normalized, unscored."""
    postings: list[dict] = []
    for source in ("wanted", "global"):
        folder = inbox / source
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.md")):
            posting = _from_markdown(path, source)
            if posting and posting.get("title") and posting.get("company"):
                postings.append(posting)
    state_path = inbox / "jasoseol" / "state.json"
    if state_path.is_file():
        seen = json.loads(state_path.read_text(encoding="utf-8")).get("seen", {})
        for pid, row in seen.items():
            if not isinstance(row, dict) or not row.get("title"):
                continue
            url = f"https://jasoseol.com/recruit/{pid}"
            postings.append({
                "source": "jasoseol", "key": f"jasoseol:{pid}", "job_id": str(pid),
                "company": row.get("company"), "title": row.get("title"), "url": url,
                "body": " ".join(row.get("sub_positions") or []), "eligibility": "korea",
                "location": "대한민국", "deadline": row.get("end_time"),
                "first_seen": row.get("first_seen"), "track": row.get("track"),
                "form": "login",
            })
    return postings


def ledger_job_ids(ledger_path: Path = LEDGER) -> set[str]:
    rows = ledger_report.load_ledger(ledger_path) if ledger_path.is_file() else []
    return {str(r.get("job_id")) for r in rows if r.get("job_id")}


# ── profile facts ────────────────────────────────────────────────────────────

_HEADING = re.compile(r"^#{2,4}\s+(§[\w.]+)")
KO_SECTIONS = ("§4", "§5", "§6", "§7")  # §8 awards repeat §6


def _fact_lines(text: str, wanted_sections: Iterable[str] | None) -> list[tuple[str, str]]:
    section = ""
    facts: list[tuple[str, str]] = []
    for raw in text.splitlines():
        heading = _HEADING.match(raw)
        if heading:
            section = heading.group(1)
            continue
        line = raw.strip()
        if wanted_sections is not None and not any(
                section == s or section.startswith(s + ".") for s in wanted_sections):
            continue
        if "[TODO" in line or line.startswith(("> ", "|--", "| ---", "| 영역")):
            continue
        if line.startswith("- "):
            facts.append((section, line[2:].strip()))
        elif line.startswith("|") and line.count("|") >= 3:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] and cells[0] != "#":
                facts.append((section, f"{cells[0]}: {cells[-1]}"))
    return [(s, t) for s, t in facts if len(t) > 12]


def load_facts(ko_path: Path = RESUME_KO, en_path: Path = RESUME_EN) -> list[dict]:
    """Verbatim, referenced profile lines. `lang` picks the letter language."""
    facts: list[dict] = []
    if ko_path.is_file():
        for section, text in _fact_lines(ko_path.read_text(encoding="utf-8"), KO_SECTIONS):
            facts.append({"lang": "ko", "text": text, "ref": f"{ko_path.name} {section}"})
    if en_path.is_file():
        for section, text in _fact_lines(en_path.read_text(encoding="utf-8"), None):
            facts.append({"lang": "en", "text": text, "ref": en_path.name})
    return facts


_STOP = frozenset("""the and for with from that this are was were has have not you your our their
into over under per via using use used can will all any one two out more most such than then also
engineer engineering team work working role experience years year ability strong related""".split())


def terms(text: str) -> set[str]:
    """English words + Korean character bigrams (tolerates particles)."""
    found: set[str] = set()
    lowered = text.lower()
    for word in re.findall(r"[a-z][a-z0-9+#.\-/]{2,}", lowered):
        word = word.strip(".-/")
        if len(word) > 2 and word not in _STOP:
            found.add(word)
    for word in re.findall(r"[가-힣]{2,}", lowered):
        found.update(word[i:i + 2] for i in range(len(word) - 1))
    return found


def _domain_hits(text: str) -> set[str]:
    return {m.group(0).lower() for m in DEEP_DOMAIN.finditer(text)}


def rank_facts(posting_text: str, facts: list[dict], lang: str) -> list[dict]:
    """Profile lines of one language ordered by IDF-weighted overlap with the posting."""
    pool = [f for f in facts if f["lang"] == lang]
    if not pool:
        return []
    fact_terms = [terms(f["text"]) for f in pool]
    df = Counter(t for ts in fact_terms for t in ts)
    wanted = terms(posting_text)
    wanted_domain = _domain_hits(posting_text)
    scored = []
    for fact, ts in zip(pool, fact_terms):
        shared = ts & wanted
        # Domain terms the profile is deep in count extra: a motor-control
        # posting should lead with motor evidence, not with a generic award.
        domain = wanted_domain & _domain_hits(fact["text"])
        score = sum(math.log(1 + len(pool) / df[t]) for t in shared) + 8 * len(domain)
        scored.append({**fact, "score": round(score, 3), "matched": sorted(shared)[:6]})
    scored.sort(key=lambda f: (-f["score"], f["ref"], f["text"]))
    return [f for f in scored if f["score"] > 0]


# ── shortlist ────────────────────────────────────────────────────────────────

# Hard-skill gate. The shortlist's fit_score only looks at titles, so a web-QA
# role can outrank a motor-control one. These lists come from RESUME.md: what
# the profile is deep in (bonus) and what it has no record of (penalty).
DEEP_DOMAIN = re.compile(
    r"모터|motor|bldc|pmsm|inverter|인버터|임베디드|embedded|firmware|펌웨어|\bcan\b|전력|power electronics|"
    r"양산|apqp|dfmea|신뢰성|reliability|시험|test bench|dynamometer|하드웨어|hardware|제어기|"
    r"로봇|robot|자율주행|autonomous|제조기술|manufacturing", re.I)
NO_RECORD_DOMAIN = re.compile(
    r"react|next\.?js|spring|javascript|typescript|프론트엔드|frontend|백엔드|backend|\bandroid\b|\bios\b|"
    r"react native|웹\s*(?:개발|서비스)|퍼블리셔|디자이너|marketing|마케팅|영업|sales|회계|인사|\bhr\b", re.I)


def domain_adjustment(title: str, body: str) -> tuple[float, list[str]]:
    """+6 per distinct deep-domain hit (max +36), -12 per no-record hit (max -48)."""
    text = f"{title} {title} {body}"
    deep = sorted({m.group(0).lower() for m in DEEP_DOMAIN.finditer(text)})
    miss = sorted({m.group(0).lower() for m in NO_RECORD_DOMAIN.finditer(text)})
    value = min(36, 6 * len(deep)) - min(48, 12 * len(miss))
    notes = []
    if deep:
        notes.append("profile domain: " + ", ".join(deep[:5]))
    if miss:
        notes.append("no record in profile: " + ", ".join(miss[:5]))
    return float(value), notes


def score_postings(postings: list[dict], facts: list[dict], applied_ids: set[str],
                   today: date | None = None) -> list[dict]:
    """Annotate and rank: feasible + profile-fit first, with plain reasons."""
    today = today or _kst_today()
    ranked: list[dict] = []
    for posting in postings:
        if posting["job_id"] in applied_ids:
            continue
        deadline = _deadline(posting.get("deadline"))
        if deadline and deadline < today:
            continue
        verdict = assess_shortlist(posting)
        if not verdict["actionable"]:
            continue
        text = f"{posting['title']} {posting.get('body', '')}"
        lang = "ko" if re.search(r"[가-힣]", text) else "en"
        top = rank_facts(text, facts, lang)[:5]
        # Capped so the profile overlap orders near-ties without swamping fit.
        title_top = rank_facts(str(posting["title"]), facts, lang)[:3]
        overlap = round(min(40.0, sum(f["score"] for f in top) / 6
                            + sum(f["score"] for f in title_top) / 2), 2)
        posting.update(verdict)
        posting["profile_overlap"] = overlap
        adjust, adjust_notes = domain_adjustment(str(posting["title"]), str(posting.get("body", "")))
        posting["rank_score"] = round(verdict["fit_score"] + overlap + adjust, 2)
        posting["reasons"] = (
            [f"fit: {', '.join(verdict['fit_evidence'][:3])}"] if verdict["fit_evidence"] else []
        ) + [f"feasible: {verdict['feasibility']}",
             f"profile lines matched: {len(top)} (overlap {overlap})", *adjust_notes,
             "form: no account needed" if posting["form"] == "open" else "form: login first"]
        ranked.append(posting)
    ranked.sort(key=lambda p: (-p["rank_score"], str(p.get("deadline") or "9999"), p["key"]))
    unique: list[dict] = []
    seen_roles: set[tuple[str, str]] = set()
    for posting in ranked:  # the same role is often re-posted under several ids
        role = (str(posting["company"]).casefold(), str(posting["title"]).casefold())
        if role not in seen_roles:
            seen_roles.add(role)
            unique.append(posting)
    return unique


def _http_ok(url: str, timeout: int = 20) -> bool | None:
    """True if the URL answers 2xx, False on 404/410, None when unknown."""
    request = urllib.request.Request(url, headers={"User-Agent": "portfolio-apply-flow/1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 300
    except urllib.error.HTTPError as err:
        return False if err.code in (404, 410) else None
    except (urllib.error.URLError, OSError):
        return None


def check_open(posting: dict, probe: Callable[[str], bool | None] = _http_ok) -> bool | None:
    """Is the posting still live on its ATS? None = could not tell."""
    url = str(posting.get("url") or "")
    job = posting["job_id"]
    parts = url.split("/")
    if "boards.greenhouse.io" in url or "job-boards.greenhouse.io" in url:
        slug = parts[3] if len(parts) > 3 else ""
        return probe(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs/{job}")
    if "jobs.lever.co" in url:
        return probe(f"https://api.lever.co/v0/postings/{parts[3]}/{job}")
    if "jobs.ashbyhq.com" in url:
        return probe(f"https://api.ashbyhq.com/posting-api/job-board/{parts[3]}") and _ashby_listed(
            parts[3], job)
    if "myworkdayjobs.com" in url:
        host = parts[2]
        tenant = host.split(".")[0]
        site = parts[3] if not re.fullmatch(r"[a-z]{2}-[A-Z]{2}", parts[3]) else parts[4]
        path = url.split(f"/{site}/", 1)[1] if f"/{site}/" in url else ""
        return probe(f"https://{host}/wday/cxs/{tenant}/{site}/{path}")
    if posting["source"] == "wanted":
        return _wanted_open(job)
    return probe(url)


def _wanted_open(job_id: str) -> bool | None:
    """Wanted answers 200 for closed postings too; the JSON `status` decides."""
    request = urllib.request.Request(
        f"https://www.wanted.co.kr/api/v4/jobs/{job_id}",
        headers={"User-Agent": "portfolio-apply-flow/1"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = json.load(response).get("job", {}).get("status")
    except urllib.error.HTTPError as err:
        return False if err.code in (404, 410) else None
    except (urllib.error.URLError, OSError, ValueError):
        return None
    return status == "active" if status else None


def _ashby_listed(slug: str, job_id: str) -> bool | None:
    request = urllib.request.Request(
        f"https://api.ashbyhq.com/posting-api/job-board/{slug}",
        headers={"User-Agent": "portfolio-apply-flow/1"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            jobs = json.load(response).get("jobs", [])
    except (urllib.error.URLError, OSError, ValueError):
        return None
    return any(j.get("id") == job_id and j.get("isListed", True) for j in jobs)


def render_shortlist(rows: list[dict], today: date) -> str:
    lines = [f"# 오늘의 지원 후보 — {today.isoformat()}", "",
             "| # | 회사 | 포지션 | 점수 | 마감 | 폼 | 열림 | 키 |", "|---|---|---|---|---|---|---|---|"]
    for index, row in enumerate(rows, 1):
        opened = {True: "열림", False: "닫힘", None: "미확인"}[row.get("open")] if "open" in row else "-"
        lines.append(
            f"| {index} | {row['company']} | {row['title']} | {row['rank_score']} | "
            f"{str(row.get('deadline') or '상시/미상')[:10]} | "
            f"{'계정 불필요' if row['form'] == 'open' else '로그인 필요'} | {opened} | `{row['key']}` |")
    lines.append("")
    for index, row in enumerate(rows, 1):
        lines.append(f"{index}. **{row['company']} — {row['title']}**: " + " · ".join(row["reasons"]))
    lines.append("")
    lines.append("지원 준비: `python3 scripts/apply_flow.py kit <키>`")
    return "\n".join(lines) + "\n"


def build_shortlist(top: int = 10, check: bool = False, inbox: Path = INBOX,
                    ledger_path: Path = LEDGER, probe: Callable = _http_ok,
                    today: date | None = None, facts: list[dict] | None = None) -> list[dict]:
    today = today or _kst_today()
    facts = load_facts() if facts is None else facts
    ranked = score_postings(load_candidates(inbox), facts, ledger_job_ids(ledger_path), today)
    if not check:
        return ranked[:top]
    live: list[dict] = []
    for row in ranked:
        row["open"] = check_open(row, probe)
        if row["open"] is not False:
            live.append(row)
        if len(live) >= top:
            break
    return live


# ── kit ──────────────────────────────────────────────────────────────────────

def slugify(text: str, fallback: str = "company") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or fallback


def company_slug(posting: dict) -> str:
    """ASCII folder name; Korean-only names fall back to `<source>-<id>`."""
    return slugify(str(posting["company"]), f"{posting['source']}-{posting['job_id']}")


def find_posting(key: str, inbox: Path = INBOX) -> dict:
    for posting in load_candidates(inbox):
        if posting["key"] == key:
            return posting
    raise SystemExit(f"posting not found: {key}")


def _bullets(rows: list[dict]) -> str:
    return "\n".join(f"- {r['text']}  \n  <sub>출처: {r['ref']}</sub>" for r in rows)


QUESTION_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("links", ("linkedin", "github", "website", "portfolio", "url", "포트폴리오")),
    ("authorization", ("authorized", "authorised", "sponsor", "visa", "work permit", "right to work", "비자")),
    ("relocation", ("relocat", "이주", "reloc")),
    ("salary", ("salary", "compensation", "expected", "희망 연봉", "연봉")),
    ("why", ("why", "motivat", "interest", "지원 동기", "지원동기")),
    ("experience", ("experience", "describe", "tell us", "background", "경험", "프로젝트")),
)


def classify_question(question: str) -> str:
    lowered = question.lower()
    for kind, needles in QUESTION_RULES:
        if any(n in lowered for n in needles):
            return kind
    return "other"


def answer_question(question: str, evidence_en: list[dict], posting: dict) -> str:
    kind = classify_question(question)
    if kind == "links":
        return f"Portfolio: {SITE_URL}\nGitHub: {GITHUB_URL}"
    if kind == "authorization":
        return "[TODO: 운영자 입력 — 근로허가/스폰서십 사실관계. 에이전트는 추정하지 않음]"
    if kind == "relocation":
        return "[TODO: 운영자 입력 — 이주 의사/가능 시점]"
    if kind == "salary":
        return "[TODO: 운영자 입력 — 희망 연봉]"
    if kind in ("why", "experience") and evidence_en:
        lead = (f"I am applying for the {posting['title']} role at {posting['company']}. "
                if kind == "why" else "")
        body = " ".join(f"{r['text'].rstrip('.')}." for r in evidence_en[:3])
        suffix = " [TODO: 운영자 입력 — 이 회사를 고른 개인적 이유 1~2문장]" if kind == "why" else ""
        return lead + body + suffix
    return "[TODO: 운영자 입력 — 프로필에 근거 없는 질문]"


def build_kit(posting: dict, facts: list[dict], questions: list[str] | None = None) -> dict[str, str]:
    """File name -> content for one posting. Pure; the caller writes the files."""
    text = f"{posting['title']} {posting.get('body', '')}"
    ko = rank_facts(text, facts, "ko")[:8]
    en = rank_facts(text, facts, "en")[:8]
    # Letters lead with work evidence (career/projects), not awards or papers.
    ko_work = [f for f in ko if f["ref"].endswith(("§4", "§5"))] or ko
    company, title, url = posting["company"], posting["title"], posting.get("url", "")
    header = (f"> 대상: {company} — {title} · 키 `{posting['key']}` · {url}\n"
              "> 모든 문장은 프로필 원문(RESUME.md / resume_en.md) 인용. `[TODO]`는 운영자 입력.\n")
    files = {
        "1_resume-variant.md": (
            f"# 이력서 변형 — {company} {title}\n\n{header}\n"
            "## 이 공고에 맞춰 앞에 둘 근거 (JD 키워드 겹침 순)\n\n" + _bullets(ko or en) + "\n\n"
            "## 기본 이력서\n\n마스터: `docs/blocks/05-extra/RESUME.md`, 영문: "
            "`docs/jd/apple/materials/resume_en.md`. 위 근거를 §2 Summary 아래 앞쪽에 배치.\n"),
        "2_cover-letter-ko.md": (
            f"# 커버레터(국문) — {company} {title}\n\n{header}\n"
            f"안녕하세요, {company}의 {title} 포지션에 지원하는 황인혁입니다.\n\n"
            "## 이 포지션과 맞닿는 경험\n\n" + _bullets(ko_work[:4]) + "\n\n"
            "## 지원 동기\n\n[TODO: 운영자 입력 — 왜 이 회사/이 포지션인지 2~3문장]\n\n"
            "감사합니다.\n황인혁\n"),
        "3_cover-letter-en.md": (
            f"# Cover letter (EN) — {company} {title}\n\n{header}\n"
            f"Dear {company} hiring team,\n\n"
            f"I am applying for the {title} position. The experience below is the closest "
            "match to your posting:\n\n" + _bullets(en[:4]) + "\n\n"
            "[TODO: 운영자 입력 — why this company, 2–3 sentences]\n\n"
            "Sincerely,\nInhyeok Hwang\n"),
        "4_form-answers.md": _form_answers_doc(posting, en, questions or [], header),
        "5_portfolio-links.md": (
            f"# 포트폴리오 링크 — {company} {title}\n\n{header}\n"
            f"- 사이트: {SITE_URL}\n- GitHub: {GITHUB_URL}\n"
            "- 이 공고와 가장 가까운 케이스는 사이트의 케이스 목록에서 위 근거 항목명으로 검색.\n"),
    }
    return files


def _form_answers_doc(posting: dict, en: list[dict], questions: list[str], header: str) -> str:
    lines = [f"# 지원서 폼 답변 — {posting['company']} {posting['title']}", "", header]
    standing = [("Email", "[TODO: 운영자 입력 — 지원용 이메일]"), ("Portfolio", SITE_URL),
                ("GitHub", GITHUB_URL), ("Current employer", "GINT Inc. (긴트)"),
                ("Phone / location", "[TODO: 운영자 입력]")]
    lines += ["## 고정 항목", ""] + [f"- **{k}**: {v}" for k, v in standing] + [""]
    lines += ["## 폼 질문", ""]
    if not questions:
        lines.append("(폼 질문 미수집 — 브라우저 단계에서 `--questions`로 채움)")
    for q in questions:
        lines += [f"### {q}", "", answer_question(q, en, posting), ""]
    return "\n".join(lines) + "\n"


def write_kit(posting: dict, facts: list[dict], questions: list[str] | None = None,
              root: Path = REPO / "docs" / "jd") -> Path:
    out = root / company_slug(posting)
    out.mkdir(parents=True, exist_ok=True)
    for name, content in build_kit(posting, facts, questions).items():
        (out / name).write_text(content, encoding="utf-8")
    return out


# ── tracking ─────────────────────────────────────────────────────────────────

def track(key: str, status: str, note: str = "", ledger_path: Path = LEDGER,
          today: date | None = None, posting: dict | None = None) -> dict:
    """Create or move the ledger row for `key`, keeping a dated history."""
    if status not in VALID_STATUSES:
        raise SystemExit(f"invalid status {status!r}; one of {VALID_STATUSES}")
    today = today or _kst_today()
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    rows = data["applications"]
    job_id = key.split(":", 1)[-1]
    row = next((r for r in rows if str(r.get("job_id")) == job_id), None)
    if row is None:
        if posting is None:
            raise SystemExit(f"{key} is not in the ledger; pass a posting to create it")
        row = {"id": f"{company_slug(posting)}-{slugify(posting['title'], 'role')}"[:60],
               "company": posting["company"], "position": posting["title"],
               "location": posting.get("location", ""), "job_id": job_id,
               "url": posting.get("url", ""), "channel": posting.get("ats") or posting["source"],
               "applied_at": None, "source": f"cron-{posting['source']}",
               "materials": f"docs/jd/{company_slug(posting)}/", "notes": ""}
        rows.append(row)
    row["status"] = status
    if status == "제출" and not row.get("applied_at"):
        row["applied_at"] = today.isoformat()
    history = row.setdefault("history", [])
    history.append({"date": today.isoformat(), "status": status, **({"note": note} if note else {})})
    data["updated_at"] = today.isoformat()
    atomic_write_json(ledger_path, data)
    return row


# ── CLI ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_short = sub.add_parser("shortlist")
    p_short.add_argument("--top", type=int, default=10)
    p_short.add_argument("--check-open", action="store_true")
    p_short.add_argument("--out", type=Path)
    p_short.add_argument("--inbox", type=Path, default=INBOX, help="collector inbox root")
    p_kit = sub.add_parser("kit")
    p_kit.add_argument("key")
    p_kit.add_argument("--inbox", type=Path, default=INBOX, help="collector inbox root")
    p_kit.add_argument("--questions", type=Path, help="JSON list of form question strings")
    p_track = sub.add_parser("track")
    p_track.add_argument("key")
    p_track.add_argument("status")
    p_track.add_argument("--note", default="")
    args = parser.parse_args(argv)

    if args.command == "shortlist":
        rows = build_shortlist(args.top, args.check_open, inbox=args.inbox)
        text = render_shortlist(rows, _kst_today())
        if args.out:
            args.out.write_text(text, encoding="utf-8")
            log(f"[shortlist] {len(rows)} rows -> {args.out}")
        else:
            sys.stdout.write(text)
        return 0
    if args.command == "kit":
        posting = find_posting(args.key, args.inbox)
        questions = json.loads(args.questions.read_text(encoding="utf-8")) if args.questions else []
        out = write_kit(posting, load_facts(), questions)
        log(f"[kit] {posting['company']} — {posting['title']} -> {out}")
        return 0
    posting = None
    try:
        posting = find_posting(args.key)
    except SystemExit:
        pass
    row = track(args.key, args.status, args.note, posting=posting)
    ledger_report.main([])  # regenerate APPLICATIONS.md from the ledger
    log(f"[track] {row['company']} {row['position']} -> {row['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
