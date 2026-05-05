# Day 4 — FRACAS 5단계 + Reliability Growth (Duane / AMSAA) (학습 가이드)

> 작성: 2026-05-05 | Apple Reliability Engineer 면접 준비 자가학습
> 베이스: `learning_day4to7.md` §4
> **자가학습 SSOT**: 본 문서는 학습용 자가 정리 자료다. 외부 제출 자료에 직접 인용 금지.

---

## 🎯 학습 목표

이 D4를 끝내면 영어로 60초 안에 다음 3가지를 설명할 수 있다.

1. **FRACAS 5단계** — Detection → Reporting → Analysis → Corrective Action → Verification의 순서와 산출물
2. **Duane Plot** — 기울기 α의 의미와 좋은 범위 (0.3~0.5)
3. **AMSAA Crow β** — β < 1이 신뢰도 향상 중을 뜻하는 이유

> GT-SS500 NCR 27건 운영이 FRACAS와 1:1 매핑된다. 가장 강력한 경험 어필 포인트.

---

## 1. FRACAS 5단계 폐루프

### 1.1 한 줄 정의

> "FRACAS is a closed-loop failure management system — every failure in test or
> field is reported, root-caused, corrected, verified, and fed back into design
> and process standards. The loop doesn't close until the corrective action is
> confirmed effective and the standard is updated."

### 1.2 FRACAS 5단계 + 산출물 (★★★ 암기)

```
    ① Failure Reporting ──► ② Analysis ──► ③ Corrective Action
           ↑                                         │
           │                                         ▼
    ⑤ System Update ◄──────────────── ④ Verification
```

| 단계 | 내용 | 산출물 |
|------|------|--------|
| ① **Failure Reporting** | 발견 즉시 기록: 날짜·제품 ID·현상·발견자 | NCR / Defect Report |
| ② **Analysis** | RCA — 5 Why / Fishbone / DoE → 근본원인 규명 | Root Cause Statement |
| ③ **Corrective Action** | 설계 변경 / 공정 변경 / SOP 개정 | ECN / PCN / SOP Rev |
| ④ **Verification** | 시정조치 효과 확인 — 재현 시험 / 통계 유의성 검증 | Re-test Report |
| ⑤ **System Update** | DFMEA·검사 가이드·SOP 업데이트 + 동종 제품 수평 전개 | 개정 문서 배포 |

**FRACAS vs CAPA**:

| 항목 | FRACAS | CAPA |
|------|--------|------|
| 표준 출처 | MIL-HDBK-2155 | FDA 21 CFR Part 820 |
| 적용 분야 | 항공·국방·반도체·소비재 | 의료기기·의약품 |
| 목적 | 필드/시험 불량 관리 | 규제 준수 기록 |

### 1.3 황인혁 NCR 27건 = FRACAS 1:1 매핑

| FRACAS 단계 | GT-SS500 NCR 운영 |
|------------|------------------|
| ① Failure Reporting | NCR 발행 (날짜·제품 ID·현상·발행자) |
| ② Analysis | RCA 4건 직접 수행 (MCB·LCD·오링·GND) |
| ③ Corrective Action | 설계 변경 (MCB 등급)·공정 변경·SOP 개정 |
| ④ Verification | 재현 시험 + IQC/OQC 재합격 확인 |
| ⑤ System Update | DFMEA 갱신·검사 가이드 개정·BOM 반영 |

> **면접 핵심 문장**: "The label was NCR, but the structure is textbook FRACAS."

---

## 2. Reliability Growth — Duane Plot

### 2.1 한 줄 정의

> "Reliability Growth tracks the improvement in reliability as design fixes accumulate
> during development. The Duane Plot shows that log of cumulative MTBF grows linearly
> with log of cumulative test time — a positive slope proves reliability is improving."

### 2.2 Duane 산식

```
log(θ_c) = log(K) + α · log(T)

θ_c : 누적 MTBF  (= T / 누적 고장 수)
T   : 누적 시험 시간
K   : 상수
α   : Duane growth rate (기울기)

건강한 성장: α = 0.3 ~ 0.5
```

**직관**:
- α = 0.4이면 시험 시간이 10배 → 누적 MTBF가 10^0.4 ≈ 2.5배 향상
- 시정조치가 효과적일수록 α 큼
- log-log 직선이 꺾이거나 평탄해지면 fix가 멈췄다는 신호

---

## 3. Reliability Growth — AMSAA Crow

### 3.1 NHPP 기반 강도 함수

```
λ(t) = λ · β · t^(β-1)

λ(t) : 순간 고장 강도 (intensity function)
λ    : 스케일 파라미터
β    : 형상 파라미터

β < 1 → 고장률 감소 = 신뢰도 향상 중 ✅
β = 1 → 일정 고장률 (포아송 프로세스)
β > 1 → 고장률 증가 (마모 또는 문제 해결 안 됨)
```

**개발 시험 중 목표**: β < 1 확인 → 시정조치가 실제로 효과 있음을 통계적으로 확인.

### 3.2 Duane vs AMSAA 비교

| 항목 | Duane | AMSAA Crow |
|------|-------|-----------|
| 기반 | 경험적 직선 관계 | 통계 모델 (NHPP) |
| 추정 방법 | 그래프적 (log-log) | MLE / Bayesian |
| 신뢰구간 | 없음 | 산출 가능 |
| 사용 시기 | 빠른 시각화·경향 파악 | 정밀 분석·예측·보고 |

