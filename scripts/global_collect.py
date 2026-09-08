#!/usr/bin/env python3
"""Global job-posting collector for the portfolio project.

Companion to scripts/wanted_collect.py (Korean boards on Wanted). This one pulls
full-company boards from global ATS APIs into docs/jd/_inbox/global/, scores each
posting against the owner's profile (motor control / power electronics / embedded
firmware / reliability & validation / hardware TPM), and tags every kept posting
with an eligibility bucket — for a Korean national in Korea the bucket usually
matters more than the score.

ATS endpoints (verified 2026-08-19, plain HTTPS, no auth, no cookies):
  - Greenhouse: GET https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true
    → {"jobs":[{"id","title","location":{"name"},"absolute_url","content"(HTML-escaped)}]}
  - Ashby:      GET https://api.ashbyhq.com/posting-api/job-board/<slug>
    → {"jobs":[{"id","title","location","department","jobUrl","descriptionPlain",...}]}
  - Lever:      GET https://api.lever.co/v0/postings/<slug>?mode=json
    → [{"id","text","categories":{...},"hostedUrl","descriptionPlain","country",...}]
  - Workday:    POST https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/jobs
    body {"appliedFacets":{},"limit":20,"offset":n,"searchText":text}
    → {"total":N,"jobPostings":[{"title","locationsText","externalPath","postedOn",
      "bulletFields"}]}. The list response carries NO JD body, so Workday postings
    are scored on title + bulletFields + location and flagged no_jd — cards must
    say the description was not available, not show a fake empty excerpt.
    PAGINATION TRAP: Workday reports "total": 0 while still returning a full
    jobPostings page, AND only loosely honours `offset` — measured 2026-08-19,
    walking to the empty-page signal cost 50 pages of 94% duplicates per tenant.
    Stop a term after N consecutive pages that add no new externalPath instead;
    that yields the identical unique set in 7-9 pages.

One request per company per run for the list ATS (full-list endpoints — never
per-posting detail pages). Workday paginates its search endpoint per tenant per
search term, unioned by externalPath. Terms in config/global_targets.json are
regexes (korea_location_terms / workday_search_terms are plain word-boundary
match terms, not regexes).

Usage:
  python3 scripts/global_collect.py [--config PATH] [--dry-run] [--limit N]
                                    [--html] [--telegram [--env ENV_PATH]]
"""
import argparse
import hashlib
import html
import json
import re
import sys
import time
import urllib.request
from datetime import date, datetime
from pathlib import Path

import requests

try:  # package import when tested; direct import when run as a script
    from scripts.shortlist import (
        KOREAN_ADMINISTRATIVE_ADDRESS_PATTERN,
        TRACK_CORE,
        TRACK_ORDER,
        annotate_shortlist,
        rank_actionable,
        reason_label,
        normalize_track,
        primary_track,
        track_label,
    )
    from scripts.state_utils import atomic_write_json
except ModuleNotFoundError:  # pragma: no cover - exercised by CLI execution
    from shortlist import (
        KOREAN_ADMINISTRATIVE_ADDRESS_PATTERN,
        TRACK_CORE,
        TRACK_ORDER,
        annotate_shortlist,
        rank_actionable,
        reason_label,
        normalize_track,
        primary_track,
        track_label,
    )
    from state_utils import atomic_write_json

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "global_targets.json"
INBOX_DIR = REPO_ROOT / "docs" / "jd" / "_inbox" / "global"
REPORT_DIR = INBOX_DIR / "report"
PM_ENV = Path("/home/window11/project-manager/.env")

GREENHOUSE_URL = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
ASHBY_URL = "https://api.ashbyhq.com/posting-api/job-board/{slug}"
LEVER_URL = "https://api.lever.co/v0/postings/{slug}"
WORKDAY_URL = "https://{tenant}.wd{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
WORKDAY_BASE_URL = "https://{tenant}.wd{wd}.myworkdayjobs.com/{site}"
WORKDAY_PAGE_SIZE = 20
WORKDAY_PAGE_LIMIT = 15   # runaway guard: max pages per tenant+searchText
WORKDAY_STALL_PAGES = 3   # stop a term after this many pages add no new externalPath

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
}
HTTP_TIMEOUT = 20
BODY_MAX_CHARS = 12000   # posting markdown truncation cap
EXCERPT_MAX_CHARS = 220


def log(msg: str) -> None:
    print(msg, flush=True)


class PoliteSession:
    """Single-threaded HTTP wrapper sleeping `delay` between every call."""

    def __init__(self, delay: float) -> None:
        self._session = requests.Session()
        self._delay = delay
        self._first_call = True
        self.n_calls = 0

    def _request(self, method: str, url: str, *, params: dict | None = None,
                 json_body: dict | None = None):
        """One rate-limited request. Returns None on non-200 / parse error
        (logged, not fatal)."""
        if not self._first_call:
            time.sleep(self._delay)
        self._first_call = False
        self.n_calls += 1
        try:
            resp = self._session.request(method, url, params=params, json=json_body,
                                         headers=HEADERS, timeout=HTTP_TIMEOUT)
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

    def get_json(self, url: str, params: dict | None = None):
        """GET and parse JSON."""
        return self._request("GET", url, params=params)

    def post_json(self, url: str, body: dict):
        """POST a JSON body and parse the JSON response."""
        return self._request("POST", url, json_body=body)


# ── text cleanup ─────────────────────────────────────────────────────────────

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def strip_html(escaped_html: str | None) -> str:
    """Greenhouse/Ashby bodies arrive as (escaped) HTML — unescape, strip tags, collapse."""
    if not escaped_html:
        return ""
    text = html.unescape(escaped_html)
    text = text.replace("</li>", "\n").replace("</p>", "\n").replace("<br>", "\n")
    text = TAG_RE.sub(" ", text)
    return WS_RE.sub(" ", text).strip()


def compile_term(term: str) -> re.Pattern:
    """Config terms are regexes; wrap with alnum lookarounds as word boundaries
    so e.g. 'foc' never matches 'focus' and plain 'can' (too noisy) is not used."""
    return re.compile(r"(?<![a-z0-9])" + term + r"(?![a-z0-9])", re.IGNORECASE)


# Korea location match terms. The config's korea_location_terms is the SSOT and
# overrides this list at load time. Workday location strings are wildly
# inconsistent ("Hwaseong-Lucestar,KOR", "KOR-Gyeonggi-do-Dongtan-KLA",
# "Gunpo-si Gyeonggi-do, Republic of Korea", "KOR Asan – MFG"), so the bucket
# matches any term, case-insensitive, on word boundaries.
DEFAULT_KOREA_LOCATION_TERMS = [
    "Korea", "KOR", "Seoul", "Suwon", "Hwaseong", "Icheon", "Cheonan", "Pyeongtaek",
    "Bundang", "Dongtan", "Gunpo", "Ulsan", "Choongju", "Youngchun", "Asan",
    "Gyeonggi", "Incheon", "Busan",
]
# Workday has no full-list endpoint — each tenant is queried per searchText and
# the results unioned by externalPath. "Korea" surfaces local roles; the domain
# terms catch Korea postings whose title/location never says Korea.
DEFAULT_WORKDAY_SEARCH_TERMS = ["Korea", "motor", "test engineer", "program manager",
                                "equipment", "quality"]


def make_excerpt(body: str, limit: int = EXCERPT_MAX_CHARS) -> str:
    text = WS_RE.sub(" ", body or "").strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


# ── board fetching: one request per company, normalized posting shape ────────

