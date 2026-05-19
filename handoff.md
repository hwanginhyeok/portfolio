# Handoff — 2026-05-19

## 작업 중이던 것

**JD-A3 (Apple Reliability Engineer 지원서 최종 제출)** — 사용자 직접 수행 대기
- 자료 v3 완성 (resume v6 + cover letter v4 + factcheck_match v2 + study/index.html D8)
- PDF 변환만 남음: `docs/jd/apple/materials/pdf_draft/resume_en.html`, `cover_letter.html` → 브라우저 Ctrl+P
- JD 직링크: https://jobs.apple.com/en-us/details/200656459-3631/reliability-engineer-core-technology-operations-korea?team=OPMFG

## 이번 세션 한 일 (커밋 5건)

1. **JD-A8 완료** (`9d48071`) — Apple 지원자료 1차 리뷰. 영문 이력서 5건 수정 (BMS 익명화 / TOEIC 재응시 표기 제거 / 60+/37+ 중복 해소 / Awards 분리 / SUMMARY 분할) + PDF 초안 HTML 생성
2. **JD 직링크 SSOT 등록** (`3636792`) — `docs/jd/apple/APPLY.md`에 jobs.apple.com 직링크 명시
3. **3라운드 전문가 리뷰 + v3 자료** (`6c4355b`) — resume v5→v6, CL v3→v4. factcheck_match v1/v2 생성. Round 1 (HM/SME/ATS 병렬) → Round 2 (Senior HM 통합) → Round 3 (사용자 결정 4건 적용)
4. **학습 자료 v3 정합화** (`21c6f40`) — reliability_competency.md SVM 주체 분리, interview_60sec_scripts.md §A v3 답변 패턴 5종 + §B 우선순위 추가
5. **study/index.html D8 신규 섹션** (`9e8e581`) — 함정 질문 5종(A1~A5) + D-day 체크리스트, nav 갱신

## 컨텍스트 (사용자 결정)

- Deep FA 방법론: **Fishbone (Ishikawa)** (RCA 4건 4M 분류)
- TOEIC 만료 표기: **"(expired)"** (재응시 언급 없이)
- 구미 근무 의향: 이력서/CL 침묵, 면접 단계 명시
- SSOT 불일치 3건: 전부 정직 정리 (60+→37+ / AIAG-VDA 미사용 / SVM 주체 분리)

## 통과 가능성 (Senior HM 페르소나 추정)

| 단계 | % |
|------|:-:|
| 서류 통과 | 70-78% |
| 1차 면접 | 50-58% |
| 최종 합격 | 25-32% |

**구조적 미해결 갭**: camera/VCM/lens 직접 경험 X (자가학습으로 보완)

## 다음 세션 첫 액션

1. **사용자가 PDF 변환** (`pdf_draft/*.html` → 브라우저 Ctrl+P, Letter, 헤더/푸터 끄기)
2. **jobs.apple.com 직링크 제출** (Job ID 200656459-3631)
3. **면접 사전 준비** (study/index.html §D8 + §면접 사전 우선순위):
   - ★★★ A3 SVM 정직 답변 암기 (Q4 지뢰 차단 — 최우선)
   - ★★★ A1 ORT vs DVT/PVT 구분 답변
   - ★★★ MCB #204 Fishbone 4M 분해 5분 즉석 재연
   - ★★ JESD47 7종 + Coffin-Manson 계산
   - ★★ Weibull β·η → B10 즉답
   - ★ camera_vcm_reliability.md 내재화
4. (선택) JD-A7 fact-check — P-01·P-02·T-01 PDF 1차 자료 수령 후

## 참고 자료 위치

| 자료 | 경로 |
|------|------|
| 매트릭스 SSOT | `docs/jd/apple/materials/factcheck_match_v2.md` |
| 영문 이력서 v6 | `docs/jd/apple/materials/resume_en.md` |
| 커버레터 v4 | `docs/jd/apple/materials/cover_letter.md` |
| 면접 60초 스크립트 | `docs/jd/apple/materials/interview_60sec_scripts.md` (§A v3 5종) |
| 학습 HTML | `docs/jd/apple/materials/study/index.html` (D1~D8 + 면접 사전 우선순위) |
| PDF 초안 | `docs/jd/apple/materials/pdf_draft/` |
| 지원 가이드 | `docs/jd/apple/APPLY.md` (JD 직링크 + 절차) |

## 메모리 갱신

- `project_portfolio_apple.md` — v3 완성 상태 반영, 3라운드 리뷰 핵심 발견 + 면접 준비 키 5건 명시
- `feedback_factcheck_submission_sync.md` (신규) — 팩트체크 매트릭스 ≠ 제출본 동기화 필수 패턴
- `MEMORY.md` 인덱스 갱신 (2건)

## 잔여 이슈

CURRENT 3건 그대로 유지 (B1-01 인벤토리 / 4-5 SVPWM 노트북 블록 / 4-7 범퍼 사진 블록). 둘 다 환경 제약으로 PC/노트북 작업 필요.
