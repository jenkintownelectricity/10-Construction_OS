# Prohibition Contract

## Entity: prohibition

## Consumer Guarantees

Any consumer reading a prohibition record from this kernel can rely on:

1. **Identity** — `prohibition_id` is unique and stable.
2. **Title** — `title` provides a human-readable description of what is prohibited.
3. **Status** — `status` is one of: active, draft, deprecated. Active prohibitions are current.
4. **Schema compliance** — the record conforms to `prohibition.schema.json` with `additionalProperties: false`.

## Validation Rules

- `schema_version` must be "v1"
- `prohibition_id` must be a non-empty string
- `title` must be a non-empty string
- `status` must be one of the defined enum values
- `conditions`, if present, is an array of strings

## Semantic Guarantees

- A prohibition represents an explicit "shall not" or "do not" statement from the specification
- Prohibitions are absolute within their stated conditions
- If `conditions` is present, the prohibition applies only under those conditions
- If `conditions` is absent, the prohibition applies unconditionally

## Immutability

Once a prohibition reaches `status: active`, it is immutable. Changes create new records; the original transitions to deprecated.

## What This Contract Does NOT Guarantee

- Completeness of conditions (the spec may have unstated conditions)
- Conflict resolution with allowances (conflicts require human review)
- Enforcement (the kernel records prohibitions, it does not enforce them)
