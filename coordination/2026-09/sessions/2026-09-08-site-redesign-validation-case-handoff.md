# Handoff — portfolio site redesign, SS500 progress, production-validation case (2026-09-06 → 08)

Session: Claude (Fable 5.1, PM pane) with three Explore subagents (image audit, test-evidence
inventory, and one review pass: design / hiring-manager content / fact-check + confidentiality).

## Goal

Bring the portfolio (site + application material) up to the September 2026 foundation: RS500
autonomy stack, SS500 April–September work (MBD, CAN ICD, DFMEA WPs, fleet ops, production
validation), a visual design pass, and an application ledger that replaces the daily Wanted dump.

## Exact state

Site (`src/`, `public/`) — **7 local commits on master, not pushed**:

| commit | content |
|---|---|
| 2456e75 | RS500 autonomy-stack case, og/canonical/JSON-LD, robots.txt, image compression |
| 3c45d50 | SS500 Apr–Sep progress: MBD case, DFMEA A-5/A-6, APQP D-9..D-13, hero "양산 1호기" |
| bfad6c1 | design pass: hero backdrop, StatStrip, SectionHead, TestGallery, Principles band, MbdPipeline SVG |
| 826d963 | production-validation case (DVP&R, QC gates, 6 TRs, patternator jig, FFR, demo fail→retest) |
| d2a2649 | design + content review applied: KPI hierarchy, mobile reflow, a11y, dispositions, safety frame, open items, MBD prediction-vs-measurement table |
| 3920f69 | fact-check pass: DVP&R 35→51, TR-1/TR-2/TR-6 figures, next-gen naming, customer names anonymized, FW internals removed |

Build: 10 pages, 0 broken local refs, 0 console errors, no horizontal overflow at 390 px. Built
HTML leak scan is clean except two pre-existing strings (fan ESC vendor name in the CAN diagram,
₩ on the insung-blog page) that predate this session.

Application material (uncommitted, on disk):
- `docs/jd/applications.json` (7 rows, SSOT) + `scripts/applications_report.py` + 11 tests;
  cron 11:47 now sends this instead of the Wanted dump (manifest + cron.md updated in project-manager)
- `docs/jd/tesla/` (README, APPLY, mapping, resume_tesla.md, JD capture, 61-opening snapshot)
- `docs/jd/nvidia/` (README, APPLY, mapping — 21 Korea openings checked, none clears the years gate)
- `docs/jd/apple/materials/` resume v7.1 + cover letter v5 rebuilt on the new foundation, PDFs in `pdf_draft/`
- `docs/blocks/01-inventory/ACTIVITY_INVENTORY.md`, `docs/blocks/02-usage/EXPERIENCE_SORT.md`

## Verification

Playwright screenshots at 1280 and 390 px for every changed section; `npm run build` after each
change; local-ref check over `dist/`; fact-check subagent verified 63 figures against HIH_2 and
rs500 sources (9 mismatches, all fixed in 3920f69).

## Blockers / decisions owed by the user

1. `git push origin master` — GitHub Pages deploys on push. Live site is still the 2026-08-19 build.
2. Hero tagline: reviewer suggests "48 V 전동 농기계 전력·제어 — 설계에서 양산 검증까지" over "분야를 막론하고".
3. AI-workflow card: keep the cron/systemd inventory numbers, or cut to the CAN log viewer + fleet SSOT lines.
4. Q1–Q6 from `ACTIVITY_INVENTORY.md` §1.2 (units shipped, J-Agri result, current NCR/DFMEA counts,
   SS600 status, HIH_2 attribution, language-test retake) — these gate the RESUME.md §4 update.
5. Whether to anonymize the two pre-existing strings named above.

## Next action

Push if approved; then apply decisions 2–3 as one small commit; then commit the application
material separately from the prior session's collector edits (`scripts/global_collect.py`,
`scripts/wanted_collect.py`, `docs/jd/_inbox/**`, `HANDOFF.md`, `TASK.md`, `TEST_LOG.md`,
`WORK_LOG.md` — untouched here, left for their owner).
