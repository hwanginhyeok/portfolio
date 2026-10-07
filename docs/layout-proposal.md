# 포트폴리오 저장소 번호 체계 레이아웃 제안 (t110, 슬라이스 1: 인덱스 + 제안)

> 이 문서는 제안서다. 파일/디렉터리 이동·이름 변경·삭제는 하나도 하지 않았다.
> 기준: `~/.claude/CLAUDE.md` 의 "Directory numbering", "Document folders", "File naming".
> 작성: 2026-10-07, 브랜치 `hih/lay-portfolio`. 영문 본문, 맨 위 요약만 한국어.

## 요약 (운영자용)

- 현재 `hih check layout .` 결과는 **100건** (번호 없음 73 + 깊이 초과 27). 검사기는 깊이 4 폴더까지만 보고하며, 실제로는 깊이 5 폴더 5개가 더 있다.
- 제안: 루트 폴더를 `01_content`, `02_recruiting`, `03_scripts`, `04_config`, `05_tests`, `06_presentations`, `07_launchd`, `90_docs`, `91_features`, `92_site`, `93_hooks` 로 번호화한다. 도구가 이름을 강제하는 `src`, `public`, `ops`, `records`, 점(.) 폴더는 번호 없이 두고 README에 사유를 적는다.
- `docs/jd`(3,068개 파일, 채용 수집 데이터)와 `scripts`/`launchd`/`config`는 **돌고 있는 잡**(plist 6개, server-pc cron 6개, state 파일 rsync)과 얽혀 있어 가장 위험하다. 서버→Mac 전환(cutover) 감시가 끝난 뒤에 옮기는 것을 권장한다.
- 슬라이스는 **7개**. 잡과 무관한 것(1~4)을 먼저, 잡을 건드리는 것(5~7)을 나중에. 각 슬라이스는 소비처 재지정과 같은 커밋.
- 운영자 결정 사항 4개 (아래 §7). 모두 권장 답 포함.

## 1. Current tree summary

Tracked files: 3,370. Sizes are on-disk (`du -sk`) and include untracked/ignored files in the folder.

| Path | Tracked files | Size | Notes |
|---|---:|---:|---|
| `docs/` | 3,175 | 25.3 MB | 3,068 under `docs/jd/_inbox` (collector output) |
| `docs/jd/` | 3,136 (est.) | ~24.7 MB | 6 company dossiers + `_inbox/{global,jasoseol,wanted}` + `applications.json` |
| `docs/jd/_inbox/global` | 1,402 | 11.7 MB | collector data + `state.json` |
| `docs/jd/_inbox/wanted` | 1,502 | 10.5 MB | collector data + `state.json` + `digest/` |
| `docs/jd/_inbox/jasoseol` | 164 | 1.1 MB | state + calendar ledger + `.cache/` |
| `docs/jd/apple` | 27 | 552 KB | has `materials/{pdf_draft,study}` (depth 5) |
| `docs/jd/{aptiv,nearlab,nvidia,tesla,xai}` | 5 / 9 / 5 / 7 / 7 | 28K / 56K / 32K / 80K / 708K | each has `materials/`; nearlab also `tech_study/` |
| `docs/blocks` | 15 | ~228 KB | 5 numbered sub-areas (`01-inventory` ... `05-extra`) |
| `docs/archive`, `docs/history`, `docs/automation`, `docs/포트폴리오` | 14 / 3 / 1 / 4 | small | `docs/archive/cases` 9 files |
| `public/` | 85 | 47.5 MB | `images/{about,hero,cases/<9 slugs>}`; `test-engineering` alone 46 files / 43.9 MB, plus `nozzle-comparison/` (depth 5) |
| `src/` | 34 | 280 KB | Astro: `components`(19) `data`(3) `layouts` `pages` `styles` |
| `src/pages/cases/` | 8 | 144 KB | one `index.astro` per case slug dir |
| `scripts/` | 12 | 312 KB | collectors, reports, `generate_site.py` |
| `tests/` | 10 | 140 KB | pytest + `fixtures/jasoseol` (3) |
| `features/` | 11 | 44 KB | feature docs + `_template.md` + README index |
| `config/` | 3 | 24 KB | collector target JSON |
| `launchd/` | 6 | 24 KB | prepared plists |
| `diagrams/` `cases/` `hooks/` `ops/` `site/` `records/` | 3 / 2 / 1 / 1 / 1 / 1 | <30 KB each | |
| `.claude/` `.github/` `.hih/` | 4 / 2 / (untracked) | small | dot-dirs |
| `참조자료/` | 2 | small | Korean-named reference notes |
| root files | | | `build_preview.py`, `generate_ppt.py`, `inspect_ppt.py`, `clean_grad_ppt.py`, `renew_grad_ppt.py`, 3 `*.pptx` (5.2 MB + 2 small), `README.md`, `AGENTS.md`, `CLAUDE.md`, Astro/Tailwind/TS configs, `package*.json` |

