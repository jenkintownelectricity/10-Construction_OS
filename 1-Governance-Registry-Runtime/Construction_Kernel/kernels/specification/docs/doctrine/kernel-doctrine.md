# Kernel Doctrine — Construction Specification Kernel

## Purpose

The Construction Specification Kernel is the single source of specification-domain truth for the construction-kernel family. It records specification facts — requirements, prohibitions, allowances, submittals, testing, warranties, qualifications, and standards references — as written in project specifications and referenced standards for CSI Division 07 (Building Envelope Systems).

## Core Principles

### 1. Single Source of Specification Truth

Every specification fact exists in exactly one place within this kernel. No other kernel in the family (Assembly, Material, Chemistry, Scope) duplicates specification truth. Other kernels and the intelligence layer read specification truth from this kernel via structured pointers.

### 2. Fail-Closed Governance

If a specification fact cannot be validated against its source document, it is rejected. No specification record is committed without a traceable source pointer. Missing data does not default to permissive — it defaults to flagged-and-blocked. When ambiguity exists, `ambiguity_flag: true` is set and downstream consumers must not treat the record as resolved.

### 3. Standards-Aware Without Copying Standards Text

This kernel references standards (IBC, ASTM, AAMA, NFPA, ASHRAE) by citation only. It never reproduces copyrighted standards text. Standards references use the shared_standards_registry.json from the family shared artifacts. The kernel records which standard applies, not what the standard says.

### 4. Immutable Committed Records

Once a specification record reaches `active` status, it becomes immutable. Changes produce new revision records with lineage pointers to the superseded record. Draft records may be edited before commitment. The revision_posture field governs mutability per the shared_enum_registry.json. Original records transition to `deprecated` status — they are never deleted.

### 5. As-Written Fidelity

Specification facts are recorded as written in the source document. This kernel does not interpret, extrapolate, or infer meaning beyond what the source states. Obligation language (shall/should/may) is captured exactly as it appears. Ambiguous specifications are flagged with `ambiguity_flag: true` and routed for human resolution.

### 6. Schema-First Structure

Every specification entity conforms to a JSON Schema (2020-12). Schemas enforce required fields, enum constraints from shared registries, and `additionalProperties: false` to prevent schema drift. Schema versions are frozen per baseline and advance only through explicit version increments.

### 7. Source Traceability

Every specification fact traces to a source document via `source_ref`. Sources include project manuals, addenda, RFIs, bulletins, and standards body publications. Unsourced facts are not admitted into the kernel.

## Governing References

- Family shared artifacts: `Construction_Reference_Intelligence/shared/`
- Enum values: `shared_enum_registry.json`
- Standards citations: `shared_standards_registry.json`
- Control layers: `control_layers.json`
- Interface zones: `interface_zones.json`
- Taxonomy: `shared_taxonomy.json`

## Doctrine Enforcement

All records entering this kernel must pass schema validation. Records missing required fields are rejected. Records with unrecognized enum values are rejected. Records without source pointers are rejected. Active records are append-only; deprecated records are never deleted. There are no exceptions.
