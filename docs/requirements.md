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
| BASE-003 | The base shall stop wheel power on a detected encoder stall. | Protect TB6612 drivers. | Test | PWM cut within 250 ms. | CTL-004 | NOT VERIFIED | — |
| BASE-004 | The robot shall publish wheel odometry with separately measured error for straight, strafe and rotation. | Mecanum slip is anisotropic. | Measurement | Five trials per motion type, mean and spread recorded. | KIN-004 | NOT VERIFIED | — |

## Power

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| PWR-001 | Mission battery shall be 3S, >=10 Ah, >=20 A stated continuous, <=13.5 V fully charged. | TB6612 supply limit and mission headroom. | Inspection | All label and datasheet fields verified. | PWR-001 | NOT VERIFIED | — |
| PWR-002 | Battery shall sustain provisional bench load safely. | Validate pack before robot use. | Test | 5 A for 5 min; >10.5 V; connector rise <20 C. | PWR-002 | NOT VERIFIED | — |
| PWR-003 | Bare base shall remain within its validated battery envelope. | Avoid BMS trip. | Test | Peak <5.5 A; sustained <4.8 A; no trip in 20 reversals. | PWR-003 | NOT VERIFIED | — |
| PWR-004 | Compute input shall remain above its validated minimum under load. | Avoid brownout. | Measurement | Jetson >=4.75 V at input; final threshold measured at load. | PWR-003 | NOT VERIFIED | — |

## Safety

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| SAFE-001 | A physical latching e-stop shall remove drive actuator power independently of Linux, ROS or WiFi. | Category-0 stop. | Test | Drive power removed <100 ms, 20 repetitions. | SAFE-001 | NOT VERIFIED | — |
| SAFE-002 | E-stop reset shall not restart motion. | Prevent stale-command restart. | Test | Explicit enable required after every reset. | SAFE-001 | NOT VERIFIED | — |
| SAFE-003 | Compute and telemetry shall remain powered during an actuator e-stop. | Preserve diagnostics. | Test | INA226 log contains stop event. | SAFE-001 | NOT VERIFIED | — |
| SAFE-004 | Loss of valid wheel command shall stop the base. | Communication fault safety. | Test | PWM ramps to zero <500 ms. | CTL-002 | NOT VERIFIED | — |
| SAFE-005 | Battery undervoltage shall warn and inhibit new goals before BMS cutoff. | Avoid sudden BMS cutoff. | Test | Warn/refuse at 10.5 V; stop at 9.9 V. | SAFE-004 | NOT VERIFIED | — |

## Control and sensing

| ID | Requirement | Rationale | Verification | Threshold | Test | Status | Evidence |
|---|---|---|---|---|---|---|---|
| CTL-001 | No Teensy GPIO shall receive a signal above 3.3 V. | Teensy 4.1 is not 5 V tolerant. | Measurement | Encoder and IMU signals <=3.3 V. | CTL-000 / IMU-001 | NOT VERIFIED | — |
| CTL-002 | Invalid or absent host communication shall not create motion. | Micro-ROS agent/USB fault safety. | Test | No motion; watchdog stop <500 ms. | CTL-002 | NOT VERIFIED | — |
| CTL-003 | Teensy encoder measurement shall remain reliable at max command speed. | Odometry integrity. | Test | No count loss against reference over 10 min. | CTL-004 | NOT VERIFIED | — |
| CTL-004 | Low-level controller shall boot with outputs inhibited. | Safe startup. | Test | Explicit enable required after ten power cycles. | CTL-002 | NOT VERIFIED | — |
| IMU-001 | IMU yaw-rate bias shall be calibrated at boot while stationary. | MPU-6050 zero-rate offset. | Test | Drift <2 deg/min after zeroing. | IMU-002 | NOT VERIFIED | — |
| IMU-002 | IMU fusion shall measurably improve navigation estimate or be disabled. | Avoid complexity without value. | Comparative test | EKF-on versus wheel-only results recorded. | IMU-005 | NOT VERIFIED | — |

## Verification rule

A test record goes under `docs/verification/TEST-<ID>.md`; data, clips, plots and bags are referenced through `data_manifest/manifest.csv`. A requirement is not verified merely because code exists or a test was attempted.
