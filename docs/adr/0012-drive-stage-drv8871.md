# ADR-0012: Drive stage substitution - DRV8871

- Status: Accepted 2026-09-16
- Supersedes: ADR-0002 (driver selection only; the 2 A continuous design value carries over)

## Context
ADR-0002 locked 4x TB6612FNG with channels paralleled to a 2 A continuous design value. Five DRV8871 breakouts (ACEIRMC / Aceirmc US, ASIN B0GF71LMRH) arrived 2026-09-06 for $15.99 total, $3.20 each installed. Listing was suspect (contaminated with N20-motor text, 1.0 star), so acceptance is contingent on inspection.

Verified against manufacturer datasheets, not the Amazon listing:

- TB6612FNG rates 1.2 A average and 3.2 A single-pulse peak per channel, no current limit, 2.5-13.5 V supply.
- DRV8871 rates 3.6 A peak, 6.5-45 V supply, 565 mOhm RDS(on) HS+LS typical, and includes internal current regulation set by a single RILIM resistor to GND - no external sense resistor. Datasheet section 8.2.2.2 reports "2 A RMS at 25 C on standard FR-4 PCBs," which assumes a soldered PowerPAD into a via-stitched ground plane. Continuous capability on a $3 breakout will be lower and must be measured.

Drive motor stall is claimed 2.8 A at 12 V nominal (hobby-motor datasheet, not measured). At the locked pack ceiling of 13.5 V charged, that implies ~3.15 A stall assuming a 4.29 Ohm winding. Both numbers are assumptions until PWR-10 runs.

RILIM equation from datasheet section 7.3.3:

    R_ILIM (kOhm) = V_ILIM (kV) / I_TRIP (A) = 64 / I_TRIP (typ)

V_ILIM is specified 59 / 64 / 69 kV min/typ/max, giving ~8 percent trip spread from silicon alone. Minimum allowed RILIM is 15 kOhm.

Boards shipped populated with a resistor marked "303" - EIA three-digit code for 30 kOhm, and three-digit markings are almost always 5 percent thick film. Trip window at 30 kOhm:

| Case | I_TRIP |
|---|---|
| Typical (V_ILIM 64 kV) | 2.13 A |
| Worst-case low (V_ILIM 59 kV, R +5%) | 1.87 A |
| Worst-case high (V_ILIM 69 kV, R -5%) | 2.42 A |

30 kOhm is the value TI works through in datasheet section 8.2.2 for a motor drawing about 2 A startup - a reasonable factory default for this class of load.

TB6612FNG's 3.2 A rating is single-pulse absolute, so a 3.15 A stall exceeds it. DRV8871 clamps below stall by design.

## Options

1. **Keep TB6612FNG paralleled.** No rework. No current limit. Stall exceeds the pulse rating and the chip has no way to protect itself; a stalled wheel is bounded only by battery impedance and thermal shutdown.
2. **DRV8871 with as-shipped 30 kOhm.** Trip at 2.13 A typical, ~74 percent of stall torque available (63-86 percent across tolerance), zero board rework, five boards for four wheels (one spare).
3. **DRV8871 with 24 kOhm swapped in.** Trip at 2.67 A typical, ~95 percent of stall torque, but removes the thermal cushion and requires desoldering an 0603 on four boards with no pad-lift insurance.

## Decision

Option 2. Adopt DRV8871, one board per wheel, **RILIM left at the factory 30 kOhm**. Supersedes ADR-0002's driver selection. Paralleling jumpers are deleted from the wiring plan.

## Consequences

