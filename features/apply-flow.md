# Feature: apply-flow

## What

Turns the collected postings into one application a human can finish: a ranked daily shortlist, a tailored kit per posting built only from the operator's own profile lines, a browser step that fills the form up to (never including) submit, and a ledger step that tracks applied / response / interview. Proposal and rationale: `docs/jd/01_apply-flow-proposal.md`.

## Entry points

- `python3 scripts/apply_flow.py shortlist [--top 10] [--check-open] [--out PATH] [--inbox DIR]` — ranked candidates with reasons; `--check-open` verifies each is still live
- `python3 scripts/apply_flow.py kit KEY [--questions FILE.json]` — writes `docs/jd/<company>/1_resume-variant.md … 5_portfolio-links.md` (KEY is `wanted:ID`, `global:ID`, `jasoseol:ID`)
- `python3 scripts/apply_flow.py track KEY STATUS [--note TEXT]` — moves the ledger row, appends a dated `history` entry, regenerates `APPLICATIONS.md`
- `<playwright-venv>/bin/python -I scripts/apply_browser.py URL --kit docs/jd/<company> --shots DIR` — fills the form in a new tab of the automation Chrome (CDP 9240); exit 2 when blocked

## Contract

- Inputs: `docs/jd/_inbox/{wanted,global,jasoseol}`, `docs/blocks/05-extra/RESUME.md`, `docs/jd/apple/materials/resume_en.md`, `docs/jd/applications.json`
- Outputs: shortlist Markdown, the five kit files, ledger rows with `history`, screenshots of the filled unsubmitted form
- Gates: postings must pass `shortlist.assess_shortlist` (feasibility + fit); expired, already-in-ledger and duplicate re-posts are dropped; domain terms the profile has no record of lower the rank
- Never: clicks a submit/apply control, types a draft containing `[TODO]`, creates an account, or invents a profile fact

## Data and state

- Repository data: kits under `docs/jd/<company>/` (company folder is an ASCII slug, `<source>-<id>` for Korean-only names)
- External state: ATS public APIs and the Wanted job API (read only); the automation Chrome via CDP
- Secrets: none; logins are `hih login` broker sessions, and a missing one is reported, not worked around

## Tests

- `.venv/bin/python -m pytest tests/test_apply_flow.py` (loading, ranking and filtering, ATS open-check URLs, kit uses only profile lines, answers, ledger tracking, browser guards and plan)
- Browser driver verified by hand against a local fixture form (filled 3 standing fields, left salary empty, stopped before submit)

## Status

built 2026-10-14, not scheduled. First real run: `wanted:383727` (도울로보틱스 로봇 제어 엔지니어) reached the Wanted login wall; no stored Wanted login (see `docs/jd/wanted-383727/README.md`).
