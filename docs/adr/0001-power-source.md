# ADR-0001: Replace the battery pack

- Status: Accepted 2026-08-26

## Context
The on-hand 12 V 10 Ah pack states a 6 A BMS limit. At 11.1 V nominal that caps output near 67 W. Estimated worst case for compute, four drive channels and eight servos is roughly 15-18 A momentary. The listing states no continuous discharge figure.

## Options
1. Keep the 6 A pack permanently - $0, requires motion scheduling and strict acceleration limits.
2. Keep for bring-up, replace after measurement - $0 now, defers the buy.
3. Replace now with a pack rated >=20 A continuous - about $54-96.

## Decision
Option 3. Single pack, 3S, >=10 Ah, >=20 A **stated continuous** (continuous and pulse ratings listed separately), <=13.5 V fully charged.

## Consequences
The voltage ceiling comes from the drive stage, not the battery, so ADR-0002 and this ADR are coupled. Rules out 4S LiPo and 4S LiFePO4 for v1. A pack advertising 20 A for two seconds does not satisfy this.

## Verification
PWR-001 identity and labels. PWR-002 sustains 5 A for five minutes above 10.5 V with under 20 C connector rise. PWR-003 bare-base transient below 5.5 A peak.

## Reversal trigger
Measured worst-case draw stays under 4.8 A with margin, or the drive stage changes the voltage ceiling.
