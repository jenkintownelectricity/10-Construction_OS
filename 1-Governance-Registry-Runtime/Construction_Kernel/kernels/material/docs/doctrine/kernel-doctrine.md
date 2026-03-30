# Kernel Doctrine — Construction Material Kernel

## Purpose

The Construction Material Kernel is the single source of material-domain truth for the construction-kernel family. It records material facts — physical properties, tested performance characteristics, compatibility relationships, weathering behavior, hygrothermal properties, and material-to-control-layer mappings — for CSI Division 07 (Building Envelope Systems).

## Core Principles

### 1. Single Source of Material Truth

Every material fact exists in exactly one place within this kernel. No other kernel in the family (Specification, Assembly, Chemistry, Scope) duplicates material truth. Other kernels and the intelligence layer read material truth from this kernel via structured pointers.

### 2. Fail-Closed Governance

If a material property cannot be validated against published test data or manufacturer technical data sheets, it is rejected. No material record is committed without a traceable evidence pointer. Missing data does not default to permissive — it defaults to flagged-and-blocked. When property values are uncertain, `ambiguity_flag: true` is set and downstream consumers must not treat the record as resolved.

### 3. Materials Characterized by Physical Properties

Materials are identified by their physical properties, material class, and tested performance — never by brand name, trade name, or manufacturer identity. A "60-mil reinforced thermoplastic polyolefin membrane" is characterized by its tensile strength, elongation, thickness, permeance, and fire classification. The manufacturer name is not part of the material truth surface.

### 4. Standards-Aware Without Copying Standards Text

This kernel references ASTM test methods and material standards by citation only. It never reproduces copyrighted standards text. Standards references use the shared_standards_registry.json from the family shared artifacts. The kernel records which test method defines a property, not what the test method says.

### 5. Immutable Committed Records

Once a material record reaches `active` status, it becomes immutable. Changes produce new revision records with lineage pointers to the superseded record. Draft records may be edited before commitment. Original records transition to `deprecated` status — they are never deleted.

### 6. Schema-First Structure

Every material entity conforms to a JSON Schema (2020-12). Schemas enforce required fields, enum constraints from shared registries, and `additionalProperties: false` to prevent schema drift. Schema versions are frozen per baseline and advance only through explicit version increments.

### 7. Evidence Traceability

Every material property traces to an evidence source via `evidence_ref`. Evidence sources include laboratory test reports, manufacturer technical data sheets, field performance data, and forensic analysis reports. Unsourced property claims are not admitted into the kernel.

## Governing References

- Family shared artifacts: `Construction_Reference_Intelligence/shared/`
- Enum values: `shared_enum_registry.json`
- Standards citations: `shared_standards_registry.json`
- Control layers: `control_layers.json`
- Interface zones: `interface_zones.json`
- Taxonomy: `shared_taxonomy.json`

## Doctrine Enforcement

All records entering this kernel must pass schema validation. Records missing required fields are rejected. Records with unrecognized enum values are rejected. Records without evidence pointers are rejected. Active records are append-only; deprecated records are never deleted. There are no exceptions.
