# Architecture Decision Records

Numbered, dated, and never edited after acceptance. To change a decision, add a new ADR that supersedes the old one.

| ADR | Decision | Status | Date |
|---|---|---|---|
| 0001 | Power source: replace pack, >=20 A continuous | Accepted | 2026-08-26 |
| 0002 | Drive stage: parallel TB6612 channels | Accepted | 2026-08-26 |
| 0003 | Compute topology: Jetson + Pi + MCU | Accepted | 2026-08-26 |
| 0004 | ROS baseline: Humble, containerized on Jetson | Accepted | 2026-08-26 |
| 0005 | Middleware: Fast DDS, simple discovery | Accepted | 2026-08-26 |
| 0006 | Network: direct wired link + Jetson M.2 WiFi | Accepted | 2026-08-26 |
| 0007 | Low-level controller: Teensy 4.1 + micro-ROS | Accepted | 2026-08-26 |
| 0008 | Kinematics split: firmware PID, ROS-side IK | Accepted | 2026-08-26 |
| 0009 | IMU: GY-521, vyaw only, SLAM owns heading | Accepted | 2026-08-26 |
| 0010 | Safety: latching hardware e-stop, staged | Accepted | 2026-08-27 |
| 0011 | Bring-up order: math, hardware, then sim | Accepted | 2026-08-27 |

## Reversal recorded

ADR-0007 reverses a decision made earlier the same session. The Arduino Mega 2560 was selected first because it was already owned. It was replaced by the Teensy 4.1 once two constraints were confirmed: micro-ROS does not support the 8-bit AVR, and the Mega has only four usable external-interrupt pins after reserving I2C for the servo driver. The Teensy provides four hardware quadrature decoders instead. The Mega is retained as a 5 V bench tool and fallback controller.

## Open decisions

D11 arm actuator class - D12 servo rail voltage and motion governor - D13 arm control approach - D14 perception scope and camera assignment - D15 detector and Nano FPS gate - D16 SLAM and localization config - D17 ultrasonic integration - D18 HMI scope - D19 mechanical layout - D20 enclosure
