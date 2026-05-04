# ARM Cortex-M MCU 심화 — 면접 핵심 (R1 갭 보강)

> 출처: ARM ARMv7-M Architecture Reference Manual · ST RM0433 (STM32H7) · ST RM0090 (STM32F4)
> 황인혁 경험 연결: SS500 STM32 VCU (1ms ISR, CAN·SPI DMA 병행)

---

## 1. Cortex-M 계열 핵심 차이

| 항목 | M0/M0+ | M3 | M4 | M7 |
|------|--------|----|----|-----|
| FPU | 없음 | 없음 | 단정도 (FPv4-SP) | 단/배정도 (FPv5-D16) |
| DSP | 없음 | 없음 | SIMD·MAC 32/64bit | SIMD·MAC + 배정도 |
| MPU | 선택(8 region) | 8 region | 8 region | 16 region |
| 파이프라인 | 2단 | 3단 | 3단 | 6단 슈퍼스칼라 |
| 대표 MCU | STM32G0/F0 | STM32F1/F2 | STM32F4 | STM32H7 |

**드론 FW에서 핵심**: M4/M7 FPU 없으면 쿼터니언 연산이 소프트웨어 부동소수점 → 레이턴시 수배. PX4 Pixhawk 4(H743)가 M7인 이유.

---

## 2. Bus Matrix — DMA와 CPU 병행

```
[CPU Core]─── I-Bus ──→ [Flash / ITCM]
            └ D-Bus ──→ [SRAM1 / DTCM]
            └ S-Bus ──→ [APB periph]

[DMA1]  ──────────────→ [SRAM2]       ← IMU SPI 수신 버퍼
[DMA2]  ──────────────→ [SPI1 CR]     ← SPI 전송 트리거
```

- 마스터(CPU, DMA1, DMA2)가 **서로 다른 슬레이브**에 접근하면 동시 진행 — 충돌 없음.
- 드론 실전: DMA가 SPI-IMU 데이터를 SRAM에 채우는 동안 CPU는 PID 연산. Zero-wait.
- **SS500 연결**: STM32 HAL_SPI_TransmitReceive_DMA() + CAN RX ISR 병행이 이 구조 덕분에 가능했음.

---

## 3. NVIC — 인터럽트 우선순위

```
SCB->AIRCR.PRIGROUP = 3  →  [7:4] preemption 4bit / [3:0] sub-priority 4bit
```

- **Preemption**: 낮은 숫자(=높은 우선순위) IRQ가 실행 중인 IRQ를 선점 가능.
- **Sub-priority**: 선점 불가. 동시에 pending된 IRQ들 사이 실행 순서 결정.
- PX4 NuttX 기본: preemption 4bit. ESC PWM > IMU DMA > MAVLink UART 순.

**드론 안전 원칙**: 모터 명령 업데이트 IRQ가 최고 우선순위. 지연되면 400Hz 루프가 무너짐.

```
우선순위 예시 (낮은 숫자 = 높음):
  0: TIM1 (PWM 업데이트)
  1: SPI1 DMA (IMU 데이터 완료)
  5: UART (MAVLink 수신)
```

---

## 4. MPU — 드론에서 추락 방지 안전망

- 메모리를 최대 16 region으로 나눠 read/write/execute 권한 지정.
- **왜 중요한가**: 비행 중 null pointer dereference, stack overflow가 제어 변수를 덮으면 추락 = 치명적.
- MPU 설정 → MemManage Fault → SafeMode 전환. 버그가 감지되는 순간 안전하게 착륙 시도.

```
Region 0: Flash (0x0800_0000) → RX only (코드 실행, 쓰기 불가)
Region 1: DTCM SRAM          → RW (제어 변수 영역)
Region 2: Stack guard page   → No access (오버플로 즉시 fault)
```

- **SS500 연결**: FreeRTOS에서 `configCHECK_FOR_STACK_OVERFLOW=2` 설정 = 소프트웨어 스택 감시. MPU는 하드웨어 레벨에서 동일한 목적.

---

## 5. 면접 답변 예시

**"Cortex-M4와 M7 차이를 설명하세요."**
> "핵심은 FPU와 캐시입니다. M4는 단정도 FPU, M7은 단/배정도 FPU + L1 I/D 캐시. 드론 자세 제어에서 쿼터니언 곱·삼각함수를 400Hz로 돌리면 M7 FPU가 없으면 소프트웨어 부동소수점으로 폴백해서 레이턴시가 수배 늘어납니다. PX4가 Pixhawk 4에 STM32H743(M7)을 쓰는 이유입니다."

**"MPU가 왜 드론 FW에서 중요한가요?"**
> "비행 중 FW 버그로 null pointer가 제어 변수를 덮으면 추락이 확정입니다. MPU로 SRAM을 region별로 나눠 Stack guard page에 no-access 설정하면 오버플로 즉시 MemManage Fault로 잡혀 SafeMode 전환이 가능합니다. SS500 VCU에서 FreeRTOS 스택 오버플로 감시를 소프트웨어로 설정했는데, MPU는 그걸 하드웨어 레벨에서 보장하는 겁니다."
