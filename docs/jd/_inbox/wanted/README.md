# docs/jd/_inbox/wanted/ — 원티드 공고 수집 인박스 (스테이징)

> 최초 작성: 2026-08-18 · 수집기: `scripts/wanted_collect.py` · 설정: `config/wanted_targets.json`

## 이 디렉토리는 무엇인가

매일 원티드(www.wanted.co.kr)에서 키워드에 맞는 공고를 자동 수집해 쌓아두는
**스테이징 인박스**다. 목적은 "오늘 뭐 새로 떴나"를 한 곳에서 보는 것.
포트폴리오 케이스(제조 AI PM · 기술 PM · 생산관리 등)로 매핑할 만한 공고를
놓치지 않기 위한 수집 장치이며, **실제 지원 활동의 SSOT가 아니다.**

## 구성

| 경로 | 역할 |
|---|---|
| `state.json` | dedup 원장. 이미 본 공고 id → 최초 발견일/회사/포지션. 같은 날 재실행 시 새 파일 0개 |
| `<id>-<회사>.md` | 공고 원문 1건. YAML frontmatter(wanted_id·company·url·skill_tags 등) + 소개/주요업무/자격요건/우대사항/혜택/채용절차 |
| `digest/YYYY-MM-DD.md` | 일일 리포트. 최상단에 와치리스트 경고(비제로 시 🚨), 그 아래 신규 공고 테이블 |
| `report/YYYY-MM-DD.html` | 일일 HTML 리포트(`--html`). digest와 같은 신규 세트를 폰에서 읽는 한 페이지로: 와치리스트(비제로 시 최상단 🚨 배너) → 핵심 공고 카드 → 기타 공고(접힘). 외부 리소스 없이 단일 파일 |
| `config/wanted_targets.json` | 키워드·와치리스트·제외 패턴·페이지 상한·요청 간격 (프로젝트 루트 `config/`) |

## 실행 방법

```bash
python3 scripts/wanted_collect.py                 # 일일 수집 (cron용 진입점)
python3 scripts/wanted_collect.py --dry-run       # 요약만 출력, 파일 없이
python3 scripts/wanted_collect.py --limit 5       # detail 5건만 (스모크 테스트)
python3 scripts/wanted_collect.py --config 다른설정.json
python3 scripts/wanted_collect.py --html          # 수집 + report/YYYY-MM-DD.html 렌더
python3 scripts/wanted_collect.py --telegram      # --html 포함. 렌더한 리포트를
                                                   # PM 비서 봇에 Telegram 문서로 전송
```

`--telegram`은 `--html`을 내포하며, 전송 실패(자격증명 누락·네트워크 오류 포함)는
경고만 남기고 수집 성공 상태를 되돌리지 않는다. 봇 자격증명은
`/home/window11/project-manager/.env`의 `PM_BOT_TOKEN`·`PM_BOT_CHAT_ID`에서만
읽으며(값은 로그에 출력되지 않는다), 정오 cron이 이 명령으로 리포트를 봇에 보낸다.

cron 등록은 PM의 판단으로 별도 수행한다(이 디렉토리는 등록하지 않은 상태로 배포됨).
키워드 조정은 항상 `config/wanted_targets.json`에서만 — 스크립트에 하드코딩 금지.

## 기업 와치리스트

현대자동차·삼성전자·SK하이닉스 등 대기업은 보통 자체 채용 포털로 뽑기 때문에
원티드 내 공고 수가 **0인 것이 정상**이다. 수집기가 매일 `confirmed_position_count`를
기록하며, 0이 아닌 날은 그날의 digest 최상단에 🚨 경고로 뜬다.
0이 나와도 버그가 아니고, 다른 사이트를 긁어 우회하지도 않는다.

## `docs/jd/README.md` 원칙 1과의 관계 (중요)

상위 디렉토리 [원칙 1 — 회사별 디렉토리 완전 분리](../../README.md)에 따라
지원 활동은 `docs/jd/{회사}/` 디렉토리 안에서만 독립적으로 운영된다.

이 인박스는 어디까지나 **스테이징**이다:

1. 여기서 공고를 검토하고, 지원할 가치가 있다고 판단되면
2. `docs/jd/{회사}/` 디렉토리를 원칙 1 절차(`README.md`·`APPLY.md`·`JD_매핑` 파일)대로 새로 만들고
3. 필요한 내용(JD 원문, 매핑에 쓸 구절)을 **복사해서** 넣는다.

인박스 파일은 언제든 다음 수집·정리 때 정리될 수 있는 임시 보관물이며,
진행 중인 지원의 근거 파일로 참조하지 않는다. 지원이 시작되면 SSOT는
`docs/jd/{회사}/` 쪽이 된다.

## 글로벌 기업 섹션

리포트 상단(신규 공고 위)에 `글로벌 기업 · 한국 채용` 섹션이 있다. 원티드에 올라온 외국계·
글로벌 기업 공고를 **원장 전체에서** 뽑는다 — 오늘 신규가 아니어도 계속 보여야 의미가 있는
정보라서, 이 섹션만 "오늘의 신규" 규칙을 따르지 않는다. 그날 새로 들어온 건에는 NEW 표시.

대상은 `config/wanted_targets.json`의 `global_companies`이고, **회사명 정확 일치**로만
매칭한다. 부분문자열은 쓰지 않는다 — 실제로 `메타`가 메타파머스를, `인텔`이 에임인텔리전스를,
`ST`가 이스트소프트를 끌어왔다. 회사가 이름을 바꾸면 매칭이 끊기는데, 조용한 오탐보다
눈에 보이는 누락이 낫다. 새 기업은 원티드가 쓰는 표기 그대로 추가할 것.

현재 잡히는 곳: NVIDIA · OpenAI · EA Korea · Concentrix · FPT Software Korea · 쿠팡 ·
STRADVISION. 나머지는 등록만 해두고 공고가 뜨면 자동으로 들어온다.
