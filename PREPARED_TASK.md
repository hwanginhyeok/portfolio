# Prepared Tasks

> 넘버링: `B{블록}-{순번}` — 자세히는 [TASK.md](TASK.md) 상단 참조

## B1 — 자료 인벤토리 (17개)

> 2026-04-26 추가: B1-09~B1-18 — 홈페이지 자료 정합성 점검 후 도출된 자료 픽스 항목

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| B1-02 | SVPWM 수치 확보 — 효율 +1%/+4% + 온도 저감 | P2 | 노트북 엑셀 이관 | 기존 4-5. N01/N02 (대기 자산) |
| B1-03 | 범퍼 실차시험 사진 확보 | P2 | 핸드폰→PC 이관 | 기존 4-7 잔여. W01 |
| B1-04 | 시험 환경 장비 사진 촬영 (다이나모/팬벤치/범퍼) | P2 | 시험실 방문 | 기존 6-5. W02/W03/W04 |
| B1-05 | 양산 전장함 사진 촬영 | P2 | 회사 촬영 | 기존 6-6. W05. **최신본 필요** (현 control-box-external.webp는 옛날 버전) |
| B1-06 | VCU PCB 실물 + CAN 장비 화면 | P3 | 촬영 | 기존 TODO. W06/W07 |
| B1-07 | GT-SS500 PM 경험 문서화 (APQP/WBS/이슈관리/BOM) | P2 | | 기존 2-3. E01 |
| B1-08 | AI 활용 사례 + 사이드 프로젝트 3종 문서화 | P2 | | 기존 2-4/2-5 병합. E02/E03 |
| B1-17b | 학위논문 정확한 제목/J-01 저널 게재지 확정 | P2 | dcollection.konkuk / KCI 직접 검색 | PAPERS.md 미해결 항목. 현재 patent 페이지 P-1 카드는 CONTENT_V2 인용 제목 사용 중 |

## B2 — 활용 전략 (1개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| B2-01 | 타겟 회사·JD 분석 + 핵심 메시지 3~5개 확정 + 자산 매트릭스 + 컷 리스트 | P1 | 사용자 입력 | `USAGE_STRATEGY.md` 골격 완료. §1 타겟 회사 / §2 메시지 확정 사용자 입력 대기 |

## B4 — 디자인 (1개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| B4-02 | `/impact` 페이지 구현 | P2 | B4-01 완료 후 | LAYOUT.md §2.4 명세. Hero 4카드 확장판 + LifecycleHeatmap + 메시지별 정량표. nav 미노출, 이력서/LinkedIn 공유용 URL |

## JD 지원 — Apple (4개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| JD-A3 | Apple 지원서 최종 제출 (사용자 직접) | P1 | JD-A5, JD-A6, JD-A7 | jobs.apple.com Job ID 200656459-3631. 자료 준비 완료(resume_en/cover_letter/learning Day1~7/STAR 5종). **제출은 사용자 직접 수행** |
| JD-A5 | Reliability 역량 정리 + 연계 경험 발굴 (사용자 인터뷰) | P1 | — | PM-83과 동일. ALT/Weibull/Arrhenius/PHM/DFMEA/FRACAS/MTBF/Bathtub/HALT-HASS/Damage Summation 보유 vs 미보유 구분. 학부/대학원/회사 미기재 경험 발굴 → `materials/reliability_competency.md` |
| JD-A6 | Apple 커버레터 작성 (`materials/cover_letter.md`) | P1 | JD-A5 | jd_resume_match.md §3 강점/갭 + JD-A5 결과를 4단락으로 압축. RBDO Lab 출신 강조하되 다른 강점도 균형 배치 |
| JD-A7 | 학습자료 fact-check 정정 — 1차 자료(P-01·P-02·T-01) 수령 후 학습자료 사후매핑 제거 + 풍부화 | P1 | 사용자 PDF 제공 (P-01 IEEE TIM 2024 / P-02 PCIM Asia 2022 / T-01 석사 학위논문) | 트리거: D1 §3 "β>1 wear-out" 단언이 P-01 검출·위치식별 방법과 mismatch (D-007 패턴 재발). FACTCHECK_bondwire.md §6~9 참조. 정정 대상: D1 §3, D2, D6, reliability_competency Block2 Arrhenius, index.html. 사용자 답변 항목: P-02 본인 역할 / PCT 직접 셋업 경험 / Weibull β 직접 산출 경험 / T-01 한글 제목 / T-01 신뢰성 챕터 유무 |

## JD 지원 — xAI (3개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| JD-X2 | xAI 맞춤 resume + cover letter 작성 (`docs/jd/xai/materials/`) | P1 | JD-X1 | Apple resume_en을 baseline으로 ME researcher 톤 전환. 저널 4편 + autonomous learner 강점 부각 |
| JD-X2b | xAI PHM SoC 표현 SSOT 정합 수정 (컨펌 후 실행) | P1 | 사용자 제출 여부 확인 | `resume_xai.md` L65 + `cover_letter_xai.md` L13: "multi-sensor fault diagnosis·RUL" → "motor/fault modeling·Co-simulation". PPT 근거 없는 표현. xAI 지원이 이미 제출됐으면 수정 불필요 |
| JD-X3 | xAI 지원서 제출 (사용자 직접) | P1 | JD-X2 | greenhouse 폼. **제출은 사용자 직접 수행** |

## B5 — 부가자료 (3개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| B5-01 | 이력서 작성 | P3 | 이메일/사이트 URL 입력 + 토익 재응시 | `RESUME.md` 마스터 완료. 어학 만료 명시 |
| B5-04 | TOEIC + TOEIC Speaking 재응시 | P2 | 사용자 외부 작업 | 이전 점수: TOEIC 920 / TS 140 (IH). 응시 후 RESUME §9 갱신 |
| B5-02 | GitHub 프로필 정비 | P3 | 사용자 실행 | `GITHUB_PROFILE.md` 가이드 완료. P1: profile README + 핀 6개 |
| B5-03 | 영문 버전 | P3 | 사용자 결정 (i18n 옵션) | `ENGLISH_VERSION.md` 가이드 완료. 어휘집 + Summary 4종 + IEEE 인용 |
