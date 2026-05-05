# Day 3 — MIL-STD-810 / IEC 60068-2 / IEC 60529 (학습 가이드)

> 작성: 2026-05-05 | Apple Reliability Engineer 면접 준비 자가학습
> 베이스: `learning_day1to3.md` §3, `reliability_competency.md` Block 5
> **자가학습 SSOT**: 본 문서는 학습용 자가 정리 자료다. 외부 제출 자료에 직접 인용 금지.

---

## 🎯 학습 목표

이 D3를 끝내면 영어로 60초 안에 다음 3가지를 설명할 수 있다.

1. **MIL-STD-810 Method 번호** — 온도/진동/충격 Method를 즉답
2. **IEC 60068-2 매핑** — MIL-STD-810 대응 IEC 시험 코드 (Fc, N, Ea 등)
3. **IP67 / IP68** — 두 자리 숫자의 의미와 차이를 30초 안에 설명

---

## 1. MIL-STD-810 주요 Method

### 1.1 한 줄 정의

> "MIL-STD-810 is a US DoD environmental engineering standard that defines test
> methods and procedures to simulate real-world environmental stresses on equipment
> — temperature, humidity, vibration, shock, sand, and immersion — throughout the
> product life cycle."

### 1.2 주요 Method 표 (★★★ 암기)

| Method | 이름 | 스트레스 | 주요 조건 | 고장 모드 |
|--------|------|---------|---------|---------|
| **501** | High Temperature | 열 | 71°C storage, 49°C operating (예시) | 크리프, 코팅 박리, 윤활유 변형 |
| **502** | Low Temperature | 냉각 | -40°C operating (예시) | 재료 취성, 기동 실패, 수분 동결 |
| **507** | Humidity | 고온·고습 | 30°C/95%RH, 10 cycles | 부식, 절연 저하 |
| **510** | Sand and Dust | 분진 | 1.1 g/m³ (blowing sand) | 삼입 이물, 마모 |
| **512** | Immersion | 침수 | 1m, 30min | 밀봉 누수 |
| **514** | Vibration | 진동 | 광대역 랜덤/사인, 프로파일별 | 피로, 체결 풀림, 커넥터 접촉 불량 |
| **516** | Shock | 충격 | 반사인파 (half-sine), 다방향 | 납땜 크랙, 스프링 파손, PCB 파손 |

**MIL-STD-810 구조**: 각 Method는 절차(Procedure) I/II/III로 나뉨. 제품 용도에 따라 적절한 Procedure 선택.

---

## 2. IEC 60068-2 — 민간 대응 표준

### 2.1 한 줄 정의

> "IEC 60068-2 is the international (non-military) environmental testing standard for
> electronic equipment. It uses letter codes instead of method numbers, and aligns
> conceptually with MIL-STD-810 but with different stress profiles and acceptance criteria."

### 2.2 MIL-STD-810 ↔ IEC 60068-2 매핑표

| MIL-STD-810 Method | IEC 60068-2 시험 | 코드 | 공통 목적 |
|--------------------|-----------------|------|---------|
| 501 High Temperature | 고온 건조열 | **Bb (2-2)** | 고온 내성 |
| 502 Low Temperature | 저온 | **Ab (2-1)** | 저온 내성 |
| 507 Humidity | 습열 사이클 | **Db (2-30)** | 고습 내성 |
| — | 열충격 | **N (2-14)** | 급격한 온도 변화 (TC 대응) |
| 514 Vibration | 정현파 진동 | **Fc (2-6)** | 진동 피로 |
| 514 Vibration | 랜덤 진동 | **Fh (2-64)** | 광대역 진동 |
| 516 Shock | 충격 | **Ea (2-27)** | 낙하·충격 |
| 512 Immersion | 침수 | **IPx7/IPx8** (IEC 60529 참조) | 방수 |

**핵심 차이**: MIL-STD-810은 Method 번호로, IEC 60068-2는 영문 코드로 시험 지정.
Apple 제품 사양서에서는 IEC 60529 IP 코드 + IEC 60068-2 병용이 일반적.

---

## 3. IEC 60529 — IP 코드 (방진·방수)

### 3.1 IP 코드 구조

```
IP  X  Y
     │  └── 두 번째 자리: 방수 (0~9K)
     └───── 첫 번째 자리: 방진 (0~6)

IP XX = 완전한 사양 명시
IPX7  = 방수만 (방진 등급 미시험/미지정)
```

### 3.2 방진 등급 (첫 번째 자리)

| 등급 | 의미 |
|------|------|
| 0 | 보호 없음 |
| 1 | 50mm 이상 이물 차단 |
| 4 | 사방 비말 차단 |
| 5 | 저압 분사 방어 |
| **6** | **방진 완전 (먼지 침입 없음)** |

### 3.3 방수 등급 (두 번째 자리)

| 등급 | 의미 |
|------|------|
| 0 | 보호 없음 |
| 4 | 사방 비말 차단 |
| 5 | 저압 분사 방어 |
| 6 | 강한 분사 방어 |
| **7** | **침수 1m, 30min** |
| **8** | **침수 — 깊이·시간 제조사 사양** (iPhone: 6m/30min) |
| 9K | 고압·고온 분사 방어 (산업 세척) |

**iPhone 방수 등급 요약**:

| 모델군 | IP 등급 | 의미 |
|--------|---------|------|
| iPhone 7~12 | **IP67** | 1m 침수 30min |
| iPhone 13+ | **IP68** | 6m 침수 30min (Apple 사양) |
| Apple Watch Series 6+ | **IP6X + WR50m** | 50m 방수 (ISO 22810) |

