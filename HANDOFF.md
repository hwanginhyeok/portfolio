# HANDOFF

## Goal
Repair the Wanted and global job collectors end to end: make JSON state writes
durable, reconstruct the zero-byte Wanted dedup ledger without losing posting
IDs or files, and expose a deterministic feasibility-and-profile-fit shortlist
while retaining the complete raw collection.

## Current State
Completed for the rejected PM-661 continuation. The Wanted ledger was rebuilt
from the committed 299-entry ledger plus local posting files and digests,
producing 327 entries. All 16 zero-byte Wanted JDs were re-fetched through the
bounded detail-read mode with 16 successes and 0 failures. Collector code now
uses shared atomic persistence and the report layer separates actionable
high-fit roles from informational/ineligible roles. The final owner-domain
gate leaves Wanted at 7 actionable / 321 informational and global at 14
actionable / 573 informational, without quota padding.

## Active Task
- ID: PORTFOLIO-20260824-01
- Priority: P0
- Owner: Codex
- Status: completed; review-ready

## Changed Files
- `scripts/state_utils.py`
- `scripts/shortlist.py`
- `scripts/wanted_state_repair.py`
- `scripts/wanted_collect.py`
- `scripts/global_collect.py`
- `tests/test_job_collectors.py`
- `HANDOFF.md`, `TEST_LOG.md`, `WORK_LOG.md`
- `WORK_ITEMS/PORTFOLIO-20260824-01.md`
- Pre-existing Wanted/global JD files and state artifacts were retained;
  they were not modified during this finalization pass.

## Decisions
- State writes use a same-directory temporary file, JSON dump, flush, file
  fsync, atomic `os.replace`, and cleanup. Failures before replacement leave
  the previous ledger intact.
- JD hydration uses the same atomic text-write contract and refuses to replace
  a target that is no longer zero bytes.
- The committed Wanted ledger is authoritative for existing rows. Local
  frontmatter and digest rows only add missing IDs or fill absent metadata;
  the hydrated rows now fill position/company evidence while preserving the
  ledger's existing first-seen values.
- ITAR/export-control and U.S.-person evidence always blocks actionability,
  including a Korea location. Remote roles require an explicit
  worldwide/Korea/APAC scope; incidental words such as `Remote Pilot` or
  company boilerplate do not qualify. Visa-needed roles remain excluded, and
  sponsorship-likely roles require affirmative sponsorship text. The
  non-Korea `korea-apac` bucket is informational unless its JD contains
  affirmative credible sponsorship evidence and no anti-sponsorship clause.
- Korean administrative-address fragments such as `금천구` are recognized as
  Korea locations only through a bounded Hangul address-suffix pattern.
- Actionable fit evidence must appear in the title or department and meet the
  minimum profile gate. It also requires a credible owner-domain connection in
  the title or department: automotive/mobility, motor/power-electronics,
  embedded/electrical hardware, robotics/industrial automation,
  machinery/equipment, physical-product test/validation/reliability/quality,
  or technical product industrialization. Consumer beauty/fashion/food/
  e-commerce, OEM production management, SCM/sourcing-only, Order Management,
  sales, CX, marketing, generic AI/software, body-only matches, and unrelated
  manager roles remain raw informational collection.
- Raw collection is preserved and rendered separately from the actionable
  shortlist. Fit ranking uses only local posting text and the portfolio's
  manufacturing/test/reliability/quality/supplier/NPI/electrical/technical-PM
  vocabulary.

## Known Issues
- The normal Wanted collector was not run because the bounded detail reads
  already validated the repaired API path and a normal run was not needed.
- No Telegram, publication, email, paid service, credential, commit, push, or
  deployment action was performed.

## Next Action
<!-- 다음 모델이 바로 실행해야 할 첫 행동. -->
1. Review the diff and the receipts below; leave the normal scheduled
   collectors for a separately authorized operational run.

## Do Not Touch
<!-- 건드리면 안 되는 파일, 브랜치, 결정. -->
- Runtime V2 state, database, status projection, and lifecycle instructions.
- Existing dirty or untracked JD files, `TASK.md`, global state, and global
  posting artifacts unless a separate task explicitly owns them.
- No commit, push, deploy, publication, Telegram delivery, or paid service.

