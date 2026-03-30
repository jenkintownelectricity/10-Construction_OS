# Construction Scope Kernel Doctrine

## Purpose

The Construction Scope Kernel is the single source of truth for scope-domain knowledge within the construction kernel family. Scope defines the boundaries of work, trade responsibilities, operation sequencing, inspection steps, commissioning steps, and closeout requirements.

## Core Principles

1. **Scope is boundary truth.** Every scope record defines what is included, what is excluded, and where responsibility transfers between trades.
2. **Fail-closed by default.** If a work item is not explicitly included in scope, it is out of scope. Ambiguity is never resolved by assumption.
3. **Trade coordination is scope truth.** Interface zones between trades are scope boundaries. Miscoordination at interfaces is a scope failure.
4. **Sequencing is scope truth.** The order in which work operations occur, and the dependencies between them, are scope-domain facts.
5. **Inspection and commissioning are scope truth.** Quality verification steps, hold points, and BECx milestones are governed by scope.
6. **Closeout is scope truth.** Warranty handoff, as-built documentation, and punch list resolution are scope-domain deliverables.

## Domain Boundaries

This kernel owns scope truth for CSI Division 07 -- Building Envelope Systems, including:

- Roofing systems (07 50 00)
- Waterproofing (07 10 00)
- Air barriers (07 27 00)
- Thermal insulation (07 21 00)
- Flashing and sheet metal (07 60 00)
- Sealants and joint treatment (07 90 00)
- Fireproofing (07 81 00)
- Membrane systems (07 50 00, 07 10 00)

## What This Kernel Does NOT Own

- Material specifications (Spec Kernel)
- Assembly instructions (Assembly Kernel)
- Material properties and chemistry (Material Kernel)
- Reference standards content (Reference Intelligence)

## Fail-Closed Enforcement

When scope is ambiguous or undefined:

1. The item is flagged as a **scope gap**.
2. No trade is assigned responsibility until the gap is resolved.
3. The gap is surfaced to human reviewers with full context.
4. Resolution requires explicit scope definition, not inference.

## Governance

- All scope records carry a `status` field: `active`, `draft`, or `deprecated`.
- Changes to scope truth require revision lineage tracking.
- Scope records reference CSI section numbers for standards alignment.
