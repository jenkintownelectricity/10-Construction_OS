# Testing Requirement Contract

## Entity: testing_requirement

## Consumer Guarantees

Any consumer reading a testing_requirement record from this kernel can rely on:

1. **Identity** — `testing_id` is unique and stable.
2. **Type** — `test_type` is one of: field_test, lab_test, mock_up, preconstruction.
3. **Status** — `status` is one of: active, draft, deprecated.
4. **Title** — `title` describes the required test.
5. **Schema compliance** — the record conforms to `testing_requirement.schema.json` with `additionalProperties: false`.

## Validation Rules

- `schema_version` must be "v1"
- `test_type` must be one of the defined enum values
- `status` must be one of the defined enum values

## Semantic Guarantees

- `test_method_ref` cites the specific test standard (e.g., "ASTM D4541") — the standard itself must be obtained separately
- `acceptance_criteria` states the pass/fail threshold as written in the specification
- `timing` indicates when relative to construction the test must occur
- `frequency` indicates how often the test must be repeated

## Test Type Semantics

- `field_test` — performed on installed work in actual project conditions
- `lab_test` — performed in a laboratory on material samples
- `mock_up` — full-scale or representative-scale construction for evaluation
- `preconstruction` — testing performed before production installation begins

## Immutability

Once a testing_requirement reaches `status: active`, it is immutable.

## What This Contract Does NOT Guarantee

- That the test has been performed or passed
- Test results or reports (those are evidence, not specification truth)
- Testing agency qualifications (those are separate qualification_requirement records)
- Weather or condition requirements for testing
