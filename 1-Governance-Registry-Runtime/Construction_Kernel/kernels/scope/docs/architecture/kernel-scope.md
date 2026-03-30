# Kernel Scope

## Domain

The Construction Scope Kernel governs scope-domain truth for CSI Division 07 -- Building Envelope Systems.

## Scope Objects

The kernel manages the following object types:

| Object Type | Purpose | Schema |
|---|---|---|
| Scope of Work | Defines work boundaries with inclusions/exclusions | `scope_of_work.schema.json` |
| Work Operation | Individual operations within a scope | `work_operation.schema.json` |
| Sequence Step | Ordered steps with dependencies | `sequence_step.schema.json` |
| Trade Responsibility | Trade-to-scope assignments | `trade_responsibility.schema.json` |
| Inspection Step | Quality verification checkpoints | `inspection_step.schema.json` |
| Commissioning Step | BECx phase milestones | `commissioning_step.schema.json` |
| Closeout Requirement | Warranty and handoff items | `closeout_requirement.schema.json` |
| Warranty Handoff Record | Warranty transfer documentation | `warranty_handoff_record.schema.json` |
| Scope Entry | Atomic scope fact record | `scope_entry.schema.json` |

## CSI Division 07 Sections in Scope

- 07 10 00 -- Dampproofing and Waterproofing
- 07 20 00 -- Thermal Protection
- 07 21 00 -- Thermal Insulation
- 07 25 00 -- Weather Barriers
- 07 27 00 -- Air Barriers
- 07 40 00 -- Roofing and Siding Panels
- 07 50 00 -- Membrane Roofing
- 07 60 00 -- Flashing and Sheet Metal
- 07 70 00 -- Roofing and Wall Specialties
- 07 81 00 -- Applied Fireproofing
- 07 84 00 -- Firestopping
- 07 90 00 -- Joint Protection
- 07 92 00 -- Joint Sealants

## Boundary Conditions

- Scope records that reference CSI sections outside Division 07 are flagged as cross-division dependencies.
- Structural scope (Division 03, 05) is out of domain but may appear as interface dependencies.
- Exterior wall assemblies that span Divisions 04 (Masonry), 07, and 08 (Openings) require interface zone definitions.