## Verification
Commands run:
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p 'test_job_collectors.py' -v`
- AST syntax parse for all five code modules and `tests/test_job_collectors.py`
  without bytecode output.
- Package imports and direct-file CLI imports for all five code modules.
- In-memory Wanted/global report fixtures with no filesystem writes.
- `git diff --check`
- Read-only ledger integrity comparison against `HEAD`, zero-byte scan, and
  hydrated-JD URL check.
- Strict local in-memory shortlist scan over Wanted and global posting files.

Result:
- 20 focused tests passed; syntax, import, report-fixture, and whitespace
  checks passed with `-B`/`PYTHONDONTWRITEBYTECODE`. The pre-existing ignored
  `scripts/__pycache__/` was left untouched.
- Repaired Wanted state: 327 entries (299 committed + 28 local additions).
- Read-only preservation receipt: all 299 baseline rows unchanged, 16
  hydrated Wanted JDs present with direct URLs, and zero-byte count 0.
- Final strict local corpus shortlist: Wanted 7 actionable / 321
  informational from 328 files; global 14 actionable / 573 informational
  from 587 files. All 21 actionable rows have title/department fit and
  owner-domain evidence.

### Final top shortlist receipt

Top five per source, ranked by the strict local classifier:

| Source | Title | Company | Location | Eligibility | Fit | Direct source |
|---|---|---|---|---|---:|---|
| Wanted | [서울] 반도체 PCB 자율제조 컨설팅 전문가 (연구원~선임급) – "현장과 기술을 잇는 DX 아키텍트" | 인터엑스 | Seoul Geumcheon-gu | Korea | 30 | https://www.wanted.co.kr/wd/358085 |
| Wanted | 하드웨어 엔지니어(회로설계) | 닷 | Geumcheon-gu | Korea | 26 | https://www.wanted.co.kr/wd/124026 |
| Wanted | System Software Engineer (Embedded AI) | 소울아트 | Seoul Jung-gu | Korea | 26 | https://www.wanted.co.kr/wd/350980 |
| Wanted | 전장설치 엔지니어 | 씨드로닉스 | Seoul Gangnam-gu | Korea | 26 | https://www.wanted.co.kr/wd/293489 |
| Wanted | 로봇 전장설계 HW 엔지니어 | 에이로봇 | Ansan, Gyeonggi | Korea | 26 | https://www.wanted.co.kr/wd/300816 |
| Global | Test Lab engineer | Aptiv | Ulsan, Republic of Korea | Korea | 30 | https://aptiv.wd5.myworkdayjobs.com/Aptiv_Careers/job/Ulsan-Republic-of-Korea/Test-Lab-engineer_J000702784 |
| Global | Manufacturing Engineering Engineer | Aptiv | KOR Asan – MFG | Korea | 30 | https://aptiv.wd5.myworkdayjobs.com/Aptiv_Careers/job/KOR-Asan--MFG/Manufacturing-Engineering-Engineer_J000666213 |
| Global | DDP/Epitaxy Module Process Engineer | Applied Materials | Icheon-Gwango, KOR | Korea | 30 | https://amat.wd1.myworkdayjobs.com/External/job/Icheon-GwangoKOR/DDP-Epitaxy-Module-Process-Engineer_R2625397 |
| Global | Epitaxy Module Process Engineer | Applied Materials | Hwaseong-Lucestar, KOR | Korea | 30 | https://amat.wd1.myworkdayjobs.com/External/job/Hwaseong-LucestarKOR/Module-Process-Engineer_R2616562 |
| Global | Thin Film (CVD / ALD / PVD / Epitaxy) Module Process Engineer | Applied Materials | Hwaseong-Lucestar, KOR | Korea | 30 | https://amat.wd1.myworkdayjobs.com/External/job/Hwaseong-LucestarKOR/Thin-Film--CVD---ALD---PVD---Epitaxy--Module-Process-Engineer_R2622443 |

## Handoff Notes
The working tree contains pre-existing user changes and artifacts. Keep them
intact when reviewing or extending this work. The repair script is
`python3 scripts/wanted_state_repair.py`; it is a no-op when the target ledger
is already valid unless `--force` is supplied. The finalization pass performed
no network read and wrote no JD or state artifact.

### Collector-track expansion receipt (2026-08-24)
`PORTFOLIO-20260824-02` added `core`, `ai-native`, and
`engineering-consulting` search tracks, focused industrial AI, Physical AI,
robotics, digital-twin, forward-deployed, and technical-consulting terms, and
deterministic owner-domain gates. Its 25 focused tests passed. No collector
run, Telegram delivery, commit, or publication occurred in that task.
<!-- Claude/Codex/다른 모델에게 남기는 짧은 맥락. -->
