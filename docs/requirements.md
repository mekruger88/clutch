# Requirements and Verification Matrix

Every claim in this repository must trace to a requirement, a test, and an evidence artifact. Status remains **NOT VERIFIED** until the artifact is committed and linked here.

## System

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| SYS-001 | The robot shall complete the defined indoor autonomous detect -> drive -> grasp demonstration. | Portfolio mission. | Acceptance test | Success rate reported over >=30 trials. | SYS-TEST-001 | NOT VERIFIED | — |
| SYS-002 | The robot shall operate untethered during the demonstration. | Demonstration credibility. | Inspection/test | No data or power cable connected during mission. | SYS-TEST-001 | NOT VERIFIED | — |
| SYS-003 | The robot shall retain a public, reproducible record of decisions, tests, and results. | Portfolio evidence. | Inspection | README, ADRs, requirements and evidence links resolve. | DOC-001 | NOT VERIFIED | — |

## Base and odometry

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| BASE-001 | The base shall independently command vx, vy and yaw rate. | Holonomic mission mobility. | Test | Correct visible motion and encoder sign for pure vx, vy and yaw. | KIN-003 | NOT VERIFIED | — |
| BASE-002 | The firmware shall control four wheel velocities in closed loop. | Reject load variation. | Test | Steady-state error <5% at 25%, 50% and 100% command. | KIN-005 | NOT VERIFIED | — |
| BASE-003 | The base shall stop wheel power on a detected encoder stall. | Protect DRV8871 breakouts from sustained chop thermal overload (ADR-0012). | Test | PWM cut within 250 ms. | CTL-004b | NOT VERIFIED | — |
| BASE-004 | The robot shall publish wheel odometry with separately measured error for straight, strafe and rotation. | Mecanum slip is anisotropic. | Measurement | Five trials per motion type, mean and spread recorded. | KIN-004 | NOT VERIFIED | — |
| BASE-005 | Mecanum IK/FK library shall pass randomized round-trip and sign/saturation checks before hardware motion. | Decouple math bugs from wiring bugs (ADR-0008, ADR-0011). | Unit test | 10,000 randomized round trips, sign patterns, and saturation tests pass. | KIN-001 | NOT VERIFIED | — |
| BASE-006 | Chassis geometry (wheel radius, lx, ly) and empirical encoder CPR shall be measured before closed-loop tuning. | Prevent listing-spec errors in odometry (ADR-0008). | Measurement | Empirical CPR within 0.5% across 3x 10-turn trials; geometry recorded with tolerances. | KIN-002 | NOT VERIFIED | — |

## Power

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| PWR-001 | Mission battery shall be 3S, >=10 Ah, >=20 A stated continuous, <=13.5 V fully charged. | 12 V drive motor nominal envelope and mission current headroom (ADR-0001, ADR-0012). | Inspection | All label and datasheet fields verified. | PWR-001 | NOT VERIFIED | — |
| PWR-002 | Battery shall sustain provisional bench load safely. | Validate pack before robot use. | Test | 5 A for 5 min; >10.5 V; connector rise <20 C. | PWR-002 | NOT VERIFIED | — |
| PWR-003 | Bare base shall remain within its validated battery envelope. | Avoid BMS trip. | Test | Peak <5.5 A; sustained <4.8 A; no trip in 20 reversals. | PWR-003 | NOT VERIFIED | — |
| PWR-004 | Compute input shall remain above its validated minimum under load. | Avoid brownout. | Measurement | Jetson >=4.75 V at input; final threshold measured at load. | PWR-004 | NOT VERIFIED | — |
| PWR-007 | DRV8871 breakouts shall pass physical silicon and RILIM inspection before wiring. | Suspect marketplace listing (ADR-0012). | Inspection/DMM | 5 boards present; DRV8871 top mark confirmed; RILIM = 30 kOhm +/-5%. | PWR-007 (PWR-07) | NOT VERIFIED | — |
| PWR-008 | Single DRV8871 board shall regulate locked-rotor current without thermal fault. | Verify hardware current chop (ADR-0012). | Test | 13.5 V, 5 s locked rotor: current plateaus 1.87-2.42 A, no reset, surface <=80 C. | PWR-008 (PWR-08) | NOT VERIFIED | — |
| PWR-009 | Four DRV8871 boards shall remain thermally bounded under continuous holonomic driving. | Breakout lacks via-stitched PowerPAD plane (ADR-0012). | Test | 60 s strafe-and-rotate loop: hottest driver <=70 C, zero UVLO/OCP/TSD faults. | PWR-009 (PWR-09) | NOT VERIFIED | — |
| PWR-010 | Drive motor no-load and stall current at 13.5 V shall match the DRV8871 design envelope. | Hobby motor stall rating is unverified (ADR-0012). | Measurement | Two motors at 13.5 V: no-load <=0.5 A, stall within 20% of 3.15 A (<=3.4 A reversal trigger). | PWR-010 (PWR-10) | NOT VERIFIED | — |

