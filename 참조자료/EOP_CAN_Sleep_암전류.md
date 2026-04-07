# EOP 400W CAN Sleep/Wakeup — 암전류(Dark Current) 기술 문서

> 출처: `EOP_12V_400W_Sleep 및 Wakeup 구현_rev4.pptx`, `20230525_MC9S12ZVMC_Sleep.pptx`
> 경로: `HIH_2/1)프로젝트/1)EOP/1)2023_2024_400W/13)CANSleep/`

---

## 요구조건

| 항목 | 요구값 | 출처 |
|------|--------|------|
| Dark Current | **100 uA 미만** | 고객사(현대 트랜시스, DIC) |
| Bus-off Sleep 진입 | Bus-off 5초 연속 감지 시 Sleep 진입 | 고객사 |
| 작동 전압 특성 | MCU, Controller 정상 동작 | 고객사 |

---

## 문제 — 기존 회로로는 불가능

| 항목 | 값 | 비고 |
|------|-----|------|
| 기존 회로 Dark Current | **1.2 mA (최소)** | NXP CPU STOP + Regulator 차단 + GDU disable 적용해도 |
| 요구조건 | 100 uA 미만 | **12배 초과 → 불가** |

**원인**: Ballast Supply 사용하는 기존 회로에서는 VDDX/VDDC 전원 차단 불가. Shutdown 기능은 S12ZVMC256에서만 구현 가능 (현재 MCU와 다름).

---

## 해결 — Dual Transistor + CAN Sleep IC 회로

### 회로 구성

1. **TR + P-MOSFET 비반전 스위치** — VINH를 입력으로 VSUP 전원 차단
2. **CAN Sleep IC (TJA1443)** — Sleep 모드에서 INH Low → VSUP Gate Off → MCU Off
   - TJA1443 Sleep 모드 Vbat 전류: typ. **12 uA**
   - 검토 과정에서 TLE9252V도 평가 (typ. 12 uA)

### 개선 회로 역기능 해결

| 문제 | 해결 |
|------|------|
| VSTB/VEN float → Reprogram 미진입 | VINH 전압으로 풀업 → Normal operation 유지 |
| VINH Pull-up → Sleep 진입 불가 | 다이오드 D2/D3 추가 (역전압 방지) |
| VSTB/VEN over voltage → MCU 고장 위험 | 제너다이오드 D1/D6 추가 (5V 이상 억제) |

---

## 실측 결과

| PCB | Dark Current | 요구(100 uA) 대비 | 판정 |
|-----|-------------|-----------------|:----:|
| **PCB #14** | **9.68 uA** | 10.3배 마진 | ✅ PASS |
| **PCB #8** | **7.6 uA** | 13.2배 마진 | ✅ PASS |

**기존 1.2 mA → 9.68 uA = 99.2% 감소 (124배 개선)**

---

## Sleep/Wakeup 시퀀스

### Sleep 진입

```
① VBAT=12V, VSUP=12V, VINH=High, MCU on, CAN IC Normal
② STB_N=LOW → CAN IC Go-to-Sleep Command
③ CAN IC Sleep Mode, VINH=Low
④ TR+FET Off → VSUP=0V → MCU Off → Dark Current = 9.68 uA
```

### Wakeup

```
⑤ CAN_H/L WUP 감지 → CAN IC Stand-by Mode → VINH=High
⑥ VSUP 복구 → MCU Wakeup → Turn-on 절차 동일
```

### Sleep Algorithm

```
Bus-off 감지 (CAN_H/L 상태 판별: 정상/Open/Short)
  → 5초 연속 CNT
  → Sleep 지령
  → CAN Sleep IC → VSUP Gate Off → MCU Sleep
```

### Wakeup Algorithm

- ISO 11898-2:2016 규격 기반 Wakeup Pattern 구현
- CAN_H/L WUP 인가 → INH High → VSUP Gate ON → MCU Wakeup

---

## 검증 항목

| 항목 | 결과 |
|------|------|
| Sleep 진입 후 Dark Current | 9.68 uA (PCB#14) / 7.6 uA (PCB#8) |
| Wakeup 후 정상 복귀 | 확인 |
| CAN Reprogram 정상 동작 | 확인 (풀업 회로 개선 후) |
| 모터 부하 구동 시 고조파 | 양호 (TR+NFET 적용 후) |
| 역기능 (over voltage) | 제너다이오드로 억제 확인 |

---

## 기술 스택

- MCU: NXP MC9S12ZVMC (S12Z 계열, 내장 GDU)
- CAN Sleep IC: NXP TJA1443 (최종) / Infineon TLE9252V (검토)
- 전원 차단: P-MOSFET + Transistor 비반전 스위치
- 규격: ISO 11898-2:2016 (CAN Physical Layer)

---

## 포트폴리오 활용 포인트

1. **정량적 성과**: 기존 1.2mA → 9.68uA (124배 개선, 요구 대비 10배 마진)
2. **문제 해결 과정**: NXP 제공 기능만으로 불가 → HW 회로 설계 변경으로 해결
3. **역기능 분석**: 3가지 역기능 발견 + 해결 (다이오드, 제너, 풀업)
4. **규격 준수**: ISO 11898-2 기반 Wakeup Pattern