def normalize_posting(company: dict, job: dict, ats: str) -> dict:
    """Map one raw ATS job to the common shape the scorer/tagger consume."""
    if ats == "greenhouse":
        location = ((job.get("location") or {}).get("name")) or ""
        if not location:
            offices = job.get("offices") or []
            location = ((offices[0] or {}).get("location")) or "" if offices else ""
        departments = [d.get("name", "") for d in job.get("departments") or [] if d.get("name")]
        body = strip_html(job.get("content"))
        return {
            "job_id": str(job.get("id", "")),
            "title": job.get("title") or "",
            "department": ", ".join(dict.fromkeys(departments)),
            "location_raw": location,
            "country_hint": "",
            "body": body,
            "url": job.get("absolute_url") or "",
            "remote_flag": bool(re.search(r"\bremote\b", f"{location} {job.get('title') or ''}", re.I)),
        }
    if ats == "ashby":
        body = strip_html(job.get("descriptionPlain") or job.get("descriptionHtml"))
        location = job.get("location") or ""
        secondary = ", ".join(l.get("location", "") for l in (job.get("secondaryLocations") or [])
                              if isinstance(l, dict) and l.get("location"))
        return {
            "job_id": str(job.get("id", "")),
            "title": job.get("title") or "",
            "department": job.get("department") or job.get("team") or "",
            "location_raw": ", ".join(x for x in [location, secondary] if x),
            "country_hint": "",
            "body": body,
            "url": job.get("jobUrl") or "",
            "remote_flag": bool(job.get("isRemote")) or (job.get("workplaceType") or "").lower() == "remote",
        }
    # lever
    categories = job.get("categories") or {}
    body = strip_html(" ".join(filter(None, [
        job.get("descriptionPlain"), job.get("additionalPlain")])))
    all_locations = categories.get("allLocations") or []
    return {
        "job_id": str(job.get("id", "")),
        "title": job.get("text") or "",
        "department": categories.get("team") or categories.get("department") or "",
        "location_raw": categories.get("location") or ", ".join(all_locations),
        "country_hint": job.get("country") or "",
        "body": body,
        "url": job.get("hostedUrl") or "",
        "remote_flag": (job.get("workplaceType") or "").lower() == "remote",
    }


def fetch_board(sess: PoliteSession, company: dict) -> list[dict] | None:
    """One full-board request per company. None = the board request itself failed."""
    ats, slug = company["ats"], company["slug"]
    if ats == "greenhouse":
        data = sess.get_json(GREENHOUSE_URL.format(slug=slug), {"content": "true"})
        jobs = (data or {}).get("jobs") if isinstance(data, dict) else None
    elif ats == "ashby":
        data = sess.get_json(ASHBY_URL.format(slug=slug))
        jobs = (data or {}).get("jobs") if isinstance(data, dict) else None
    elif ats == "lever":
        data = sess.get_json(LEVER_URL.format(slug=slug), {"mode": "json"})
        jobs = data if isinstance(data, list) else None
    else:
        log(f"[board] {company['name']}: unknown ats {ats!r}")
        return None
    if jobs is None:
        return None
    postings = [normalize_posting(company, job, ats) for job in jobs]
    # ashby can list unlisted jobs; keep only listed ones when the flag exists
    listed = [job.get("isListed") for job in jobs]
    if ats == "ashby" and any(flag is False for flag in listed):
        postings = [p for p, flag in zip(postings, listed) if flag is not False]
    for posting in postings:
        posting["company"] = company["name"]
        posting["ats"] = ats
        posting["slug"] = slug
    return postings


def workday_job_id(external_path: str) -> str:
    """Stable ledger id: the requisition number Workday embeds in externalPath
    (observed as ".../Korea-Procurement-Lead_2637575-1"), or a short hash when
    the path carries no number."""
    m = re.search(r"\d{4,}", external_path or "")
    if m:
        return m.group(0)
    return hashlib.sha1((external_path or "").encode("utf-8")).hexdigest()[:12]


def normalize_workday_posting(company: dict, job: dict, base_url: str) -> dict:
    """Map one Workday jobPosting row to the common shape. The list endpoint
    carries no JD body, so `body` is bulletFields + location (the scoring text)
    and the posting is flagged no_jd so cards say the description was missing."""
    bullets = []
    for field in job.get("bulletFields") or []:
        text = field.get("value") if isinstance(field, dict) else field
        if text:
            bullets.append(str(text))
    location = job.get("locationsText") or ""
    title = job.get("title") or ""
    external_path = job.get("externalPath") or ""
    body = " · ".join(bullets + [location]) if (bullets or location) else ""
    return {
        "job_id": workday_job_id(external_path),
        "title": title,
        "department": "",
        "location_raw": location,
        "country_hint": "",
        "body": body,
        "url": (base_url + external_path) if external_path else "",
        "remote_flag": bool(re.search(r"\bremote\b", f"{location} {title}", re.I)),
        "no_jd": True,
        "external_path": external_path,
    }


def hydrate_workday_korea(sess: PoliteSession, company: dict, postings: list[dict],
                          korea_patterns: list[re.Pattern]) -> int:
    """Fetch the real JD body for the Korea-located rows of one Workday tenant.

    The list endpoint carries no description, which leaves Korea postings scored
    on their title alone (measured ceiling ~9) — enough to keep them via the
    location rule, but not enough to *rank* them, so a Quality Inspector sorts
    level with a Program Manager. The per-posting endpoint does carry it:

        GET https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site><externalPath>
        -> {"jobPostingInfo": {"jobDescription": "<html>", ...}}

    Only Korea rows are hydrated — that is the section the owner reads, and it
    bounds the cost to ~1 request per Korea posting instead of one per row.
    A row whose fetch fails keeps no_jd and its title-only score; it is never
    dropped for that.
    """
    detail_base = (f"https://{company['tenant']}.wd{company['wd']}.myworkdayjobs.com"
                   f"/wday/cxs/{company['tenant']}/{company['site']}")
    n = 0
    for posting in postings:
        if not matches_any(korea_patterns, posting.get("location_raw") or ""):
            continue
        path = posting.get("external_path") or ""
        if not path:
            continue
        data = sess.get_json(detail_base + path)
        if not data:
            continue  # already logged; keep the title-only score
        body = strip_html(((data.get("jobPostingInfo") or {}).get("jobDescription")))
        if not body:
            continue
        posting["body"] = body
        posting["no_jd"] = False
        n += 1
    log(f"    [workday] {company['tenant']}: hydrated {n} Korea postings with full JD")
    return n


def fetch_workday(sess: PoliteSession, company: dict, search_terms: list[str],
                  page_limit: int, stall_pages: int = WORKDAY_STALL_PAGES
                  ) -> list[dict] | None:
    """Search one Workday tenant with every search term, unioned by externalPath.
    None = the tenant itself was unreachable (logged, never fatal to the run).

    PAGINATION TRAP, two halves. Workday reports "total": 0 (or any low number)
    while still returning a full jobPostings page, so stopping at
    `offset >= total` silently under-collects. But the offset is *also* only
    loosely honoured: measured 2026-08-19, walking to the empty-page signal took
    50 pages and returned 94% duplicates (kla 988 rows -> 68 unique, amat 997 ->
    117, aptiv 983 -> 63) for ~85s per tenant. An empty page may never arrive.

    So the end signal is neither `total` nor emptiness: stop after
    WORKDAY_STALL_PAGES consecutive pages that add no new externalPath. That
    reproduces the identical unique sets (68/117/63) in 7-9 pages and ~12s per
    tenant. `page_limit` stays as the outer runaway guard.
    """
    tenant, site = company["tenant"], company["site"]
    search_url = WORKDAY_URL.format(tenant=tenant, wd=company["wd"], site=site)
    base_url = WORKDAY_BASE_URL.format(tenant=tenant, wd=company["wd"], site=site)
    union: dict[str, dict] = {}
    n_ok = 0
    for term in search_terms:
        pages = 0
        offset = 0
        stall = 0
        while True:
            data = sess.post_json(search_url, {"appliedFacets": {},
                                               "limit": WORKDAY_PAGE_SIZE,
                                               "offset": offset,
                                               "searchText": term})
            if data is None:
                break  # already logged; keep what this term yielded so far
            n_ok += 1  # tenant answered with valid JSON — reachable, even if empty
            postings = data.get("jobPostings") or []
            if not postings:
                break
            pages += 1
            fresh = 0
            for job in postings:
                path = job.get("externalPath") or ""
                if path and path not in union:
                    union[path] = job
                    fresh += 1
            offset += WORKDAY_PAGE_SIZE
            # the real end signal: pages that stopped contributing anything new
            stall = stall + 1 if fresh == 0 else 0
            if stall >= stall_pages:
                break
            if pages >= page_limit:
                log(f"    [workday] {tenant}: searchText={term!r} hit the {page_limit}-page "
                    "runaway cap — results for this term are truncated")
                break
        log(f"    [workday] {tenant}: searchText={term!r} pages={pages} "
            f"union={len(union)}")
    if n_ok == 0:
        return None
    postings = [normalize_workday_posting(company, job, base_url)
                for job in union.values()]
    for posting in postings:
        posting["company"] = company["name"]
        posting["ats"] = "workday"
        posting["slug"] = tenant
    return postings