## 2. `hih check layout .` findings (baseline)

Summary line: `hih check layout: 100 finding(s) in <repo> (max-depth 3)` — 73 `unnumbered`, 27 `too-deep`.

**Unnumbered (73)**
- Top level (15): `cases`, `config`, `diagrams`, `docs`, `features`, `hooks`, `launchd`, `ops`, `public`, `records`, `scripts`, `site`, `src`, `tests`, `참조자료` (incl. the Korean-named one).
- `docs/*` (4 + 5): `archive`, `archive/cases`, `automation`, `blocks`, `history`, `jd`, `포트폴리오`, `blocks/{01-inventory..05-extra}`.
- `docs/jd/*` (18): `_inbox`, `_inbox/{global,jasoseol,wanted}`, `{apple,aptiv,nearlab,nvidia,tesla,xai}`, their `materials`, `nearlab/tech_study`.
- `public/*` (14): `images`, `images/{about,hero,cases}`, `images/cases/<9 slugs>`.
- `src/*` (14): `components`, `data`, `layouts`, `pages`, `styles`, `pages/cases`, `pages/cases/<8 slugs>`.
- `tests/fixtures`, `tests/fixtures/jasoseol`.

**Too deep, depth 4 (27)**
- `docs/jd/_inbox/{global,jasoseol,wanted}` (3), `docs/jd/{apple,aptiv,nearlab,nvidia,tesla,xai}/materials` (6), `docs/jd/nearlab/tech_study` (1).
- `public/images/cases/<9 slugs>` (9).
- `src/pages/cases/<8 slugs>` (8).

**Not reported by the checker but also too deep (depth 5), must be fixed too:**
`docs/jd/apple/materials/pdf_draft`, `docs/jd/apple/materials/study`, `docs/jd/_inbox/wanted/digest`, `public/images/cases/test-engineering/nozzle-comparison`; also gitignored `docs/jd/_inbox/*/report/` and `docs/jd/report/` (generated). `docs/jd/_inbox/jasoseol/.cache` is a dot-dir (exempt).

**Other rule gaps (not flagged by the tool):** three PPTX + five PPT/preview scripts sit at the repo root; `docs/포트폴리오` and `참조자료` have Korean directory names (File naming rule wants English); `docs/blocks` and `docs/archive` overlap in role with `cases/` (case manuscripts in three places: `cases/`, `docs/archive/cases/`, `src/pages/cases/`).

## 3. Target tree

Rules applied: two-digit prefix by importance; 90-98 support; 99 archive; max 3 directory levels below root; one home per kind of material. Directory names only; **file names stay as they are** in these slices (see decision D4).

### 3a. Directory mapping

