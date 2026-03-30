# Authoritative Paths — Construction Specification Kernel

## Repository Structure

The following directories are the authoritative paths within this kernel. Only files within these paths constitute kernel truth. Files outside these paths are not governed by kernel doctrine.

## Authoritative Directories

### kernel/

Kernel model files defining the conceptual foundations of the specification kernel. Contains truth models, taxonomy definitions, context models, and the kernel version overview.

- `kernel/CONSTRUCTION_SPECIFICATION_KERNEL_V0.1.md` — Version overview
- `kernel/truth_model.md` — What constitutes specification truth
- `kernel/taxonomy.md` — CSI Division 07 taxonomy
- `kernel/requirement_model.md` — Requirement structure and obligation levels
- `kernel/source_model.md` — Source document types and traceability
- `kernel/reference_model.md` — Standards and code references
- `kernel/evidence_model.md` — Evidence supporting compliance
- `kernel/obligation_model.md` — Obligation level definitions
- `kernel/interface_model.md` — Interface zone specification coverage
- `kernel/climate_context_model.md` — Climate-dependent requirements
- `kernel/geometry_context_model.md` — Geometry-dependent requirements
- `kernel/lifecycle_context_model.md` — Lifecycle stage applicability
- `kernel/revision_lineage_model.md` — Revision chains and supersession
- `kernel/standards_reference_model.md` — Standards citation protocol
- `kernel/evidence_linkage_model.md` — Evidence-to-requirement linkage
- `kernel/division07_taxonomy.md` — Detailed Division 07 section mapping

### schemas/

JSON Schema (2020-12) definitions for all kernel entities. Every schema enforces `additionalProperties: false` and explicit required fields.

### contracts/

Markdown contracts defining the commitments each entity type makes to consumers. Contracts specify what fields are guaranteed, what validation rules apply, and what consumers can rely on.

### maps/

Relationship maps showing how kernel entities connect to each other, to sibling kernels, to the intelligence layer, and to future runtime hooks.

### examples/

Realistic JSON examples conforming to kernel schemas. Examples use Division 07 content and demonstrate proper field usage.

### state/

Baseline state tracking. Contains `BASELINE_STATE.json` recording the current baseline version, pass number, and artifact inventory.

### docs/

Documentation organized into three subdirectories:
- `docs/doctrine/` — Core doctrine and governance principles
- `docs/architecture/` — Architectural decisions and posture documents
- `docs/system/` — System-level coordination files

### shared/

Contains `SHARED_ARTIFACTS_POINTER.md` pointing to the canonical shared artifacts in `Construction_Reference_Intelligence/shared/`. No shared artifact data is stored here.

## Non-Authoritative Paths

Files in `.git/`, temporary files, and any files outside the directories listed above are not kernel truth and are not governed by kernel doctrine.
