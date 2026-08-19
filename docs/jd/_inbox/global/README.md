# docs/jd/_inbox/global/ — 글로벌 채용공고 스테이징

> 최초 작성: 2026-08-19 (PM-568)
> 수집기: `scripts/global_collect.py` · 설정: `config/global_targets.json`

원티드 스테이징(`../wanted/`)의 글로벌 대응물. 해외 기업의 채용 ATS 공개 API에서 공고를
받아, **포트폴리오 실제 역량으로 점수를 매겨** 걸러낸 뒤 여기에 쌓는다.

## 실행

```bash
python3 scripts/global_collect.py --dry-run          # 수집·채점만, 파일 안 씀
python3 scripts/global_collect.py --html             # 파일 + HTML 리포트
python3 scripts/global_collect.py --html --telegram  # + 비서봇 전송
```

기업당 요청 1회(목록 API가 JD 본문까지 준다) + 기업 간 1초 대기. Workday는 테넌트×검색어×페이지
단위로 요청이 늘어난다(아래). 개별 공고 상세 페이지는 받지 않는다.

## 소스 — 18개 보드 + Workday 4개 테넌트 (2026-08-19 실측 확인)

| ATS | 엔드포인트 | 기업 |
|---|---|---|
| Greenhouse | `boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` | waymo · anthropic · lucidmotors · scaleai · figureai · wayve · nuro · apptronik · neuralink · agilityrobotics · archer |
| Ashby | `api.ashbyhq.com/posting-api/job-board/<slug>` | openai · shield-ai · 1x · physicalintelligence · gecko-robotics |
| Lever | `api.lever.co/v0/postings/<slug>?mode=json` | zoox · dexterity |
| Workday | `POST <tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/jobs` | amat · kla · aptiv · micron |

전부 무인증. 인증·쿠키·브라우저 불필요.

**기업 추가 시 반드시 슬러그를 먼저 찔러볼 것.** 틀린 슬러그는 404를 조용히 반환하고,
그건 "이 회사는 채용 안 함"과 구분되지 않는다. 실제로 공고가 나오는 것을 확인한 뒤에만
`config/global_targets.json`의 `companies`에 넣는다.

### Workday — 왜 따로 있는가

미국 발 글로벌 기업들이 한국 채용을 Greenhouse 미국 보드가 아니라 **Workday**로 걸기
때문이다. 위 18개 보드에서 한국 근무 공고는 0건이었고, 아래 4개 테넌트에서 바로 나온다.

| 기업 | tenant | wd | site | 비고 |
|---|---|---|---|---|
| Applied Materials | `amat` | 1 | `External` | 화성·분당·평택·이천 |
| KLA | `kla` | 1 | `Search` | 화성·동탄·평택 |
| Aptiv | `aptiv` | 5 | `Aptiv_Careers` | 울산·군포·충주·아산 |
| Micron | `micron` | 1 | `External` | 현재 한국 공고 0 — 나중에 열릴 수 있어 유지 |

엔드포인트는 POST JSON:

```
POST https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/jobs
Content-Type: application/json
{"appliedFacets":{}, "limit":20, "offset":<n>, "searchText":"<text>"}
```

응답의 `jobPostings[]`는 `title`·`locationsText`·`externalPath`·`postedOn`·`bulletFields`
만 준다 — **목록에는 JD 본문이 없다.** 공고 URL은
`https://<tenant>.wd<N>.myworkdayjobs.com/<site>` + `externalPath`.

본문은 공고별 엔드포인트에 있다:

```
GET https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site><externalPath>
→ {"jobPostingInfo": {"jobDescription": "<html>", ...}}
```

수집기는 **한국 위치 공고만** 이걸로 본문을 채운다(`hydrate_workday_korea`). 이유는
비용과 효용 둘 다다 — 사용자가 실제로 읽는 섹션이 거기고, 요청 수도 한국 건수만큼으로
묶인다. 본문 없이 제목만으로 채점하면 전건이 0~9점에 몰려 `Quality Inspector`가
`Program Manager`와 같은 줄에 서기 때문에 순위가 무의미해진다. 수화에 실패한 건은
`no_jd`를 유지한 채 제목 점수로 남고, 그 이유로 탈락시키지는 않는다.

**페이지네이션 함정 — 두 겹이다.** 첫째, Workday는 `total`에 0(또는 틀린 값)을 담고도
`jobPostings`에 한 페이지 가득 반환한다. `offset >= total`에서 멈추는 루프는 첫 페이지만
읽고 조용히 누락된다. 둘째, `offset` 자체도 느슨하게만 지켜진다 — 2026-08-19 실측으로
"빈 페이지가 올 때까지" 돌리면 테넌트당 50페이지를 돌면서 **94%가 중복**이었다
(kla 988행 → 고유 68 / amat 997 → 117 / aptiv 983 → 63, 각 85초). 빈 페이지는 영영
오지 않을 수도 있다.

그래서 종료 신호는 `total`도 빈 페이지도 아니고, **연속 N페이지가 새 `externalPath`를
하나도 추가하지 못하면 중단**(`workday_stall_pages`, 기본 3)이다. 동일한 고유 집합을
7~9페이지·12초에 얻는다. `workday_page_limit`(기본 15)는 바깥쪽 폭주 방지용으로 남고,
걸리면 로그에 남긴다.

