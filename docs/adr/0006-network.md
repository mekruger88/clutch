# ADR-0006: Direct wired link plus Jetson M.2 WiFi

- Status: Accepted 2026-08-26

## Context
The Jetson Nano Developer Kit has no onboard wireless; NVIDIA provides an M.2 Key E site instead. Nothing in the parts inventory gave the Jetson any wireless capability, so untethered operation - a stated success criterion - was blocked. Auto MDI-X is part of the gigabit spec, so no crossover cable is needed. Pi Ethernet runs over USB 2.0 and caps near 300 Mbps, which is the real bandwidth ceiling regardless of topology.

## Options
1. Direct Jetson<->Pi cable plus an M.2 Key E WiFi card - about $25-35.
2. Direct cable plus a USB WiFi dongle - about $17, but driver support on L4T R32 is chipset-dependent and a dongle protrudes on a moving robot.
3. Onboard 5-port switch, no Jetson WiFi - about $25, adds 2-3 W and does not solve untethered operation.

## Decision
Option 1. Point-to-point Cat6 for the data plane, static addressing on a dedicated private subnet, no DHCP. Jetson wlan0 carries SSH, apt and the Foxglove WebSocket only.

## Consequences
Requires opening the Jetson to fit the card under the module. Antenna placement and cable strain relief become dimensioned CAD requirements, clear of the wheels and the arm sweep. A switch can be inserted later without changing addressing.

## Verification
LINK-001 zero-loss ping over 10 min and across 10 reboots. LINK-002 measured throughput ceiling recorded, not assumed. LINK-003 wireless isolation. LINK-004 30 min under motion with zero link-down events.

## Reversal trigger
The M.2 card cannot be made to associate reliably on L4T R32 - fall back to the dongle.