| Current | Proposed | Why / reason |
|---|---|---|
| `src/` | `src/` — tool-required (Astro `srcDir` default) | |
| `src/pages/` | `src/pages/` — tool-required (Astro file routing) | |
| `src/components`, `layouts`, `styles`, `data` | unchanged — framework convention (see D2) | imported by relative path from 19+ files |
| `src/pages/cases/<slug>/index.astro` | `src/pages/cases/<slug>.astro` | removes 8 depth-4 dirs; same URL `/cases/<slug>/` with Astro's default `format: 'directory'` |
| `public/` | `public/` — tool-required (Astro static root, URL space) | |
| `public/images/` | `public/images/` — URL contract (see D2) | |
| `public/images/{about,hero}` | unchanged (depth 3) | URL contract |
| `public/images/cases/<slug>/` | `public/images/<slug>/` (drop the `cases` level) | depth 4 -> 3; update 9 slugs' refs in `src/` (~37 refs in 11 files) |
| `public/images/cases/test-engineering/nozzle-comparison/` | files flattened into `public/images/test-engineering/` with a `nozzle-comparison-` prefix | depth 5 -> 3 |
| `cases/` | `01_content/01_cases/` | case manuscripts |
| `docs/blocks/0N-*` | `01_content/02_blocks/0N_*` (`01_inventory`, `02_usage`, `03_layout`, `04_design`, `05_extra`) | content-planning blocks; depth 3 |
| `docs/포트폴리오/` | `01_content/03_content-reviews/` | English name; CONTENT_V2, THEME_MAP_V3, PAPERS, expert review |
| `diagrams/` | `01_content/04_diagrams/` | Mermaid sources |
| `참조자료/` | `01_content/05_references/` | English name |
| `docs/jd/` | `02_recruiting/` | live recruiting pipeline + dossiers |
| `docs/jd/apple` / `nearlab` / `aptiv` / `nvidia` / `tesla` / `xai` | `02_recruiting/01_apple` / `02_nearlab` / `03_aptiv` / `04_nvidia` / `05_tesla` / `06_xai` | order: application-ready first |
| `docs/jd/<co>/materials` | `02_recruiting/0N_<co>/01_materials` | depth 3 |
| `docs/jd/apple/materials/pdf_draft`, `study` | `02_recruiting/01_apple/02_pdf-draft`, `03_study` | lifted one level (depth 3) |
| `docs/jd/nearlab/tech_study` | `02_recruiting/02_nearlab/02_tech-study` | |
| `docs/jd/_inbox/jasoseol` / `wanted` / `global` | `02_recruiting/91_inbox-jasoseol` / `92_inbox-wanted` / `93_inbox-global` | collector data (support range) |
| `docs/jd/_inbox/wanted/digest` | `02_recruiting/92_inbox-wanted/01_digest` | depth 3 |
| `docs/jd/_inbox/*/report`, `docs/jd/report` | `.../90_report` (generated, gitignored) | `.gitignore` patterns updated |
| `scripts/` | `03_scripts/` | not an import package; modules found via `sys.path` |
| `config/` | `04_config/` | |
| `tests/` | `05_tests/` | pytest discovers by file name, `conftest.py` stays |
| `tests/fixtures/jasoseol` | `05_tests/01_fixtures/` (files keep names) | |
| root `*.pptx`, `generate_ppt.py`, `inspect_ppt.py`, `clean_grad_ppt.py`, `renew_grad_ppt.py`, `build_preview.py` | `06_presentations/` (flat, 9 files) | one home for deck tooling + outputs |
| `launchd/` | `07_launchd/` | |
| `docs/` (rest: plan, decisions, runbook, cutover, harness-integration, review) | `90_docs/` (project-standard names kept) | numbered repos use `90_docs/` |
| `docs/history/` | `90_docs/98_history/` | |
| `docs/archive/` (+ `archive/cases`) | `90_docs/99_archive/` (cases flattened by prefix or kept as `99_archive/01_cases`) | archive range |
| `docs/automation/` | `90_docs/01_automation/` | one file |
| `features/` | `91_features/` | numbered-repo rule |
| `site/` | `92_site/` | generated dashboard |
| `hooks/` | `93_hooks/` | |
| `ops/` | `ops/` — tool-required (harness `prep/context.py` reads `ops/ops.yaml`) | |
| `records/` | `records/` — tool-required (harness records path) | |
| `.claude`, `.github`, `.hih`, `.git` | unchanged — dot-dirs | |
| root files | unchanged — `README.md`, `AGENTS.md`, `CLAUDE.md`, `package*.json`, `astro.config.mjs`, `tailwind.config.mjs`, `tsconfig.json` are tool-mandated | |

### 3b. "After" README directory map (proposed; do not apply to the live README)

