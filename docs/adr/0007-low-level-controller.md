# ADR-0007: Teensy 4.1 running micro-ROS

- Status: Accepted 2026-08-26
- Supersedes: the Arduino Mega 2560 decision made earlier the same session

## Context
The Mega was chosen first because it was already owned. Two constraints then surfaced. micro-ROS has no 8-bit AVR target, so keeping the Mega forces a custom binary protocol and forecloses native ROS interfaces at the MCU boundary. And the Mega exposes only six attachInterrupt pins, two of which are the I2C lines needed for the servo driver - leaving exactly four for four encoder A channels, with B channels pushed onto pin-change interrupts and every edge costing CPU time at 16 MHz.

## Options
1. Keep the Mega - $0, custom protocol, eight interrupt sources on one 16 MHz core.
2. Single Teensy 4.1 - about $35, 600 MHz Cortex-M7, 1 MB RAM, four hardware quadrature decoders, micro-ROS supported.
3. Split: Mega for drive, Teensy for arm - two firmware bases and two protocols before the wheels turn once.

## Decision
Option 2. One Teensy 4.1 (standard variant with the Ethernet PHY) as the sole low-level controller, micro-ROS over USB serial to the Jetson.

## Consequences
COBS+CRC16 framing is withdrawn; micro-ROS provides transport. Safety requirements are unchanged and still mandatory - inhibited outputs on boot, explicit enable handshake, 300-500 ms command watchdog, encoder stall timeout, hardware watchdog timer. **Teensy 4.x GPIO is 3.3 V and not 5 V tolerant; 5 V on a pin destroys the chip.** Every incoming signal must be checked. Buy two - the line has been flagged for discontinuation and the whole control layer depends on it. The Mega is retained as a 5 V bench tool and fallback.

## Verification
CTL-000 encoder A-channel output voltage measured **before purchase**. CTL-002 watchdog authority across process kill, USB unplug and WiFi loss. CTL-003 latency p99 under 50 ms under perception load. CTL-004 no count loss at full speed.

## Reversal trigger
Encoders prove 5 V push-pull and the level-shifting work is declined, or Teensy availability collapses. The Mega remains the fallback.
