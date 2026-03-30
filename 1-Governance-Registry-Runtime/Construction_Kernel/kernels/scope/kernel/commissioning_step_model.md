# Commissioning Step Model

## Purpose

Defines building enclosure commissioning (BECx) steps within scope. Commissioning steps verify that the building envelope performs as designed across multiple project phases.

## Definition

A commissioning step is a BECx milestone tied to a scope of work. It defines the commissioning phase, responsible party, acceptance criteria, and required documentation.

## BECx Phases

| Phase | Description | Typical Timing |
|---|---|---|
| `design_review` | Review of envelope design documents | Design phase |
| `construction_observation` | Field observation during installation | Construction phase |
| `pre_cover_inspection` | Inspection before concealment | Before cover/cladding |
| `performance_testing` | Quantitative performance verification | After installation complete |
| `closeout_review` | Review of closeout documentation | Project closeout |
| `seasonal_observation` | Observation across seasonal conditions | Post-occupancy, first year |

## BECx Scope Boundaries

The Scope Kernel defines WHAT commissioning steps are required and WHEN they occur. It does not define:
- HOW to perform commissioning procedures (Assembly Kernel domain)
- WHAT performance levels are required (Spec Kernel domain)
- Testing equipment or methodology details (Reference Intelligence)

## Acceptance Criteria

Commissioning steps carry acceptance criteria that define pass/fail conditions:
- Design review: all envelope details reviewed and approved
- Construction observation: installation matches approved details
- Pre-cover inspection: continuous coverage, proper laps, sealed penetrations
- Performance testing: air leakage below threshold, water penetration resistance
- Closeout review: all documentation complete and accurate
- Seasonal observation: no moisture intrusion, thermal anomalies, or air leakage

## Documentation Requirements

Each commissioning step may specify required documentation:
- Observation reports with photographs
- Test reports with quantitative results
- Deficiency logs with resolution tracking
- Final commissioning report

## Relationship to Inspection Steps

Commissioning steps and inspection steps are distinct:
- **Inspection steps** are point-in-time quality checks during construction
- **Commissioning steps** are phase-level verification activities spanning the project lifecycle

A commissioning step (e.g., `pre_cover_inspection` phase) may encompass multiple inspection steps (individual pre-cover checks at various locations).

## Schema Reference

See `schemas/commissioning_step.schema.json` for the formal schema definition.
