# Kernel-to-Digital Twin Map

## Purpose

Documents the relationship between the Construction Chemistry Kernel and any digital twin layer.

## Status

Reserved for future digital twin integration. No digital twin is implemented.

## Design Intent

- The chemistry kernel provides material chemistry truth that a digital twin could embed in its model.
- No digital twin geometry, simulation logic, or spatial data exists in this kernel.
- Future digital twins would reference chemistry records to model material behavior over time.

## Placeholder Notes

- A digital twin could use degradation mechanisms to simulate service life under climate conditions.
- Cure mechanism constraints could feed into construction sequencing simulations.
- Incompatibility rules could trigger alerts when adjacent materials are modeled in contact.
- No timeline is established for digital twin integration.

## Constraints

- Kernel records must never contain geometric or spatial data.
- Digital twin layers must treat kernel chemistry data as source truth.
- Any future integration must reference kernel records by ID, not embed copies.

## References

- See `kernel_map.md` for entity overview.
- See `degradation_mechanism` schema for climate context modeling data.