# ── scoring ──────────────────────────────────────────────────────────────────

def score_posting(posting: dict, keyword_rules: list[tuple[str, re.Pattern, int]],
                  weights: dict) -> tuple[int, list[dict], int]:
    """Score = Σ weight·scope_multiplier over every (keyword, scope) hit.
    Title counts 3×, department 2×, body 1×. Returns (score, matched, core_weight)
    where core_weight is the highest weight matched anywhere (used for the
    'data scientist unless paired with hardware' exception)."""
    scopes = [("title", weights["title"]), ("department", weights["department"]),
              ("body", weights["body"])]
    score = 0
    matched: dict[str, dict] = {}
    core_weight = 0
    for term, pattern, weight in keyword_rules:
        hit = False
        for field, multiplier in scopes:
            text = posting.get(field) or ""
            if text and pattern.search(text):
                score += weight * multiplier
                hit = True
        if hit:
            matched[term] = {"term": term, "weight": weight}
            core_weight = max(core_weight, weight)
    ranked = sorted(matched.values(), key=lambda m: (-m["weight"], m["term"]))
    return score, ranked, core_weight


def matches_any(patterns: list[re.Pattern], text: str) -> bool:
    return any(p.search(text or "") for p in patterns)


# ── eligibility: location normalization + ITAR / visa / remote detection ─────

# (pattern, country, region) — first match wins, so specific rules precede the
# US default heuristic. Locations on these boards are free strings ("Fremont",
# "Mountain View, CA", "London, UK"), hence a token table.
LOCATION_RULES: list[tuple[str, str, str]] = [
    (r"korea|seoul|busan|incheon|daejeon|daegu", "South Korea", "apac"),
    (r"japan|tokyo|osaka|yokohama|nagoya|fukuoka", "Japan", "apac"),
    (r"singapore", "Singapore", "apac"),
    (r"china|beijing|shanghai|shenzhen|hangzhou|suzhou|guangzhou", "China", "apac"),
    (r"taiwan|taipei", "Taiwan", "apac"),
    (r"hong kong", "Hong Kong", "apac"),
    (r"india|bengaluru|bangalore|hyderabad|pune|gurgaon|noida|mumbai|new delhi|chennai", "India", "apac"),
    (r"australia|sydney|melbourne|brisbane|perth", "Australia", "apac"),
    (r"new zealand|auckland", "New Zealand", "apac"),
    (r"vietnam|hanoi|ho chi minh", "Vietnam", "apac"),
    (r"malaysia|kuala lumpur", "Malaysia", "apac"),
    (r"indonesia|jakarta", "Indonesia", "apac"),
    (r"philippines|manila", "Philippines", "apac"),
    (r"thailand|bangkok", "Thailand", "apac"),
    (r"united kingdom|\buk\b|england|london|manchester|scotland|edinburgh|bristol", "United Kingdom", "emea"),
    (r"germany|munich|berlin|stuttgart|hamburg|frankfurt|cologne", "Germany", "emea"),
    (r"france|paris|toulouse|grenoble", "France", "emea"),
    (r"netherlands|amsterdam|eindhoven", "Netherlands", "emea"),
    (r"switzerland|zurich|lausanne|geneva", "Switzerland", "emea"),
    (r"sweden|stockholm|gothenburg", "Sweden", "emea"),
    (r"norway|oslo", "Norway", "emea"),
    (r"denmark|copenhagen", "Denmark", "emea"),
    (r"finland|helsinki|espoo", "Finland", "emea"),
    (r"ireland|dublin|cork", "Ireland", "emea"),
    (r"poland|warsaw|krakow|wroclaw", "Poland", "emea"),
    (r"spain|madrid|barcelona|valencia", "Spain", "emea"),
    (r"portugal|lisbon|porto", "Portugal", "emea"),
    (r"italy|milan|turin|bologna", "Italy", "emea"),
    (r"austria|vienna|graz", "Austria", "emea"),
    (r"belgium|brussels|leuven", "Belgium", "emea"),
    (r"czech|prague|brno", "Czechia", "emea"),
    (r"romania|bucharest|cluj", "Romania", "emea"),
    (r"greece|athens", "Greece", "emea"),
    (r"israel|tel aviv|herzliya|jerusalem", "Israel", "emea"),
    (r"united arab emirates|emirates|dubai|abu dhabi|saudi|riyadh|qatar|doha|kuwait|bahrain", "Middle East", "emea"),
    (r"turkey|istanbul|ankara", "Türkiye", "emea"),
    (r"south africa|johannesburg|cape town", "South Africa", "emea"),
    (r"canada|toronto|vancouver|montreal|ottawa|calgary|waterloo|kitchener", "Canada", "americas"),
    (r"mexico|mexico city|guadalajara|monterrey|juarez|tijuana", "Mexico", "americas"),
    (r"brazil|s[ãa]o paulo|curitiba|belo horizonte", "Brazil", "americas"),
    (r"argentina|buenos aires|cordoba", "Argentina", "americas"),
    (r"chile|santiago", "Chile", "americas"),
    (r"colombia|bogot[áa]|medell[íi]n", "Colombia", "americas"),
    (r"costa rica|san jos[ée]", "Costa Rica", "americas"),
    (r"united states|\busa\b|u\.s\.a|, usa|washington,? d\.?c\.|\bdc, usa\b", "United States", "americas"),
    (r"mountain view|palo alto|menlo park|san francisco|south san francisco|san mateo|"
     r"redwood city|foster city|fremont|newark|union city|hayward|oakland|berkeley|alameda|"
     r"emeryville|pleasanton|livermore|milpitas|sunnyvale|santa clara|san jose|cupertino|"
     r"saratoga|los gatos|campbell|santa cruz|gilroy|morgan hill|sacramento|davis|folsom|"
     r"roseville|fresno|bakersfield|santa barbara|goleta|ventura|oxnard|thousand oaks|"
     r"simi valley|burbank|glendale|pasadena|los angeles|culver city|el segundo|"
     r"manhattan beach|playa vista|santa monica|beverly hills|inglewood|torrance|"
     r"long beach|carson|hawthorne|gardena|downey|norwalk|whittier|anaheim|irvine|"
     r"santa ana|tustin|costa mesa|newport beach|huntington beach|garden grove|fullerton|"
     r"yorba linda|riverside|corona|temecula|escondido|san diego|la jolla|carlsbad|"
     r"oceanside|vista|san marcos|chula vista|poway", "United States", "americas"),
    (r"seattle|bellevue|kirkland|redmond|renton|tacoma|everett|bothell|spokane|vancouver, wa",
     "United States", "americas"),
    (r"austin|round rock|dallas|plano|frisco|fort worth|houston|san antonio|el paso|college station",
     "United States", "americas"),
    (r"phoenix|tempe|tucson|mesa|scottsdale|chandler|gilbert, az|goodyear", "United States", "americas"),
    (r"denver|boulder|colorado springs|aurora, co|golden, co|fort collins|longmont|lakewood, co|"
     r"westminster, co|broomfield|englewood, co|centennial, co|highlands ranch", "United States", "americas"),
    (r"chicago|naperville|evanston|schaumburg|peoria, il", "United States", "americas"),
    (r"detroit|dearborn|ann arbor|warren, mi|novi|auburn hills|troy, mi|plymouth, mi|livonia|"
     r"grand rapids|pontiac", "United States", "americas"),
    (r"boston|cambridge, ma|waltham|burlington, ma|bedford, ma|westford|hopkinton|marlborough|"
     r"westborough|north andover|andover|peabody|woburn|framingham|natick|needham|norton, ma|"
     r"north billerica|billerica", "United States", "americas"),
    (r"new york|new york city|\bnyc\b|manhattan|brooklyn|queens|long island city|jersey city|"
     r"newark, nj|hoboken|princeton|trenton|piscataway|edison, nj|bridgewater|morristown|"
     r"philadelphia|pittsburgh|state college|horsham|exton", "United States", "americas"),
    (r"atlanta|alpharetta|marietta|norcross|duluth, ga|savannah|peachtree", "United States", "americas"),
    (r"miami|fort lauderdale|orlando|tampa|jacksonville|cape canaveral|melbourne, fl|"
     r"st\.? petersburg|sarasota", "United States", "americas"),
    (r"charleston|north charleston|greenville, sc|columbia, sc", "United States", "americas"),
    (r"raleigh|durham|research triangle|chapel hill|cary, nc|charlotte|blacksburg|greensboro",
     "United States", "americas"),
    (r"richmond, va|arlington, va|alexandria, va|reston|herndon|chantilly|sterling, va|ashburn|"
     r"leesburg|manassas|virginia beach|norfolk|newport news|hampton, va|blacksburg, va|"
     r"charlottesville|roanoke, va", "United States", "americas"),
    (r"huntsville|washington|washington dc|\bwashington,\s+dc\b|bethesda|rockville|gaithersburg|"
     r"germantown, md|silver spring|baltimore|columbia, md|aberdeen, md|college park|"
     r"lanham|hanover, md|linthicum", "United States", "americas"),
    (r"columbus, oh|cleveland|cincinnati|dayton, oh|toledo, oh|ohio state", "United States", "americas"),
    (r"indianapolis|kansas city|st\.? louis|minneapolis|st\.? paul|rochester, mn|duluth, mn",
     "United States", "americas"),
    (r"salt lake city|provo|lehi|ogden|draper|orem", "United States", "americas"),
    (r"las vegas|reno|albuquerque|santa fe, nm|los alamos|boise|idaho falls", "United States", "americas"),
    (r"portland|eugene|bend, or|honolulu|omaha|lincoln, ne|milwaukee|madison, wi|green bay|"
     r"nashville|knoxville|memphis|chattanooga|oklahoma city|tulsa|wichita|little rock|"
     r"louisville|lexington, ky|buffalo|rochester, ny|albany, ny|syracuse|west lafayette|"
     r"south bend|carmel, in|fishers, in", "United States", "americas"),
    (r"houston, texas|texas|california|nevada|arizona|colorado|florida|georgia|michigan|ohio|"
     r"washington state|oregon|utah|virginia|maryland|massachusetts|new jersey|new york state|"
     r"illinois|pennsylvania|arlington, texas", "United States", "americas"),
]
LOCATION_RULE_COMPILED = [(compile_term(p), c, r) for p, c, r in LOCATION_RULES]
US_STATE_SUFFIX = re.compile(r",\s*[A-Z]{2}\s*,?\s*(?:USA)?\s*$")
# South Korea is deliberately absent: a Korea match routes to the dedicated
# `korea` bucket before APAC is ever consulted, and `korea-apac` keeps only the
# rest of APAC (Japan, Singapore, Taiwan, India, ...).
APAC_COUNTRIES = {"Japan", "Singapore", "China", "Taiwan", "Hong Kong",
                  "India", "Australia", "New Zealand", "Vietnam", "Malaysia",
                  "Indonesia", "Philippines", "Thailand"}
