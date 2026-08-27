# Clutch

ROS 2 autonomous mobile manipulator: a mecanum base carrying a custom 3D-printed six-axis arm, running detect -> drive -> grasp.

**Status:** Phase 1 - math and structure. No hardware energized yet.

## Where to start

- [Decision index](adr/README.md) - every accepted decision with its rejected alternatives and reversal trigger.
- [Requirements matrix](requirements.md) - each requirement with a numeric threshold, a test, and an evidence slot.
- [Bench checklist](validation/bench_checklist.md) - the ordered bring-up sequence and its blocking constraints.
- [Hazard analysis](safety/hazard_analysis.md) - hazard register and the mandatory pre-first-motion checklist.

## Baseline exit criteria

Wheels turning under ROS 2. Odometry validated against tape measure with straight-line, strafe and rotation reported separately. Power rail verified under load, measured at the load. E-stop authority proven. Watchdog authority proven.

Nothing above is marked verified until its evidence artifact is committed and linked from the requirements matrix.
