# Submittal Requirement Contract

## Entity: submittal_requirement

## Consumer Guarantees

Any consumer reading a submittal_requirement record from this kernel can rely on:

1. **Identity** — `submittal_id` is unique and stable.
2. **Type** — `submittal_type` is one of: product_data, shop_drawing, sample, test_report, certificate, warranty, mix_design.
3. **Status** — `status` is one of: active, draft, deprecated.
4. **Title** — `title` describes what must be submitted.
5. **Schema compliance** — the record conforms to `submittal_requirement.schema.json` with `additionalProperties: false`.

## Validation Rules

- `schema_version` must be "v1"
- `submittal_type` must be one of the defined enum values
- `status` must be one of the defined enum values

## Semantic Guarantees

- A submittal requirement represents a specification obligation to provide documentation or samples for review
- `timing` indicates when the submittal must be provided relative to construction activities
- `review_requirement` indicates the level of review required (architect action, information only, etc.)

## Immutability

Once a submittal_requirement reaches `status: active`, it is immutable.

## What This Contract Does NOT Guarantee

- That the submittal has been provided or reviewed (tracking is outside kernel scope)
- Specific formatting requirements for submittals
- Completeness of timing or review_requirement fields
