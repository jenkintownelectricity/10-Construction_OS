# Kernel-to-Digital Twin Map — Construction Scope Kernel

## Purpose

This map defines the integration boundary between the Construction Scope Kernel and any digital twin platform.

## Current Status

Reserved for future digital twin integration. No digital twin integration is implemented.

## Design Intent

- A digital twin may consume scope truth records to understand scope boundaries spatially.
- Scope records define what work is included at specific interface zones and assemblies.
- The digital twin may visualize scope boundaries, trade responsibilities, and inspection hold points.

## Future Integration Points

- `interface_zones` from scope records may map to spatial regions in the digital twin.
- `control_layers_affected` may map to layer visualizations in the twin model.
- `inspection_step` hold points may appear as verification markers in the twin timeline.
- `warranty_handoff_record` entries may attach to twin components for lifecycle tracking.

## Constraints

- The scope kernel does not store geometry, coordinates, or BIM object references.
- Spatial mapping MUST occur in an adapter layer, not in the kernel.
- The digital twin MUST NOT modify scope truth records.

## Governance

- This map will be updated when a digital twin integration is designed and approved.
- Integration adapters MUST comply with kernel contracts.
- No geometric or spatial data may be introduced into kernel schemas.

## No-Execution Guarantee

- The scope kernel does not render, simulate, or interact with digital twin environments.
- All digital twin integration occurs outside the kernel boundary.
