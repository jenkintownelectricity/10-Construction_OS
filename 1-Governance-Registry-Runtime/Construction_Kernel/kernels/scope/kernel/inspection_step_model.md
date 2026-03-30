# Inspection Step Model

## Purpose

Defines quality inspection steps within scope. Inspection steps are scope truth because they define what must be verified, when, and by whom before work can proceed or be concealed.

## Definition

An inspection step is a quality verification checkpoint tied to a scope of work. It defines the inspection type, timing, acceptance criteria, and whether it constitutes a hold point.

## Inspection Types

| Type | Description | Typical Timing |
|---|---|---|
| `pre_cover` | Inspection before concealment | Before insulation over air barrier |
| `substrate` | Substrate condition verification | Before membrane application |
| `adhesion` | Bond strength verification | After membrane/coating cure |
| `continuity` | Continuous coverage verification | After air/water barrier application |
| `penetration` | Penetration seal verification | After penetration sealing |
| `transition` | Transition detail verification | After flashing/transition installation |
| `flood_test` | Water ponding test | After waterproofing completion |
| `air_test` | Air leakage test per ASTM E2357 | After air barrier completion |
| `visual` | General visual inspection | At hold points and completion |

## Hold Points

A hold point is an inspection step that blocks subsequent work. When an inspection step has `hold_point: true`:
1. Successor operations in the sequence cannot begin.
2. The inspection must be completed and documented.
3. Acceptance criteria must be met before release.
4. If criteria are not met, deficiency resolution is required.

## Acceptance Criteria

Each inspection step may define acceptance criteria that specify measurable or observable conditions for passing:
- Air leakage rate below threshold (e.g., 0.04 CFM/sf at 75 Pa)
- No visible defects in membrane continuity
- Substrate moisture content below threshold (e.g., 5% per ASTM D4263)
- Adhesion pull test above minimum (e.g., manufacturer's requirement)

## Responsible Party

The `responsible_party` field identifies who performs the inspection:
- Building enclosure consultant
- Owner's representative
- General contractor quality team
- Third-party testing agency
- Manufacturer's technical representative

## Evidence Requirements

Inspection steps define what evidence must be collected via the `evidence_required` field. This connects to the evidence linkage model.

## Schema Reference

See `schemas/inspection_step.schema.json` for the formal schema definition.
