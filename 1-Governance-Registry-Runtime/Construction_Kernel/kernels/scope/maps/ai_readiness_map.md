# AI Readiness Map — Construction Scope Kernel

## Purpose

This map documents the machine-readability posture of the Construction Scope Kernel and confirms that no execution leakage exists in any kernel artifact.

## Machine-Readability

All scope kernel records are designed for machine consumption:

| Property | Status |
|----------|--------|
| Schema format | JSON Schema 2020-12 |
| Record format | JSON |
| Identifier convention | String-based, unique per entity type |
| Enumerated values | Closed enums in all classification fields |
| Reference style | String IDs, no embedded objects |
| Additional properties | Forbidden (additionalProperties: false) |
| Required fields | Explicitly declared in every schema |

## Structured for AI Consumption

- Every record has a `schema_version` field for compatibility detection.
- Every record has a `status` field (active, draft, deprecated) for lifecycle filtering.
- All enums are lowercase_snake_case for consistent tokenization.
- All descriptions are concise and unambiguous for LLM interpretation.
- Array fields use string items for uniform reference resolution.

## No Execution Leakage

The following guarantees hold across all kernel artifacts:

| Guarantee | Enforcement |
|-----------|-------------|
| No executable code in schemas | Schemas are pure JSON Schema; no $code, no scripts |
| No behavioral logic in contracts | Contracts use MUST/SHOULD/MAY rules, not if/then logic |
| No runtime state in records | Records are truth snapshots, not stateful objects |
| No event handlers | No on_change, on_create, or trigger definitions exist |
| No API endpoints | The kernel defines no routes, endpoints, or protocols |
| No database queries | The kernel defines no SQL, GraphQL, or query syntax |

## Validation Readiness

- All schemas can be validated with any JSON Schema 2020-12 validator.
- All records can be validated against their schema without runtime context.
- Contract rules can be checked with static analysis tools.

## Integration Readiness

- AI assistants can read scope records to answer scope boundary questions.
- AI agents can read trade_responsibility records to identify coordination gaps.
- AI validators can check records against schemas and contracts programmatically.
- Reference intelligence layers can index all scope records by ID, type, and status.

## Principles

- Machine-readability is a first-class design requirement, not an afterthought.
- Human-readability is preserved through title and description fields.
- No kernel artifact requires human interpretation to be machine-processable.
- Execution leakage is treated as a defect and MUST be corrected immediately.
