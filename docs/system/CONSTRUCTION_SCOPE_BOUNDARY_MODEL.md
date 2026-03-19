# Construction Scope Boundary Model

## Purpose

Define the canonical model for scope boundaries, responsibility ownership, and coordination obligations within the Construction domain. This model enables deterministic reasoning about what work belongs to which responsible party, preventing automated systems from absorbing or inferring responsibility belonging to other trades.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Identity System
    → Assembly Composition Model
    → Interface and Adjacent Systems Model
    → Scope Boundary Model  ← this document
    → Product / Material Model
    → View Intent Model
    → Drawing Instruction IR
    → Construction_Runtime
```

The Scope Boundary Model sits after the Interface Model. Interfaces define where assemblies meet. Scope defines who is responsible. Scope boundaries consume interface context but do not redefine it.

---

## Scope-Bearing Objects

The following construction objects commonly carry scope declarations:

| Object | Typical Scope Context |
|---|---|
| Roof assembly | Primary scope of roofing trade; interfaces with structural, mechanical, electrical |
| Parapet condition | Often shared scope between roofing and masonry/cladding trades |
| Curb condition | Scope may belong to roofing, mechanical, or general contractor depending on contract |
| Drain condition | Plumbing scope below deck; roofing scope for flashing and membrane integration |
| Penetration condition | By-others for the penetrating element; in-scope for sealing and flashing |
| Expansion joint condition | Often coordination-required between multiple trades |
| Coping condition | May be roofing, masonry, or sheet metal scope depending on contract |
| Flashing condition | Typically roofing scope but may require coordination with adjacent trades |
| Edge condition | Scope depends on assembly type and contract allocation |

---

## Scope Classifications

| Classification | Description |
|---|---|
| `in_scope` | Within the declared responsibility of the assembly owner |
| `out_of_scope` | Explicitly outside the declared responsibility of the assembly owner |
| `by_others` | Responsibility of another identified trade or party |
| `coordination_required` | Requires coordination between multiple parties before scope can be resolved |

---

## Scope Attributes

| Attribute | Description |
|---|---|
| `scope_owner` | The responsible party for the condition (trade-neutral identifier) |
| `scope_classification` | One of: `in_scope`, `out_of_scope`, `by_others`, `coordination_required` |
| `coordination_parties` | List of parties involved in coordination (populated when `coordination_required`) |
| `coordination_condition` | Description of the specific coordination requirement |

---

## Scope Determination Inputs

Scope classification draws on the following inputs:

- **Contract scope** — the contractual allocation of work responsibility
- **Trade responsibility** — the trade-standard responsibility for the condition type
- **Adjacent system ownership** — the declared owner of the adjacent system at the interface
- **Interface obligations** — coordination requirements arising from interface conditions

No single input is deterministic. Scope classification requires governed evaluation of available inputs.

---

## Unresolved Scope Rule

Assemblies lacking scope classification cannot proceed to:
- Drawing generation
- Buildability claims
- Detail applicability resolution
- Package release

The system must fail closed on all downstream operations for conditions with unresolved scope.

---

## Graph Discipline Rule

Scope edges must remain separate from composition edges and interface edges. Scope relationships must not modify structural composition graphs. Scope is a property attached to conditions and assemblies, not a structural relationship within the composition graph.

---

## Coordination Obligation Model

### Purpose

Explicitly model coordination responsibilities between trades to prevent ambiguity and dispute. Coordination obligations declare required collaboration without transferring scope ownership.

### Coordination Obligation Types

| Obligation | Description |
|---|---|
| `requires_coordination_with` | This condition requires coordination with another trade |
| `provides_interface_to` | This assembly provides a receiving condition for another trade's work |
| `receives_interface_from` | This assembly receives a condition provided by another trade |
| `dependent_on_trade` | This condition cannot be completed until another trade completes their work |

### Example

```
Roofing assembly
  → requires_coordination_with: HVAC penetration
  → provides_interface_to: HVAC curb flashing

HVAC penetration
  → dependent_on_trade: roofing flashing
  → receives_interface_from: roofing curb flashing
```

### Coordination Rule

Coordination obligations declare required collaboration but do not transfer scope ownership. A `requires_coordination_with` declaration means the parties must collaborate. It does not mean the other party's work becomes `in_scope`.

### Ownership Protection Rule

Coordination obligations must never override scope classification. If a coordination obligation exists, the scope classification of each party's work remains independently governed. Coordination is a procedural relationship. Scope is a responsibility determination.

### Unresolved Coordination Rule

If a coordination obligation exists but the responsible adjacent trade is unknown:
- The condition must be marked unresolved
- The system must fail closed on downstream operations for that condition
- The system must not infer the responsible trade from naming, position, or document context

### Escalation Rule

Unresolved coordination conditions must be surfaced to review workflows rather than inferred automatically. No automated system may resolve coordination ambiguity without governed determination. Escalation is the correct response to unresolved coordination, not inference.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Governance doctrine: `Construction_Kernel/docs/governance/construction-scope-boundary-doctrine.md`
