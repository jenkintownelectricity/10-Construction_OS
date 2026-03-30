# Assistant-to-Stack Map

## Purpose

Maps assistant capabilities to the stack layers they depend on.

## Capability Map

| Assistant Capability | Stack Layer | System | Surface Used |
|---|---|---|---|
| Domain fact retrieval | Layer 5 | Construction_Kernel | Domain kernel truth surfaces (Governance, Geometry, Chemistry, Assembly, Reality, Deliverable, Intelligence) |
| Governance rule lookup | Layer 5 | Construction_Kernel | Governance kernel truth surface |
| Pipeline state query | Layer 6 | Construction_Runtime | Execution state surface (parse, normalize, validate, generate, audit) |
| Validation result query | Layer 6 | Construction_Runtime | Validation output surface |
| Application state query | Layer 7 | Construction_Application_OS | Application state surface (Assembly Parser, Spec Intelligence) |
| Workflow position query | Layer 7 | Construction_Application_OS | Workflow state surface |
| Next valid action derivation | Layer 7 | Construction_Application_OS | Workflow state surface |
| Lineage tracing | Layer 5 | Construction_Kernel | Source reference metadata |
| Conflict detection query | Layer 5 + Layer 6 | Construction_Kernel + Construction_Runtime | Domain truth + validation surfaces |
| Completeness check query | Layer 6 + Layer 7 | Construction_Runtime + Construction_Application_OS | Validation + application state surfaces |

## Capabilities Not Mapped to Any Layer

| Capability | Reason |
|---|---|
| Emission classification | Internal to assistant. No upstream dependency. |
| Query routing | Internal to assistant. Uses routing model, not upstream query. |
| Guardrail enforcement | Internal to assistant. Structural constraint. |

## Doctrinal Reference

| Reference | Layer | System | Relationship |
|---|---|---|---|
| Root doctrine alignment | Layer 0 | Universal_Truth_Kernel | Conceptual reference only. No runtime consumption. |