```
| Path | What |
|---|---|
| `01_content/` | Portfolio writing: `01_cases` manuscripts, `02_blocks` planning blocks, `03_content-reviews`, `04_diagrams` (Mermaid), `05_references` |
| `02_recruiting/` | Application dossiers per company (`01_apple` .. `06_xai`), `applications.json`/`APPLICATIONS.md` ledger, collector inboxes `91_`-`93_inbox-*` (state files live here) |
| `03_scripts/` | Collectors, reports, `generate_site.py`, `update_insung_stats.py` |
| `04_config/` | Collector target JSON (`*_targets.json`) |
| `05_tests/` | Hermetic pytest suite; `01_fixtures/` |
| `06_presentations/` | Graduate-portfolio PPTX files and their generators |
| `07_launchd/` | Prepared LaunchAgent plists |
| `90_docs/` | plan, decisions, runbook, cutover, harness-integration, review; `98_history/`, `99_archive/` |
| `91_features/` | Feature specs + `_template.md` + index |
| `92_site/` | Generated operational dashboard |
| `93_hooks/` | Git hooks (`pre-commit`) |
| `ops/ops.yaml` | Operations inventory (unnumbered: harness reads this path) |
| `records/` | Generated worker records (unnumbered: harness path; git-ignored except README) |
| `src/`, `public/` | Astro website (unnumbered: Astro-required) |

Unnumbered (tool-required): `src/` and `src/pages/` (Astro), `public/` (Astro static root), `ops/` (harness), `records/` (harness),
`.github/`, `.claude/`, `.hih/`, `.git/` (dot-dirs); `src/{components,layouts,styles,data}` and `public/images` (framework/URL conventions).
Root files: `README.md`, `AGENTS.md`, `CLAUDE.md`, `package.json`, `package-lock.json`, `astro.config.mjs`, `tailwind.config.mjs`, `tsconfig.json`.
```

## 4. Consumer list (what must be repointed in the same commit)

Searched: this repo (`git grep`), `~/Workspace` (excluding `node_modules`, `.git`, `records`, `worktrees`), `~/Library/LaunchAgents`. Note: `launchctl list` and `crontab -l` were denied in this session, so the loaded/unloaded state of the plists is **not verified here**. `ops/ops.yaml` says all six are `prepared`/not loaded; the six plists do exist in `~/Library/LaunchAgents/` (copied, absolute paths). Production cron still runs on server-pc.

| Move | Consumers |
|---|---|
| `scripts/` -> `03_scripts/` | `launchd/hih.portfolio.*.plist` (6; `ProgramArguments` + `WorkingDirectory` = `/Users/hwang-inhyeok/Workspace/projects/portfolio/...`); the 6 installed copies in `~/Library/LaunchAgents/`; `ops/ops.yaml` (`mac_launchagents[].command`); `~/Workspace/infra/data/nodes/mac.yaml` (plist `source:` lines 356-377); `.github/workflows/sync-insung-stats.yml` (`python scripts/update_insung_stats.py`); `hooks/pre-commit` (`scripts/generate_site.py`); `tests/conftest.py` (`SCRIPTS_DIR`) and `tests/test_*.py` `sys.path` inserts; `features/*.md`, `README.md`, `docs/runbook.md`, `docs/cutover.md`, `docs/harness-integration.md`; server-pc crontab (6 lines, separate checkout, must keep old paths until cutover ends). |
| `config/` -> `04_config/` | `scripts/jasoseol_collect.py`, `jasoseol_report.py`, `jasoseol_calendar.py`, `wanted_collect.py`, `global_collect.py` (`REPO_ROOT / "config"`); `config/global_targets.json` `_doc`; features and README rows. |
| `docs/jd/` -> `02_recruiting/` | `scripts/applications_report.py` (`LEDGER`, `MARKDOWN`, `REPORT_DIR`), `jasoseol_collect.py`, `jasoseol_report.py`, `jasoseol_calendar.py`, `wanted_collect.py`, `global_collect.py` (inbox/report dirs); `tests/test_applications_report.py` (reads `docs/jd/applications.json`), other tests with inbox fixtures; `.gitignore` (report patterns); `ops/ops.yaml` (`state_paths`, `cutover.state_files_to_rsync`); `docs/cutover.md`, `docs/runbook.md`; **other repo** `~/Workspace/projects/personal/scripts/brief.py:57` (hardcoded `projects/portfolio/docs/jd/applications.json`) and `projects/personal/{README.md,features/brief.md,docs/sources.md,docs/plan.md,docs/decisions.md}`; `docs/jd/README.md` and per-company docs that cite sibling paths; `docs/jd/applications.json` (path fields). The server-pc job state files are rsynced by path from the PM runbook. |
| `docs/jd/apple/materials/study/index.html` | embedded relative links (verify after lift). |
| `launchd/` -> `07_launchd/` | `ops/ops.yaml` (`plist:` paths), `~/Workspace/infra/data/nodes/mac.yaml` (`source:`), `docs/cutover.md`, `docs/harness-integration.md`, `features/harness-scheduling.md`, README. Installed `~/Library/LaunchAgents/*.plist` are copies (no repoint needed unless re-installed). |
| `tests/` -> `05_tests/` | `tests/conftest.py` (`REPO_ROOT` is `parent.parent`, still valid), `FIXTURES_DIR` in `test_jasoseol_collect.py`; any CI/doc command lines (`pytest tests/`) in README, runbook, features. |
| `docs/` -> `90_docs/`, `features/` -> `91_features/`, `site/` -> `92_site/`, `hooks/` -> `93_hooks/` | `scripts/generate_site.py` (`FEATURES_DIR`, `OUTPUT`); `hooks/pre-commit` (`site/index.html`, own path); git config `core.hooksPath=hooks` (shared `.git/config`; PM sets it to the new name in the same step); `README.md`, `CLAUDE.md`, `AGENTS.md` (required-read list: `docs/history/handoff.md`, `docs/decisions.md`, `docs/history/test-log.md`), `features/README.md`, `docs/*.md` cross-links, `docs/blocks/**` and `docs/archive/**` links; `hih-worker accept` docs gate (already knows `90_docs`/`91_features` for numbered repos per the shared rules; confirm for this repo); `~/Workspace/agents/project-standard.md` names `docs/`/`features/`/`site/` (PM to note numbered variant). `ops/ops.yaml` itself stays. |
| `cases/`, `diagrams/`, `참조자료/`, `docs/blocks`, `docs/포트폴리오` -> `01_content/` | `build_preview.py` (`Path(__file__).parent / "diagrams"`); `CLAUDE.md` file-structure block and Rules table; `features/presentation-builder.md` (repository data line); docs inside `docs/blocks/**` that cite `cases/`, `docs/포트폴리오`. No scripts, jobs or other repos found. |
| root PPTX + PPT scripts -> `06_presentations/` | `features/presentation-builder.md` (entry-point commands `python3 generate_ppt.py`, `inspect_ppt.py`); the `*.py` scripts' own relative pptx/diagram paths (verify; `build_preview.py` reads diagrams); `.gitignore` (`preview.html`). |
| `src/pages/cases/<slug>/index.astro` -> `<slug>.astro` | relative imports `../../../layouts/BaseLayout.astro` become `../../layouts/BaseLayout.astro` (8 files); `features/astro-portfolio.md`. |
| `public/images/cases/<slug>` -> `public/images/<slug>` | image refs in `src/components/{Hero,TestGallery}.astro`, `src/pages/index.astro`, `src/pages/cases/*` (11 files, ~37 refs); `public/robots.txt` has the sitemap URL only (no change); external deep links to `hwanginhyeok.github.io/portfolio/images/cases/...` (GitHub profile, resume text in `docs/blocks/05-extra/GITHUB_PROFILE.md`) would break. |
| `infra/data/projects.yaml` | root `~/Workspace/projects/portfolio` unchanged; no edit. |

