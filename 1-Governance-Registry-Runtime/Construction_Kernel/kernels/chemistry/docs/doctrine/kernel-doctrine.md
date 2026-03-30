# Chemistry Kernel Doctrine

## Purpose

The Construction Chemistry Kernel is the single source of chemistry-domain truth for the construction-kernel family. All chemical behavior data — compatibility, cure chemistry, adhesion profiles, solvent interactions, VOC constraints, and degradation mechanisms — originates from and is governed by this kernel.

## Core Principles

1. **Chemistry governs compatibility at the molecular level.** Physical proximity of materials is meaningless without verified chemical compatibility. This kernel provides the chemical behavior data that determines whether two materials can coexist.

2. **Fail-closed by default.** If chemical compatibility between two systems is not verified by evidence in this kernel, the combination is treated as incompatible. No assumption of compatibility is permitted.

3. **Evidence-backed truth only.** Every chemistry fact must trace to a verifiable source: manufacturer SDS, published lab test data, peer-reviewed research, or ASTM/ISO test results. Anecdotal field observations may inform investigation but do not constitute truth.

4. **Chemistry truth is distinct from material truth.** This kernel owns how chemicals behave — reactions, cure mechanisms, adhesion behavior, solvent effects, degradation pathways. The Material Kernel owns what materials are — density, tensile strength, dimensions, thermal conductivity.

5. **Standards-aware, not standards-reproducing.** This kernel references ASTM, ISO, and regulatory standards by identifier. It does not copy or reproduce standards text.

6. **Immutable lineage.** Every chemistry record carries revision lineage. Deprecated records are never deleted; they are marked deprecated with a reason and superseded-by reference.

## Governance

- All chemistry entries require `status` field: `active`, `draft`, or `deprecated`.
- Draft entries may not be consumed by downstream systems.
- Active entries require at least one evidence reference.
- Deprecation requires a reason and must reference the superseding entry if one exists.

## Boundary Enforcement

This kernel rejects any request to store, interpret, or adjudicate:
- Physical material properties (Material Kernel)
- Assembly sequencing or detailing (Assembly Kernel)
- Specification clauses or submittals (Specification Kernel)
- Scope or trade responsibility (Scope Kernel)
- Intelligence synthesis or recommendations (Reference Intelligence layer)

## Consumption Model

Downstream consumers (assembly kernel, reference intelligence, runtime agents) consume chemistry truth via schema-validated JSON records. This kernel publishes; it does not subscribe.
