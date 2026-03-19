# Material Model Consumption Note

## Purpose

Document how Construction_Runtime consumes material taxonomy and compatibility rules defined by the Construction Material Taxonomy and Compatibility Model.

---

## Consumption Rule

Runtime consumes material rules defined in:
- `Construction_Kernel/docs/system/CONSTRUCTION_MATERIAL_TAXONOMY.md`
- `Construction_Kernel/docs/system/CONSTRUCTION_MATERIAL_COMPATIBILITY_MODEL.md`

Governed by:
- `Construction_Kernel/docs/governance/construction-material-doctrine.md`

---

## Runtime Constraints

- Runtime consumes canonical material classes. Runtime does not define them.
- Runtime must not invent material classes not present in the canonical taxonomy.
- Runtime must not substitute manufacturer product names for canonical material classes.
- Runtime must not assume compatibility where no rule exists.
- Runtime must fail closed on assemblies referencing undefined material classes.
- Runtime must fail closed on unknown material compatibility.

---

## Scope

Runtime behavior is not modified in this wave. This document records the consumption relationship only.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
