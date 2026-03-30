# Capability Slice Catalog

**Command C — Capability Slice Architecture**
**Kernel:** KERN-INTEGRATION-MIRROR-NUCLEUS

## Overview

This directory contains the complete capability slice catalog for the Integration Mirror Nucleus kernel. A **capability slice** is a self-contained unit of functionality that can be independently activated, staged, measured, and (in some cases) transferred or promoted. Each slice encapsulates a specific domain capability — from normalizing shop drawing details to enforcing governance policies — with clearly defined inputs, outputs, dependencies, and classification metadata.

The slice architecture enables:

- **Incremental activation**: Slices can be staged (defined but inactive) or active within a specific mirror context, allowing gradual capability rollout.
- **Dependency management**: Each slice declares its required and optional dependencies, enabling the kernel to validate activation feasibility and compute processing pipelines.
- **Transfer planning**: Classification metadata (trust class, transfer class, detachability) enables systematic evaluation of which capabilities can be licensed, white-labeled, or fully transferred to external parties.
- **Parity measurement**: Slices flagged as parity-eligible can have their mirror-reflected behavior quantitatively compared against core kernel behavior.
- **Core promotion**: Slices classified as CORE_PROMOTABLE can have improvements discovered during mirror operation promoted back to the core kernel.

## Slice Inventory

| # | Slice ID | Name | GCP Shop Drawing Status |
|---|----------|------|------------------------|
| 1 | `governance` | Mirror Governance & Policy Enforcement | STAGED |
| 2 | `registry` | Mirror & Slice Lifecycle Registry | STAGED |
| 3 | `receipt_audit` | Receipt & Audit Trail Management | STAGED |
| 4 | `detail_normalization` | Detail Normalization Engine | **ACTIVE** |
| 5 | `rules_engine` | Construction Rules & Constraints Engine | **ACTIVE** |
| 6 | `validation` | Submission Validation & Completeness Verification | **ACTIVE** |
| 7 | `artifact_manifest` | Artifact Manifest & Inventory Tracker | **ACTIVE** |
| 8 | `artifact_generation` | Artifact Generation & Document Production | STAGED |
| 9 | `lineage` | Data Lineage & Provenance Tracking | **ACTIVE** |
| 10 | `execution_orchestration` | Workflow Execution Orchestration | STAGED |
| 11 | `review_support` | Human Review Support & Coordination | STAGED |
| 12 | `delivery_packaging` | Deliverable Assembly & Distribution Packaging | STAGED |
| 13 | `standards_mapping` | Construction Standards & Code Mapping | STAGED |
| 14 | `spec_ingestion` | Project Specification Ingestion & Parsing | STAGED |
| 15 | `submittal_analysis` | Submittal Analytics & Predictive Insights | STAGED |

**Active in GCP Shop Drawing mirror:** 5 slices
**Staged:** 10 slices

## How to Read a Slice Definition

Each slice is defined in a YAML file named `{slice_id}.yaml`. The structure is consistent across all slices:

```yaml
slice_id: <identifier>
name: <human-readable name>
version: <semver>
purpose: <multi-line description>
status:
  gcp_shopdrawing: ACTIVE | STAGED
  default: STAGED
inputs: [...]
outputs: [...]
required_dependencies: [...]
optional_dependencies: [...]
trust_class: <classification>
transfer_class: <classification>
detachability_level: <classification>
parity_eligibility: true | false
promotion_eligibility: true | false
classification: MIRROR_ONLY | CORE_PROMOTABLE
operational_notes: <multi-line notes>
```

## Field Reference

### Identity Fields

| Field | Type | Description |
|-------|------|-------------|
| `slice_id` | string | Unique identifier for the slice. Uses snake_case. |
| `name` | string | Human-readable name for display purposes. |
| `version` | semver | Semantic version of the slice definition. |
| `purpose` | text | Detailed description of what this slice does and why it exists. |

### Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.gcp_shopdrawing` | enum | Activation status in the GCP Shop Drawing mirror context. |
| `status.default` | enum | Default activation status for new mirror contexts. |

**Status values:**
- `ACTIVE` — The slice is operational and processing data in this mirror context.
- `STAGED` — The slice is defined and configured but not yet activated. It is ready for activation when conditions are met.

### Data Contract Fields

| Field | Type | Description |
|-------|------|-------------|
| `inputs` | list | Data inputs consumed by this slice. Each entry has `name`, `description`, `format`, and `required`. |
| `outputs` | list | Data outputs produced by this slice. Each entry has `name`, `description`, `format`, and `retention`. |

**Input entry fields:**
- `name` — Identifier for the input.
- `description` — What this input provides.
- `format` — Data format or schema type.
- `required` — Whether this input is mandatory (true) or optional (false).

**Output entry fields:**
- `name` — Identifier for the output.
- `description` — What this output contains.
- `format` — Data format or schema type.
- `retention` — How long this output is retained (e.g., `permanent`, `project_lifetime`, `365_days`, `90_days`, `30_days`, `current_state`).

### Dependency Fields

| Field | Type | Description |
|-------|------|-------------|
| `required_dependencies` | list of slice_ids | Slices that MUST be active for this slice to function. |
| `optional_dependencies` | list of slice_ids | Slices that enhance this slice's functionality when available but are not required. |