# Populated from config korea_location_terms in main() (the config is the SSOT),
# with the bounded Korean administrative-address rule always retained.
KOREA_LOCATION_PATTERNS: list[re.Pattern] = [
    *(compile_term(t) for t in DEFAULT_KOREA_LOCATION_TERMS),
    KOREAN_ADMINISTRATIVE_ADDRESS_PATTERN,
]

# 'clearance' alone is deliberately absent (mechanical 'gear clearance' false
# positives); the phrases below only appear in export-control contexts.
ITAR_PATTERNS = [compile_term(p) for p in [
    r"\bitar\b", "international traffic in arms", "export[- ]control",
    "export(ed)?[- ]controlled", "ear (export administration|regulation)",
    r"u\.?s\.?[- ]person", "united states[- ]person", r"u\.?s\.?[- ]citizen",
    "united states[- ]citizen", "american citizen", r"u\.?s\.? citizens? only",
    "security clearance", "top[- ]secret", r"ts/?sci", "clearance (check|requirement|to work)",
    r"obtain (a |an )?(u\.?s\.? )?(security )?clearance", "clearable",
]]
SPONSORSHIP_PATTERNS = [compile_term(p) for p in [
    "visa sponsorship (is )?(available|offered|provided)",
    r"(we|the company) sponsor(s)? (work )?visas?",
    r"sponsor(s|ing|ed)? (a )?(work )?visas?",
    "sponsorship (is )?(available|offered|provided)",
]]
ANTI_SPONSORSHIP_PATTERNS = [compile_term(p) for p in [
    r"(do(es)? not|cannot|can't|unable to|will not|won't) (offer |provide )?(visa |work )?(sponsor|sponsorship)",
    "no (visa )?sponsorship", "sponsorship (is )?not (available|offered|provided)",
    "without (visa )?sponsorship", "must already (have|possess|hold)",
    "(existing|current|pre-existing) work (authorization|permit)",
    "does not offer (visa|sponsorship|relocation)",
]]
REMOTE_STRONG_PATTERNS = [compile_term(p) for p in [
    r"full(y|y)? remote", r"100% remote", "remote[- ]first", "remote[- ]friendly",
    "remote[- ]eligible|remote eligible", r"work (from|remotely) (anywhere|home)",
    "remote (position|opportunity|role|job)", "distributed (team|company)",
]]

# `korea-apac` is a location bucket, not Korean work authorization. It remains
# visible in the raw eligibility distribution, but shortlist actionability
# requires affirmative sponsorship evidence and is counted from the classifier.
APPLICABLE_BUCKETS = ("korea", "sponsorship-likely", "remote")
# Single ordering used for ranking inside the report, for the distribution
# table rows, and for the caption: korea outranks everything, blocked-itar last.
BUCKET_PRIORITY = ("korea", "sponsorship-likely", "remote", "korea-apac",
                   "visa-needed", "blocked-itar")
BUCKET_LABELS = {
    "korea": "한국 근무",
    "sponsorship-likely": "비자 스폰서 가능성",
    "remote": "원격 근무 가능",
    "korea-apac": "한국 외 APAC",
    "visa-needed": "비자 필요 (스폰서 미확인)",
    "blocked-itar": "지원 불가 (ITAR/미국인 요건)",
}


