# Construction Interface Doctrine

## Purpose

Define governed rules for how construction assemblies declare, type, and manage interface conditions with other assemblies, building edges, and adjacent systems. Interfaces are the governed boundaries where assemblies meet their surrounding context.

---

## Interface Principle

Every point where a construction assembly meets another assembly, a building edge, or an adjacent system must be declared as an explicit, typed interface. Interfaces must not be inferred from proximity, drawing arrangement, or document co-occurrence. Undeclared interfaces are governance violations for completeness claims.

---

## Adjacent System Principle

Adjacent systems are external systems that influence conditions at assembly boundaries but are not owned components of the assembly. Adjacent systems remain external. They provide context but do not become part of the assembly's composition graph. The assembly declares the interface; it does not absorb the adjacent system.

---

## Assembly-to-Assembly Interface Rule

Where two assemblies meet at a shared boundary, both assemblies must declare the interface. The interface must be typed. The relationship must reference the adjacent assembly's governed identity where established.

---

## Assembly-to-Building-Edge Interface Rule

Where an assembly meets a building edge (roof edge, foundation, grade line, parapet cap, soffit line), the assembly must declare the edge condition as a typed interface. Building edges are not assemblies. They are boundary conditions that constrain termination, transition, or support behavior.

---

## Termination Rule

Where an assembly or component ends, the termination must be explicitly declared with a termination type. Termination types include: free edge, return, cap, drip edge, reglet, counterflashing receiver, abutment, and transition. Unterminated assemblies must be flagged as incomplete. Termination must not be inferred from drawing extent.

---

## Transition Rule

Where one assembly type transitions to another (e.g., roof membrane to wall cladding, metal panel to curtain wall), the transition must be explicitly declared. Transition interfaces must identify both the source and target assembly types. Transition conditions must specify the weatherproofing and structural continuity posture at the boundary.

---

## Penetration Rule

A penetration is an element passing through an assembly. Penetrations must be explicitly declared with penetration type, size classification, and surrounding condition. Penetrations must not be confused with openings. Penetrations create interface conditions that require sealing, flashing, or structural reinforcement.

---

## Opening Rule

An opening is a bounded void intentionally framed or formed within an assembly. Openings must be explicitly declared with opening type and framing condition. Openings create perimeter interface conditions (head, jamb, sill) that require termination and weatherproofing treatment.

Penetrations pass through. Openings are framed within. This distinction must be maintained.

---

## Support Interface Rule

Where an assembly receives structural support from an external system (structure, blocking, curb, equipment base), the support interface must be explicitly declared. Support interfaces must identify the supporting element, attachment method, and load path direction.

---

## Adjacency Interface Rule

Where an assembly is spatially adjacent to another system without direct physical connection, the adjacency must be declared as a context interface. Adjacency interfaces record coordination requirements, clearance conditions, and sequencing dependencies without implying structural attachment.

---

## Structural vs Contextual Interface Distinction

Interfaces are classified as structural or contextual:

**Structural interfaces** — direct physical connection or load transfer:
- `supported_by` — assembly receives structural support from external element
- `attached_to` — assembly is mechanically fastened to external element
- `anchored_to` — assembly is anchored into substrate or structure

**Context interfaces** — spatial or coordination relationship without direct load transfer:
- `bounded_by` — assembly extent is defined by an external boundary
- `coordinated_with` — assembly requires sequencing or clearance coordination with adjacent system
- `interfaces_with` — general typed interface declaration

Structural and contextual interfaces must not be conflated. A structural interface implies physical dependency. A context interface implies spatial or procedural relationship only.

---

## Directionality Rule

Some interface relationships are directional. Direction must be explicitly encoded where interpretation changes with direction.

Directional relationships include:
- `supported_by` — direction: from supported to supporter
- `terminates_at` — direction: from terminating element to boundary
- `discharges_to` — direction: from source to receiver
- `receives_from` — direction: from receiver to source

Bidirectional relationships (e.g., `interfaces_with`, `coordinated_with`) must be declared from at least one side. Both sides declaring the relationship strengthens the record but is not required for validity.

---

## Fail-Closed Interface Rule

If required interface context is missing or ambiguous, the assembly must be considered incomplete. Downstream systems must fail closed on completeness, buildability, and deterministic generation claims for assemblies with unresolved interfaces.

Missing interface context includes:
- Undeclared termination at a known boundary
- Undeclared penetration through the assembly
- Undeclared adjacent system where coordination is required
- Ambiguous support conditions

---

## Relationship to Other Doctrine

- **Truth Spine**: Interface changes produce truth events. Interfaces attach to governed identities.
- **Identity System**: Interfaces reference adjacent assembly identities where established. Interface declarations do not constitute identity claims.
- **Evidence System**: Interface conditions must be traceable to source evidence. Interface declarations without evidence support are provisional.
- **Composition Model**: Interfaces are declared at composition boundaries. Interface edges connect composition graphs to external context. Interfaces must not redefine composition layering.

Interfaces must not redefine identity, evidence, or composition. Interfaces declare boundary context only.

---

## Safety Note

- This document defines construction-domain governance only
- No runtime code, schemas, or implementations are modified
- This doctrine is specific to the Construction domain and does not modify root ValidKernel governance
