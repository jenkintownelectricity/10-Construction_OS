# Chemistry Kernel AI Readiness Posture

## Purpose

Defines how the Chemistry Kernel's data structures support AI/ML consumption while maintaining truth integrity.

## Readiness Level

**Level: Structured and Schema-Validated, Not Embedding-Optimized**

Chemistry truth is stored as schema-validated JSON with typed IDs, enums, and explicit relationships. This is sufficient for rule-based AI consumption. Embedding-based or vector-search optimization is a future consideration.

## AI Consumption Patterns

### 1. Compatibility Checking (Rule-Based)
- **Input:** Two chemistry_ref IDs
- **Process:** Query incompatibility_rule records for the pair
- **Output:** Compatible, incompatible (with mechanism), or untested
- **AI readiness:** Full. Structured pairwise rules are directly queryable.

### 2. Cure Feasibility Assessment
- **Input:** Cure mechanism ID + environmental conditions (temp, humidity)
- **Process:** Compare conditions against cure_mechanism min/max ranges
- **Output:** Within range, outside range, or boundary condition
- **AI readiness:** Full. Numeric ranges are directly evaluable.

### 3. Degradation Risk Identification
- **Input:** Chemistry_ref + exposure conditions
- **Process:** Query degradation_mechanism records for matching chemistry
- **Output:** List of applicable degradation pathways with rate factors
- **AI readiness:** Partial. Qualitative rate factors require interpretation.

### 4. Adhesion Verification
- **Input:** Chemistry_ref + substrate_type
- **Process:** Query adhesion_rule records
- **Output:** Verified, conditional, not_recommended, or untested
- **AI readiness:** Full. Enumerated status values are directly consumable.

## Guardrails for AI Consumers

1. **Respect status flags.** Only `active` records are truth. `draft` and `deprecated` must not inform decisions.
2. **No interpolation.** AI must not interpolate between chemistry records. If no record matches, return `untested`.
3. **Evidence chain required.** Any AI output derived from chemistry truth must carry the originating record IDs for traceability.
4. **Pairwise limitation.** Incompatibility rules are pairwise. Multi-chemistry scenarios require explicit handling, not assumed transitivity.
5. **Confidence tiers.** AI consumers should propagate source confidence (Tier 1-4) through their outputs.

## Future Considerations

- Embedding representations of chemistry families for semantic search
- Graph-based traversal of the chemistry object model
- Automated evidence linking from new SDS publications
