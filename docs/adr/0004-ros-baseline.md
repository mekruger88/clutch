# ADR-0004: ROS 2 Humble, containerized on the Jetson

- Status: Accepted 2026-08-26

## Context
JetPack 4 ended at 4.6.6 and the original Nano is capped at L4T R32 on Ubuntu 18.04. Humble targets Ubuntu 22.04 and is supported to May 2027. ROS 2 does not support cross-distro communication, so every machine including the ground station must match.

## Options
1. Humble everywhere with a pinned prebuilt L4T R32.7.1 container on the Jetson.
2. Humble everywhere, container built from source - 30-60 hours on a 4 GB board.
3. Galactic on all machines - already end of life.

## Decision
Option 1, starting from a **ros-base** image rather than desktop. Pi and laptop run native Humble on 22.04. Simulation is Gazebo Fortress, the recommended Humble pairing.

## Consequences
No RViz, Gazebo or compilers in the deployed Jetson image; visualization lives on the laptop. The runtime depends on a community-maintained base image, so pin by digest, commit the Dockerfile, and archive a known-good build. Roughly nine months of formal Humble support remain - a migration review is due before May 2027.

## Verification
ENV-001 reproducible build from committed instructions. ENV-002 GPU reachable in-container. ENV-003 CSI and LiDAR publishing to MCAP for 30 min.

## Reversal trigger
ENV-001 to ENV-003 failure, a Jetson replacement, or the Humble EOL review.
