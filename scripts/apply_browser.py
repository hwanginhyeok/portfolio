#!/usr/bin/env python3
"""Submission assist: fill an application form in the automation Chrome, stop before submit.

The operator presses the final button, never this script. Rules enforced in code:

- the page is opened in a NEW tab of the automation Chrome (CDP, default port
  9240) and closed afterwards; other agents' tabs are never touched;
- only text inputs and textareas are filled; no control whose text looks like a
  submit/apply action is ever clicked (``is_submit_control``);
- values come from the kit (``4_form-answers.md`` rules in apply_flow) or the
  standing profile fields; a field with no sourced answer is left empty and
  reported, never guessed;
- a screenshot of the filled, unsubmitted form is saved as evidence.

Needs Playwright (not part of the portfolio venv), e.g. the experience venv:
    /path/to/venv/bin/python -I scripts/apply_browser.py URL --kit docs/jd/<company> --shots DIR

A login wall is reported as ``blocked-login`` (no account is ever created).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:  # package import when tested; direct import when run as a script
    from scripts import apply_flow
except ModuleNotFoundError:  # pragma: no cover - exercised by CLI execution
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import apply_flow

CDP_URL = "http://127.0.0.1:9240"
# Words that make a control a final submission. Matching is case-insensitive.
SUBMIT_WORDS = ("submit", "apply", "send application", "지원하기", "지원 완료", "제출", "지원서 제출")
LOGIN_WORDS = ("로그인", "sign in", "log in", "회원가입", "create account")

# Standing answers the repo itself records (RESUME.md §1, applications ledger).
STANDING = {
    "name": "황인혁",
    "full name": "Inhyeok Hwang",
    "email": "dlsgur5560@gmail.com",
    "portfolio": apply_flow.SITE_URL,
    "website": apply_flow.SITE_URL,
    "github": apply_flow.GITHUB_URL,
}


def is_submit_control(text: str) -> bool:
    lowered = (text or "").strip().lower()
    return any(word in lowered for word in SUBMIT_WORDS)


def looks_like_login_wall(url: str, body_text: str) -> bool:
    lowered = f"{url} {body_text[:2000]}".lower()
    return "/login" in lowered or sum(w in lowered for w in LOGIN_WORDS) >= 2


def plan_fill(fields: list[dict], evidence_en: list[dict], posting: dict) -> list[dict]:
    """One row per form field: the value to type, or None with the reason."""
    plan = []
    for field in fields:
        label = str(field.get("label") or field.get("name") or "").strip()
        lowered = label.lower()
        value = next((v for k, v in STANDING.items() if re.search(rf"\b{re.escape(k)}\b", lowered)), None)
        reason = "standing profile field" if value else ""
        if value is None and field.get("type") in ("textarea", "text"):
            answer = apply_flow.answer_question(label, evidence_en, posting).replace("**", "")
            if "[TODO" in answer:  # never type a draft that still needs the operator
                reason = "needs operator input; draft kept in 4_form-answers.md"
            else:
                value, reason = answer, f"kit answer ({apply_flow.classify_question(label)})"
        plan.append({"label": label, "type": field.get("type"), "value": value, "reason": reason})
    return plan


def read_fields(page) -> list[dict]:
    """Visible text-like controls with their label text."""
    return page.evaluate(
        """() => [...document.querySelectorAll('input, textarea')].filter(e => {
            const t = (e.type || 'text').toLowerCase();
            const r = e.getBoundingClientRect();
            return ['text','email','tel','url','search',''].includes(t) || e.tagName === 'TEXTAREA'
              ? r.width > 0 && r.height > 0 && !e.disabled : false;
        }).map((e, i) => {
            const id = e.id && document.querySelector(`label[for="${CSS.escape(e.id)}"]`);
            const wrap = e.closest('label');
            const label = (id && id.innerText) || (wrap && wrap.innerText) || e.getAttribute('aria-label')
              || e.placeholder || e.name || '';
            e.setAttribute('data-apply-idx', String(i));
            return {idx: i, label: label.trim(), name: e.name || '',
                    type: e.tagName === 'TEXTAREA' ? 'textarea' : (e.type || 'text')};
        })"""
    )


def run(url: str, kit_dir: Path, shots: Path, cdp: str = CDP_URL,
        inbox: Path = apply_flow.INBOX) -> dict:
    from playwright.sync_api import sync_playwright  # imported late: optional dependency

    posting_key = _kit_key(kit_dir)
    posting = apply_flow.find_posting(posting_key, inbox) if posting_key else {"company": "", "title": ""}
    evidence_en = apply_flow.rank_facts(
        f"{posting.get('title', '')} {posting.get('body', '')}", apply_flow.load_facts(), "en")[:3]
    shots.mkdir(parents=True, exist_ok=True)
    report: dict = {"url": url, "result": "", "fields": [], "screenshots": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp)
        page = browser.contexts[0].new_page()  # our own tab only
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)
            if looks_like_login_wall(page.url, page.inner_text("body")):
                report["result"] = "blocked-login"
                return report
            fields = read_fields(page)
            plan = plan_fill(fields, evidence_en, posting)
            for field, row in zip(fields, plan):
                if row["value"]:
                    page.locator(f'[data-apply-idx="{field["idx"]}"]').fill(row["value"])
            report["fields"] = plan
            shot = shots / "3_form-filled-not-submitted.png"
            page.screenshot(path=str(shot), full_page=True)
            report["screenshots"].append(str(shot))
            report["result"] = "filled-not-submitted"
        finally:
            page.close()
    return report


def _kit_key(kit_dir: Path) -> str:
    """The posting key a kit was written for (first `키` line of its README-style header)."""
    for name in sorted(kit_dir.glob("*.md")):
        match = re.search(r"키 `([^`]+)`", name.read_text(encoding="utf-8"))
        if match:
            return match.group(1)
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("url")
    parser.add_argument("--kit", type=Path, required=True, help="kit directory written by apply_flow kit")
    parser.add_argument("--shots", type=Path, required=True)
    parser.add_argument("--cdp", default=CDP_URL)
    parser.add_argument("--inbox", type=Path, default=apply_flow.INBOX)
    args = parser.parse_args(argv)
    report = run(args.url, args.kit, args.shots, args.cdp, args.inbox)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["result"] == "filled-not-submitted" else 2


if __name__ == "__main__":
    sys.exit(main())
