# Construction Scope Boundary Doctrine

## Purpose

Define governed rules for how construction scope boundaries, responsibility ownership, and coordination obligations are declared and enforced. Scope boundaries determine what work belongs to which responsible party and prevent automated systems from absorbing responsibility belonging to other trades.

---

## Scope Boundary Principle

Scope boundaries define ownership of construction responsibility. Every construction condition that affects buildability, drawing generation, or truth assertions must carry an explicit scope classification. Adjacent systems may influence conditions at assembly boundaries but do not transfer ownership of responsibility to the assembly owner.

---

## Scope Classifications

| Classification | Description |
|---|---|
| `in_scope` | The condition is within the declared responsibility of the assembly owner |
| `out_of_scope` | The condition is explicitly outside the declared responsibility of the assembly owner |
| `by_others` | The condition is the responsibility of another identified trade or party |
| `coordination_required` | The condition requires coordination between multiple parties before responsibility can be fully resolved |

Every scope-bearing condition must carry exactly one of these classifications. Unclassified conditions are governance violations.

---

## Trade-Neutral Rule

Scope boundaries must remain trade-neutral. The model describes responsibility conditions without embedding contractor assumptions, trade-specific naming conventions, or organizational hierarchies. Scope classifications reference responsibility, not specific companies, subcontractors, or trade unions.

---

## Scope Declaration Rule

Assemblies and conditions must explicitly declare scope classification. Scope must not be inferred from:
- Document authorship
- Drawing sheet ownership
- File path or directory structure
- Contractor name or trade label

Scope classification is a governed declaration, not a derived property.

---

## Fail-Closed Scope Rule

If scope ownership cannot be determined, the condition must be marked unresolved. The system must not:
- Default to `in_scope` when ownership is unclear
- Silently absorb `by_others` work into owned assemblies
- Treat `coordination_required` as resolved without explicit determination
- Proceed to drawing generation for conditions with unresolved scope

---

## Scope Precedence Rule

If two assemblies claim conflicting scope ownership over the same condition:
- The system must mark the condition as unresolved
- The system must not infer or override scope ownership
- The conflict must be surfaced for governed resolution
- Silent precedence assignment is a governance violation

---

## Conflict Detection Rule

Conflicting scope classifications must trigger an unresolved coordination condition. When detected:
- Both conflicting classifications must be preserved
- Resolution must occur through governed determination
- The determination must record which classification was accepted and the basis for the decision
- Silent replacement of conflicting scope claims is a governance violation

---

## Relationship to Other Doctrine

- **Identity System**: Scope classifications attach to governed identities. Scope does not replace or redefine identity.
- **Evidence System**: Scope determinations must be traceable to source evidence (contracts, specifications, scope documents). Scope without evidence support is provisional.
- **Composition Model**: Scope boundaries may align with composition boundaries but must not redefine composition structure. Scope classification is a property of a condition, not a structural relationship.
- **Interface Model**: Scope boundaries often coincide with interface conditions. Interface declarations identify where assemblies meet; scope declarations identify who is responsible. These are distinct concerns.

Scope must reference these models but must not redefine them.

---

## Safety Note

- This document defines construction-domain governance only
- No runtime code, schemas, or implementations are modified
- This doctrine is specific to the Construction domain and does not modify root ValidKernel governance
