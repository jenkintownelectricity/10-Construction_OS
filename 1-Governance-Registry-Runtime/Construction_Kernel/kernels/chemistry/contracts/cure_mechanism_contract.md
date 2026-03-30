# Cure Mechanism Contract

## Purpose

Defines the validation rules and structural requirements for cure mechanism records. A cure mechanism describes the chemical or physical process by which a construction chemistry product transitions from its applied state to its final cured state.

## Required Fields

- `schema_version` — Must be `"v1"`.
- `mechanism_id` — Unique identifier, prefixed `CURE-`.
- `title` — Human-readable name for the cure mechanism.
- `cure_type` — Must be one of: moisture_cure, heat_cure, uv_cure, chemical_cure, evaporative, anaerobic, room_temperature_vulcanizing.
- `status` — Must be one of: active, draft, deprecated.

## Validation Rules

1. Every cure mechanism must validate against `schemas/cure_mechanism.schema.json`.
2. `mechanism_id` must be unique across all cure mechanism records.
3. Temperature fields (`min_temp_f`, `max_temp_f`) must satisfy min <= max when both are present.
4. Humidity fields (`min_humidity_pct`, `max_humidity_pct`) must be between 0 and 100.
5. `cure_time_hours` and `full_cure_days` must be positive numbers when present.
6. Moisture-cure types should set `moisture_sensitive` to true.
7. Chemical systems referencing a cure mechanism via `cure_mechanism_ref` must use a valid `mechanism_id`.

## Consumers

- Chemical system records reference cure mechanisms to define curing behavior.
- Field installation guidance depends on cure temperature and humidity constraints.
- Quality control checks verify that ambient conditions satisfy cure requirements.

## Change Policy

Cure parameter changes require manufacturer or test data backing. Deprecated mechanisms must not be removed.
