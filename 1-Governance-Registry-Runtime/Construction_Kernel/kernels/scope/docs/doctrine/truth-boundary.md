# Truth Boundary Declaration

## Scope Kernel Truth Domain

The Construction Scope Kernel owns exactly one domain of truth: **scope**.

Scope truth encompasses:

- **Work boundaries** -- what is included and excluded from a given scope of work
- **Trade responsibilities** -- which trade is responsible for which scope items
- **Interface zones** -- where scope boundaries meet between trades
- **Operation sequencing** -- the order of work operations and their dependencies
- **Inspection steps** -- quality verification checkpoints within scope
- **Commissioning steps** -- BECx phases tied to scope deliverables
- **Closeout requirements** -- warranty, as-built, and handoff obligations
- **Division alignment** -- mapping scope items to CSI Division 07 sections

## What This Kernel Does NOT Own

| Truth Domain | Owning Kernel | Relationship to Scope |
|---|---|---|
| Specifications | Spec Kernel | Scope references spec sections but does not define them |
| Assembly procedures | Assembly Kernel | Scope sequences operations but does not define how to assemble |
| Material properties | Material Kernel | Scope identifies materials in use but does not define their properties |
| Chemical behavior | Material Kernel | Scope is agnostic to chemistry |
| Reference standards | Reference Intelligence | Scope references standards but does not interpret their content |
| Product data | Product Kernel | Scope identifies products in use but does not evaluate them |
| Cost data | Cost Kernel | Scope defines work items but does not price them |

## Boundary Enforcement Rules

1. If a query asks "what material should I use," the Scope Kernel returns: **out of domain -- refer to Spec Kernel**.
2. If a query asks "how do I install this," the Scope Kernel returns: **out of domain -- refer to Assembly Kernel**.
3. If a query asks "what is the R-value," the Scope Kernel returns: **out of domain -- refer to Material Kernel**.
4. If a query asks "who is responsible for flashing at the roof-to-wall transition," the Scope Kernel answers from its trade responsibility model.

## Cross-Kernel References

Scope records may contain references to other kernel domains using pointer fields:

- `spec_ref` -- points to Spec Kernel records
- `assembly_ref` -- points to Assembly Kernel records
- `material_ref` -- points to Material Kernel records
- `standard_ref` -- points to Reference Intelligence records

These are outbound references only. The Scope Kernel does not resolve or validate them.
