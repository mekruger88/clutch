# Baseline Bench Checklist

Canonical implementation order for the first exit criterion: wheels turning under ROS 2 with validated odometry, verified power rail, e-stop authority and watchdog authority. Numbers are identifiers, not a substitute for this dependency order.

## Blocking order

1. **CTL-000 precedes the Teensy purchase.** A 5 V encoder signal can destroy a Teensy 4.1.
2. **SAFE-001 on a dummy load precedes any motor energizing.**
3. **PWR-001 and PWR-002 precede battery connection to electronics.**
4. **IMU-001 precedes connecting the GY-521 to the Teensy.**
5. **KIN-001 precedes any wheel spin.**
6. **PWR-003 precedes extended floor driving.**

## Ordered tasks

| Order | ID | Task | Pass criterion | Evidence |
|---:|---|---|---|---|
| 1 | CTL-000 | Power one encoder from its intended supply; rotate by hand; measure A/B high levels and determine push-pull versus open collector. | Every eventual Teensy input <=3.3 V, or a documented level-shifter design exists. | Photo, voltage table, scope trace if available. |
| 2 | PWR-001 | Inspect new battery label, chemistry, polarity, charger and continuous/pulse discharge ratings. | 3S; >=10 Ah; >=20 A stated continuous; <=13.5 V full charge. | Label photos, datasheet link. |
| 3 | SAFE-001 | Build master fuse, DC-rated disconnect, relay coil and latching mushroom circuit using a dummy load. | Actuator feed opens <100 ms, 20 times; reset never restarts; telemetry stays powered. | Wiring diagram, video, current log. |
| 4 | PWR-002 | Bench-load battery in 1 A increments to 5 A. | Sustains 5 A for 5 min; >10.5 V; connector rise <20 C; no BMS interruption. | CSV, temperature record. |
| 5 | PWR-004 | Verify regulators at no load and target load, measured at each device input. | Jetson input >=4.75 V; no abnormal heating or ripple observed. | Voltage table, photos. |
| 6 | ENV-001 | Reproduce Jetson ROS image from committed files. | Build without manual in-container changes; versions and digest recorded. | Build log, image digest. |
| 7 | ENV-002 | Verify GPU access in container under 30 min load. | GPU visible; no crash or throttle. | tegrastats log. |
| 8 | IMU-001 | Power GY-521 at 3.3 V; read WHO_AM_I; measure I2C idle high. | Correct identity; SDA/SCL <=3.3 V. | I2C output, voltage table. |
| 9 | KIN-001 | Run ROS-free IK/FK library tests before hardware. | 10,000 randomized round trips pass; signs and saturation tests pass. | CI output. |
| 10 | CTL-004 | Hardware encoder counter test at max command speed. | No count loss versus reference over 10 min. | CSV and method. |
| 11 | KIN-002 | Measure wheel radius, lx, ly; determine encoder CPR by 10 marked rotations, three trials. | CPR agreement within 0.5%; dimensions recorded with instrument/tolerance. | Measurement sheet. |
| 12 | KIN-003 | Wheels off ground: verify direction and encoder signs; then demonstrate pure vx, vy and yaw on floor. | All signs correct; each pure command gives expected motion. | Video, table. |
| 13 | KIN-005 | Tune per-wheel velocity PID. | Settles <300 ms; steady error <5% at 25/50/100%; no sustained oscillation. | Plots, gains file. |
| 14 | PWR-003 | Twenty floor accelerations/reversals including strafing. | Peak <5.5 A; sustained <4.8 A; no BMS trip; Jetson input >=4.75 V. | INA226 CSV, video. |
| 15 | CTL-002 | Kill host, unplug USB, then interrupt WiFi during commanded motion. | PWM ramps to zero <500 ms in each case; explicit re-enable required. | Video, diagnostics log. |
| 16 | KIN-004 | Run five tape-measured trials each: 5 m straight, 5 m strafe, 360 deg turn. | Mean and spread reported separately; covariance updated from results. | CSV, analysis plot. |
| 17 | IMU-002 | Stationary 10 min after boot bias calibration. | Integrated yaw drift <2 deg/min; residual bias stable within 0.5 deg/s. | MCAP, plot. |
| 18 | IMU-003 | Ten marked 360 deg turns. | Integrated yaw within 2%; correct sign; spread <1%. | CSV, calibration result. |
| 19 | IMU-004 | Four motors running with robot held stationary. | Bias shift <1 deg/s versus quiet baseline. | MCAP, plot. |
| 20 | IMU-005 | Five 5 m square paths with EKF on and wheel-only. | Both errors reported; EKF retained only if it measurably improves estimate. | Overlay plot, config choice. |

## Baseline exit

Do not call the base complete until KIN-004, PWR-003, SAFE-001 and CTL-002 have passed and their evidence is committed. Capture 10-30 seconds of video before closing every motion, measurement or failure item.