## 5. Slices

Order is lowest risk first. Each slice is a single commit that moves one area and repoints its consumers. Common checks: `hih check layout .` (finding count drops, no new findings), `git grep` for the old path (zero hits outside history/archive text), `python -m pytest -q 05_tests` (after S4; `tests` before), `npm run build` when `src/`/`public/` change.

| # | Slice | Consumers touched | Check | Risk | Touches running jobs |
|---|---|---|---|---|---|
| S1 | `01_content/` (cases, blocks, content-reviews, diagrams, references) + `06_presentations/` (root PPTX/py) | `CLAUDE.md`, `build_preview.py`, `features/presentation-builder.md`, blocks docs links | `git grep` old paths; `python 06_presentations/build_preview.py` dry check not run (no jobs); layout count | Low (docs/tools only) | No |
| S2 | Astro: flatten `src/pages/cases/<slug>`, `public/images/cases/<slug>` -> `public/images/<slug>`, nozzle-comparison flatten | `src/**` imports and image refs, `features/astro-portfolio.md` | `npm run build`; compare list of generated routes/`dist` file tree before vs after (URLs `/cases/<slug>/` unchanged; image URL change documented) | Medium (public URLs; GitHub Pages deploy happens only after merge/push) | No (deploy workflow untouched but runs on push) |
| S3 | `docs/` -> `90_docs/` (+ `98_history`, `99_archive`, `01_automation`), `features/` -> `91_features/`, `site/` -> `92_site/`, `hooks/` -> `93_hooks/` (+ `core.hooksPath`) | `scripts/generate_site.py`, `hooks/pre-commit`, README/CLAUDE/AGENTS, features index, docs cross-links, `docs/jd` stays put in this slice | `python scripts/generate_site.py` output equal to prior `site/index.html` except paths; pre-commit hook runs; docs gate path check | Medium (hook path is repo-shared config; many doc links) | No |
| S4 | `tests/` -> `05_tests/` (+ `01_fixtures`) | `FIXTURES_DIR`, any docs with `pytest tests/` | `python -m pytest -q 05_tests` fresh, exit 0 | Low | No |
| S5 | `config/` -> `04_config/` | 5 collector/report scripts' `DEFAULT_CONFIG`, config `_doc`, docs | pytest; `python scripts/<each> --help` loads default; `--dry-run` only for `global_collect.py` is NOT run (no jobs) | Medium | **Yes** (all collectors read it at start; server-pc cron uses the old checkout) |
| S6 | `docs/jd/` -> `02_recruiting/` (company renumber, depth fixes, `90_report`, `91_`-`93_inbox-*`) | 6 scripts' path constants, `ops/ops.yaml` state paths and rsync list, `.gitignore`, `docs/cutover.md`, `docs/runbook.md`, `tests/test_applications_report.py`, **`projects/personal/scripts/brief.py` + its docs** | pytest; `git mv` keeps history; compare state-file hashes (`state.json`, `calendar_events.json`, `applications.json`) before/after; `brief.py` dry read of ledger path | **High** (3,068 files; live state ledgers; second repo reads the ledger; server-pc rsync) | **Yes** |
| S7 | `scripts/` -> `03_scripts/`, `launchd/` -> `07_launchd/` | 6 repo plists + 6 installed `~/Library/LaunchAgents` copies (PM re-installs from `proposed/`), `ops/ops.yaml`, `infra/data/nodes/mac.yaml`, `.github/workflows/sync-insung-stats.yml`, `hooks/pre-commit`/`93_hooks`, `generate_site.py`, `tests`, docs | `plutil -lint` each plist; `hih node check` (infra drift); pytest; workflow yaml reviewed | **High** | **Yes** (LaunchAgents, GitHub Action, infra node file; workers cannot edit infra/LaunchAgents: delivered via `proposed/` and applied by the PM) |

