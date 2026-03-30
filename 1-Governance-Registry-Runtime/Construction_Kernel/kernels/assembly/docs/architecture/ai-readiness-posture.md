# AI Readiness Posture — Construction Assembly Kernel

## Purpose

This document defines how the Construction Assembly Kernel structures its data for consumption by AI systems, language models, and automated reasoning tools.

## Structural Readiness

### Schema-First Design

Every kernel object type has a formal JSON Schema (2020-12) with:
- Explicit `required` fields — AI systems know which fields are guaranteed present
- Enum constraints — finite, enumerable value sets for classification fields
- `additionalProperties: false` — no unexpected fields; parseable with confidence
- Consistent `schema_version` — version tracking enables migration-aware consumers

### Consistent Identifiers

All objects use string identifiers (`system_id`, `layer_id`, `transition_id`, etc.) that are stable across revisions. AI systems can build and maintain relationship graphs using these identifiers.

### Typed Relationships

Cross-object references use explicit `_ref` suffixed fields (`assembly_ref`, `material_ref`, `spec_ref`). AI systems can resolve these references to traverse the object graph without ambiguity.

## Semantic Readiness

### Control-Layer Vocabulary

The 11 control-layer IDs from the shared registry provide a consistent semantic vocabulary. AI systems can reason about assembly function using these IDs without interpreting free-text descriptions.

### Interface Zone Vocabulary

The 10 interface zone IDs provide semantic anchors for spatial reasoning about assembly boundaries and transitions.

### Enum-Based Classification

Assembly types, component types, edge types, penetration types, tie-in types, continuity statuses, and risk levels are all enum-constrained. AI systems can classify, filter, and aggregate using these values.

## Query Patterns Supported

The kernel structure supports these AI query patterns:

1. **Assembly decomposition** — Given a system_id, retrieve all layers, their control-layer assignments, and their material references.
2. **Continuity analysis** — For a given control layer, find all assemblies where it is continuous, interrupted, or terminated.
3. **Interface risk assessment** — Retrieve all transitions and penetrations at a given risk level.
4. **Standards compliance** — Find all tested assembly records for a given test standard.
5. **Climate-filtered queries** — Retrieve assemblies applicable to a given climate zone or exposure condition.
6. **Evidence tracing** — Follow evidence references from assembly records to test reports and field observations.

## Limitations for AI Consumers

- The kernel provides structured truth, not inference. AI systems must not treat absence of data as negative evidence.
- Ambiguity flags (`ambiguity_flag: true`, `status: draft`) signal records that require human judgment.
- Material properties and chemical behavior must be resolved through sibling kernel references, not assumed from assembly data.
- Standards compliance is recorded as tested, not inferred. AI systems must not extrapolate compliance to untested configurations.

## Future Readiness

The kernel structure is designed to support:
- Embedding-based similarity search across assembly configurations
- Graph-based reasoning across assembly-transition-penetration networks
- Automated continuity verification across assembly boundaries
- Natural language query interfaces backed by schema-validated data
