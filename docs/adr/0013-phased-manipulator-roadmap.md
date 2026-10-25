# ADR-0013: Phased manipulator roadmap

- Status: Accepted 2026-10-25
- Resolves: D11 arm actuator class, per phase
- Leaves open: D12 servo rail voltage and motion governor, D13 arm control approach
- Supersedes: none. Replaces the "custom 3D-printed six-axis arm" description in README.md, docs/index.md and mkdocs.yml, which was never an accepted decision.

## Context
The repository described the arm as a custom 3D-printed six-axis MG996R arm, but no ADR accepted that, and D11-D13 stayed open. The project goal for bring-up is to prove professional integration on hardware already owned before spending more.

Owned arm hardware:

- RobotGeek Snapper: four joint hobby PWM servos (base, shoulder, elbow, wrist) plus a parallel gripper servo.
- PCA9685 16-channel PWM driver (logic 3.3 V capable).
- 8x MG996R servos (catalog and manufacturer specs disagree; unverified).
- FEICHAO 8 A UBEC for the servo rail.

Target arm: SO-ARM101 follower in the 12 V configuration, which uses six Feetech STS3215 12 V serial bus servos. These are half-duplex serial bus servos, not PWM servos, and are normally driven through a serial bus servo driver board whose input range is about 9-12.6 V and must match the servo voltage.

Two constraints follow:

1. Phases built on PWM servos share the PCA9685 and the PWM servo rail. The SO-ARM101 does not. Nothing on the PWM signal path carries forward to the bus-servo arm.
2. ADR-0001 allows a pack up to 13.5 V fully charged. A 12.6 V maximum at the bus-servo driver leaves no margin for any pack that charges above 12.6 V.

## Options
1. **Build the custom MG996R arm directly** (the old README description). Uses owned servos, but requires mechanical design, printing and tuning before the first ROS-controlled grasp, on servos whose specs are unverified.
2. **Buy the SO-ARM101 now.** Best path to LeRobot and the strongest end state, but spends money and adds a 12 V branch and a bus-servo interface before the base has passed baseline exit.
3. **Phased.** Phase A Snapper, optional Phase B custom MG996R arm, Phase C SO-ARM101. Owned hardware first; the ROS-facing arm boundary stays fixed while the actuator behind it changes.

## Decision
Option 3. Phases are entered on evidence, not dates.

- **Phase A - RobotGeek Snapper.** Four joint servos and the gripper servo on PCA9685 channels. The PCA9685 sits on a Teensy I2C bus separate from the IMU bus (ADR-0009). PCA9685 VCC is 3.3 V from the Teensy side; servo V+ comes from the UBEC on its own fused branch that the e-stop removes (ADR-0010 stage 2). The original Snapper controller is retired from the signal path so the Teensy stays the single low-level controller (ADR-0007).
- **Phase B - custom 3D-printed MG996R arm, optional.** Same PCA9685 and rail. Entered only if Phase A shows a specific, measured limitation that a custom arm fixes and the SO-ARM101 is not yet justified. Requires its own ADR covering geometry and MG996R verification.
- **Phase C - SO-ARM101 12 V follower.** Requires its own ADR before purchase, deciding the bus-servo interface (host-side USB bus driver versus Teensy UART) and the 12 V servo branch.

Locked across every phase:

- Arm hardware sits behind a single ROS 2 hardware-interface boundary, so a phase change does not touch perception, planning or the base. The control approach behind that boundary is D13 and is not decided here.
- Arm actuator power is removed by the hardware e-stop in every phase.
- Arm power never shares a regulator with compute or Teensy logic.

## Consequences
- The Snapper is four joints plus a gripper, not six axes. Without wrist roll, Phase A grasps are limited to poses reachable with base yaw and a planar shoulder-elbow-wrist chain. The SYS-001 demonstration object and pose must be defined against Phase A reach.
- Hobby PWM servos report no position or load. In Phases A and B the arm state is commanded, not measured; grasp success must be confirmed by the camera or by servo-rail current on the INA226. Phase C bus servos report position and load, which is a real capability gain.
- PCA9685 outputs can glitch at power-up. The OE pin is held high (outputs disabled) until the Teensy completes its enable handshake, matching the inhibited-on-boot rule in CTL-004.
- The PCA9685 and PWM servo rail are discarded at Phase C. Acceptable, because both are owned.
- The Category-0 arm-drop hazard in docs/safety/hazard_analysis.md applies in every phase.
- Phase C cannot run directly from a pack that charges above 12.6 V. Either the measured fully charged pack voltage is at or below 12.6 V, or a regulated 12 V servo branch is added.
- D12 stays open. The Snapper servo case labels are unread, and the UBEC jumper options need confirming: the BOM lists 5 V/6 V, while a pre-restart plan (2026-08-20) used a 7 V jumper.

## Verification
Phase A gates, before any arm servo is powered from the robot:

- **ARM-001** Servo identification. Read the case label on all five Snapper servos; record model and rated voltage. Pass: the D12 rail voltage is at or below the lowest rated maximum of any servo on the rail.
- **ARM-002** Rail isolation. With the servo rail powered and the Teensy unpowered, Teensy 3V3 and PCA9685 VCC read below 0.1 V. With everything powered, SDA and SCL idle at or below 3.3 V. Pass: both.
- **ARM-003** Power-up inhibit. Ten power cycles with OE held high by its pull-up. Pass: zero servo motion until the explicit enable.
- **ARM-004** Rail under load. INA226 on the servo rail; stall one joint for 1 s at a time (shoulder first), then move all joints together. Pass: peak current below the UBEC continuous rating (8 A per BOM), rail droop under 10 percent, no Teensy or Jetson reset, no UBEC shutdown.
- **ARM-005** E-stop extension (ADR-0010 stage 2). Pass: the mushroom removes servo rail power in under 100 ms across 20 repetitions; releasing it does not move the arm; the unloaded drop is recorded on video.

Phase C entry gate:

- **ARM-010** Measured fully charged pack voltage at the servo branch is at or below 12.6 V, or a regulated 12 V branch is specified and bench-verified.

## Reversal trigger
- ARM-004 fails at every allowed rail voltage, or the Snapper cannot perform the defined SYS-001 grasp: skip Phase B and go to Phase C through a new ADR.
- The SO-ARM101 becomes unavailable, or a safe 12 V branch cannot be built on the ADR-0001 pack: Phase B becomes the end-state arm through a new ADR.

## Not decided here
- D12 servo rail voltage (gated by ARM-001).
- D13 arm control approach.
- D14 camera assignment and the Traxxas main-connector decision, which belong in separate records.

## Sources
- TheRobotStudio SO-ARM100/101 repository (STS3215 7.4 V and 12 V variants): https://github.com/TheRobotStudio/SO-ARM100
- Waveshare SO-ARM100/101 setup wiki: https://www.waveshare.com/wiki/SO-ARM100/101_Set_Servo_ID
- Seeed Studio SO-ARM course, bus servo supply must match servo type: https://wiki.seeedstudio.com/robotics/soarm_physical_ai_course_chapter_4/
- Waveshare Serial Bus Servo Driver Board listing: https://eckstein-shop.de/WaveShare-Serial-Bus-Servo-Driver-Board-for-ST-SC-Serial-Bus-Servos-EN
