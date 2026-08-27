# Clutch

ROS 2 autonomous mobile manipulator: a mecanum base carrying a custom 3D-printed six-axis arm, running detect -> drive -> grasp.

**Status:** Phase 1 - math and structure. No hardware energized yet.

## Locked baseline

| Area | Decision |
|---|---|
| Power | 3S, >=10 Ah, >=20 A stated continuous, <=13.5 V charged |
| Drive | 4x TB6612FNG, channels paralleled, ~2 A continuous design value |
| Compute | Jetson Nano A02 + Pi 3B+ (HMI) + Teensy 4.1 |
| ROS | Humble everywhere; pinned L4T R32.7.1 ros-base container on Jetson |
| Middleware | Fast DDS, simple discovery, pinned to the wired interface |
| Network | Direct Cat6 Jetson<->Pi; Jetson M.2 WiFi for SSH and Foxglove only |
| Low level | Teensy 4.1 running micro-ROS; hardware quadrature encoders |
| Kinematics | Velocity PID in firmware; IK + odometry in a ros2_control plugin |
| IMU | GY-521 (MPU-6050) read by the Teensy; vyaw only into the EKF |
| Safety | Latching mushroom e-stop breaking the drive-rail relay coil |

Rationale for every line is in [docs/adr/](docs/adr/).

## Baseline exit criteria

Wheels turning under ROS 2, odometry validated against tape measure with straight-line, strafe, and rotation reported separately, power rail verified under load at the load, e-stop authority proven, watchdog authority proven.

## License

TBD
