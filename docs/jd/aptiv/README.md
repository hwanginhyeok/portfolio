# docs/jd/aptiv/ — Aptiv 지원 디렉토리

> 지원 직군: 제조기술(Manufacturing Engineering) 2개 포지션
> 지원 상태: 준비 중 — JD 원문 확보 완료, 사용자 확인 4건 대기

Aptiv는 자동차 Tier-1(본사 더블린, 임직원 20만+)이고 **국내 생산거점이 울산·군포·충주·아산**에
있다. 원티드에는 공고를 올리지 않고 Workday로만 뽑는다 — 그래서 이 두 건은 국내 채용
플랫폼만 봐서는 보이지 않는다.

## 파일 목록

| 파일 | 내용 | 상태 |
|------|------|:----:|
| [JD_매핑_Aptiv.md](JD_매핑_Aptiv.md) | JD 요건 × 자산 매트릭스 + 핵심 메시지 3개 + 갭 분석 + 면접 답변 | ✅ 완료 (2026-08-19) |
| [APPLY.md](APPLY.md) | 공고 URL · 필요 서류 · 지원 트래킹 | 🟡 서류 준비 대기 |
| [materials/](materials/) | 이력서·자기소개서 등 포지션별 자료 | 빈 상태 |

## 대상 포지션

| | 아산 | 울산 |
|---|---|---|
| 직함 | Manufacturing Engineering Engineer | CC Mfg. Engineer |
| Job ID | J000666213 | J000699670 |
| 경력 요건 | **3년** | **5년** |
| 필수 지식 | — | PFMEA · SPC · 공정능력 · Control Plan |
| 판정 | **요건 충족 · 1순위** | 경력 1.5년 미달 + 지식 2종 무근거 · 2순위 |

**아산이 1순위인 이유**: 요건을 전부 충족하는 데다, JD가 이 자리의 미션을
"신규 사업 SOP 도입 담당"이라고 직접 밝히고 그 목록에 **Hanon Thermal Management module**과
**TMED II**를 넣었다. EOP 400W 차량용 전동오일펌프 이력과 도메인이 겹친다.

## 이 매핑에서 지키는 선

JD가 요구하는 **SPC·공정능력분석·Control Plan은 포트폴리오에 근거가 없다.** PFMEA도
`CONTENT_V2` 의 `P-15 노이즈 경로` 1건뿐이고 실제 강점은 DFMEA다.

매핑 문서는 이걸 갭으로 명시했고 **보유한 것처럼 쓰지 않는다.** 지원 서류에서 부풀리면
면접 질문 하나에 무너지고, 그건 이 프로젝트 전체의 신뢰를 깎는다.
`§4 갭 분석`이 그 선을 어떻게 지킬지와 압박 질문 대응까지 담고 있다.

## 참조

- 원본 공고: `docs/jd/_inbox/global/aptiv-000666213.md` · `aptiv-000699670.md`
  (파일명은 Workday req 번호에서 `J` 접두를 뗀 형태다)
- 자산 출처: `docs/blocks/05-extra/RESUME.md` §5·§7, `cases/E01_pm_experience.md`
- 수집 경로: Workday `aptiv.wd5` — 매일 11:50 자동 갱신 (`scripts/global_collect.py`)