def normalize_location(location_raw: str, country_hint: str = "") -> tuple[str, str]:
    """(country, region) from a free-text location. Region '' when unknown."""
    text = f"{location_raw or ''} {country_hint or ''}"
    if not text.strip():
        return "", ""
    for pattern, country, region in LOCATION_RULE_COMPILED:
        if pattern.search(text):
            return country, region
    # "Mountain View, CA" style: trailing US state abbreviation
    if location_raw and US_STATE_SUFFIX.search(location_raw.strip()):
        return "United States", "americas"
    return "", ""


def eligibility(posting: dict) -> tuple[str, str, str]:
    """Derive (eligibility, country, region), with ITAR always blocking first."""
    haystack = " ".join([posting.get("title") or "", posting.get("body") or ""])
    country, region = normalize_location(posting.get("location_raw") or "",
                                         posting.get("country_hint") or "")
    if matches_any(ITAR_PATTERNS, haystack):
        return "blocked-itar", country, region
    if matches_any(KOREA_LOCATION_PATTERNS,
                   f"{posting.get('location_raw') or ''} {posting.get('country_hint') or ''}"):
        return "korea", "South Korea", "apac"
    if country in APAC_COUNTRIES:
        return "korea-apac", country, region
    remote = posting.get("remote_flag") or matches_any(REMOTE_STRONG_PATTERNS, haystack)
    if remote:
        return "remote", country, region
    if matches_any(SPONSORSHIP_PATTERNS, haystack) and not matches_any(
            ANTI_SPONSORSHIP_PATTERNS, haystack):
        return "sponsorship-likely", country, region
    return "visa-needed", country, region


def filter_and_score(postings: list[dict], keyword_rules, negative_patterns,
                     negative_unless_core, seniority_patterns, weights,
                     min_score: int, keyword_tracks: dict[str, str] | None = None
                     ) -> tuple[list[dict], int, int]:
    """Shared keep-filter + scoring pass over one source's normalized postings
    (identical for every ATS). Returns (kept, n_negative, n_seniority); kept
    postings gain score/matched/eligibility/country/region/excerpt and explicit
    search-lane metadata in place. `keyword_tracks` is optional for callers
    using the legacy three-column keyword rule shape.
    """
    kept: list[dict] = []
    n_neg = n_sen = 0
    keyword_tracks = keyword_tracks or {}
    for posting in postings:
        title_dept = f"{posting['title']} {posting['department']}"
        if matches_any(seniority_patterns, posting["title"]):
            n_sen += 1
            continue
        if matches_any(negative_patterns, title_dept):
            n_neg += 1
            continue
        bucket, country, region = eligibility(posting)
        score, matched, core_weight = score_posting(posting, keyword_rules, weights)
        # Korea is the owner's priority bucket, so location replaces the score
        # gate there outright — a Korea role is worth seeing even at score 3,
        # and the score still orders the section. (Tying this to no_jd instead
        # was wrong: hydrating the real JD cleared the flag and silently cut
        # Korea from 114 to 2.) Negatives and seniority still apply, so the
        # non-fits are already gone; body-carrying non-Korea sources are
        # untouched and still face min_score.
        location_kept = bucket == "korea"
        if score < min_score and not location_kept:
            continue
        # 'data scientist' is disqualifying only when no core (weight>=5)
        # hardware keyword matched anywhere — see config negative_unless_core.
        if core_weight < 5 and matches_any(negative_unless_core, title_dept):
            n_neg += 1
            continue
        search_lanes = sorted(
            {
                normalize_track(keyword_tracks.get(match["term"], TRACK_CORE))
                for match in matched
            }
        ) or [TRACK_CORE]
        posting.update(score=score, matched=matched, eligibility=bucket,
                       country=country, region=region,
                       track=primary_track(search_lanes),
                       search_lane=primary_track(search_lanes),
                       search_lanes=search_lanes,
                       excerpt=make_excerpt(posting["body"]))
        kept.append(posting)
    return kept, n_neg, n_sen


# ── posting markdown ─────────────────────────────────────────────────────────

def yaml_value(value) -> str:
    """JSON is a YAML subset, so json.dumps is a safe way to quote scalars and lists."""
    return json.dumps(value, ensure_ascii=False)


def render_markdown(posting: dict, matched_terms: list[str]) -> str:
    body = posting["body"]
    truncated = len(body) > BODY_MAX_CHARS
    if truncated:
        body = body[:BODY_MAX_CHARS].rstrip() + "\n\n[... 이하 생략 — 본문 길이 제한]"
    search_lanes = sorted(
        {
            normalize_track(lane)
            for lane in (posting.get("search_lanes") or [posting.get("search_lane") or TRACK_CORE])
            if lane
        }
    ) or [TRACK_CORE]
    track = normalize_track(posting.get("track") or primary_track(search_lanes))
    if track == TRACK_CORE and any(lane != TRACK_CORE for lane in search_lanes):
        track = primary_track(search_lanes)
    lines = ["---"]
    lines.append(f"company: {yaml_value(posting['company'])}")
    lines.append(f"ats: {yaml_value(posting['ats'])}")
    lines.append(f"job_id: {yaml_value(posting['job_id'])}")
    lines.append(f"title: {yaml_value(posting['title'])}")
    lines.append(f"location: {yaml_value(posting['location_raw'])}")
    lines.append(f"country: {yaml_value(posting['country'])}")
    lines.append(f"region: {yaml_value(posting['region'])}")
    lines.append(f"eligibility: {yaml_value(posting['eligibility'])}")
    lines.append(f"track: {yaml_value(track)}")
    lines.append(f"search_lane: {yaml_value(track)}")
    lines.append(f"search_lanes: {yaml_value(search_lanes)}")
    lines.append(f"score: {posting['score']}")
    lines.append(f"matched_keywords: {yaml_value(matched_terms)}")
    lines.append(f"url: {yaml_value(posting['url'])}")
    lines.append(f"first_seen: {yaml_value(posting['first_seen'])}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {posting['title']} — {posting['company']}")
    lines.append("")
    lines.append(f"- 지원 자격: **{BUCKET_LABELS[posting['eligibility']]}** "
                 f"({posting['eligibility']}) · 점수 {posting['score']}")
    lines.append(f"- Track: **{track_label(track)}** ({track})")
    lines.append(f"- 위치: {posting['location_raw']}"
                 + (f" ({posting['country']})" if posting['country'] else ""))
    lines.append("")
    if posting.get("no_jd"):
        # Workday 목록 API는 JD 본문을 주지 않는다 — 요약이 본문인 척하지 않는다.
        lines.append("## JD 요약 (Workday 목록 API — 본문 미제공)")
        lines.append("")
        lines.append(body or "(JD 본문 미제공 — 제목·위치 기반 스코어링. "
                            "상세 요건은 원문 링크에서 확인)")
    else:
        lines.append("## JD 본문")
        lines.append("")
        lines.append(body or "(본문 없음 — 제목/부서 기반 스코어링)")
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
    if not isinstance(state, dict) or not isinstance(state.get("seen"), dict):
        log(f"ERROR: {path} has no valid seen mapping; refusing to overwrite the dedup ledger.")
        raise SystemExit(2)
    return state


# ── HTML daily report (same design system as the Wanted report) ──────────────

MAX_APPLICABLE_CARDS = 100
MAX_COLLAPSED_CARDS = 40
MAX_KEYWORD_CHIPS = 6

