# ADR-0003: Jetson Nano A02 + Pi 3B+ + MCU

- Status: Accepted 2026-08-26

## Context
The Nano A02 carrier exposes only one CSI connector. The official 7 in touchscreen is a Raspberry Pi DSI device. Two CSI cameras plus that display therefore cannot attach to the Jetson alone. The Pi 3B+ has 1 GB RAM and Ethernet over USB 2.0 capped near 300 Mbps.

## Options
1. Jetson + Pi + MCU - $0, uses owned hardware, three deployment targets.
2. Jetson + MCU only - $50-120 for an HDMI display and second-camera path; spends money to stop using owned parts.
3. Orin Nano Super + Pi HMI + MCU - $249+, 8 GB, two CSI ports, deletes the cross-machine camera problem.

## Decision
Option 1, staged: Jetson plus MCU first, Pi added only when the HMI, telemetry and end-effector camera enter the build.

## Consequences
The Pi is frozen as a thin edge node - HMI, INA226 telemetry, end-effector camera. It must not absorb Nav2, SLAM, detection or desktop visualization. ROS interfaces stay portable so a future Jetson swap does not touch firmware.

## Verification
CMP-001 Jetson 60 min under 80 percent RAM, no swap growth. CMP-002 Pi thin-node budget. CMP-004 detector FPS gate on the Nano.

## Reversal trigger
The Nano fails the perception benchmark after one bounded optimization pass.
