# ADR-0008: Firmware velocity loop, ROS-side kinematics

- Status: Accepted 2026-08-26

## Context
Humble has no official mecanum controller - mecanum_drive_controller is documented under Jazzy - so the controller gets written regardless. The question is only which side of the USB link owns the math. The Teensy now has hardware quadrature counters and a 600 MHz core sitting directly on the encoders.

## Options
1. All in firmware - fastest to a moving robot, but the derivation, covariance and odometry integration end up in embedded C where they are hard to test and invisible to a reviewer.
2. All in ros2_control - idiomatic, but puts the wheel velocity loop across a USB link and at the mercy of host scheduling.
3. Split by timescale - velocity PID in firmware, kinematics and odometry in a custom controller plugin.

## Decision
Option 3. Anything that must run at a fixed high rate against encoder edges belongs on the Teensy; anything representing robot-level geometry or ROS interface belongs on the Jetson.

## Consequences
Kinematics goes in a plain C++ library with no ROS dependencies, unit tested with randomized IK/FK round trips, with the controller plugin as a thin wrapper. Derivation, coordinate conventions and wheel numbering are documented. Wheel radius, lx, ly and encoder CPR are **measured** constants, never listing values.

Mecanum dead reckoning is slip-limited by design - the rollers are meant to slip. Publish anisotropic covariance (larger for vy than vx), calibrate straight-line, strafe and rotation separately, and treat the IMU and SLAM as required rather than optional corrections.

## Verification
KIN-001 10,000-sample round trip plus sign patterns and saturation, before any wheel spins. KIN-002 measured geometry and empirical CPR within 0.5 percent across three trials. KIN-003 direction mapping on all four wheels. KIN-004 odometry error reported separately per motion type. KIN-005 step response settles under 300 ms.

## Reversal trigger
CTL-003 latency data shows the firmware PID adds nothing over host-side control.
