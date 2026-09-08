# docs/jd/nvidia/ — NVIDIA Korea 지원 디렉토리

> 지원 직군: Senior Automotive Software Program Manager (Korea, Seoul)
> 지원 상태: 초안 — JD 원문 확보 완료, **요건 갭이 커서 지원 여부 결정 대기**
> 지원 이력 상태값은 여기가 아니라 [`../applications.json`](../applications.json)에 있다.

NVIDIA Korea는 **Workday(nvidia.wd5)**로만 채용한다. 우리 글로벌 수집기가 Workday를 다루긴
하지만 등록된 회사가 Applied Materials·KLA·Aptiv·Micron 4곳뿐이라 **NVIDIA는 목록에 없다.**
이 공고도 사용자가 직접 찾아서 넘겼다. 2026-09-06 기준 한국 공고 **21건**.

## 파일 목록

| 파일 | 내용 | 상태 |
|------|------|:----:|
| [JD_매핑_NVIDIA_Automotive_SW_PM.md](JD_매핑_NVIDIA_Automotive_SW_PM.md) | JD 요건 × 자산 매트릭스 + 갭 분석 + 대안 포지션 검토 | ✅ 초안 (2026-09-06) |
| [APPLY.md](APPLY.md) | 공고 URL · 지원 채널 · 필요 서류 · 체크리스트 | ✅ 초안 (2026-09-06) |
| [JD_원문_Senior_Automotive_Software_Program_Manager.md](JD_원문_Senior_Automotive_Software_Program_Manager.md) | 공고 원문 (Workday cxs JSON) | ✅ 2026-09-06 |
| [materials/](materials/) | 이력서·자기소개서 | 빈 상태 — 지원 결정 후 |

## 대상 포지션

| | 내용 |
|---|---|
| 직함 | Senior Automotive Software Program Manager |
| 근무지 | Korea, Seoul |
| Requisition | `JR2017800` |
| 게시일 | 2026-05-12 |
| 고용형태 | Full time |
| 경력 요건 | **automotive software 개발 6년 이상** (ADAS/AV 선호) |
| 판정 | **핵심 요건 미달** — 현재 3년 7개월, ADAS/AV 소프트웨어 스택 무경험 |

## 솔직한 판정을 먼저 적는 이유

이 디렉토리는 "지원하자"로 시작하지 않는다. JD가 요구하는 두 가지가 지금 없다.

1. **automotive software 개발 6년 이상** — 현재 산업 경력이 3년 7개월(2023-02~)이다.
   연구 경력 2년 6개월을 합쳐도 6년이 안 되고, 합산 표기는 "automotive **software** 개발"이라는
   문구와 맞지 않는다.
2. **ADAS/AV 프로그램을 양산까지 리드한 경험** — GT-SS500 풀사이클이 가장 가깝지만
   농업용 자율주행 플랫폼이지 차량 ADAS/AV 프로그램이 아니다.

부풀려 쓸 수는 있다. 하지만 이 자리는 리크루터 스크리닝 단계에서 연차를 먼저 본다.
`JD_매핑 §5`에 대안 포지션 검토를 넣어뒀다 — **NVIDIA Korea 21건을 전수로 훑었고,
연차 게이트를 깨끗이 통과하는 자리는 없다**는 것이 결론이다.

## 참조

- 공고 원문: [`JD_원문_Senior_Automotive_Software_Program_Manager.md`](JD_원문_Senior_Automotive_Software_Program_Manager.md)
- 자산 출처: `docs/blocks/05-extra/RESUME.md` §4·§5·§7
- 수집 경로: **없음** — `config/global_targets.json`의 `workday` 목록에 NVIDIA를 넣으면
  기존 `scripts/global_collect.py`가 그대로 처리한다 (cxs JSON API로 JD 전문까지 받아진다)
