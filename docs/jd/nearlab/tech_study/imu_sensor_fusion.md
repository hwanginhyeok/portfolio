# IMU 센서 퓨전 기본 — 면접 핵심 (R5 갭 보강)

> 출처: IEEE Std 1293 (Gyro spec), Allan Variance (IEEE 952-1997), PX4 ekf2 소스 (GitHub)
> 황인혁 경험 연결: SS500 RTK+IMU 자율주행 · 대학원 IPMSM 센서 퓨전 상태 추정

---

## 1. MEMS 가속도계·자이로 특성

| 파라미터 | 정의 | 드론 영향 |
|---------|------|---------|
| Noise density (ARW) | 단위 √Hz당 각속도 노이즈 (°/hr/√Hz) | 짧은 시간 자세 추정 노이즈 |
| Bias instability | Allan Variance 최저점. 장기 zero-offset 안정성 | 수십 초 이상 dead-reckoning 오차 |
| Scale factor | 입력-출력 선형성 오차 (ppm) | 고속 회전 시 누적 오차 |
| Cross-axis sensitivity | 1축 입력이 타축으로 누설 | 로터 진동 coupling |

**핵심 직관**:
- **자이로**: 단기 정밀 (낮은 ARW), 장기 bias drift. 고주파 신뢰.
- **가속도계**: 장기 안정 (중력 기준), 그러나 선형 가속·진동에 오염. 저주파 신뢰.
- → "고주파=자이로, 저주파=가속도계"가 모든 센서 퓨전의 기본 논리.

---

## 2. Complementary Filter

```
angle = α × (angle + gyro_rate × dt) + (1 - α) × accel_angle
```

- α = 0.98 (전형적). 자이로 적분 98% + 가속도계 2%.
- **장점**: 구현 단순, 수 μs 연산. MCU에서 충분히 실시간.
- **단점**: Yaw 불가(가속도계는 Yaw 성분 없음), 기동 중 선형가속으로 accel_angle 오염.
- **드론 적용**: 정적·Hover 상태에서 유효. 급기동 중에는 EKF 필요.

---

## 3. Extended Kalman Filter — 드론 적용

### 상태벡터 (PX4 ekf2 간소화)

```
x = [q0, q1, q2, q3,    ← 쿼터니언 (자세)
     vx, vy, vz,         ← 속도 (NED)
     px, py, pz,         ← 위치 (NED)
     bg_x, bg_y, bg_z,   ← 자이로 바이어스  ← 핵심: 바이어스를 상태에 포함
     ba_x, ba_y, ba_z]   ← 가속도계 바이어스
```

### predict / update 루프

```
[IMU 400Hz]
  predict():  F(x) = f(x, accel, gyro)  ← 상태 전파
              P_pred = F × P × Fᵀ + Q   ← 공분산 전파

[GPS 10Hz]
  update():   y = z - H(x)              ← 관측 잔차
              K = P × Hᵀ × (H×P×Hᵀ+R)⁻¹ ← 칼만 게인
              x = x + K × y
              P = (I - K×H) × P
```

- **바이어스 추정의 의미**: 자이로 바이어스를 상태벡터에 포함 → 비행 중 실시간 교정. 온도 변화로 drift가 변해도 update()에서 보정됨.
- `EKF2_AID_MASK` 파라미터: 어떤 센서를 update()에 쓸지 비트마스크. GPS 없으면 optical flow + 초음파로 대체 가능. 자세(Roll/Pitch/Yaw)는 IMU + Magnetometer만으로도 유지.

### 센서별 역할

| 센서 | update() 주기 | 제공 정보 | 없을 때 |
|------|:------------:|---------|--------|
| IMU | 400Hz (predict) | 자세·가속도 | EKF 동작 불가 |
| GPS | 10Hz | 절대 위치·속도 | 수평 위치 drift 누적 |
| Baro | 25Hz | 고도 | 고도 drift |
| Magnetometer | 100Hz | Yaw 절대 방향 | Yaw drift |
| Optical flow | 30~100Hz | 수평 속도 (실내) | GPS 대체 |

---

## 4. 황인혁 경험 연결

**SS500 연결**: RTK-GPS(1~2cm) + IMU + 카메라 기반 경로 추종. IMU가 자율주행 루프의 핵심 입력. predict/update 분리 구조와 동일.

**대학원 연결**: IPMSM 고장 진단 — Ansys Maxwell FEM + MATLAB 코-시뮬레이션에서 전류·진동·자속 신호를 퓨전해 고장 상태 추정. 상태벡터에 고장 파라미터를 포함해 real-time 추정하는 구조가 EKF 바이어스 추정과 동일한 프레임워크.

**IEEE TIM 2024 연결**: "측정값 신뢰도 가중치 + 이상 탐지" = ekf2의 R 행렬 조정과 본질적으로 같은 개념.

---

## 5. 면접 답변 예시

**"GPS 없을 때 드론 위치를 어떻게 추정하나요?"**
> "EKF2_AID_MASK 파라미터로 GPS update를 끄고 optical flow + 초음파 고도계 조합으로 대체합니다. 자세(Roll/Pitch/Yaw)는 IMU + Magnetometer만으로도 추정이 유지됩니다. 수평 위치만 시간이 지날수록 drift가 누적됩니다. SS500에서도 RTK-GPS 불량 시 IMU dead reckoning + 오도메트리로 단기 추정을 했었는데, 드론에서는 Visual Odometry 추가가 표준입니다."

**"EKF2에서 자이로 바이어스를 어떻게 처리하나요?"**
> "바이어스를 상태벡터에 포함합니다. predict()에서 바이어스가 상태 전파에 반영되고, GPS·Magnetometer update() 때 관측 잔차로 바이어스도 보정됩니다. 온도가 변해서 bias가 달라져도 비행 중 자동 교정이 됩니다. 대학원에서 IPMSM 고장 파라미터를 상태벡터에 넣어 실시간 추정한 구조와 동일합니다."
