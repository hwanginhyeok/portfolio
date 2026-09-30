# features/ - feature specification index

One spec per shipped feature, following `features/_template.md`
(What, Entry points, Contract, Data and state, Tests, Status).
`site/index.html` is generated from these files by `scripts/generate_site.py`.

| Spec | What |
|---|---|
| `features/astro-portfolio.md` | Astro + Tailwind static engineering portfolio (case studies, diagrams, charts) |
| `features/jasoseol-collector.md` | Jasoseol calendar/recruit API crawler with profile fit scoring |
| `features/jasoseol-report.md` | Daily actionable Jasoseol HTML digest announced via `hih notify` |
| `features/jasoseol-calendar.md` | Jasoseol application deadlines synced to Google Calendar |
| `features/wanted-collector.md` | Wanted API crawler with owner-domain fit gate and dedup ledger |
| `features/global-collector.md` | Global ATS (Workday/Greenhouse/Ashby/Lever) crawler and reports |
| `features/applications-ledger.md` | Application pipeline ledger, Markdown view, and morning report |
| `features/presentation-builder.md` | Graduate portfolio PPTX deck generators |
| `features/harness-scheduling.md` | Six macOS LaunchAgents, `hih notify` alerts, Keychain secrets |
