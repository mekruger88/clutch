# ADR-0011: Math first, then hardware, then simulation

- Status: Accepted 2026-08-27

## Context
Two external reviews both recommended simulation-first as the opening move. The tooling supports it - gz_ros2_control is released for Humble against Fortress. But this project's hardware is already bought and on the bench, and ADR-0008 makes wheel radius, lx, ly and encoder CPR **measured** constants.

## Options
1. Hardware-first - fastest to physical validation, protects against nothing in software.
2. Simulation-first - about 4-6 weeks before wheels turn; protects against URDF, TF and kinematics sign errors.
3. Math-first, then hardware, then simulation built from measured geometry.

## Decision
Option 3, in three phases. Phase 1: kinematics library plus unit tests, placeholder URDF with real chassis dimensions, CI green, ADRs written - roughly a week, no hardware, no simulator. Phase 2: hardware bring-up in strict order, ending at validated odometry. Phase 3: simulation built from the measured robot.

## Consequences
What simulation-first actually protects is kinematics correctness and URDF structural validity, and both are obtainable from unit tests and a parse check in hours rather than weeks. Building the sim after measurement makes it a **verification tool** rather than a hypothesis, and avoids the sim/real divergence that comes from modeling a robot before measuring it. The laptop's Polaris GPU was dropped from ROCm, so simulation buys rendering and nothing else.

Ordering constraints that matter more than the numbering: CTL-000 before any Teensy purchase. SAFE-001 verified on a dummy load before any motor is energized. IMU-001 bus voltage before the IMU touches the Teensy. KIN-001 passing before any wheel spins.

## Verification
Baseline exit criteria: wheels turning under ROS 2; odometry validated against tape measure with straight-line, strafe and rotation reported separately; power rail verified under load measured at the load; e-stop authority proven; watchdog authority proven.

## Reversal trigger
A part shortage blocks all hardware work - then simulation is the right use of the gap.