### 🖼️ 참고 figure URL

- **FRACAS 폐루프 다이어그램 (Wikipedia)**:
  https://en.wikipedia.org/wiki/Failure_reporting,_analysis,_and_corrective_action_system
  → FRACAS 개요 + 루프 다이어그램. 면접 준비용.

- **Reliability Growth / Duane Plot (ReliaWiki)**:
  https://reliawiki.org/index.php/Reliability_Growth_Reference
  → Duane Plot + AMSAA Crow 모델 상세. log-log 직선 figure 포함.

- **AMSAA Crow-AMSAA (ReliaSoft Help)**:
  검색어: site:help.reliasoft.com "Crow-AMSAA"
  → ReliaSoft 공식 매뉴얼. β 해석 figure + 신뢰구간 chart.

- **Root Cause Analysis 도구 (Wikipedia 5 Whys)**:
  https://en.wikipedia.org/wiki/Five_whys
  → 5 Why 방법론. RCA(② Analysis) 핵심 도구.

---

## 4. 황인혁 경험 ↔ 개념 연결

| 개념 | 내 경험 | 인터뷰 한 줄 |
|------|--------|------------|
| FRACAS 5단계 | NCR 27건 트래킹, RCA 4건 직접 수행 | "I ran 27 NCRs through the GT-SS500 program. The structure was identical to FRACAS — reporting, root cause, corrective action, verification, and standard update." |
| Reliability Growth | DFMEA AP=H 5건 → 전부 시정조치 → 잔여 위험 0 | "Resolving all five AP=H DFMEA items before ramp is functionally equivalent to driving a Reliability Growth curve to target — β<1 trajectory to zero residual high-risk items." |
| Duane Plot α | 개념 학습 (수치 계산 직접 경험 X) | "I haven't computed Duane alpha directly, but the NCR closure trend on a time-series plot would give the same signal — accelerating closure rate = reliability growing." |

---

## 5. 인터뷰 60초 답변 (영문 — 외워야 함)

> Q: "How do you manage a FRACAS system in a product development program?"

> A: "FRACAS is a five-step closed loop: Failure Reporting, Analysis, Corrective
> Action, Verification, and System Update. On the GT-SS500 program I tracked
> 27 NCRs through this loop. Each NCR started with a standard form — date,
> product ID, observed symptom, who found it. We then ran RCA: I personally
> led four, including an MCB carbonization case traced to electrolytic corrosion.
> The corrective action — upgrading to an IEC 60947-2 compliant breaker — was
> verified by reproducing the original failure mode and confirming zero recurrence
> over 200 power cycles. Then I updated the DFMEA, IQC inspection list, and BOM
> so the same failure couldn't slip through in production. The label was NCR,
> but the structure is textbook FRACAS."

— 약 62초. 5단계 명시, 정량 수치 (27 NCRs, 4 RCAs, 200 cycles), 폐루프 완결.

---

## 6. 예상 Follow-up 5개

1. **"How do you decide when to close an NCR?"**
   → 재현 시험 통과 + DFMEA·SOP 업데이트 완료 + 동종 제품 수평 전개 확인. 하나라도 미완이면 미닫힘.

2. **"What's the hardest part of FRACAS?"**
   → ④ Verification — 시정조치가 새 문제를 만들지 않았는지 확인. 2차 효과(side effect) 검증이 RCA 자체보다 어렵다.

3. **"Difference between FRACAS and CAPA?"**
   → CAPA = FDA QSR Part 820, 의료기기 규제 준수 중심. FRACAS = MIL-HDBK-2155, 항공·반도체·소비재. 구조 유사하나 규정 목적 다름.

4. **"How do you prioritize multiple open NCRs?"**
   → Severity × 양산 일정 영향도. S=9~10 (Safety)은 무조건 1순위. Critical Path 블로킹 여부 두 번째 기준.

5. **"What does Duane alpha of 0.5 mean practically?"**
   → 시험 시간 10배 → 누적 MTBF 10^0.5 ≈ 3.2배. 빠른 신뢰도 성장. 개발 초기에는 α 높고, 말기에 낮아지면 더 이상 쉬운 fix가 없다는 신호.

---

## 7. 학습 체크리스트

- [ ] FRACAS 5단계 순서 + 산출물 손으로 써보기
- [ ] GT-SS500 MCB RCA를 FRACAS 5단계로 매핑 (각 단계에 실제 일어난 일 대입)
- [ ] Duane α = 0.4에서 시험시간 10배 → MTBF 배수 직접 계산
- [ ] AMSAA β < 1 / β = 1 / β > 1 각각의 의미를 영어로 1문장씩
- [ ] 60초 답변 Script 4-A (learning_day4to7.md) 외워서 녹음

---

## 8. 다음 학습 (D5 예고)

**Bayesian Reliability + Six Sigma Cpk/Ppk**
- Prior × Likelihood → Posterior — 소표본 강점
- Cpk = 1.33 (4σ) vs 2.0 (6σ) 즉답
- Cpk > Ppk 이면 공정 드리프트 존재 — 해석법