# Copied from scripts/wanted_collect.py REPORT_CSS so the two reports render as
# one product, plus global-only additions (eligibility chips, muted blocked deck).
REPORT_CSS = """
:root{--bg:#f4f5f7;--panel:#ffffff;--panel2:#eef0f3;--ink:#1c212b;--dim:#59637a;
--faint:#8b94a8;--line:#e2e5eb;--accent:#2a63e7;--accent-ink:#ffffff;
--alert-bg:#fdecec;--alert-border:#f2b8b5;--alert-ink:#9c1c1c;--alert-dim:#8a3030;
--chip-bg:#eef0f4;--ok:#1c7c4a;--ok-bg:#e3f3ea}
@media (prefers-color-scheme:dark){:root{--bg:#0f1319;--panel:#181d27;--panel2:#202634;
--ink:#e8ebf2;--dim:#a3adc2;--faint:#6e7880;--line:#2a3140;--accent:#5b8cff;
--accent-ink:#0d1220;--alert-bg:#3a1518;--alert-border:#7a2a2f;--alert-ink:#ff9d9d;
--alert-dim:#d98c8c;--chip-bg:#242b3a;--ok:#5fd39a;--ok-bg:#15301f}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.6 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif}
.wrap{max-width:680px;margin:0 auto;padding:20px 16px 56px}
h1{font-size:22px;margin:0;letter-spacing:-.02em}
.sub{color:var(--dim);font-size:13.5px;margin:3px 0 0}
h2{font-size:17px;margin:30px 0 12px;letter-spacing:-.01em}
.group{font-size:13.5px;color:var(--dim);font-weight:700;margin:16px 0 10px}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:16px 0 2px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.stat .k{display:block;font-size:11.5px;color:var(--faint);letter-spacing:.04em}
.stat .v{font-size:20px;font-weight:700}
.stat.core .v{color:var(--accent)}
.quiet{color:var(--faint);font-size:13.5px;background:var(--panel);
border:1px dashed var(--line);border-radius:10px;padding:12px 14px;margin:0}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{width:100%;border-collapse:collapse;font-size:14px;min-width:300px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}
thead th{color:var(--faint);font-size:11.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase}
tbody th{font-weight:500}
td.num,th.num{text-align:right}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:14px 16px;margin-bottom:12px}
.card.core{border-left:4px solid var(--accent)}
.card .pos{margin:0;font-size:16.5px;font-weight:700;line-height:1.4}
.card .co{margin:4px 0 0;color:var(--dim);font-size:13.5px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.chip{font-size:12px;padding:3px 9px;border-radius:999px;background:var(--chip-bg);
color:var(--dim);white-space:nowrap}
.chip-more{font-weight:700}
.chip-score{background:var(--panel2);color:var(--ink);font-weight:700}
.chip.elig-ok{background:var(--ok-bg);color:var(--ok);font-weight:700}
.chip.elig-blocked{background:var(--alert-bg);color:var(--alert-ink);font-weight:700}
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
details.muted{opacity:.62}
details.muted>summary{color:var(--alert-ink)}
.card.blocked .pos{color:var(--dim)}
.foot{margin-top:40px;color:var(--faint);font-size:12px;text-align:center}
a{color:var(--accent)}
"""


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def eligibility_chip(bucket: str) -> str:
    cls = "elig-ok" if bucket in APPLICABLE_BUCKETS else (
        "elig-blocked" if bucket == "blocked-itar" else "")
    return f'<span class="chip {cls}">{esc(BUCKET_LABELS[bucket])}</span>'


def keyword_chips(score: int, matched: list[dict]) -> str:
    chips = [f'<span class="chip chip-score">{score}점</span>']
    terms = [m["term"] for m in matched]
    chips += [f'<span class="chip">{esc(t)}</span>' for t in terms[:MAX_KEYWORD_CHIPS]]
    hidden = len(terms) - MAX_KEYWORD_CHIPS
    if hidden > 0:
        chips.append(f'<span class="chip chip-more">+{hidden}</span>')
    return f'<div class="chips">{"".join(chips)}</div>'


def report_card(posting: dict) -> str:
    blocked = posting["eligibility"] == "blocked-itar"
    core = bool(posting.get("actionable")) and not blocked
    classes = ["card"]
    if core:
        classes.append("core")
    if blocked:
        classes.append("blocked")
    meta = esc(posting["company"]) + " · " + esc(posting["location_raw"] or "위치 미기재")
    if posting.get("country"):
        meta += f' ({esc(posting["country"])})'
    parts = [f'<article class="{" ".join(classes)}">']
    parts.append(f'<h3 class="pos">{esc(posting["title"])}</h3>')
    parts.append(f'<p class="co">{meta}</p>')
    decision = reason_label(str(posting.get("reason", "actionable")))
    fit = posting.get("fit_score", 0)
    parts.append(f'<div class="chips"><span class="chip">{esc(track_label(posting.get("track")))}</span>'
                 f'{eligibility_chip(posting["eligibility"])}'
                 f'<span class="chip">{esc(decision)}</span>'
                 f'<span class="chip">fit {esc(fit)}</span></div>')
    parts.append(keyword_chips(posting["score"], posting["matched"]))
    if posting.get("no_jd"):
        # the list API gave no description — say so instead of an empty excerpt
        parts.append('<p class="req">JD 본문 미제공(Workday 목록 API) — 제목·위치·요약 '
                     "기준 채점. 상세 요건은 원문 링크에서 확인하세요.</p>")
        if posting.get("excerpt"):
            parts.append(f'<p class="req">{esc(posting["excerpt"])}</p>')
    elif posting.get("excerpt"):
        parts.append(f'<p class="req">{esc(posting["excerpt"])}</p>')
    if posting.get("url"):
        parts.append(f'<a class="btn" href="{esc(posting["url"])}">공고 원문 보기</a>')
    parts.append("</article>")
    return "".join(parts)


def render_deck(postings: list[dict], max_cards: int, label: str) -> list[str]:
    """One collapsed <details> deck; over-cap cards are counted, not rendered."""
    omitted = max(0, len(postings) - max_cards)
    note = f" · {omitted}건 표시 생략" if omitted else ""
    parts = [f'<details class="more"><summary>{esc(label)} {len(postings)}건'
             f'{esc(note)}</summary><div class="details-body">']
    visible = postings[:max_cards]
    for track in TRACK_ORDER:
        track_rows = [
            posting for posting in visible
            if normalize_track(posting.get("track")) == track
        ]
        if not track_rows:
            continue
        parts.append(
            f'<h4 class="group">{esc(track_label(track))} '
            f'({len(track_rows)}건)</h4>'
        )
        parts += [report_card(posting) for posting in track_rows]
    if omitted:
        parts.append(f'<p class="quiet">리포트 크기 상한({max_cards}건)으로 {omitted}건은 '
                     "표시에서 뺐습니다. 전체 목록은 state.json / 공고 파일을 참고하세요.</p>")
    parts.append("</div></details>")
    return parts


