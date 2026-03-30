# Construction Specification Kernel v0.1

## Version Overview

Version 0.1 establishes the foundational structure of the Construction Specification Kernel. This version defines the core object model, schema definitions, truth boundaries, and governance doctrine for specification-domain truth within the construction-kernel family.

## Scope

- **Domain:** CSI Division 07 — Thermal and Moisture Protection (Building Envelope Systems)
- **Truth surface:** Specification documents, sections, requirements, prohibitions, allowances, submittals, testing, warranties, qualifications, standards references, source pointers, revisions
- **Schema version:** v1 (JSON Schema 2020-12)
- **Baseline:** construction-kernel-pass-2

## What v0.1 Includes

### Core Object Model
Twelve entity types with corresponding JSON Schemas, all enforcing `additionalProperties: false`, explicit required fields, and enum values from shared registries.

### Doctrine
- Single source of specification truth
- Fail-closed governance
- Standards-aware without copying standards text
- Immutable committed records
- As-written fidelity with ambiguity flagging

### Shared Artifact Integration
Consumption of control layers, interface zones, enums, standards, and taxonomy from `Construction_Reference_Intelligence/shared/` via pointer reference.

### Division 07 Taxonomy
Complete mapping of Division 07 CSI sections to control layers and interface zones, covering waterproofing, insulation, air barriers, vapor retarders, membrane roofing, flashing, firestopping, and sealants.

### Context Models
Climate context, geometry context, and lifecycle context models enabling specification requirements to carry structured environmental and temporal metadata.

## What v0.1 Does NOT Include

- Runtime hooks or execution surfaces
- Worker, assistant, or digital twin integrations
- Cross-division expansion beyond Division 07
- Automated specification authoring
- Compliance evaluation logic

## Future Versions

- **v0.2** — Example data population, validation tooling stubs
- **v0.3** — Cross-kernel pointer validation, sibling kernel coordination
- **v1.0** — Production-ready schema set with migration tooling

## Governing State

Current state is tracked in `state/BASELINE_STATE.json`. The kernel_id is `KERN-CONST-SPEC` and the kernel is registered in `ValidKernel_Registry`.
