# Requirement Contract

## Entity: requirement

## Consumer Guarantees

Any consumer reading a requirement record from this kernel can rely on:

1. **Identity** — `requirement_id` is unique and stable.
2. **Obligation level** — `obligation_level` is one of: shall, should, may. This field is always present.
3. **Status** — `status` is one of: active, draft, deprecated. Active requirements are current obligations.
4. **Title** — `title` provides a human-readable description of the requirement.
5. **Schema compliance** — the record conforms to `requirement.schema.json` with `additionalProperties: false`.
6. **Ambiguity transparency** — if `ambiguity_flag` is true, the requirement contains known ambiguous language. Consumers must not treat it as fully resolved.

## Validation Rules

- `schema_version` must be "v1"
- `obligation_level` must be one of the defined enum values
- `control_layers` values, if present, must be valid control layer IDs
- `interface_zones` values, if present, must be valid interface zone IDs
- `lifecycle_stage`, if present, must be a valid lifecycle stage enum value

## Interpretation Rules

- `obligation_level: "shall"` — mandatory; non-compliance is a specification violation
- `obligation_level: "should"` — recommended; deviation requires justification
- `obligation_level: "may"` — permissive; establishes what is allowed

## Immutability

Once a requirement reaches `status: active`, it is immutable. Changes produce new requirement records linked through the revision lineage model. The original record transitions to `status: deprecated`.

## What This Contract Does NOT Guarantee

- Completeness of optional fields (climate_context, geometry_context, etc.)
- Resolution of ambiguity flags (resolution requires human action outside the kernel)
- Existence of referenced source pointers or standards
- Compliance status (the kernel records requirements, not compliance)
