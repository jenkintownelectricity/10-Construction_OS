# Routing Model

## Purpose

Defines how operator queries are routed to the appropriate stack surfaces for truth retrieval.

## Routing Principle

Every query is routed to the governed system that owns the truth being requested. The assistant does not answer from its own state. It retrieves from the authoritative source.

## Routing Table

| Query Category | Target Layer | Target System | Surface Type |
|---|---|---|---|
| Domain definition (materials, geometry, assemblies) | Layer 5 | Construction_Kernel | Domain kernel truth surface |
| Governance rules (what is permitted, what is required) | Layer 5 | Construction_Kernel | Governance kernel truth surface |
| Pipeline state (parse, normalize, validate, generate, audit) | Layer 6 | Construction_Runtime | Execution state surface |
| Validation results (pass, fail, warnings) | Layer 6 | Construction_Runtime | Validation output surface |
| Application state (Assembly Parser, Spec Intelligence) | Layer 7 | Construction_Application_OS | Application state surface |
| Workflow position (what step, what next) | Layer 7 | Construction_Application_OS | Workflow state surface |
| Doctrine or foundational rules | Layer 0 | Universal_Truth_Kernel | Conceptual reference only |

## Routing Rules

1. **Single-source routing.** Each query component routes to exactly one governing system. If a query spans multiple systems, it is decomposed and each component is routed independently.
2. **No cross-layer inference.** The assistant does not combine data from multiple layers to synthesize truth. If synthesis is required, the assistant identifies which governed system should perform it.
3. **Fallback on routing failure.** If a query cannot be routed to a governed source, the assistant emits an insufficiency emission stating that no governed source is available for the query.
4. **Operator redirection.** If a query requires action (not just information), the assistant routes the operator to the appropriate system interface rather than attempting to act.
