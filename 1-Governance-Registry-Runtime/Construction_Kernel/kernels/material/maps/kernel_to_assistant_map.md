# Kernel-to-Assistant Map — Construction Material Kernel

## Status: Stub

No AI assistant integration currently exists. This map will be populated when AI assistant interfaces are implemented.

## Planned Assistant Integration Points

| Integration Point | Purpose | Status |
|---|---|---|
| Material property lookup | Natural language queries for property values | Not implemented |
| Compatibility check | Ask about material pair compatibility | Not implemented |
| Weathering data retrieval | Query degradation behavior by material and exposure | Not implemented |
| Standards reference lookup | Find applicable test methods for a material class | Not implemented |

## Assistant Design Constraints

1. Assistants have read-only access to active records
2. Assistants must present evidence references with property values
3. Assistants must surface ambiguity flags and data gaps
4. Assistants must respect truth boundaries — no speculation beyond published data
5. Assistants must not generate material recommendations (non-goal)
