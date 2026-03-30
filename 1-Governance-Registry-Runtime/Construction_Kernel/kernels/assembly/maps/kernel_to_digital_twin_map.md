# Kernel-to-Digital Twin Map — Construction Assembly Kernel

## Status: Reserved for Future

This map is reserved for documenting how digital twin systems consume assembly kernel truth.

## Anticipated Digital Twin Integration Points

| Integration | Description | Status |
|---|---|---|
| Assembly layer mapping | Digital twin layers mapped to kernel assembly_layer records | Not yet implemented |
| Control layer visualization | Control-layer continuity rendered in 3D model | Not yet implemented |
| Transition condition tagging | Interface zones in digital twin tagged with transition_condition IDs | Not yet implemented |
| Penetration inventory | Digital twin penetrations linked to penetration_condition records | Not yet implemented |
| Lifecycle state sync | Assembly status synced between kernel records and digital twin | Not yet implemented |

## Design Principles

1. The kernel is the source of truth for assembly configuration. The digital twin is a visualization and simulation consumer.
2. Digital twin geometry is not stored in the kernel. The kernel stores structured assembly data.
3. Bi-directional sync requires conflict resolution protocols (not yet defined).
4. Sensor data from digital twin systems may generate evidence linked to kernel objects.

## Current State

No digital twin integrations exist. The kernel's structured data model is designed to support future digital twin consumption.
