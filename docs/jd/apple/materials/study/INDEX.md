# Apple Reliability Engineer 자가학습 가이드 — INDEX

> 작성: 2026-05-05 | 면접 준비 D1~D7 학습 가이드 목차
> **자가학습 SSOT**: 외부 제출 자료에 직접 인용 금지. RESUME.md가 사실 SSOT.

---

## 가이드 목록

| 파일 | 주제 | 핵심 1줄 | 예상 학습 시간 |
|------|------|---------|:----------:|
| [D1](D1_stress_strength_weibull.md) | Stress-Strength Interference + Weibull / B10 | S-S overlap = 고장 확률, β가 고장 모드를 말한다 | 90분 |
| [D2](D2_jesd47_coffin_manson.md) | JESD47 7종 + PCT / Coffin-Manson | PCT = 시험 프로토콜, Coffin-Manson = 수명 모델 — 혼용 금지 | 90분 |
| [D3](D3_mil_std_iec_mapping.md) | MIL-STD-810 / IEC 60068-2 / IP 코드 | IP68 = 6m/30min, IEC Fc = 진동, MIL-STD 514 동일 | 60분 |
| [D4](D4_fracas_reliability_growth.md) | FRACAS 5단계 + Duane / AMSAA ★★★ | NCR 27건 = textbook FRACAS. α=0.3~0.5, β<1 성장 중 | 90분 |
| [D5](D5_bayesian_six_sigma.md) | Bayesian Reliability + Cpk / Ppk | Cpk 1.33=4σ, 2.0=6σ=3.4ppm. Cpk>Ppk → 공정 드리프트 | 90분 |
| [D6](D6_camera_vcm_integration.md) | Camera/VCM 도메인 + D1~5 교차연결 | VCM 5 고장모드 + Day1~5 수식이 모두 연결된다 | 120분 |
| [D7](D7_star_answers_english.md) | STAR 영문 답변 5종 핵심 카드 | 5 stories × 핵심 수치 암기 + 외울 1단락 | 120분 |

**총 예상 학습 시간**: 10.5시간 (집중 시 3일, 여유 있게 7일)

---

## 학습 순서 옵션

### 옵션 A — 시험 기술 우선 (Apple 신뢰성 엔지니어 기준)

```
D2 (JESD47/Coffin-Manson) → D4 (FRACAS ★★★) →
D1 (Weibull/B10) → D3 (환경시험) → D5 (Bayesian/Cpk) →
D6 (Camera 통합) → D7 (STAR 답변)
```
→ 핵심 시험 지식 먼저, STAR로 마무리. 면접까지 1주 이상 여유 시.

### 옵션 B — 면접 답변 우선 (D-day 임박)

```
D7 (STAR 카드) → D1 (Weibull 기초) → D2 (JESD47/PCT) →
D4 (FRACAS 경험 연결) → D6 (Camera 적용) →
D3 (환경시험 보조) → D5 (Bayesian/Cpk 보조)
```
→ 바로 답변 연습 시작. 면접 D-3 이하.

### 옵션 C — 순서대로 (기초부터 통합)

```
D1 → D2 → D3 → D4 → D5 → D6 → D7
```
→ 개념 체계를 깔끔하게 쌓고 싶을 때. 시간 여유 2주+.

---

## 면접 D-day 타임라인 (권장)

| D-day | 할 일 |
|-------|-------|
| D-7 | D1 + D2 완료 (Weibull, JESD47, Coffin-Manson) |
| D-6 | D4 완료 (FRACAS — 가장 강력한 경험 어필 포인트) |
| D-5 | D3 + D5 완료 (환경시험 + Cpk) |
| D-4 | D6 완료 (Camera 통합, 교차연결) |
| D-3 | D7 완료 — STAR 5종 첫 녹음 |
| D-2 | 전체 복습 + STAR 재녹음 (Script 없이) |
| D-1 | 60초 답변만 반복. 새 내용 학습 금지. |
| D-0 | 핵심 수치 카드(D7 하단) 5분 훑기 |

---

## 우선순위 요약

| 중요도 | 주제 | 이유 |
|:------:|------|------|
| ★★★ | D2 (JESD47/PCT), D4 (FRACAS) | 직접 경험 연결 최강 어필 |
| ★★ | D1 (Weibull), D6 (Camera) | 도메인 깊이 + Apple 직결 |
| ★ | D3 (환경시험), D5 (Bayesian) | 보조 지식 — 질문 나오면 답할 수준 |
| 필수 | D7 (STAR) | 면접 실전 — 나머지 다 준비해도 D7 못 하면 떨어짐 |

---

## 병행 자료

| 자료 | 경로 | 용도 |
|------|------|------|
| 풀스크립트 원본 (D7) | `learning_day4to7.md` §7.1~7.5 | STAR 답변 전문 |
| 60초 스크립트 세트 | `interview_60sec_scripts.md` | 전 개념 60초 답변 모음 |
| 도메인 역량 SSOT | `reliability_competency.md` | 개념 우선순위 기준 |
| Camera/VCM 상세 | `camera_vcm_reliability.md` | D6 원본 학습 자료 |
| HTML 통합 학습 페이지 | `study/index.html` | figure 보면서 공부 (브라우저로 열기) |