### 🖼️ 참고 figure URL

- **IP 코드 표 (Wikipedia, 전체 등급 + 아이콘)**:
  https://en.wikipedia.org/wiki/IP_code
  → 방진·방수 등급 전체 표 + 아이콘 figure. 암기용으로 적합.

- **MIL-STD-810 개요 (Wikipedia)**:
  https://en.wikipedia.org/wiki/MIL-STD-810
  → 각 Method 번호 목록 + 역사. 면접 준비용 overview.

- **IEC 60068 개요 (Wikipedia)**:
  https://en.wikipedia.org/wiki/IEC_60068
  → IEC 60068 시리즈 코드 목록. Fc/N/Ea 코드 확인.

- **IEC 60529 / IP 코드 상세**:
  https://en.wikipedia.org/wiki/IEC_60529
  → IP 등급 정의 전체 + 시험 방법 개요.

---

## 4. 황인혁 경험 ↔ 개념 연결

| 개념 | 내 경험 | 인터뷰 한 줄 |
|------|--------|------------|
| MIL-STD-810 M516 Shock | GT-SS500 범퍼 시험대 직접 제작 (정지거리 0.082m, 피크 308A) | "The bumper safety rig I built aligns with MIL-STD-810 Method 516 — I was verifying half-sine shock response of the safety system." |
| MIL-STD-810 M502 Low Temp | -40°C 극저온 기동 실증 (특허 #2 기여) | "The cold-start validation at −40°C maps to MIL-STD-810 Method 502 low temperature — 300s to 100s start time." |
| IP 코드 (방수·방진) | GT-SS500 농업용 자율주행 — 야외 분무 작업 환경 | "For the agricultural sprayer, IP65+ was a design requirement — operating in direct water spray and dusty fields." |
| IEC 60068-2 Fc (진동) | GT-SS500 필드 진동 환경 (농업 노면) | "Field terrain vibration for an agricultural vehicle required verifying the CAN connector retention against IEC 60068-2 Fc-equivalent profiles." |

---

## 5. 인터뷰 60초 답변 (영문 — 외워야 함)

> Q: "How would you specify environmental test conditions for an outdoor product like
> an agricultural robot?"

> A: "I'd start with the use environment — outdoor, dusty fields, water spray,
> temperature extremes, and rough terrain vibration. That maps to specific test
> standards: IP66 or IP67 for dust and water ingress per IEC 60529, IEC 60068-2
> Ab and Bb for low and high temperature, thermal shock per IEC 60068-2 N, and
> random vibration per IEC 60068-2 Fh for terrain-induced vibration. If DoD
> traceability is needed, MIL-STD-810 Methods 502, 501, 514, and 516 are the
> direct equivalents. On the GT-SS500 program, the dominant field failure modes
> from the DFMEA were pump O-ring freeze at −40°C and GND noise from vibration
> — which told me where to focus the test matrix. You always design the test plan
> around the failure mechanisms, not around checking boxes."

— 약 60초. IP 코드 + IEC/MIL-STD 매핑 + GT-SS500 경험 연결.

---

## 6. 예상 Follow-up 5개

1. **"What is the difference between MIL-STD-810 and ISTA?"**
   → ISTA (International Safe Transit Association) = 포장 + 운송 진동/충격. MIL-STD-810 = 제품 자체의 환경 내성. 적용 계층이 다름.

2. **"How do you select vibration test profile level?"**
   → 실제 필드 진동 측정 (accelerometer로 데이터 수집) → PSD (Power Spectral Density) 프로파일 도출 → ALT용 상향 조정. HALT도 보완 수단.

3. **"IP68 vs IP67 — what's the key difference?"**
   → IP67 = 1m/30min (IEC 기본 정의). IP68 = 제조사가 더 깊은/긴 조건 지정 (Apple: 6m/30min). IP68이 반드시 IP67 포함.

4. **"How does thermal shock differ from temperature cycling?"**
   → Thermal Shock (IEC 60068-2 N): 급격한 온도 전환 (수 초~수 분) — 솔더·세라믹 크랙 유발. TC (IEC 60068-2 Db): 느린 전환 — 크리프 피로. 타겟 고장 메커니즘이 다름.

5. **"What's HALT and how is it different from JESD47?"**
   → HALT (Highly Accelerated Life Test): 고장 한계 탐색용, 규정 스트레스 없음. JESD47: 합격 기준 있는 양산 검증 시험. HALT는 설계 개선, JESD47은 출하 기준 검증.

---

## 7. 학습 체크리스트

- [ ] MIL-STD-810 Method 번호 (501/502/507/510/512/514/516) 5초 안에 매칭
- [ ] IP67 vs IP68 설명을 비전공자에게 30초 안에 설명
- [ ] IEC 60068-2 코드 (Ab/Bb/Fc/Fh/Ea/N) 영문으로 설명
- [ ] GT-SS500 범퍼·저온 시험 경험을 MIL-STD-810 언어로 재표현 연습

---

## 8. 다음 학습 (D4 예고)

**FRACAS 5단계 + Duane/AMSAA Reliability Growth** ★★★
- GT-SS500 NCR 27건 = FRACAS 폐루프 (명칭만 다름)
- DFMEA AP=H 5건 해소 = Reliability Growth 추세로 재해석
- Duane Plot α, AMSAA Crow β < 1 의미
