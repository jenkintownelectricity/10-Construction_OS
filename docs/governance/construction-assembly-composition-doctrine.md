# Construction Assembly Composition Doctrine

## Purpose

Define governed rules for how construction assemblies are composed from components, how compositional relationships are typed and bounded, and how composition integrity is maintained across the truth lifecycle.

---

## Composition Principle

Construction assemblies are composed of discrete, typed components connected by explicit, typed relationships. Composition is not implied by proximity, naming, or document co-occurrence. Every compositional relationship must be explicit, typed, and traceable.

---

## Assembly vs Component Distinction

An assembly is a governed, identity-bearing construction object that represents a buildable configuration. A component is a constituent part of an assembly that contributes to the assembly's physical realization.

- Assemblies carry governed identity.
- Components exist within the context of their parent assembly.
- A component may itself be an assembly when it carries independent identity and truth history.
- The assembly/component distinction is structural, not a matter of scale.

---

## Bounded Graph Rule

The composition of an assembly must form a bounded, acyclic, typed graph. The graph must have a single root assembly node. Every node must be reachable from the root. No cycles are permitted. No orphan nodes are permitted within a composition graph.

If a composition graph cannot be fully resolved, the system must fail closed on completeness claims for that assembly.

---

## Typed Relationship Rule

Every relationship in an assembly composition must carry an explicit type. Untyped relationships are governance violations. Relationship types are defined by the Construction Assembly Composition Model and must not be invented ad hoc by runtime or downstream consumers.

---

## Layering Rule

Assemblies may contain layered compositions where components occupy ordered positions within a build-up sequence. Layer order must be explicit. Layer boundaries must be defined. Implicit layering inferred from document order or drawing position is not valid.

---

## Support/Attachment Rule

Components that provide structural support, backing, blocking, or attachment for other components must have their support role explicitly typed in the composition. Support relationships must not be inferred from proximity alone.

---

## Interface Rule

Where an assembly meets another assembly, a building edge, or an adjacent system, the interface must be explicitly declared. Interfaces are composition boundaries. Undeclared interfaces are governance violations for completeness claims.

---

## Fail-Closed Incomplete Composition Rule

If an assembly's composition is incomplete, ambiguous, or contains unresolved relationships, the system must fail closed on completeness and buildability claims for that assembly. Incomplete composition must be explicitly marked. The system must not treat incomplete compositions as buildable.

---

## Relationship to Truth Spine / Identity / Evidence

- Composition attaches to identity. Components reference their parent assembly's governed identity.
- Composition changes are truth events. Adding, removing, or modifying components produces events in the truth spine.
- Evidence supports composition claims. The composition of an assembly must be traceable to source evidence.
- Composition does not replace identity. Two assemblies with identical composition are not thereby the same object.
- Composition does not replace evidence. Compositional similarity is a matching signal, not an identity proof.

---

## Safety Note

- This document defines construction-domain governance only
- No runtime code, schemas, or implementations are modified
- This doctrine is specific to the Construction domain and does not modify root ValidKernel governance
