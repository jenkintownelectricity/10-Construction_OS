# Adhesion Rule Contract

## Purpose

Defines the validation rules and structural requirements for adhesion rule records. An adhesion rule captures the verified or conditional adhesion relationship between a chemistry system and a substrate type.

## Required Fields

- `schema_version` — Must be `"v1"`.
- `rule_id` — Unique identifier, prefixed `ADH-`.
- `title` — Human-readable description of the adhesion relationship.
- `substrate_type` — The substrate material (e.g., concrete, aluminum, EPDM).
- `chemistry_ref` — Reference to a chemical system or chemistry entry.
- `adhesion_status` — Must be one of: verified, conditional, not_recommended, untested.
- `status` — Must be one of: active, draft, deprecated.

## Validation Rules

1. Every adhesion rule must validate against `schemas/adhesion_rule.schema.json`.
2. `rule_id` must be unique across all adhesion rule records.
3. `chemistry_ref` must reference an existing chemical system or chemistry entry.
4. If `primer_required` is true, `primer_ref` should reference a valid primer system.
5. If `test_method_ref` is provided, it should reference a recognized test standard (e.g., ASTM C794).
6. `evidence_refs` entries must reference valid evidence records when provided.
7. `min_temp_f` constrains the lowest application temperature for the adhesion claim.

## Consumers

- Specification writers use adhesion rules to validate sealant-substrate pairings.
- Inspection workflows check adhesion status before approving joint installations.
- Incompatibility checks cross-reference adhesion rules for conflict detection.

## Change Policy

Adhesion status changes require supporting evidence. Deprecated rules must retain history.