Order note: S3's doc moves and S6's `docs/jd` move interact. Recommended: do S6 before S3 only if cutover is finished; otherwise S3 moves `docs/*` except `docs/jd`, and S6 later lifts `docs/jd` -> `02_recruiting/` (a short-lived `docs/jd` remnant is acceptable and is the only deliberate exception in between).

Expected finding count after all slices: 0 `unnumbered`/`too-deep` among tracked paths (`src/*`, `public/images`, `ops`, `records` listed as tool-required in the parent README per the rule). Without D2 accepted, 11 residual `unnumbered` findings remain (`src/{components,data,layouts,styles}`, `public/images/*`).

## 6. Risks and constraints to keep

- `docs/jd/_inbox/*` holds the collectors' dedup/calendar state; a wrong path creates a fresh ledger and re-sends Telegram notifications and calendar events. Move only with state hashes recorded before/after.
- Server-pc production cron uses its own checkout at the old layout; per `docs/cutover.md` jobs switch one at a time. Do S5-S7 only for jobs already on the Mac, or after cutover plus the 2-day watch.
- Public image URLs under `/portfolio/images/cases/...` change in S2; any external reference (GitHub README, resumes) breaks silently.
- File names are not touched (D4). Korean/uppercase file names remain until the operator approves a rename slice.

## 7. Open decisions for the operator

1. **D1 — Timing of S5-S7.** Wait until the server-pc -> Mac cutover and the 2-day watch finish for all 6 jobs? *Recommend: yes; run S1-S4 now, S5-S7 after cutover.*
2. **D2 — Exempt framework-convention folders?** Treat `src/{components,layouts,styles,data}` and `public/images` as tool/URL conventions (unnumbered, listed in README), instead of renaming them? *Recommend: yes (renaming would break relative imports and public URLs for no benefit).*
3. **D3 — Image URL change.** Accept dropping the `cases/` level (`public/images/cases/<slug>` -> `public/images/<slug>`), which breaks external deep links, or exempt `public/` entirely and accept the depth-4 findings? *Recommend: drop the level (`public/images/<slug>`); external links are few.*
4. **D4 — File renames.** Normalize Korean/uppercase file names (e.g. `JD_분석_Apple_...md`, `ACTIVITY_INVENTORY.md`) to the File naming rule inside these slices? *Recommend: no, directories only now; do file renames as a later, separate approved slice.*
