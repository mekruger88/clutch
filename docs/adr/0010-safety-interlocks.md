# ADR-0010: Latching hardware e-stop, staged

- Status: Accepted 2026-08-27

## Context
ISO 13850 requires an emergency stop to be manually actuated, to **latch** in the activated position, and to require a deliberate manual reset - and disengaging the device must not restart the machine, only permit restarting. Category 0 is immediate removal of actuator power. A touchscreen button does not satisfy this. Separately, switch DC ratings run far below their AC ratings because a DC arc has no current zero to quench it, so the on-hand toggle markings are unverified.

## Options
1. Master switch on battery positive only - cheapest, but non-latching, and cutting the battery kills the INA226 telemetry at the exact moment the log matters.
2. Master plus an independent actuator-rail toggle - telemetry survives the cut, but still no latching and no distinct reset.
3. Master plus a latching mushroom e-stop breaking a relay coil, plus a separate enable.

## Decision
Option 3, staged. Stage 1 before first powered motion: DC-rated master rocker ahead of the main fuse; latching mushroom with a positive-opening NC contact breaking the **relay coil** rather than switching motor current; relay on the drive rail only. Stage 2 with the arm: the same e-stop extends to the servo rail, separately fused.

## Consequences
Compute and telemetry never lose power, so the INA226 chain logs the event instead of vanishing with it. Twisting out the mushroom restores circuit capability only - the Teensy latches inhibited and requires the explicit enable handshake, so stale setpoints cannot resume motion. The relay must fail open. Mushroom placement must be reachable without leaning over the arm sweep, which is a CAD constraint before the enclosure exists.

**Documented hazard: Category 0 power removal drops a gravity-loaded arm.** There is no software mitigation, because software is what was just removed. Keep stowed and working poses low, keep payload light, never place hands beneath a loaded arm.

Software LVC from the battery INA226: warn and refuse new goals at 10.5 V (3.5 V/cell), auto-stop at 9.9 V (3.3 V/cell). The pack BMS trips near 2.8-3.0 V/cell and is a backstop only.

## Verification
SAFE-001 drive power removed under 100 ms, 20 repetitions, telemetry survives, mushroom release does not restart motion. SAFE-002 fail-open on coil loss. SAFE-003 50 DC load interruptions with no contact welding. SAFE-004 LVC verified by bench-discharging into a resistive load, not by running the robot flat. SAFE-005 someone else executes the written preflight checklist cold.

## Reversal trigger
None for the architecture. If SAFE-003 fails, the switch is replaced with a DC-rated part.