def render_html_report(today: str, fresh: list[dict], bucket_counts: dict,
                       n_companies: int, total_seen: int) -> str:
    """Render actionable high-fit roles separately from the complete raw set."""
    annotate_shortlist(fresh)
    actionable = rank_actionable(fresh)
    informational = sorted(
        [p for p in fresh if not p["actionable"]],
        key=lambda p: (
            str(p.get("reason", "")),
            -int(p.get("fit_score") or 0),
            str(p.get("company") or "").casefold(),
            str(p.get("title") or "").casefold(),
        ),
    )
    korea = [p for p in actionable if p.get("feasibility") == "korea"]
    other_actionable = [p for p in actionable if p.get("feasibility") != "korea"]
    n_applicable = len(actionable)

    def append_track_cards(rows: list[dict]) -> list[str]:
        parts: list[str] = []
        for track in TRACK_ORDER:
            track_rows = [
                row for row in rows
                if normalize_track(row.get("track")) == track
            ]
            if not track_rows:
                continue
            parts.append(
                f'<h4 class="group">{esc(track_label(track))} '
                f'({len(track_rows)}건)</h4>'
            )
            parts.extend(report_card(row) for row in track_rows)
        return parts

    body: list[str] = ['<main class="wrap">']
    body.append("<h1>글로벌 채용 리포트</h1>")
    body.append(f'<p class="sub">{esc(today)} · 글로벌 {n_companies}개사 보드 수집 '
                "(Greenhouse · Ashby · Lever · Workday)</p>")
    body.append(
        '<div class="stats">'
        f'<div class="stat core"><span class="k">한국</span>'
        f'<span class="v">{len(korea)}건</span></div>'
        f'<div class="stat"><span class="k">신규</span><span class="v">{len(fresh)}건</span></div>'
        f'<div class="stat"><span class="k">지원가능</span>'
        f'<span class="v">{n_applicable}건</span></div>'
        f'<div class="stat"><span class="k">누적</span>'
        f'<span class="v">{total_seen}건</span></div>'
        "</div>")

    body.append("<h2>지원 자격 분포 (오늘 신규 기준)</h2>")
    rows = []
    for bucket in BUCKET_PRIORITY:
        count = bucket_counts.get(bucket, 0)
        rows.append(f'<tr><th scope="row">{esc(BUCKET_LABELS[bucket])}</th>'
                    f'<td class="num">{count}건</td></tr>')
    body.append('<div class="scroll"><table><thead><tr><th>자격 구간</th>'
                f'<th class="num">공고 수</th></tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table></div>')

    body.append(f"<h2>Actionable high-fit shortlist ({len(actionable)}건)</h2>")
    body.append('<p class="group">한국 근무를 우선하고, 이후 한국 외 APAC·명시적 글로벌 원격·'
                "근거가 있는 스폰서 가능 역할을 fit 점수순으로 정렬했습니다.</p>")
    if korea:
        body.append(f'<h3 class="group">🇰🇷 한국 근무 {len(korea)}건</h3>')
        body += append_track_cards(korea)
    if other_actionable:
        body.append(f'<h3 class="group">기타 실행 가능 구간 {len(other_actionable)}건</h3>')
        body += append_track_cards(other_actionable)
    if not actionable:
        body.append('<p class="quiet">오늘 신규 중 실행 가능한 high-fit 공고가 없습니다.</p>')

    body.append(f"<h2>Raw collection · informational / ineligible ({len(informational)}건)</h2>")
    body.append('<p class="group">원시 수집 결과를 숨기지 않고, 비자·ITAR·미국 전용 원격·프로필 밖 역할을 '
                "지원 검토 목록과 분리했습니다. 각 카드의 판정 칩이 제외 사유입니다.</p>")
    if informational:
        body += render_deck(informational, len(informational),
                            "정보성 / 지원 불가 원문 전체")
    else:
        body.append('<p class="quiet">정보성/지원 불가 공고가 없습니다.</p>')

    body.append('<footer class="foot">scripts/global_collect.py 자동 생성 · '
                f"누적 {total_seen}공고 추적 중 · {datetime.now().strftime('%H:%M')} 생성 · "
                "승격 시 docs/jd/{회사}/ 디렉토리 생성 (docs/jd/README.md 참고)</footer>")
    body.append("</main>")

    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>글로벌 채용 리포트 {esc(today)}</title>"
        f"<style>{REPORT_CSS}</style></head><body>{''.join(body)}</body></html>")


