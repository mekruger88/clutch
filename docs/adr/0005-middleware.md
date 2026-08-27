# ADR-0005: Fast DDS with simple discovery

- Status: Accepted 2026-08-26

## Context
Fast DDS is the default RMW in Humble and ships with the binaries. The robot data plane is two computers on an isolated wired segment. Default discovery uses multicast, which will happily select WiFi if the interface is not restricted.

## Options
1. Fast DDS, simple discovery, transport pinned to the wired interface.
2. Fast DDS with a Discovery Server on the Jetson - centralized discovery, one more process that must boot correctly.
3. Cyclone DDS with explicit interface configuration - another package inside the pinned container and on the Pi.

## Decision
Option 1. Start with the supported default, configure it deliberately, measure it, and add centralized infrastructure only when evidence requires it.

## Consequences
DDS stays on the wired link only; WiFi is not part of the ROS domain. The laptop never joins DDS during validated runs - it connects through foxglove_bridge over WebSocket. Reliable QoS for commands and state, best-effort for high-rate sensors, compressed images only when crossing machines. Config files live in the repo, not in shell profiles.

## Verification
NET-001 discovery within 10 s across 20 alternating start orders. NET-002 command round trip p99 under 50 ms. NET-003 mixed traffic under 30 percent of measured link throughput. NET-004 disabling WiFi mid-run changes nothing.

## Reversal trigger
NET-001 to NET-004 failure after one configuration pass. Escalate to Discovery Server, then Cyclone DDS, only against identical benchmarks.
