# Kernel-to-Family Map — Construction Scope Kernel

## Purpose

This map defines how the Construction Scope Kernel fits within the broader construction-kernel family.

## Family Position

The Construction Scope Kernel is a **domain kernel** within the ValidKernel construction-kernel family. It owns the truth about scope boundaries, trade responsibilities, inspection requirements, commissioning steps, closeout deliverables, and warranty handoffs.

## Sibling Kernels

- **Construction Detail Kernel** — Owns constructible detail truth (assemblies, layers, materials).
- **Construction QA Kernel** — Owns quality assurance truth (test methods, acceptance criteria).
- **Construction Standards Kernel** — Owns code and standards truth (IBC, IECC, ASTM references).
- **Construction Scheduling Kernel** — Owns sequencing and schedule truth.

## Relationship to Siblings

- Scope records reference detail assemblies by ID but do not embed detail truth.
- Scope records reference QA test methods by ID but do not own test procedures.
- Scope records reference standards by section number but do not store code text.
- Scope sequencing defines execution order but does not own calendar scheduling.

## Shared Artifacts

- Interface zone identifiers are shared across the family via the shared registry.
- Control layer taxonomy is shared across the family.
- CSI MasterFormat section numbers are shared across the family.

## Governance

- Each kernel owns its own schema, contracts, and truth records.
- Cross-kernel references use string identifiers, never embedded objects.
- No kernel imports runtime behavior from another kernel.
- Schema changes require versioned updates across the family.

## Principles

- The scope kernel is authoritative for scope truth. No sibling kernel may override scope boundaries.
- All cross-kernel references are loosely coupled and validated at integration time.
- The family shares a common schema_version convention ("v1") for compatibility.
