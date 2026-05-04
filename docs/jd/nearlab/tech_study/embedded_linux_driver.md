# Embedded Linux 드라이버 기초 — 면접 핵심 (R7 갭 보강)

> 출처: Linux Kernel Documentation (kernel.org) · Linux Device Drivers 3rd Ed. (O'Reilly) · i2c-dev.h · spidev.h
> 황인혁 경험 연결: STM32 HAL SPI/I2C 드라이버 · NI-DAQ 계측 · SS500 CAN/SPI 페리퍼럴

---

## 1. Character Device Driver 핵심 구조

```c
static struct file_operations my_fops = {
    .owner          = THIS_MODULE,
    .open           = my_open,
    .release        = my_release,
    .read           = my_read,       // 센서 데이터 읽기
    .write          = my_write,      // 명령 전송
    .unlocked_ioctl = my_ioctl,      // 설정 변경 (ODR, 풀스케일 등)
};
```

**등록 순서**: `alloc_chrdev_region()` → `cdev_init()` → `cdev_add()` → `class_create()` → `device_create()`

- `ioctl`: 드론 IMU 드라이버에서 `IOCTL_SET_ODR`, `IOCTL_READ_FIFO` 등으로 userspace에서 센서 제어.
- `copy_to_user()` / `copy_from_user()`: 커널-유저 메모리 경계 안전 복사. **생략하면 kernel oops**.
- IRQ 기반 read: `wait_queue_head_t` + `wake_up_interruptible()`. data-ready IRQ → wake, userspace read() → block.

**STM32 HAL 연결**: `HAL_SPI_TransmitReceive_DMA()` = Linux `spi_sync()` + DMA의 HAL 래퍼. 추상화 레이어만 다름.

---

## 2. Device Tree — 하드웨어 기술 분리

```dts
/* ICM-42688 IMU 예시 DTS 노드 */
&spi1 {
    icm42688: imu@0 {
        compatible = "invensense,icm42688";
        reg = <0>;                          /* CS0 */
        spi-max-frequency = <10000000>;     /* 10MHz */
        interrupt-parent = <&gpio1>;
        interrupts = <5 IRQ_TYPE_EDGE_RISING>;
    };
};
```

- `compatible` 문자열이 드라이버의 `of_device_id` 테이블과 매칭 → `probe()` 자동 호출.
- **왜 DTS인가**: 보드별 HW 정보(핀 번호, 주소, 클럭)를 커널 코드에서 분리 → 동일 드라이버로 다른 보드 지원.
- sysfs: `/sys/bus/iio/devices/iio:device0/in_anglvel_x_raw` — `cat`으로 raw 값 디버깅 가능.

---

## 3. I2C/SPI: Userspace API vs 커널 드라이버

| 항목 | Userspace (i2c-dev, spidev) | 커널 드라이버 |
|------|----------------------------|-------------|
| 접근 | `/dev/i2c-N`, `/dev/spidevX.Y` | `probe()`, `spi_sync()`, `i2c_transfer()` |
| 레이턴시 | syscall overhead (수~수십 μs) | 더 낮음 (IRQ·DMA 직접) |
| 실시간 보장 | 어려움 | 가능 (PREEMPT_RT 조합) |
| 개발 속도 | 빠름 (Python/C) | 느림 (커널 빌드) |
| 드론 사용처 | 프로토타입, 레지스터 초기화 | 고속 IMU (4kHz+), 실시간 루프 |

```c
/* i2c-dev userspace 예시 */
int fd = open("/dev/i2c-1", O_RDWR);
ioctl(fd, I2C_SLAVE, 0x68);   // ICM-42688 I2C 주소
write(fd, &reg, 1);
read(fd, data, 6);
```

---

## 4. 드론 보드 센서 드라이버 패턴

| 센서 | 인터페이스 | PX4 드라이버 위치 | 핵심 패턴 |
|------|----------|-----------------|---------|
| ICM-42688 IMU | SPI 10~24MHz | `src/drivers/imu/invensense/icm42688p/` | FIFO burst read + DMA + data-ready IRQ |
| MS5611 Baro | I2C 400kHz | `src/drivers/barometer/ms5611/` | 변환 명령 → 9ms 대기(타이머) → ADC read |
| u-blox GPS | UART 115200 | `src/drivers/gps/` | UBX 이진 프로토콜 파서 + serdev |
| 공통 패턴 | — | — | `probe()` → 칩 ID 확인 → 초기화 → IRQ 등록 → IIO 등록 |

---

## 5. 황인혁 경험 연결

**STM32 HAL → Linux 커널 서브시스템 1:1 대응**:

| STM32 HAL | Linux 커널 |
|-----------|----------|
| `HAL_SPI_TransmitReceive_DMA()` | `spi_sync()` + DMA 설정 |
| `HAL_I2C_Master_Transmit()` | `i2c_transfer()` |
| CAN HAL_CAN_RxFifo0MsgPending | SocketCAN `can0` + `candump` |
| GPIO IRQ 핸들러 | `request_irq()` + handler |

**NI-DAQ 연결**: SS500 다이나모미터에서 NI-DAQ Linux 드라이버(comedi)를 통해 `/dev/comedi0`로 데이터 스트림. character device read() 패턴을 이미 사용자로서 경험.

---

## 6. 면접 답변 예시

**"ARM 임베디드 리눅스에서 드라이버 작성 경험이 있나요?"**
> "커널 드라이버 직접 작성 경험은 없습니다. 다만 STM32 HAL에서 SPI DMA, I2C, CAN 페리퍼럴 드라이버를 직접 구현했고, NI-DAQ 기반 계측 시스템을 comedi 드라이버(/dev/comedi0)를 통해 운용했습니다. Linux 커널 드라이버는 같은 HW 추상화 원칙을 커널 레이어에서 구현한 것이라 구조 전이 비용이 낮습니다. 현재 i2c-dev API와 IIO 서브시스템 예제를 진행 중입니다."

**"sysfs와 Device Tree의 역할을 설명해보세요."**
> "Device Tree는 보드별 HW 정보(핀, 주소, 클럭)를 커널 코드에서 분리하는 메커니즘입니다. compatible 문자열로 드라이버와 매칭되면 probe()가 자동 호출됩니다. sysfs는 드라이버가 /sys 경로에 속성을 노출하는 인터페이스로, 디버깅 시 cat으로 IMU raw 값을 실시간 확인할 수 있습니다. SS500에서 CAN DBC로 노드별 데이터를 구조화한 것과 비슷한 '인터페이스 명시적 정의' 원칙입니다."
