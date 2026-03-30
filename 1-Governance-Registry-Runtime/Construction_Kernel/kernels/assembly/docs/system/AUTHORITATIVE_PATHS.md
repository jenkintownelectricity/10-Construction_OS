# Authoritative Paths — Construction Assembly Kernel

## Purpose

Defines the canonical file paths for all truth surfaces, schemas, and governance artifacts in this kernel. Any system reading from or writing to this kernel must use these paths.

## Schema Paths

| Schema | Path | Status |
|---|---|---|
| Assembly Entry (generic) | `schemas/assembly_entry.schema.json` | Active — original entry schema |
| Assembly System | `schemas/assembly_system.schema.json` | Active |
| Assembly Layer | `schemas/assembly_layer.schema.json` | Active |
| Assembly Component | `schemas/assembly_component.schema.json` | Active |
| Control Layer Assignment | `schemas/control_layer_assignment.schema.json` | Active |
| Transition Condition | `schemas/transition_condition.schema.json` | Active |
| Penetration Condition | `schemas/penetration_condition.schema.json` | Active |
| Edge Condition | `schemas/edge_condition.schema.json` | Active |
| Tie-In Condition | `schemas/tie_in_condition.schema.json` | Active |
| Tested Assembly Record | `schemas/tested_assembly_record.schema.json` | Active |
| Continuity Requirement | `schemas/continuity_requirement.schema.json` | Active |

## Doctrine Paths

| Document | Path |
|---|---|
| Kernel Doctrine | `docs/doctrine/kernel-doctrine.md` |
| Truth Boundary | `docs/doctrine/truth-boundary.md` |
| Non-Goals | `docs/doctrine/non-goals.md` |
| Interpretation Limitations | `docs/doctrine/interpretation-limitations.md` |

## Architecture Paths

| Document | Path |
|---|---|
| Kernel Scope | `docs/architecture/kernel-scope.md` |
| Object Model Overview | `docs/architecture/object-model-overview.md` |
| Standards Alignment | `docs/architecture/standards-alignment.md` |
| Division 07 Alignment | `docs/architecture/division07_alignment.md` |
| Interface Risk Posture | `docs/architecture/interface-risk-posture.md` |
| AI Readiness Posture | `docs/architecture/ai-readiness-posture.md` |
| Reference Intelligence Linkage | `docs/architecture/reference-intelligence-linkage.md` |
| Lifecycle Posture | `docs/architecture/lifecycle-posture.md` |
| Climate Posture | `docs/architecture/climate-posture.md` |
| Geometry Posture | `docs/architecture/geometry-posture.md` |

## System Paths

| Document | Path |
|---|---|
| Repository Manifest | `docs/system/REPO_MANIFEST.md` |
| Frozen Seams | `docs/system/FROZEN_SEAMS.md` |
| Dependency Map | `docs/system/DEPENDENCY_MAP.md` |
| Authoritative Paths | `docs/system/AUTHORITATIVE_PATHS.md` (this file) |
| Family Shared Pointer | `docs/system/FAMILY_SHARED_POINTER.md` |

## Kernel Model Paths

| Model | Path |
|---|---|
| Kernel V0.1 | `kernel/CONSTRUCTION_ASSEMBLY_KERNEL_V0.1.md` |
| Truth Model | `kernel/truth_model.md` |
| Taxonomy | `kernel/taxonomy.md` |
| Assembly Model | `kernel/assembly_model.md` |
| Control Layer Model | `kernel/control_layer_model.md` |
| Transition Model | `kernel/transition_model.md` |
| Penetration Model | `kernel/penetration_model.md` |
| Tested Assembly Model | `kernel/tested_assembly_model.md` |
| Continuity Model | `kernel/continuity_model.md` |
| Standards Reference Model | `kernel/standards_reference_model.md` |
| Evidence Linkage Model | `kernel/evidence_linkage_model.md` |
| Interface Model | `kernel/interface_model.md` |
| Revision Lineage Model | `kernel/revision_lineage_model.md` |
| Lifecycle Context Model | `kernel/lifecycle_context_model.md` |
| Climate Context Model | `kernel/climate_context_model.md` |
| Geometry Context Model | `kernel/geometry_context_model.md` |

## State and Shared Paths

| Artifact | Path |
|---|---|
| Baseline State | `state/BASELINE_STATE.json` |
| Shared Artifacts Pointer | `shared/SHARED_ARTIFACTS_POINTER.md` |

## Path Rules

1. All paths are relative to the repository root.
2. Schemas use `.schema.json` suffix.
3. Examples use `.example.json` suffix.
4. No path may be renamed without updating all references and frozen seam documentation.