검색어(`workday_search_terms`)는 `"Korea"` + 도메인 용어들. 결과는 `externalPath`로
합집합. 테넌트 하나가 실패해도 로그만 남기고 건너뛴다(치명 아님).

**Workday 테넌트 추가 시**: `tenant`/`wd`/`site` 세 쌍을 먼저 직접 찔러서 200 +
`jobPostings`를 확인한 뒤 config에 넣는다. 잘못된 조합은 404/422가 조용히 나서
"채용 없음"과 구분되지 않는다 — Greenhouse 슬러그와 같은 함정. (실제로 asml ·
lamresearch · continental · teradyne · zf · valeo · borgwarner · magna은 2026-08-19
프로브에서 전부 실패했다.)

## 채점

`config/global_targets.json`이 SSOT다. 코드에 키워드를 하드코딩하지 않는다.

- `profile_keywords` — 포트폴리오 역량 가중치. 모터제어/전력전자(BLDC·IPMSM·FOC·SVPWM·
  인버터·액추에이터)가 최고 가중치, 임베디드/CAN/시뮬레이션/신뢰성·검증이 그다음,
  하드웨어 TPM(NPI·DVT/EVT/PVT·APQP·공급업체 품질)이 그다음.
- `negative_keywords` — 웹/백엔드/영업/리크루팅 등 즉시 탈락.
- `seniority_exclude` — director·VP·principal·chief·head 등. 경력 3.5년 기준.
- `min_score` — 통과 기준선. 낮추면 노이즈가, 높이면 누락이 는다. **한 가지 예외:
  `korea` 버킷은 점수 게이트를 적용하지 않는다.** 한국 근무는 이 프로젝트의 최우선
  관심사라 3점짜리도 볼 가치가 있고, 점수는 섹션 내부 정렬에만 쓴다. 부정어·시니어리티
  필터는 그대로 걸리므로 비적합 직무는 이미 제거된 뒤다. 그 밖의 버킷은 종전대로
  `min_score`를 넘어야 한다.

  > 이 예외를 `no_jd`(본문 없음)에 묶었다가 회귀가 났다. 한국 공고에 JD 본문을 채우자
  > `no_jd`가 꺼지면서 면제도 같이 사라져 한국이 114건 → 2건으로 잘렸다. 조건은
  > **버킷**이지 본문 유무가 아니다.

출처는 `docs/blocks/05-extra/RESUME.md` §5·§7과 `cases/E01_pm_experience.md`.
이력이 바뀌면 그 문서를 먼저 고치고, 그다음 이 config를 맞춘다.

## 지원 자격 버킷 (`eligibility`)

점수보다 이게 먼저다. 아무리 잘 맞아도 지원할 수 없으면 의미가 없다.

| 버킷 | 뜻 |
|---|---|
| `korea` | **한국 현지 근무** — 위치가 `korea_location_terms`(Korea·KOR·화성·평택·울산 등)에 매칭. Workday가 주 출처 |
| `sponsorship-likely` | 비자 스폰서/이주 지원을 본문에 명시 |
| `remote` | 원격 근무 명시 |
| `korea-apac` | 한국 외 APAC — 일본·싱가포르·대만·인도 등 |
| `visa-needed` | 해외 근무 + 스폰서 언급 없음 |
| `blocked-itar` | ITAR·수출통제·보안취급인가·"U.S. person" 요건 — **한국 국적 지원 불가** |

우선순위(랭킹·리포트 섹션 순서 모두): `korea` → `sponsorship-likely` → `remote` →
`korea-apac` → `visa-needed` → `blocked-itar`. `korea`는 다른 모든 버킷보다 위 —
한국 위치 매칭이면 ITAR 문구가 있어도 `korea`다. 거주지가 한국이므로.

앞의 넷이 "지원 가능"이다. 리포트 맨 위에 🇰🇷 한국 근무 섹션이 `korea` 전건을 카드로
뿌린다(0건이어도 한 줄로 표시, 섹션을 숨기지 않는다). `blocked-itar`는 기록은 하되
리포트에서 흐리게 접어 두고 절대 지원 가능 건보다 위에 놓지 않는다. shield-ai·
neuralink에서 많이 나오는 것이 정상이다.

## 산출물

- `state.json` — `<ats>:<slug>:<job_id>` 키의 중복 방지 원장. Workday는
  `workday:<tenant>:<req번호>` (externalPath에서 추출, 없으면 해시). 같은 날 재실행하면 신규 0건.
  `first_seen`만 불변이고 `score`/`eligibility`/`title`은 매 실행 갱신된다 — 안 그러면
  최초 등록 당시 점수가 굳어 리포트와 원장이 서로 다른 말을 한다.
- `<slug>-<job_id>.md` — 공고별 파일. frontmatter(company/title/location/country/
  eligibility/score/matched_keywords/url/first_seen) + JD 본문.
- `report/YYYY-MM-DD.html` — 자기완결 모바일 리포트. 매일 비서봇으로 전송된다.

## 승격

여기는 **스테이징일 뿐**이다. 실제로 지원하기로 한 공고는 `docs/jd/README.md` 원칙 1에 따라
`docs/jd/{회사}/`를 새로 만들어 옮긴다. 이 디렉토리는 진행 중인 지원의 SSOT가 아니다.
