# Degradation Mechanism Contract

## Purpose

Defines the validation rules and structural requirements for degradation mechanism records. A degradation mechanism describes how a construction chemistry material deteriorates over time due to environmental, chemical, or biological factors.

## Required Fields

- `schema_version` — Must be `"v1"`.
- `mechanism_id` — Unique identifier, prefixed `DEG-`.
- `title` — Human-readable description of the degradation process.
- `degradation_type` — Must be one of: oxidation, hydrolysis, uv_chain_scission, plasticizer_loss, thermal_decomposition, biological, chemical_attack.
- `chemistry_ref` — Reference to the affected chemistry system or family.
- `status` — Must be one of: active, draft, deprecated.

## Validation Rules

1. Every degradation mechanism must validate against `schemas/degradation_mechanism.schema.json`.
2. `mechanism_id` must be unique across all degradation mechanism records.
3. `chemistry_ref` must reference an existing chemistry system or entry.
4. `rate_factors` should describe the conditions that accelerate or decelerate degradation.
5. `climate_context` object, when present, should include relevant environmental parameters.
6. `evidence_refs` must reference valid lab test, field study, or manufacturer data records.
7. Records describing active degradation in installed systems should be flagged for inspection review.

## Consumers

- Lifecycle analysis workflows reference degradation mechanisms for service life estimation.
- Inspection protocols check for signs of active degradation by type.
- Material selection guidance warns against chemistries with known degradation risks in specific climates.

## Change Policy

New degradation mechanisms require supporting evidence. Deprecated records must retain full history for traceability.
