# Incompatibility Rule Contract

## Purpose

Defines the validation rules and structural requirements for incompatibility rule records. An incompatibility rule captures a known adverse interaction between two chemistry systems or materials.

## Required Fields

- `schema_version` — Must be `"v1"`.
- `rule_id` — Unique identifier, prefixed `INCOMPAT-`.
- `title` — Human-readable description of the incompatibility.
- `chemistry_a_ref` — Reference to the first chemistry system or family.
- `chemistry_b_ref` — Reference to the second chemistry system or family.
- `incompatibility_type` — Must be one of the defined enum values (adhesion_failure, chemical_attack, plasticizer_migration, staining, corrosion, off_gassing, cure_inhibition).
- `severity` — Must be one of: critical, high, medium, low.
- `status` — Must be one of: active, draft, deprecated.

## Validation Rules

1. Every incompatibility rule must validate against `schemas/incompatibility_rule.schema.json`.
2. `rule_id` must be unique across all incompatibility rule records.
3. `chemistry_a_ref` and `chemistry_b_ref` must reference existing chemistry records.
4. `chemistry_a_ref` and `chemistry_b_ref` must not be identical.
5. `mechanism` should describe the chemical or physical basis when provided.
6. `evidence_refs` must reference valid lab test or field observation records.
7. Critical severity rules must include at least one evidence reference.

## Consumers

- Design review workflows flag incompatible material pairings.
- Inspection checklists verify that incompatible materials are not in contact.
- AI assistants reference these rules for material substitution recommendations.

## Change Policy

Severity downgrades require documented evidence. Critical rules cannot be deprecated without replacement.
