# Kernel-to-Reference Intelligence Map

## Purpose

Describes how the reference intelligence layer reads chemistry truth from this kernel.

## Intelligence Layer Role

The reference intelligence layer aggregates structured truth from domain kernels to support decision-making, material selection, and specification authoring. The chemistry kernel is a primary source.

## Data Consumed by Intelligence Layer

| Entity | Intelligence Use |
|---|---|
| Chemical System | Material selection queries filter by chemistry family, system type, and VOC limits. |
| Adhesion Rule | Substrate compatibility lookups for specification validation. |
| Incompatibility Rule | Conflict detection when multiple chemistries are specified in proximity. |
| Cure Mechanism | Environmental constraint checks for installation planning. |
| Degradation Mechanism | Service life estimation and climate-adjusted material recommendations. |
| Polymer Family | Chemistry family classification for grouping and filtering. |
| Chemical Hazard Record | Safety data retrieval for jobsite planning and compliance. |

## Data Flow

1. Intelligence layer indexes all active chemistry kernel records.
2. Queries are resolved against indexed records using schema-defined fields.
3. Results include kernel record IDs for traceability back to source truth.
4. Intelligence layer does not modify kernel records.

## Query Patterns

- "Which sealant chemistries have verified adhesion to aluminum?"
- "Are there incompatibilities between silicone sealant and SBS membrane?"
- "What are the cure constraints for moisture-cure polyurethane below 40 degrees F?"
- "Which chemistries have known plasticizer migration risks?"

## Constraints

- Intelligence layer must not cache stale kernel data beyond a session.
- All intelligence outputs must cite kernel record IDs.
- Chemistry kernel records are the authoritative source; intelligence layer does not override them.
