# Frozen Seams — Construction Material Kernel

## Purpose

Frozen seams define the stable interface contracts between this kernel and external consumers. Once a seam is frozen, its schema, field names, enum values, and response structure are immutable within the current baseline. Changes require a new baseline version.

## Frozen Seam Registry

| Seam ID | Name | Direction | Status |
|---|---|---|---|
| SEAM-MATL-001 | Material Class Query | Outbound | Frozen v1 |
| SEAM-MATL-002 | Material Property Query | Outbound | Frozen v1 |
| SEAM-MATL-003 | Compatibility Lookup | Outbound | Frozen v1 |
| SEAM-MATL-004 | Weathering Behavior Query | Outbound | Frozen v1 |
| SEAM-MATL-005 | Hygrothermal Property Query | Outbound | Frozen v1 |
| SEAM-MATL-006 | Standards Reference Lookup | Outbound | Frozen v1 |
| SEAM-MATL-007 | Evidence Linkage Query | Outbound | Frozen v1 |
| SEAM-MATL-008 | Shared Enum Ingest | Inbound | Frozen v1 |
| SEAM-MATL-009 | Shared Taxonomy Ingest | Inbound | Frozen v1 |

## Seam Freeze Rules

1. A seam is frozen when it is referenced by at least one external consumer
2. Frozen seams are append-only — new optional fields may be added; existing fields are never removed or renamed
3. Enum values in frozen seams are append-only — new values may be added; existing values are never removed
4. Breaking changes require a new seam version (SEAM-MATL-001-v2) and a deprecation period for the old version
5. Frozen seam definitions are stored in the contracts directory

## Current Baseline

- Baseline: `construction-kernel-pass-2`
- Freeze date: 2026-03-17
- All v1 seams frozen at this baseline

## Seam Validation

Seam compliance is validated through schema validation. Any record crossing a frozen seam must conform to the seam's schema. Invalid records are rejected at the boundary.
