# Compatibility Model — Construction Material Kernel

## Purpose

This model defines how material-to-material compatibility is recorded. Compatibility is a pairwise relationship between two materials that describes whether they can be placed in direct contact or proximity without adverse interaction.

## Compatibility Record Structure

| Field | Type | Required | Description |
|---|---|---|---|
| record_id | string | Yes | Unique identifier |
| material_a_ref | string | Yes | ID of the first material |
| material_b_ref | string | Yes | ID of the second material |
| compatibility_result | enum | Yes | compatible, incompatible, conditional, untested |
| status | enum | Yes | active, draft, deprecated |
| conditions | string | No | Conditions for conditional compatibility |
| evidence_refs | array | No | Evidence supporting the result |
| chemistry_ref | string | No | Pointer to Chemistry Kernel for mechanism |
| notes | string | No | Additional context |

## Compatibility Results

| Result | Meaning | Downstream Action |
|---|---|---|
| compatible | Materials may contact safely | No restrictions |
| incompatible | Materials must not contact | Physical separation required |
| conditional | Contact permitted under specific conditions | Conditions must be met |
| untested | No evidence for this pair | Fail-closed — treat as unknown risk |

## Common Compatibility Concerns in Division 07

| Material A | Material B | Typical Result | Concern |
|---|---|---|---|
| PVC membrane | Polystyrene insulation | Incompatible | Plasticizer migration attacks EPS/XPS |
| PVC membrane | Polyiso insulation | Conditional | Requires separation sheet |
| TPO membrane | Polyiso insulation | Compatible | No known adverse interaction |
| EPDM membrane | TPO membrane | Conditional | Different polymer families; adhesion concerns |
| Bituminous membrane | Polystyrene insulation | Incompatible | Solvents in bitumen attack polystyrene |
| Silicone sealant | Bituminous material | Incompatible | Adhesion failure |
| Urethane sealant | Concrete substrate | Compatible | Good adhesion with proper primer |

## Directionality

Compatibility records are bidirectional. If Material A is incompatible with Material B, then Material B is incompatible with Material A. A single record covers both directions.

## Compatibility Evidence

Compatibility results trace to:
- Manufacturer compatibility charts
- Independent laboratory contact tests
- Published field failure investigations
- Industry technical bulletins (NRCA, SPRI)

## Fail-Closed Rule

When no compatibility evidence exists for a material pair, the result is `untested`. No system should infer compatibility from the absence of incompatibility data. Untested pairs are surfaced to the intelligence layer for prioritized testing.

## Chemistry Kernel Boundary

This kernel records the compatibility result (what happens). The Chemistry Kernel explains the mechanism (why it happens). The optional `chemistry_ref` field links to the Chemistry Kernel's explanation without duplicating chemistry truth.
