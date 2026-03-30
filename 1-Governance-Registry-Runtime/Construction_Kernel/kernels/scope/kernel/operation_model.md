# Operation Model

## Purpose

Defines work operations -- the individual activities that occur within a scope of work. Operations are the executable units of scope.

## Definition

A work operation is a discrete activity performed by a trade within a defined scope. Operations have types, trade assignments, sequencing positions, and may carry weather constraints.

## Operation Types

| Type | Description | Example |
|---|---|---|
| `surface_prep` | Substrate preparation | Concrete grinding, primer application |
| `installation` | Primary material installation | Membrane sheet installation |
| `flashing` | Flashing installation | Base flashing at parapet |
| `sealing` | Sealant or adhesive application | Perimeter sealant at windows |
| `insulating` | Insulation installation | Roof insulation board layup |
| `waterproofing` | Waterproofing membrane application | Below-grade membrane |
| `air_sealing` | Air barrier installation | Fluid-applied air barrier |
| `fire_stopping` | Firestop installation | Penetration firestopping |
| `testing` | Quality testing | Flood test, air test |
| `protection` | Protection of completed work | Protection board, temporary covers |
| `cleanup` | Site cleanup and demobilization | Debris removal, equipment removal |

## Operation Structure

Each operation links to:
- **Scope reference**: The scope of work this operation belongs to
- **Trade reference**: The trade responsible for performing this operation
- **Sequence position**: Where this operation falls in the installation sequence
- **Prerequisites**: Operations that must be complete before this one can start

## Operation Sequencing

Operations within a scope follow a defined sequence. The sequence is expressed through:
1. `sequence_position` on the operation (ordinal within scope)
2. `prerequisites` listing operation IDs that must precede
3. Related sequence step records for cross-trade coordination

## Weather Constraints

Operations may carry weather constraints that define acceptable conditions:
- Temperature range (min/max)
- Wind speed limit
- Precipitation restrictions
- Humidity limits

These constraints are recorded as scope facts. The Scope Kernel does not evaluate weather conditions against constraints.

## Duration Estimates

Operations may carry advisory duration estimates. These are informational only and do not constitute schedule commitments. Duration estimates support coordination planning but are not authoritative for project scheduling.

## Schema Reference

See `schemas/work_operation.schema.json` for the formal schema definition.
