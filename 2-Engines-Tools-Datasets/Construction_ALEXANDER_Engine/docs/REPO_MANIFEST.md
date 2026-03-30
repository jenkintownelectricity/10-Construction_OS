# Construction ALEXANDER Engine — Repo Manifest

## Identity

| Field | Value |
|-------|-------|
| Repo | Construction_ALEXANDER_Engine |
| Type | Ring 2 Pattern Intelligence Engine |
| Owner | Armand Lefebvre |
| Authority | L0 |
| Schema Version | 1.0.0 |

## Purpose

ALEXANDER is the governed pattern resolver that consumes pattern truth from
Construction_Pattern_Language_OS and emits deterministic advisory resolution
outputs. It resolves ConditionSignature inputs into PatternFamily → Pattern →
PatternVariant → ArtifactIntent proposals.

## Authority Boundary

### May Consume
- Construction_Pattern_Language_OS (governed pattern truth)
- Construction_Atlas (spatial context)
- Construction_Reference_Intelligence (reference intelligence)

### May Emit
- Proposals (advisory pattern resolution proposals)
- Observations (resolution status, anomalies, constraint violations)
- Internal ResolutionResult (structured resolution outputs)

### May NOT
- Define canonical truth
- Mutate any kernel
- Render artifacts
- Bypass the Cognitive Bus
- Emit execution commands
- Introduce intelligence into Runtime

## Resolution Pipeline

```
ConditionSignature
  → Intake (validate shape)
  → Normalization (canonical form)
  → Family Classification (map to PatternFamily)
  → Pattern Resolution (narrow within family)
  → Variant Selection (select by dimensions/method/materials)
  → Constraint Enforcement (fail-closed on violations)
  → Conflict Detection (emit conflict records)
  → Scoring (machine-readable score breakdown)
  → ResolutionResult
```

## Fail-Closed Policy

All stages fail closed. If any required truth, context, or reference data is
missing, incompatible, ambiguous, or conflicting, the engine emits an
UNRESOLVED, BLOCKED, or CONFLICT result with explicit fail reason codes.
No guessing. No silent failures.

## Resolution Status Enum

| Status | Meaning |
|--------|---------|
| RESOLVED | Full resolution completed successfully |
| UNRESOLVED | Could not resolve — missing data or no match |
| BLOCKED | Resolution blocked — ambiguous or constraint violation |
| CONFLICT | Conflict detected between patterns |

## Directory Structure

```
Construction_ALEXANDER_Engine/
├── manifest/           # Engine manifest with authority boundary
├── engine/             # Core engine modules
│   ├── config.py       # Constants and configuration
│   ├── condition_intake.py    # ConditionSignature validation
│   ├── normalizer.py          # Deterministic normalization
│   ├── family_classifier.py   # Family classification
│   ├── pattern_resolver.py    # Pattern resolution
│   ├── variant_selector.py    # Variant selection
│   ├── constraint_engine.py   # Constraint enforcement
│   ├── conflict_detector.py   # Conflict detection
│   ├── scoring_engine.py      # Score calculation
│   ├── resolution_pipeline.py # Main orchestrator
│   └── event_emitter.py       # Cognitive Bus event builder
├── contracts/          # Consumer contracts
│   └── pattern_kernel_consumer.py  # Pattern Language OS consumer
├── schemas/            # JSON schemas
│   ├── condition_signature.schema.json
│   ├── resolution_result.schema.json
│   ├── proposal_event.schema.json
│   └── observation_event.schema.json
├── tests/              # Unit and integration tests
└── docs/               # Documentation
```