- Peak torque capped at ~74 percent of stall (63-86 percent across tolerance). A wheel meeting a hard obstruction chops rather than drawing stall current. That is the point.
- 8 PWM lines for 4 wheels (IN1/IN2 per board) replace PWM+direction+shared STBY. Both low is sleep. Firmware output stage is rewritten and untested until CTL-05 passes.
- **t_OFF is fixed at 25 us.** Once I_TRIP is hit, both low-side FETs enable for 25 us regardless of PWM. At 20 kHz the period is 50 us, so a wheel in regulation loses half its period to chop. PWM lands near 5-10 kHz - audible - not 20 kHz.
- **Velocity PID needs explicit anti-windup.** A chopping wheel does not track its setpoint and the integrator will run away.
- ILIM caps inrush at ~2.13 A instead of ~3.15 A, reducing the bulk capacitance the drive rail needs.
- Forecloses any future motor upgrade drawing over ~2 A continuous without also reworking RILIM and adding heatsinking.
- Forecloses current-sense-based stall detection in firmware. DRV8871 exposes no current-feedback pin; the chip handles regulation silently and software never learns a wheel is stalled. Any closed-loop stall detection has to come from encoder velocity error.
- The datasheet contradicts itself on f_PWM (Recommended Operating Conditions says 0-200 kHz, Overview says 0-100 kHz). Planned operating point ~5-10 kHz sits well inside both.
- 3.3 V logic drive sits inside the DRV8871's 0-5.5 V input window; the driver presents no output signal back to the MCU, so nothing from the drive stage can reach Teensy GPIO. This removes a 5 V hazard rather than adding one.
- **Unresolved risk:** TI's 2 A RMS continuous figure assumes PowerPAD soldered into a via-stitched plane. Breakouts have far less copper, so thermal shutdown may fire before the 2.13 A current limit does. PWR-09 is the deciding test.
- **Unresolved risk:** the 2.8 A / 12 V stall figure is a manufacturer claim from a hobby-motor listing, not a measurement. If the motor is actually rated at 6 V, real stall on a 3S pack is closer to 5.6 A and this analysis inverts. PWR-10 must run before this ADR's numbers are trusted.

## Verification

- **PWR-07** - Physical inspection. Pass: 5 boards present, DRV8871 top mark confirmed under magnification, ILIM resistor measures 30 kOhm +/-5 percent on a DMM.
- **PWR-08** - Single board, one wheel motor, 13.5 V, locked rotor 5 s. Pass: current plateaus 1.87-2.42 A, no reset, board surface <=80 C.
- **PWR-09** - Four boards, robot driving 60 s strafe-and-rotate loop. Pass: hottest driver <=70 C, zero UVLO/OCP/TSD faults.
- **PWR-10** - Measured no-load and stall current on two motors at 13.5 V. Pass: no-load <=0.5 A, measured stall within 20 percent of the claimed 3.15 A.
- **CTL-05** - Open-loop duty sweep 0 to 100 percent via IN1/IN2, measure wheel rad/s. Pass: monotonic, no dead zone wider than 8 percent duty.
- **CTL-06** - Retuned per-wheel velocity PID with anti-windup. Pass: 0.3 m/s step settles <=400 ms, overshoot <=15 percent, integrator recovers within 200 ms of releasing a deliberately stalled wheel.

## Reversal trigger

Revert to ADR-0002 (rebuy a 4th TB6612 board) if any of:

- PWR-09 exceeds 70 C on any board under the loop.
- PWR-10 shows measured stall above 3.4 A, putting the design outside DRV8871's usable envelope even with tolerance.
- PWR-07 fails - fake silicon, missing/wrong RILIM, or <4 usable boards.

Drop RILIM to 24 kOhm only if the robot demonstrably cannot break static friction or climb a 10 mm threshold - measured, not assumed.

## Sources

- TI DRV8871 datasheet (SLVSCY8): https://www.ti.com/lit/ds/symlink/drv8871.pdf
- Toshiba TB6612FNG datasheet: https://toshiba.semicon-storage.com/info/TB6612FNG_datasheet_en_20141001.pdf
- Amazon listing (ACEIRMC DRV8871 breakouts, ASIN B0GF71LMRH): https://www.amazon.com/dp/B0GF71LMRH
