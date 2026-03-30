# AI Readiness Posture

## Purpose

Defines the Scope Kernel's posture toward AI and machine consumption of scope data. All scope records are structured for deterministic machine parsing, not free-text interpretation.

## Readiness Level

**Level: Structured and Queryable**

All scope objects are defined by JSON Schema with strict typing, required fields, and controlled enums. No free-text fields carry load-bearing scope truth -- `notes` fields are advisory only.

## AI-Safe Design Principles

### 1. Enumerated Scope Types
Scope types, operation types, inspection types, commissioning phases, and closeout types are all controlled enums. AI systems consume enums, not free text.

### 2. Explicit References
All cross-object references use explicit ID fields (`scope_ref`, `trade_ref`, `step_id`). AI systems traverse references, not implied relationships.

### 3. Fail-Closed for AI
If an AI system encounters a scope gap, it must surface the gap to a human. The kernel does not provide fallback defaults for missing scope assignments.

### 4. Status-Aware Consumption
AI consumers must filter by `status: active`. Draft records are not authoritative. Deprecated records must not be used for current scope queries.

## Machine-Readable Outputs

| Artifact | Format | AI Use Case |
|---|---|---|
| Scope of Work | JSON | Trade coordination queries |
| Work Operations | JSON | Sequencing validation |
| Trade Responsibilities | JSON | Responsibility matrix generation |
| Inspection Steps | JSON | QA checklist generation |
| Commissioning Steps | JSON | BECx tracking |
| Closeout Requirements | JSON | Project closeout dashboards |

## Constraints on AI Interpretation

- AI must not infer scope from adjacent records. Each scope record is self-contained.
- AI must not merge overlapping scope records without human authorization.
- AI must not generate scope records autonomously. Scope authoring requires human input.
- AI may flag potential scope gaps by analyzing missing references across the object graph.

## Future Readiness

The schema structure supports future graph-based queries, semantic search over scope objects, and automated scope gap detection. No schema changes are required to enable these capabilities.
