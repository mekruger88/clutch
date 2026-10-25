# Safety Hazard Analysis

This is a small prototype, not a certified industrial machine. The purpose is to identify hazards, estimate risk, reduce risk, and verify controls before operation. A ROS message is not a safety function.

## Risk scale

- Likelihood: Low / Medium / High
- Severity: Low / Medium / High
- Residual risk is accepted only after the named control is installed and tested.

## Hazard register

| Hazard | Initial risk | Controls | Verification | Residual risk |
|---|---|---|---|---|
| Battery short, connector fault or wiring fire | High | Main fuse sized to wire, per-rail fuses, insulated terminals, keyed polarity, strain relief, battery inspection. | PWR-001, visual preflight. | Medium |
| Runaway base after host, USB or WiFi failure | High | Teensy outputs inhibited on boot; explicit enable; 300-500 ms firmware watchdog; latching hardware e-stop. | CTL-002, SAFE-001. | Low |
| Motor stall or continuous strafe overheats DRV8871 breakout or wiring | High | DRV8871 30 kOhm RILIM internal current chop (~2.13 A typ), PID anti-windup, encoder stall timeout <250 ms, current logging, per-rail fuse. | PWR-007, PWR-008, PWR-009, PWR-010, CTL-004b, CTL-006, PWR-003. | Medium |
| E-stop fails or restart occurs after reset | High | Latching mushroom, NC contact opens relay coil, relay fails open, release does not restart, explicit enable required. | SAFE-001, SAFE-002. | Low |
| Category-0 e-stop drops arm under gravity | High | Documented operating characteristic; keep arm low; light payload; no body part or fixture below loaded arm; arm rail cut added only after this behavior is understood. | ARM-005. | Medium |
| Servo rail back-feeds Teensy or PCA9685 logic, or arm twitches at power-up | High | Servo V+ from its own fused UBEC branch; PCA9685 VCC from 3.3 V logic only; V+ never tied to VCC; PCA9685 OE held high until explicit enable (ADR-0013). | ARM-002, ARM-003. | Low |
| Pinch, crush or entanglement at arm, wheels, mecanum rollers | High | Keep observers clear; powered-motion exclusion zone; covers where practical; no loose clothing/cables; reachable e-stop. | Preflight, visual inspection. | Medium |
| Tip-over with extended arm | High | Low battery placement, arm-stowed travel rule, speed limit when extended, reach envelope derived by static stability test. | Future stability sweep. | Medium |
| Teensy destroyed by 5 V sensor outputs | High | CTL-000 and IMU-001 before connection; power GY-521 at 3.3 V; level shifters where required. | Voltage measurement. | Low |
| Lithium battery charging/over-discharge | High | Correct matching charger only, charge attended on nonflammable surface, inspect pack, LVC at 10.5/9.9 V, BMS treated as backstop. | PWR-001, SAFE-004. | Medium |
| Exposed conductors or poor grounds cause resets or shocks | Medium | Star ground, insulated terminals, no live breadboard in final power path, continuity check before power. | Preflight, PWR-004. | Low |

## Mandatory before first powered motor motion

- [ ] CTL-000 proves every Teensy input is <=3.3 V or a verified level shifter is installed.
- [ ] PWR-001 and PWR-002 pass for the selected battery.
- [ ] Main and per-rail fuses are installed; values recorded.
- [ ] Master disconnect and latching mushroom e-stop are wired; SAFE-001 passes on a dummy load.
- [ ] Teensy boots with outputs inhibited and requires explicit enable.
- [ ] Firmware watchdog and encoder stall timeout are compiled and demonstrated with wheels off ground.
- [ ] Wires are secured away from wheels, arm path and sharp chassis edges.
- [ ] A charged fire extinguisher is accessible; battery charging procedure is printed.
- [ ] Wheels are raised for first motor direction test; observers are outside the motion area.
- [ ] Preflight checklist is completed and the test is logged.

## Preflight checklist

1. Inspect battery, leads, connectors, fuses, cable routing and enclosure fasteners.
2. Confirm arm is stowed or absent; remove payload and loose objects.
3. Confirm e-stop is accessible and test its mechanical latch.
4. Confirm floor area is clear and no one is in the motion envelope.
5. Apply compute power, verify diagnostics healthy, then explicitly enable actuator power.
6. Start at the lowest commanded speed and retain a clear path to the e-stop.
7. Stop, isolate battery and inspect temperature/connectors after the run.