# ── Telegram delivery (same helper as wanted_collect.py) ─────────────────────

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
    scripts/wanted_collect.py. Returns False on any failure; a delivery problem
    must never fail the collection run that already succeeded.
    """
    creds = telegram_creds(env_path)
    if creds is None:
        log(f"WARNING: Telegram credentials not found in {env_path}; report not sent "
            "(the collection run itself succeeded)")
        return False
    token, chat = creds
    boundary = "----global" + datetime.now().strftime("%H%M%S%f")
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


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect global job postings (Greenhouse/Ashby/Lever/Workday) "
                    "into the staging inbox.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG,
                        help=f"targets config (default: {DEFAULT_CONFIG})")
    parser.add_argument("--dry-run", action="store_true",
                        help="fetch + score every board, print counts, write nothing")
    parser.add_argument("--limit", type=int, default=None,
                        help="cap postings written (smoke test)")
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
    companies = config["companies"]
    workday_companies = config.get("workday", [])
    # config is the SSOT for the korea bucket terms and the Workday search plan
    KOREA_LOCATION_PATTERNS[:] = [
        *(compile_term(t) for t in (config.get("korea_location_terms")
                                    or DEFAULT_KOREA_LOCATION_TERMS)),
        KOREAN_ADMINISTRATIVE_ADDRESS_PATTERN,
    ]
    workday_search_terms = (config.get("workday_search_terms")
                            or DEFAULT_WORKDAY_SEARCH_TERMS)
    workday_page_limit = int(config.get("workday_page_limit", WORKDAY_PAGE_LIMIT))
    workday_stall_pages = int(config.get("workday_stall_pages", WORKDAY_STALL_PAGES))
    keyword_rules = [(kw["term"], compile_term(kw.get("pattern") or kw["term"]), int(kw["weight"]))
                     for kw in config["profile_keywords"]]
    keyword_tracks = {
        kw["term"]: normalize_track(kw.get("track", TRACK_CORE))
        for kw in config["profile_keywords"]
    }
    negative_patterns = [compile_term(t) for t in config["negative_keywords"]]
    negative_unless_core = [compile_term(t) for t in config["negative_unless_core"]]
    seniority_patterns = [compile_term(t) for t in config["seniority_exclude"]]
    weights = {"title": int(config["title_weight"]), "department": int(config["department_weight"]),
               "body": int(config["body_weight"])}
    min_score = int(config["min_score"])
    delay = float(config["request_delay_seconds"])

    state_path = INBOX_DIR / "state.json"
    state = load_state(state_path)
    seen = state["seen"]

    sess = PoliteSession(delay)
    today = date.today().isoformat()

    # ---- phase 1: fetch every source -> filter, score ------------------------
    kept: list[dict] = []
    fetched_total = 0
    failed_companies: list[str] = []
    for company in companies:
        postings = fetch_board(sess, company)
        if postings is None:
            failed_companies.append(company["name"])
            log(f"[board] {company['name']} ({company['ats']}:{company['slug']}): FAILED")
            continue
        fetched_total += len(postings)
        kept_here, n_neg, n_sen = filter_and_score(
            postings, keyword_rules, negative_patterns, negative_unless_core,
            seniority_patterns, weights, min_score, keyword_tracks)
        kept.extend(kept_here)
        log(f"[board] {company['name']}: fetched={len(postings)} kept={len(kept_here)} "
            f"negatives={n_neg} seniority={n_sen}")

    for company in workday_companies:
        postings = fetch_workday(sess, company, workday_search_terms,
                                 workday_page_limit, workday_stall_pages)
        if postings is None:
            failed_companies.append(f"{company['name']} (workday:{company['tenant']})")
            log(f"[workday] {company['name']} ({company['tenant']}): FAILED")
            continue
        fetched_total += len(postings)
        # Korea rows only: pull the real JD so the 한국 section can be ranked
        # rather than sorted by a title-only score that tops out near 9.
        hydrate_workday_korea(sess, company, postings, KOREA_LOCATION_PATTERNS)
        kept_here, n_neg, n_sen = filter_and_score(
            postings, keyword_rules, negative_patterns, negative_unless_core,
            seniority_patterns, weights, min_score, keyword_tracks)
        kept.extend(kept_here)
        n_korea_here = sum(1 for p in kept_here if p["eligibility"] == "korea")
        log(f"[workday] {company['name']}: fetched={len(postings)} kept={len(kept_here)} "
            f"korea={n_korea_here} negatives={n_neg} seniority={n_sen}")

    n_sources = len(companies) + len(workday_companies)
    if n_sources and len(failed_companies) == n_sources:
        log("ERROR: every company board failed - APIs down or response shapes changed.")
        return 1
    if failed_companies:
        log(f"NOTE: board fetch failed for (skipped): {failed_companies}")

    log(f"[score] fetched={fetched_total} kept_after_scoring={len(kept)} "
        f"min_score={min_score}")

    bucket_counts = {b: 0 for b in BUCKET_LABELS}
    for p in kept:
        p["key"] = f"{p['ats']}:{p['slug']}:{p['job_id']}"
        bucket_counts[p["eligibility"]] += 1
    annotate_shortlist(kept)
    log("[eligibility] " + " · ".join(f"{b}={bucket_counts[b]}" for b in BUCKET_LABELS))
    n_actionable = sum(1 for p in kept if p["actionable"])
    log(f"[shortlist] actionable_high_fit={n_actionable} informational_or_ineligible="
        f"{len(kept) - n_actionable}")

    if args.dry_run:
        log(f"[dry-run] would write {sum(1 for p in kept if p['key'] not in seen)} posting "
            f"files ({sum(1 for p in kept if p['key'] in seen)} already seen); "
            "no files written.")
        log(f"[stats] http calls: {sess.n_calls}")
        return 0

    # ---- phase 2: write new posting files (skip everything the ledger knows) --
    written: list[dict] = []
    backfilled = 0
    for posting in kept:
        if posting["key"] in seen:
            # A Workday posting is first written before its JD is hydrated, and
            # after that the ledger keeps skipping it — so the archived file
            # keeps the empty body it was born with, for exactly the Korea rows
            # that matter most. Rewrite it once the body arrives.
            if posting.get("body") and not posting.get("no_jd"):
                path = INBOX_DIR / f"{posting['slug']}-{posting['job_id']}.md"
                try:
                    if path.exists() and len(path.read_text(encoding="utf-8")) < len(
                            posting["body"]):
                        posting["first_seen"] = seen[posting["key"]].get("first_seen", today)
                        path.write_text(
                            render_markdown(posting,
                                            [m["term"] for m in posting["matched"]]),
                            encoding="utf-8")
                        backfilled += 1
                except OSError as e:
                    log(f"    [backfill {posting['key']}] ERROR {e}")
            continue
        if args.limit is not None and len(written) >= args.limit:
            break
        posting["first_seen"] = today
        filename = f"{posting['slug']}-{posting['job_id']}.md"
        try:
            content = render_markdown(posting, [m["term"] for m in posting["matched"]])
            INBOX_DIR.mkdir(parents=True, exist_ok=True)
            (INBOX_DIR / filename).write_text(content, encoding="utf-8")
        except OSError as e:
            log(f"    [write {posting['key']}] ERROR {e}")
            continue
        written.append(posting)
        # only mark seen once the file exists, so failed ids retry next run
        seen[posting["key"]] = {
            "first_seen": today,
            "company": posting["company"],
            "title": posting["title"],
            "score": posting["score"],
            "eligibility": posting["eligibility"],
            "track": posting["track"],
            "search_lane": posting["search_lane"],
            "search_lanes": posting["search_lanes"],
            "fit_score": posting["fit_score"],
            "actionable": posting["actionable"],
            "fit_evidence": posting["fit_evidence"],
            "technical_signal_evidence": posting["technical_signal_evidence"],
            "owner_domain_evidence": posting["owner_domain_evidence"],
        }
        log(f"[write] {filename} — {posting['title']} @ {posting['company']} "
            f"(score {posting['score']}, {posting['eligibility']})")

    if backfilled:
        log(f"[backfill] rewrote {backfilled} posting files with their hydrated JD")

    # Refresh the mutable fields of postings already in the ledger. `first_seen`
    # is the one immutable field — it is what dedup and "new today" rest on.
    # Score and eligibility are re-derived every run (a Workday row's score
    # jumps once its JD is hydrated, and a role can be reposted to a new
    # location), so leaving the first-seen values in place makes state.json
    # disagree with the report it is supposed to describe.
    n_refreshed = 0
    for posting in kept:
        row = seen.get(posting["key"])
        if row is None or posting in written:
            continue
        if (row.get("score") != posting["score"]
                or row.get("eligibility") != posting["eligibility"]
                or row.get("track") != posting["track"]
                or row.get("search_lane") != posting["search_lane"]
                or row.get("search_lanes") != posting["search_lanes"]
                or row.get("fit_score") != posting["fit_score"]
                or row.get("actionable") != posting["actionable"]
                or row.get("fit_evidence") != posting["fit_evidence"]
                or row.get("technical_signal_evidence")
                != posting["technical_signal_evidence"]
                or row.get("owner_domain_evidence")
                != posting["owner_domain_evidence"]):
            row["score"] = posting["score"]
            row["eligibility"] = posting["eligibility"]
            row["title"] = posting["title"]
            row["track"] = posting["track"]
            row["search_lane"] = posting["search_lane"]
            row["search_lanes"] = posting["search_lanes"]
            row["fit_score"] = posting["fit_score"]
            row["actionable"] = posting["actionable"]
            row["fit_evidence"] = posting["fit_evidence"]
            row["technical_signal_evidence"] = posting["technical_signal_evidence"]
            row["owner_domain_evidence"] = posting["owner_domain_evidence"]
            n_refreshed += 1
    if n_refreshed:
        log(f"[state] refreshed score/eligibility on {n_refreshed} known postings")

    # ---- phase 3: persist state ----------------------------------------------
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    try:
        atomic_write_json(state_path, state)
    except (OSError, TypeError, ValueError) as e:
        log(f"ERROR: atomic state persistence failed for {state_path}: {e}")
        return 1

    # today's set: covers re-runs within the same day (files come from `kept`,
    # which re-scores every board each run, so cards stay complete on re-render)
    fresh_today = [p for p in kept if p["key"] in seen
                   and seen[p["key"]]["first_seen"] == today]
    fresh_counts = {b: 0 for b in BUCKET_LABELS}
    for p in fresh_today:
        fresh_counts[p["eligibility"]] += 1
    n_new = len(fresh_today)
    n_applicable = sum(1 for p in fresh_today if p.get("actionable"))
    log(f"[done] written: {len(written)} | new today: {n_new} "
        f"(한국 {fresh_counts['korea']} · 지원가능 {n_applicable}) | "
        f"state: {len(seen)} postings seen")

    # ---- phase 4: HTML report + optional Telegram delivery --------------------
    report_path: Path | None = None
    if args.html:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = REPORT_DIR / f"{today}.html"
        report_path.write_text(
            render_html_report(today, fresh_today, fresh_counts,
                               len(companies) + len(workday_companies), len(seen)),
            encoding="utf-8")
        log(f"[report] {report_path.relative_to(REPO_ROOT)} "
            f"({report_path.stat().st_size:,} bytes)")
    if args.telegram:
        if report_path is None or not report_path.exists():
            log("WARNING: --telegram requested but no rendered report exists; nothing sent.")
        else:
            caption = (f"🌐 글로벌 채용 리포트 {today}\n"
                       f"🇰🇷 한국 {fresh_counts['korea']}건\n"
                       f"신규 {n_new}건 (지원가능 {n_applicable}) / 누적 {len(seen)}건")
            if send_report_via_telegram(report_path, caption, args.env):
                log("[telegram] report delivered to the PM bot")

    log(f"[stats] http calls: {sess.n_calls}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
