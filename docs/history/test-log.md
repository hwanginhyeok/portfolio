# TEST_LOG

## t34 macOS cutover prep (2026-09-29)
Test venv created per README (`uv venv .venv --python 3.12` then
`uv pip install --offline pytest requests pyyaml`; the repo has no pyproject).

| Command | Result | Notes |
|---|---|---|
| `.venv/bin/python -m pytest` | 106 passed, 1 failed, 16 subtests | The single failure is the pre-existing, date-sensitive `test_live_inbox_loads_and_renders` (asserts >=5 actionable postings; 4 remain now that deadlines passed). Unrelated to this change; see Known Failures. |
| `.venv/bin/python -m pytest tests/test_notify.py tests/test_jasoseol_report.py tests/test_jasoseol_calendar.py tests/test_applications_report.py` | PASS (except the same live-inbox test) | New notify/secret tests, notify-based report tests, direct `hih-schedule` exec tests. |
| `plutil -lint launchd/*.plist` | OK (6/6) | Absolute paths only; exact server times/args; `Aqua`; logs under `~/Library/Logs/hih/`. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile scripts/*.py` | PASS | Six jobs plus the new `scripts/notify.py` compile. |
| `.venv/bin/python scripts/generate_site.py` | PASS | `site/index.html` regenerated with the `harness-scheduling` feature row. |
| `git diff --check` | PASS | No whitespace errors. |

No network, no Keychain access, and no `launchctl` call were made.


## Final Verification
| Date | Command | Result | Notes |
|---|---|---|---|
| 2026-08-24 | `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p 'test_job_collectors.py' -v` | PASS | 20 focused tests: atomic persistence, lossless ledger reconstruction, bounded hydration seam, strict owner-domain gates, three realistic Wanted false positives, Aptiv Manufacturing Engineering/Test Lab positives, motor/reliability/test positives, APAC sponsorship gates, Korean district-address recognition, feasibility precedence, and ranking. |
| 2026-08-24 | AST parse with `PYTHONDONTWRITEBYTECODE=1 python3 -B` | PASS | All five code modules and `tests/test_job_collectors.py` parsed without bytecode output. |
| 2026-08-24 | Package/direct import smoke checks | PASS | All five code modules import as a package and their direct-file CLIs import from both repository root and `scripts/`. |
| 2026-08-24 | In-memory Wanted/global report rendering fixture | PASS | Both reports contain separate actionable high-fit and raw informational/ineligible sections; no filesystem or JD writes. |
| 2026-08-24 | Read-only ledger integrity and hydration preservation check | PASS | 327 current entries = 299 baseline + 28 additions; all 299 baseline rows preserved; 16 hydrated JDs have direct URLs; zero-byte Wanted JD count is 0. |
| 2026-08-24 | Strict local Wanted/global shortlist scan | PASS | Read-only scan of 328 Wanted and 587 global JD files: Wanted 7 actionable / 321 informational; global 14 actionable / 573 informational. All 21 actionable rows have title/department fit and owner-domain evidence; non-sponsored APAC rows remain informational. |
| 2026-08-24 | `git diff --check` | PASS | No whitespace errors. |
| 2026-08-24 | `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p 'test_job_collectors.py' -v` | PASS | 25 focused tests: preserved core/feasibility behavior, actionable industrial AI solutions architect and feasible forward-deployed robotics engineer, informational generic cloud solutions architect and AI product manager, and Wanted/global track metadata propagation. |
| 2026-08-24 | AST/JSON/report-fixture checks | PASS | Collector modules and focused tests parsed; both configs parsed; Wanted/global HTML fixtures rendered with separate track headings; no collector or delivery run. |

### Final top shortlist

Top five per source, ranked by the strict local classifier:

| Source | Title | Company | Direct source |
|---|---|---|---|
| Wanted | Semiconductor PCB autonomous manufacturing consultant | 인터엑스 | https://www.wanted.co.kr/wd/358085 |
| Wanted | Hardware Engineer (Circuit Design) | 닷 | https://www.wanted.co.kr/wd/124026 |
| Wanted | System Software Engineer (Embedded AI) | 소울아트 | https://www.wanted.co.kr/wd/350980 |
| Wanted | 전장설치 엔지니어 | 씨드로닉스 | https://www.wanted.co.kr/wd/293489 |
| Wanted | 로봇 전장설계 HW 엔지니어 | 에이로봇 | https://www.wanted.co.kr/wd/300816 |
| Global | Test Lab engineer | Aptiv | https://aptiv.wd5.myworkdayjobs.com/Aptiv_Careers/job/Ulsan-Republic-of-Korea/Test-Lab-engineer_J000702784 |
| Global | Manufacturing Engineering Engineer | Aptiv | https://aptiv.wd5.myworkdayjobs.com/Aptiv_Careers/job/KOR-Asan--MFG/Manufacturing-Engineering-Engineer_J000666213 |
| Global | DDP/Epitaxy Module Process Engineer | Applied Materials | https://amat.wd1.myworkdayjobs.com/External/job/Icheon-GwangoKOR/DDP-Epitaxy-Module-Process-Engineer_R2625397 |
| Global | Epitaxy Module Process Engineer | Applied Materials | https://amat.wd1.myworkdayjobs.com/External/job/Hwaseong-LucestarKOR/Module-Process-Engineer_R2616562 |
| Global | Thin Film Module Process Engineer | Applied Materials | https://amat.wd1.myworkdayjobs.com/External/job/Hwaseong-LucestarKOR/Thin-Film--CVD---ALD---PVD---Epitaxy--Module-Process-Engineer_R2622443 |

## Prior hydration receipt

The bounded hydration run was completed before this no-network finalization.
Success IDs: `110132`, `350510`, `361079`, `361330`, `370445`,
`370706`, `378719`, `379130`, `380499`, `380543`, `381187`, `381554`,
`381602`, `381666`, `381759`, `381814`. Failure IDs: none. Skipped IDs: none.

## Known Failures
| Date | Command | Failure | Owner | Next Action |
|---|---|---|---|---|
| 2026-08-24 | N/A | Resolved before finalization: 16 pre-existing Wanted JD files were zero bytes. | Codex | Preserve the 16 hydrated files; no network re-run is authorized in this pass. |
| 2026-09-29 | `.venv/bin/python -m pytest` | `test_live_inbox_loads_and_renders` expects >=5 actionable postings but only 4 remain (their deadlines passed at the current date). | PM | Date/data-sensitive live assertion, not introduced by t34; fix by adding a future-dated fixture or making the count relative to the clock. |
