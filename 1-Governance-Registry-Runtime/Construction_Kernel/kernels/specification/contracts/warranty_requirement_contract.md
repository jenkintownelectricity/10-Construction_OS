# Warranty Requirement Contract

## Entity: warranty_requirement

## Consumer Guarantees

Any consumer reading a warranty_requirement record from this kernel can rely on:

1. **Identity** — `warranty_id` is unique and stable.
2. **Type** — `warranty_type` is one of: manufacturer_standard, manufacturer_extended, system_warranty, nol, workmanship.
3. **Duration** — `duration_years` is a number representing the warranty period in years.
4. **Status** — `status` is one of: active, draft, deprecated.
5. **Schema compliance** — the record conforms to `warranty_requirement.schema.json` with `additionalProperties: false`.

## Validation Rules

- `schema_version` must be "v1"
- `warranty_type` must be one of the defined enum values
- `duration_years` must be a number greater than or equal to 0
- `status` must be one of the defined enum values

## Semantic Guarantees

- `warranty_type: "nol"` indicates a no-dollar-limit warranty — the manufacturer covers full repair/replacement costs without prorating
- `warranty_type: "system_warranty"` covers the complete installed system, not just individual components
- `conditions` lists prerequisites for warranty validity (e.g., manufacturer inspection, authorized installer)
- `exclusions` lists items not covered by the warranty

## Immutability

Once a warranty_requirement reaches `status: active`, it is immutable.

## What This Contract Does NOT Guarantee

- That the warranty has been issued or executed
- Financial terms or coverage limits beyond type and duration
- Warranty transferability or assignment provisions
- Manufacturer's actual warranty document content
