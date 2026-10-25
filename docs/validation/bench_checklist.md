# Baseline Bench Checklist

Canonical implementation order for the first exit criterion: wheels turning under ROS 2 with validated odometry, verified power rail, e-stop authority and watchdog authority. Numbers are identifiers, not a substitute for this dependency order.

## Blocking order

1. **CTL-000 precedes the Teensy purchase.** A 5 V encoder signal can destroy a Teensy 4.1.
2. **PWR-007 precedes wiring any DRV8871 board (ADR-0012).**
3. **SAFE-001 on a dummy load precedes any motor energizing, including bench-supply motor tests.**
4. **PWR-001 and PWR-002 precede battery connection to electronics.**
5. **PWR-010 precedes PWR-008 and any wheel spin on a DRV8871.** A measured stall above 3.4 A stops work and triggers the ADR-0012 reversal.
6. **IMU-001 precedes connecting the GY-521 to the Teensy.**
7. **KIN-001 precedes any wheel spin.**
8. **PWR-008, CTL-005, and CTL-006 precede floor driving.**
9. **PWR-003 and PWR-009 precede extended floor driving.**

## Ordered tasks

| Order | ID | Task | Pass criterion | Evidence |
|---:|---|---|---|---|
| 1 | CTL-000 | Power one encoder from its intended supply; rotate by hand; measure A/B high levels and determine push-pull versus open collector. | Every eventual Teensy input <=3.3 V, or a documented level-shifter design exists. | Photo, voltage table, scope trace if available. |
| 2 | PWR-007 (PWR-07) | Inspect DRV8871 breakouts under magnification and measure RILIM with a DMM. | 5 boards present; DRV8871 top mark confirmed; RILIM measures 30 kOhm +/-5%. | Macro photo, DMM table. |
| 3 | PWR-001 | Inspect new battery label, chemistry, polarity, charger and continuous/pulse discharge ratings. | 3S; >=10 Ah; >=20 A stated continuous; <=13.5 V full charge. | Label photos, datasheet link. |
| 4 | SAFE-001 | Build master fuse, DC-rated disconnect, relay coil and latching mushroom circuit using a dummy load. | Actuator feed opens <100 ms, 20 times; reset never restarts; telemetry stays powered. | Wiring diagram, video, current log. |
| 5 | PWR-002 | Bench-load battery in 1 A increments to 5 A. | Sustains 5 A for 5 min; >10.5 V; connector rise <20 C; no BMS interruption. | CSV, temperature record. |
| 6 | SAFE-004 | Bench-discharge into resistive load to verify INA226 software LVC thresholds (ADR-0010). | Warn and refuse new goals at 10.5 V; auto-stop at 9.9 V before BMS cutoff. | INA226 CSV, log output. |
| 7 | PWR-004 | Verify regulators at no load and target load, measured at each device input. | Jetson input >=4.75 V; no abnormal heating or ripple observed. | Voltage table, photos. |
| 8 | PWR-010 (PWR-10) | Behind the SAFE-001 circuit, on a current-limited supply at 13.5 V, measure no-load and locked-rotor stall current on two drive motors. | No-load <=0.5 A; measured stall within 20% of 3.15 A (if >3.4 A, trigger ADR-0012 reversal). | DMM/clamp log, photo. |
| 9 | PWR-008 (PWR-08) | Single DRV8871 board, one wheel motor at 13.5 V, locked rotor for 5 s. | Current plateaus 1.87-2.42 A; no reset; board surface <=80 C. | Current trace, thermal photo. |
| 10 | ENV-001 | Reproduce Jetson ROS image from committed files. | Build without manual in-container changes; versions and digest recorded. | Build log, image digest. |
| 11 | ENV-002 | Verify GPU access in container under 30 min load. | GPU visible; no crash or throttle. | tegrastats log. |
| 12 | IMU-001 | Power GY-521 at 3.3 V; read WHO_AM_I; measure I2C idle high. | Correct identity; SDA/SCL <=3.3 V. | I2C output, voltage table. |
| 13 | KIN-001 | Run ROS-free IK/FK library tests before hardware. | 10,000 randomized round trips pass; signs and saturation tests pass. | CI output. |
| 14 | CTL-005 (CTL-05) | Wheels off ground: open-loop IN1/IN2 duty sweep 0-100% at 5-10 kHz PWM. | Monotonic wheel rad/s; dead zone <=8% duty. | Sweep CSV, plot. |
| 15 | CTL-004a / CTL-004b | Hardware encoder counter test at max speed (10 min) and deliberate encoder-stall timeout check. | Zero count loss over 10 min; PWM cut within 250 ms of stalled encoder counts. | CSV, method, scope/log capture. |
| 16 | KIN-002 | Measure wheel radius, lx, ly; determine encoder CPR by 10 marked rotations, three trials. | CPR agreement within 0.5%; dimensions recorded with instrument/tolerance. | Measurement sheet. |
| 17 | KIN-003 | Wheels off ground: verify direction and encoder signs; then demonstrate pure vx, vy and yaw on floor. | All signs correct; each pure command gives expected motion. | Video, table. |
| 18 | KIN-005 / CTL-006 | Tune per-wheel velocity PID with anti-windup (ADR-0012 CTL-06). | Settles <=300-400 ms; steady error <5% at 25/50/100%; overshoot <=15%; integrator recovers <=200 ms after stall release. | Plots, gains file. |
| 19 | PWR-003 / PWR-009 | Twenty floor reversals plus 60 s continuous strafe-and-rotate thermal loop (ADR-0012 PWR-09). | Peak <5.5 A; sustained <4.8 A; hottest DRV8871 <=70 C; zero UVLO/OCP/TSD faults; Jetson >=4.75 V. | INA226 CSV, thermal log, video. |
| 20 | CTL-002 | Kill host, unplug USB, then interrupt WiFi during commanded motion. | PWM ramps to zero <500 ms in each case; explicit re-enable required. | Video, diagnostics log. |
| 21 | KIN-004 | Run five tape-measured trials each: 5 m straight, 5 m strafe, 360 deg turn. | Mean and spread reported separately; covariance updated from results. | CSV, analysis plot. |
| 22 | IMU-002 | Stationary 10 min after boot bias calibration. | Integrated yaw drift <2 deg/min; residual bias stable within 0.5 deg/s. | MCAP, plot. |
| 23 | IMU-003 | Ten marked 360 deg turns. | Integrated yaw within 2%; correct sign; spread <1%. | CSV, calibration result. |
| 24 | IMU-004 | Four motors running with robot held stationary. | Bias shift <1 deg/s versus quiet baseline. | MCAP, plot. |
| 25 | IMU-005 | Five 5 m square paths with EKF on and wheel-only. | Both errors reported; EKF retained only if it measurably improves estimate. | Overlay plot, config choice. |

## Baseline exit

Do not call the base complete until KIN-004, PWR-003, PWR-009, SAFE-001 and CTL-002 have passed and their evidence is committed. Capture 10-30 seconds of video before closing every motion, measurement or failure item.