## Safety

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| SAFE-001 | A physical latching e-stop shall remove drive actuator power independently of Linux, ROS or WiFi. | Category-0 stop. | Test | Drive power removed <100 ms, 20 repetitions. | SAFE-001 | NOT VERIFIED | — |
| SAFE-002 | E-stop reset shall not restart motion, and relay coil loss shall fail open without contact welding. | Prevent stale-command restart and fail-closed faults (ADR-0010). | Test | Explicit enable required after reset; fail-open on coil loss; 50 DC interruptions without welding. | SAFE-001 / SAFE-002 / SAFE-003 | NOT VERIFIED | — |
| SAFE-003 | Compute and telemetry shall remain powered during an actuator e-stop. | Preserve diagnostics. | Test | INA226 log contains stop event; cold preflight execution passes. | SAFE-001 / SAFE-005 | NOT VERIFIED | — |
| SAFE-004 | Loss of valid wheel command shall stop the base. | Communication fault safety. | Test | PWM ramps to zero <500 ms. | CTL-002 | NOT VERIFIED | — |
| SAFE-005 | Battery undervoltage shall warn and inhibit new goals before BMS cutoff. | Avoid sudden BMS cutoff. | Test | Warn/refuse at 10.5 V; stop at 9.9 V. | SAFE-004 | NOT VERIFIED | — |

## Control and sensing

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| CTL-001 | No Teensy GPIO shall receive a signal above 3.3 V. | Teensy 4.1 is not 5 V tolerant. | Measurement | Encoder and IMU signals <=3.3 V. | CTL-000 / IMU-001 | NOT VERIFIED | — |
| CTL-002 | Invalid or absent host communication shall not create motion. | Micro-ROS agent/USB fault safety. | Test | No motion; watchdog stop <500 ms. | CTL-002 | NOT VERIFIED | — |
| CTL-003 | Teensy encoder measurement shall remain reliable at max command speed, and micro-ROS command latency shall stay bounded under load. | Odometry and control loop integrity (ADR-0007). | Test | No count loss over 10 min; command round-trip p99 <50 ms under perception load. | CTL-003 / CTL-004a | NOT VERIFIED | — |
| CTL-004 | Low-level controller shall boot with outputs inhibited. | Safe startup. | Test | Explicit enable required after ten power cycles. | CTL-002 | NOT VERIFIED | — |
| CTL-005 | DRV8871 IN1/IN2 dual-PWM output stage shall produce a monotonic velocity response. | Fixed 25 us t_OFF alters effective PWM frequency (ADR-0012). | Test | 0-100% duty sweep at 5-10 kHz: monotonic rad/s, dead zone <=8% duty. | CTL-005 (CTL-05) | NOT VERIFIED | — |
| CTL-006 | Per-wheel velocity PID shall include anti-windup and recover cleanly after DRV8871 current chop. | Chopping wheel cannot track setpoint and winds up integrator (ADR-0012). | Test | 0.3 m/s step settles <=400 ms, overshoot <=15%, integrator recovers <=200 ms after stall release. | CTL-006 (CTL-06) | NOT VERIFIED | — |
| IMU-001 | IMU yaw-rate bias shall be calibrated at boot while stationary. | MPU-6050 zero-rate offset. | Test | Drift <2 deg/min after zeroing. | IMU-002 | NOT VERIFIED | — |
| IMU-002 | IMU fusion shall validate scale/vibration immunity and measurably improve navigation estimate or be disabled. | Avoid complexity without value (ADR-0009). | Comparative test | 360 deg turn within 2% (IMU-003); motor-on bias shift <1 deg/s (IMU-004); EKF-on vs wheel-only recorded (IMU-005). | IMU-003 / IMU-004 / IMU-005 | NOT VERIFIED | — |

## Compute, environment, and network

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| CMP-001 | Compute nodes shall remain within memory, thermal, and detector FPS budgets. | Prevent swap thrashing on 4 GB Nano and 1 GB Pi 3B+ (ADR-0003). | Test | Jetson <80% RAM over 60 min with zero swap growth; Pi within thin-node budget; Nano passes detector FPS gate. | CMP-001 / CMP-002 / CMP-004 | NOT VERIFIED | — |
| ENV-001 | Jetson ROS 2 Humble container shall build reproducibly with GPU and sensor access. | L4T R32.7.1 ceiling requires containerized Humble (ADR-0004). | Test | Builds cleanly from Dockerfile; GPU visible for 30 min under tegrastats; CSI and LiDAR log to MCAP for 30 min. | ENV-001 / ENV-002 / ENV-003 | NOT VERIFIED | — |
| NET-001 | Direct Cat6 data plane and Fast DDS simple discovery shall stay isolated from WiFi. | Prevent multicast spillover onto wlan0 (ADR-0005, ADR-0006). | Test | Zero-loss ping/30 min motion link; discovery <10 s (20 starts); p99 <50 ms; traffic <30% link capacity; WiFi drop changes nothing. | LINK-001..004 / NET-001..004 | NOT VERIFIED | — |

## Verification rule

A test record goes under `docs/verification/TEST-<ID>.md`; data, clips, plots and bags are referenced through `data_manifest/manifest.csv`. A requirement is not verified merely because code exists or a test was attempted.
