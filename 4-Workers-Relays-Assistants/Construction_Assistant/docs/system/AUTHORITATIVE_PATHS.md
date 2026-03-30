# Authoritative Paths

## Reading Order

The following files are authoritative for this repo. They should be read in the order listed.

### System Files

1. `docs/system/REPO_MANIFEST.md` — Repo identity, purpose, owned/non-owned components, dependencies, frozen seams, mutable surfaces, cache rules.
2. `docs/system/AUTHORITATIVE_PATHS.md` — This file. Canonical reading order.
3. `docs/system/DEPENDENCY_MAP.md` — Upstream and downstream dependency relationships.
4. `docs/system/FROZEN_SEAMS.md` — Frozen boundaries that must not be altered without governance review.

### Doctrine Files

5. `docs/doctrine/assistant-doctrine.md` — Core doctrine: position, principles, constraints.
6. `docs/doctrine/truth-emission-model.md` — Four emission classes with definitions and constraints.
7. `docs/doctrine/uncertainty-and-insufficiency-policy.md` — Policy for known/unknown/insufficient/inferred states.
8. `docs/doctrine/authority-boundaries.md` — What the assistant may and must not do.
9. `docs/doctrine/routing-model.md` — Query routing to stack surfaces.

### Architecture Files

10. `docs/architecture/system-map.md` — System architecture diagram and relationships.
11. `docs/architecture/stack-position.md` — Layer position and constraints.
12. `docs/architecture/operator-model.md` — Operator interaction pattern and trust model.
13. `docs/architecture/future-expansion-notes.md` — Bounded future expansion directions (not yet built).

### Implementation Files

14. `assistant/intent_inventory.md` — Intent classes.
15. `assistant/response_modes.md` — Response modes mapped to emission classes.
16. `assistant/question_classes.md` — Question type taxonomy.
17. `assistant/guardrails.md` — Operational guardrails.

### Mapping Files

18. `maps/assistant_to_stack_map.md` — Assistant capabilities mapped to stack layers.
19. `maps/intent_to_repo_map.md` — Intent classes mapped to target repos.
20. `maps/truth_surface_map.md` — Truth surfaces the assistant may read.

### Interface Files

21. `interfaces/operator_queries.md` — Operator query interface contract.
22. `interfaces/bounded_output_contract.md` — Bounded output contract for all emissions.
23. `interfaces/no_mutation_policy.md` — Explicit no-mutation policy.

### State Files

24. `state/BASELINE_STATE.json` — Baseline state and cache configuration.
