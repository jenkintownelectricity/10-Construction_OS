# Truth Ownership Statement

**Document ID:** CPLOS-GOV-TRUTH-001
**Date:** 2026-03-22
**Authority:** Armand Lefebvre, L0
**Status:** ACTIVE

## Purpose

This document establishes the explicit truth ownership boundary between
Construction_Kernel and Construction_Pattern_Language_OS. No authority
overlap is permitted. Any unresolved conflict halts all downstream
consumption.

## Ownership Matrix

| Truth Domain | Owner | Non-Owner | Boundary Rule |
|---|---|---|---|
| Construction detail patterns (families, patterns, variants) | **Construction_Pattern_Language_OS** | Construction_Kernel | Kernel consumes pattern definitions; it does not define them |
| Pattern relationships (adjacency, conflict, dependency) | **Construction_Pattern_Language_OS** | Construction_Kernel | Kernel references relationship IDs; it does not author relationships |
| Pattern variant materials and methods | **Construction_Pattern_Language_OS** | Construction_Kernel | Kernel may reference variant IDs; it does not define material composition |
| Artifact intents (shop drawing, specification, submittal, inspection) | **Construction_Pattern_Language_OS** | Construction_Kernel | Kernel does not define what artifacts a pattern produces |
| Constraint profiles (manufacturer, code, dimensional, environmental) | **Construction_Pattern_Language_OS** | Construction_Kernel | Kernel does not define constraint parameters |
| Pattern identifier assignment and format | **Construction_Pattern_Language_OS** | Construction_Kernel | Kernel uses assigned IDs; it does not allocate or modify them |
| Construction truth structures and contracts | **Construction_Kernel** | Construction_Pattern_Language_OS | CPLOS does not define assembly schemas, drawing schemas, or revision schemas |
| Condition pattern library (triggers, evaluation, boundary constraints) | **Construction_Kernel** | Construction_Pattern_Language_OS | CPLOS defines detail patterns, not condition evaluation logic |
| Assembly composition and layer structure | **Construction_Kernel** | Construction_Pattern_Language_OS | CPLOS defines variants with materials; Kernel defines how assemblies compose |
| Graph backbone (node/edge types, traversal rules) | **Construction_Kernel** | Construction_Pattern_Language_OS | CPLOS defines pattern relationships; Kernel defines the graph reference model |
| Issue typing, blocker typing, remediation references | **Construction_Kernel** | Construction_Pattern_Language_OS | CPLOS does not define issue taxonomies or remediation strategies |
| QA constraints, export contracts, drawing packages | **Construction_Kernel** | Construction_Pattern_Language_OS | CPLOS does not define QA rules or export formats |
| Evidence schemas and field types | **Construction_Kernel** | Construction_Pattern_Language_OS | CPLOS does not define evidence structures |
| Root doctrine (3 frozen sentences) | **Universal_Truth_Kernel** | Both | Neither kernel redefines root doctrine |

## Consumption Direction

```
Universal_Truth_Kernel (Layer 0 — root doctrine)
        ↓ operates within
ValidKernel_Patterns (structural patterns — CPLOS parent)
        ↓ grown from
Construction_Pattern_Language_OS (pattern truth — families, patterns, variants, relationships)
        ↓ consumed by
Construction_Kernel (construction truth — contracts, schemas, condition patterns)
        ↓ consumed by
Construction_Runtime (execution — deterministic processing)
```

## Dependency Edge

```
Construction_Kernel --[consumes-pattern-definitions]--> Construction_Pattern_Language_OS
```

Construction_Kernel depends on Construction_Pattern_Language_OS for pattern
definitions. Construction_Pattern_Language_OS does NOT depend on
Construction_Kernel.

## Conflict Resolution Protocol

1. If both repos claim authority over the same truth domain, HALT.
2. The truth domain must be assigned to exactly one owner.
3. The non-owner must remove or demote the conflicting content.
4. Resolution requires L0 approval.
5. Until resolved, no downstream consumer may reference the contested domain.

## What Construction_Pattern_Language_OS Owns

- Pattern families (`DNA-CONSTR-FAM-*`)
- Patterns (`DNA-CONSTR-PAT-*`)
- Pattern variants (`CHEM-CONSTR-VAR-*`)
- Pattern relationships (`SOUND-CONSTR-REL-*`)
- Artifact intents (`COLOR-CONSTR-ART-*`)
- Constraint profiles (`TEXTURE-CONSTR-CNS-*`, `CLIMATE-CONSTR-CNS-*`)
- Identifier format and assignment rules
- Entity hierarchy: PatternFamily → Pattern → PatternVariant
- JSON Schema definitions for all pattern entities
- Validators for pattern structural integrity

## What Construction_Pattern_Language_OS Does NOT Own

- Root doctrine (Universal_Truth_Kernel)
- Structural repo patterns (ValidKernel_Patterns)
- Assembly schemas, drawing schemas, revision schemas (Construction_Kernel)
- Condition pattern evaluation logic (Construction_Kernel)
- Graph backbone model (Construction_Kernel)
- Runtime execution (Construction_Runtime)
- Rendering, visualization, UI (Construction_Application_OS)
- Topology authority (Construction_OS_Registry)
- Reasoning or inference logic (any intelligence layer)

## Immutability

This statement is frozen upon acceptance. Changes require L0 governance
review and explicit authorization. The ownership matrix above is the
single source of truth for domain boundary adjudication.
