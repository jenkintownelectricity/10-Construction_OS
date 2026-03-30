# Assembly Composition Consumption Note

## Purpose

Document how Construction_Runtime consumes composition rules defined by the Construction Assembly Composition Model and Assembly Graph.

---

## Consumption Rule

Runtime consumes composition rules defined in:
- `Construction_Kernel/docs/system/CONSTRUCTION_ASSEMBLY_COMPOSITION_MODEL.md`
- `Construction_Kernel/docs/system/CONSTRUCTION_ASSEMBLY_GRAPH.md`

Governed by:
- `Construction_Kernel/docs/governance/construction-assembly-composition-doctrine.md`

---

## Runtime Constraints

- Runtime consumes composition rules. Runtime does not define them.
- Runtime must not invent missing components or relationships silently.
- Runtime must not infer layer order from document position or drawing arrangement.
- Runtime must not create untyped nodes or edges in composition structures.
- Runtime must fail closed where composition is incomplete or ambiguous.
- Runtime must not treat partial or stub compositions as complete.

---

## Scope

Runtime behavior is not modified in this pass. This document records the consumption relationship only.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
