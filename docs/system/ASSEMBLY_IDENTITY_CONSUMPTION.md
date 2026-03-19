# Assembly Identity Consumption

## Purpose

Document how Construction_Runtime consumes identity rules defined by the Construction Assembly Identity System.

---

## Consumption Rule

Runtime consumes identity and evidence rules defined in `Construction_Kernel/docs/system/CONSTRUCTION_ASSEMBLY_IDENTITY_SYSTEM.md` and governed by `Construction_Kernel/docs/governance/construction-assembly-identity-doctrine.md`.

---

## Runtime Constraints

- Runtime must not infer object identity from labels, titles, sheet positions, drawing callouts, or document paths.
- Runtime must not establish identity continuity without governed evidence.
- Runtime must fail closed where identity continuity is unresolved.
- Runtime must not define identity rules. Identity rules are defined by Construction_Kernel.

---

## Scope

Runtime behavior is not modified in this pass. This document records the consumption relationship only.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
