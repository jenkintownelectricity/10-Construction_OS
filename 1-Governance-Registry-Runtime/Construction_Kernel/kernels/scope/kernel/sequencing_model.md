# Sequencing Model

## Purpose

Defines installation sequence requirements between trades and within trades. Sequencing is scope truth because the order of work operations directly affects building envelope performance and trade coordination.

## Definition

A sequence step is an ordered position in an installation sequence that defines what must happen before and after it. Sequence steps form a directed acyclic graph (DAG) of dependencies.

## Sequencing Principles

1. **Sequence is explicit.** Every dependency between operations must be stated as a predecessor/successor relationship. Implied sequencing is flagged.
2. **Hold points are blocking.** A hold point in the sequence means work cannot proceed past that point until an inspection or approval occurs.
3. **Cross-trade sequencing is critical.** The most important sequences are those that cross trade boundaries, because no single trade controls both sides.
4. **Weather constraints modify timing, not sequence.** The order of operations is fixed by the sequence model. Weather may delay when a step occurs but does not change its position in the sequence.

## Sequence Step Structure

Each sequence step contains:
- **Sequence position**: Ordinal position in the sequence
- **Scope reference**: The scope of work this step belongs to
- **Predecessor steps**: Steps that must complete before this one
- **Successor steps**: Steps that follow this one
- **Trade reference**: The trade performing this step
- **Hold point**: Whether this step is a hold point requiring inspection

## Common Division 07 Sequences

### Roof Installation Sequence
1. Structural deck inspection (hold point)
2. Vapor retarder installation
3. Insulation board installation (layer 1)
4. Insulation board installation (layer 2 / cover board)
5. Membrane installation -- field sheets
6. Membrane installation -- flashing and details
7. Sheet metal installation (copings, edge metal)
8. Pre-cover inspection at penetrations (hold point)
9. Sealant application
10. Final roofing inspection (hold point)

### Air Barrier Sequence
1. Substrate inspection (hold point)
2. Surface preparation / priming
3. Air barrier application -- field areas
4. Air barrier application -- transitions and penetrations
5. Pre-cover inspection (hold point)
6. Insulation installation over air barrier
7. Cladding support installation

## Sequencing Conflicts

A sequencing conflict exists when:
- Two operations claim the same sequence position
- A circular dependency exists in predecessor/successor references
- A trade requires access to an area that another trade has already closed

Conflicts are flagged as scope gaps requiring human resolution.

## Schema Reference

See `schemas/sequence_step.schema.json` for the formal schema definition.
