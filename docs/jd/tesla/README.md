# docs/jd/tesla/ — Tesla Korea 지원 디렉토리

> 지원 직군: Field Support Engineer, Dongtan (Engineering and R&D)
> 지원 상태: 초안 — JD 원문 확보 완료, 사용자 결정 3건 대기
> 지원 이력 상태값은 여기가 아니라 [`../applications.json`](../applications.json)에 있다.

Tesla Korea는 **mokahr(hire-r1)** 자사 채용 사이트로만 뽑는다. 원티드에도, Greenhouse·Lever·
Ashby에도 올라오지 않고 Workday도 쓰지 않는다. 우리 수집기(11:40 원티드 / 11:50 글로벌 18개
보드 + Workday 4개사) 중 어느 쪽에도 잡히지 않는 채널이라, 이 공고는 사용자가 직접 찾아서
넘겼다. 2026-09-06 기준 한국 채용 **61건**이 열려 있다.

## 파일 목록

| 파일 | 내용 | 상태 |
|------|------|:----:|
| [JD_매핑_Tesla_Field_Support_Engineer.md](JD_매핑_Tesla_Field_Support_Engineer.md) | JD 요건 × 자산 매트릭스 + 갭 분석 + 면접 대응 | ✅ 초안 (2026-09-06) |
| [APPLY.md](APPLY.md) | 공고 URL · 지원 채널 · 필요 서류 · 체크리스트 | ✅ 초안 (2026-09-06) |
| [JD_원문_Field_Support_Engineer_Dongtan.md](JD_원문_Field_Support_Engineer_Dongtan.md) | 공고 원문 캡처 (CDP 렌더링) | ✅ 2026-09-06 |
| [openings_snapshot_20260906.json](openings_snapshot_20260906.json) | Tesla Korea 전체 공고 61건 스냅샷 | ✅ 2026-09-06 |
| [materials/resume_tesla.md](materials/resume_tesla.md) | 진단·현장지원 톤 파생 이력서 | ✅ 초안 (2026-09-06) |

## 대상 포지션

| | 내용 |
|---|---|
| 직함 | Field Support Engineer |
| 부서 | Engineering and R&D · Engineering & IT |
| 근무지 | Dongtan (공고상 Job Location은 **Hwaseong, Korea**) |
| 고용형태 | Full-time |
| Job ID | `d4de2072-9365-47a7-b473-3d455620250d` (orgId=tesla, siteId=100000166) |
| 경력 요건 | **3년 이상 관련 경력 우대** |
| 판정 | **요건 충족 · 도메인 적합** |

**적합한 이유**: JD가 요구하는 축이 "복잡한 전기기계 시스템의 고장을 데이터로 진단하고,
현장 실패의 패턴을 설계로 되돌린다"인데, 이게 EOP 400W·GT-SS500에서 실제로 한 일과 겹친다.
CAN 프로토콜 분석(DBC 4종·CANoe·VN1600), 현장 RCA 4건, 다중센서 PHM, 없으면 만드는 시험
장비 7종이 JD 문장에 거의 1:1로 붙는다.

## 이 매핑에서 지키는 선

JD가 요구하는 **UDS·OEM 진단장비·서비스 엔지니어링 조직 경험·CATIA는 포트폴리오에 근거가
없다.** 고전압도 48V(GT-SS500)와 12V(EOP)까지이지 400V급 트랙션 시스템 실무는 없다.

이 문서들은 그걸 갭으로 명시하고 **보유한 것처럼 쓰지 않는다.** 진단·시험·RCA 쪽 근거가
충분히 강해서 부풀릴 이유도 없다. `JD_매핑 §4`가 갭별 대응과 압박 질문 답변을 담고 있다.

## 참조

- 공고 원문: [`JD_원문_Field_Support_Engineer_Dongtan.md`](JD_원문_Field_Support_Engineer_Dongtan.md)
- 자산 출처: `docs/blocks/05-extra/RESUME.md` §4·§5·§6·§7
- 수집 경로: **없음** — mokahr는 아직 어떤 수집기도 다루지 않는다.
  API는 확인됨: `POST https://hire-r1.mokahr.com/api/outer/ats-apply/website/jobs/v2`
  (`orgId` + `siteId`, `limit` 최대 30, `offset` 페이징)
