# Handoff — Q1–Q6 resolved from HIH_2, site pushed, ledger and collector commits (2026-09-08)

Session: Claude (Fable 5.1, PM pane) with two Explore subagents over `~/HIH_2`
(Notion crawl cache, data CSVs, dashboard data, git history).

## Done

- Pushed the six site commits from the previous handoff; GitHub Pages deployed
  (live site now carries the September foundation).
- Decisions 2, 3, 5 applied (`173fc5c`): hero tagline "48 V 전동 농기계 전력·제어 —
  설계에서 양산 검증까지", AI card swaps cron/systemd counts for the CAN log viewer
  and fleet SSOT lines, meta description aligned. Hobbywing ESC model and the
  insung-blog KRW prices stay — public product facts.
- Committed the 2026-08-24 Codex collector work (`b1652d7`) and the application
  ledger material (`808c003`) as two commits, plus the JD inbox through today.
  `docs/jd/report/` is now ignored (daily generated HTML).
- Q1–Q5 answered from the repo instead of the user (`ACTIVITY_INVENTORY.md` §1.2
  holds the answers with source paths); `RESUME.md` §2/§4/§5.1/§A, `cases.json`,
  Principles, APQPSystem (new D-15), Timeline, and the NVIDIA mapping carry the
  verified numbers: first customer delivery 2026-04-16 (2 units), 5 customer
  deliveries by 2026-09, 15/21 built, issues 128 (own 30), NCR 27+17, DFMEA AP=H
  20 (14 confirmed), DVP&R 51 (row count; the header's 35 is stale).
- Fixed `sync_task_summary.py` in project-manager (`0714494`): its summary regex
  ended at any `---`, so markdown table separators ate the heading after the
  summary on every sync. Restored the headers in portfolio `TASK.md` and HIH_2
  `TASK.md` (`78a091e`).

## Refuted during verification

- Subagent reported DVP&R = 35 from the matrix header. The table has 51 ID rows
  and the previous session already counted them; 51 stands.
- J-Agri 2025 never happened in the record. The only J-AGRI is October 2026
  (mock-up still in build on 2026-09-07). Do not present it as a result.
- SS1000 is not the successor; SS600 (600 L-class) is, user-confirmed 2026-08-25,
  still at G0/G1 planning.

## Open

- Q6 language retake: no date anywhere (calendar searched). User decision.
- HIH_2 ownership: no confidentiality policy exists in the company repo, and every
  commit is the user's (plus the user's own agents), but `HIH_Claude` is a personal
  GitHub submodule inside a company project. The site shows text descriptions
  only, no customer data — kept as is; confirm with the company before any
  screenshot-level disclosure.
- Apple resume v7.1 still says "27 NCRs" (true for the first report). Left
  untouched because it is submission-ready; regenerate PDFs if the number is
  updated to 44.
- Sync Insung Stats GitHub Action fails weekly — B4-05 secrets not registered.
