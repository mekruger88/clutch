# ADR-0002: Parallel TB6612FNG channels

- Status: Accepted 2026-08-26

## Context
Toshiba rates the TB6612FNG at 1.2 A average and 3.2 A single-pulse peak per channel, 2.5-13.5 V supply. Chassis motors draw about 360 mA rated with stall assumed near 2.8 A (unmeasured). Mecanum strafing dumps power into roller friction, so the worst continuous case is a loaded strafe, not a straight-line dash.

## Options
1. As bought, one channel per motor - $0, 1.2 A continuous, no stall margin.
2. Parallel both channels per board, one board per motor - about $10 for a fourth board, roughly 2 A continuous.
3. Cytron MDD10A x2 - about $47, 10 A continuous, 5-30 V, removes the voltage ceiling.

## Decision
Option 2. Design value is **2 A continuous**, not 2.4 A - current sharing and thermal limits prevent simply summing the ratings.

## Consequences
Requires four boards; three are owned. Keeps pack voltage <=13.5 V, making ADR-0001 chemistry final. Firmware stall timeout and heatsinking are mandatory.

## Verification
Strafe 30 s under 1.2 A per motor mean. Three 1 s stalls with under 30 C case rise. Stall timeout cuts PWM within 250 ms of counts stopping.

## Reversal trigger
Sustained strafe current above 1.5 A per motor, thermal shutdown, any driver failure, or a decision to raise pack voltage.