### Classification Fields

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `trust_class` | enum | `CORE_OWNED`, `MIRROR_REFLECTED`, `SHARED_GOVERNED` | Who owns and controls this slice's logic and data. |
| `transfer_class` | enum | `NON_TRANSFERABLE`, `LICENSE_ONLY`, `WHITE_LABELABLE`, `BUYOUT_READY`, `FULL_HANDOFF_READY` | How this slice's capabilities can be transferred to external parties. |
| `detachability_level` | enum | `FULLY_DETACHABLE`, `PARTIALLY_DETACHABLE`, `NON_DETACHABLE` | Whether this slice can be separated from the kernel and operate independently. |
| `classification` | enum | `MIRROR_ONLY`, `CORE_PROMOTABLE` | Whether improvements to this slice can be promoted from mirror to core. |
| `parity_eligibility` | boolean | `true`, `false` | Whether parity (behavioral equivalence) can be quantitatively measured for this slice. |
| `promotion_eligibility` | boolean | `true`, `false` | Whether reflections and improvements from this slice can be promoted to the core kernel. |

### Trust Class Values

- **CORE_OWNED** — The slice logic and data are owned entirely by the core kernel. Mirror instances execute core-provided logic without modification. Examples: governance, registry, standards_mapping.
- **MIRROR_REFLECTED** — The slice operates within a mirror context and may adapt behavior to mirror-specific requirements. The mirror has operational autonomy within policy bounds. Examples: detail_normalization, validation, spec_ingestion.
- **SHARED_GOVERNED** — The slice has shared ownership between core and mirror, with governance arbitrating conflicts. Both core and mirror may contribute logic and data. Examples: rules_engine, artifact_manifest, lineage.

### Transfer Class Values

- **NON_TRANSFERABLE** — Cannot be transferred to any external party. Intrinsic to the kernel. Examples: governance, registry.
- **LICENSE_ONLY** — Can be licensed for use but not transferred. The kernel retains ownership and control. Examples: receipt_audit, rules_engine, standards_mapping.
- **WHITE_LABELABLE** — Can be rebranded and deployed under a different identity. The logic is self-contained enough for independent operation. Examples: detail_normalization, validation, spec_ingestion.
- **BUYOUT_READY** — Can be fully purchased and transferred, including data and configuration. Examples: artifact_manifest, lineage, submittal_analysis.
- **FULL_HANDOFF_READY** — Ready for complete operational handoff to a client, including support documentation and operational procedures. Examples: review_support, delivery_packaging.

### Detachability Levels

- **FULLY_DETACHABLE** — The slice can be completely separated from the kernel and operate independently with appropriate configuration.
- **PARTIALLY_DETACHABLE** — Some components can be extracted but others are tied to kernel infrastructure.
- **NON_DETACHABLE** — The slice is intrinsic to the kernel and cannot be meaningfully separated.

## Dependency Graph

The following shows the required dependency relationships between slices:

```
spec_ingestion ──────────────────┐
                                 ├──> detail_normalization ──┐
standards_mapping ───────────────┤                           ├──> rules_engine ──┐
                                 │                           │                   │
                                 │                           ├──> validation <───┘
                                 │                           │        │
registry ──┬──> receipt_audit    │                           │        │
           │                     │                           │        │
           ├──> artifact_manifest ◄──────────────────────────┤        │
           │                     │                           │        │
           ├──> lineage          │    artifact_generation <──┘────────┘
           │                              │
           ├──> execution_orchestration   │
           │         ▲                    │
           │         │                    ▼
governance ──────────┘         delivery_packaging
                                         ▲
                                         │
review_support <── validation + detail_normalization

submittal_analysis <── validation + registry
```

## Catalog Index

The file `slice-catalog-index.yaml` provides a machine-readable index of all slices with summary metadata, dependency matrices, and classification distributions. Use this file for programmatic queries against the catalog.

## File Listing

```
capability-slices/
  README.md                        # This file
  slice-catalog-index.yaml         # Machine-readable catalog index
  governance.yaml                  # Slice: Mirror Governance & Policy Enforcement
  registry.yaml                    # Slice: Mirror & Slice Lifecycle Registry
  receipt_audit.yaml               # Slice: Receipt & Audit Trail Management
  detail_normalization.yaml        # Slice: Detail Normalization Engine
  rules_engine.yaml                # Slice: Construction Rules & Constraints Engine
  validation.yaml                  # Slice: Submission Validation & Completeness Verification
  artifact_manifest.yaml           # Slice: Artifact Manifest & Inventory Tracker
  artifact_generation.yaml         # Slice: Artifact Generation & Document Production
  lineage.yaml                     # Slice: Data Lineage & Provenance Tracking
  execution_orchestration.yaml     # Slice: Workflow Execution Orchestration
  review_support.yaml              # Slice: Human Review Support & Coordination
  delivery_packaging.yaml          # Slice: Deliverable Assembly & Distribution Packaging
  standards_mapping.yaml           # Slice: Construction Standards & Code Mapping
  spec_ingestion.yaml              # Slice: Project Specification Ingestion & Parsing
  submittal_analysis.yaml          # Slice: Submittal Analytics & Predictive Insights
```
