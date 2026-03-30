# Capability Slice Model

## Overview

A capability slice is the fundamental unit of functionality governance within a mirror. Every discrete capability that a mirror exposes must be declared as a slice. Slices are how Construction OS sells, enables, disables, detaches, and governs individual integration capabilities.

Slices are not arbitrary subdivisions — they represent meaningful, bounded capabilities that a customer or operator would recognize as a distinct feature or function. A slice has clear inputs, clear outputs, declared dependencies, and a known cost of detachment.

---

## What a Capability Slice Is

A capability slice is a declared, bounded unit of functionality within a mirror that:

1. **Serves a single, identifiable purpose** — Each slice does one thing that can be described in one sentence.
2. **Has explicit boundaries** — The inputs, outputs, and dependencies are fully declared.
3. **Is independently governable** — It can be enabled, disabled, assessed, and detached independently of other slices (respecting dependency declarations).
4. **Is the unit of commercial packaging** — Slices are what get sold, licensed, or transferred.
5. **Is the unit of detachment** — Slices are what get removed during breakaway operations.

---

## Required Fields

Every capability slice declaration must include all of the following fields. Missing any required field makes the slice declaration invalid, which in turn makes the parent mirror invalid (validity rule 2).

### slice_id
- **Type:** String
- **Format:** `SLICE-{MIRROR_ID}-{SEQUENTIAL_NUMBER}` (e.g., `SLICE-MIRROR-PROCORE-001`)
- **Description:** Globally unique identifier for this slice within the Construction OS ecosystem.
- **Constraints:** Immutable once assigned. Must be registered.

### purpose
- **Type:** String (1-500 characters)
- **Description:** A clear, human-readable description of what this slice does. Must be understandable without prior context.
- **Example:** "Reflects project schedule milestones from Procore into Construction OS project timeline view."

### inputs
- **Type:** Array of input declarations
- **Description:** Every data input this slice consumes, including source, format, frequency, and whether the input is required or optional.
- **Structure per input:**
  - `input_id`: Unique identifier within the slice
  - `source`: Where the input comes from (source system entity, Construction OS entity, or another slice)
  - `format`: Data format or schema reference
  - `frequency`: How often the input is consumed (real-time, periodic with interval, on-demand)
  - `required`: Boolean indicating whether the slice can function without this input

### outputs
- **Type:** Array of output declarations
- **Description:** Every data output this slice produces, including destination, format, and freshness guarantee.
- **Structure per output:**
  - `output_id`: Unique identifier within the slice
  - `destination`: Where the output is sent (Construction OS reflection surface, another slice, external callback)
  - `format`: Data format or schema reference
  - `freshness_guarantee`: Maximum age of the output data before it is considered stale

### required_dependencies
- **Type:** Array of dependency declarations
- **Description:** Every dependency that must be available for this slice to function. If any required dependency is unavailable, the slice cannot operate.
- **Structure per dependency:**
  - `dependency_id`: Identifier of the dependency
  - `dependency_type`: Type of dependency (SLICE, PLATFORM_SERVICE, EXTERNAL_SERVICE, DATA_SOURCE)
  - `description`: What this dependency provides to the slice
  - `failure_impact`: What happens if this dependency becomes unavailable

### optional_dependencies
- **Type:** Array of dependency declarations
- **Description:** Dependencies that enhance the slice's functionality but are not required for basic operation. The slice operates in a degraded mode without these.
- **Structure:** Same as required_dependencies, plus:
  - `degradation_description`: How the slice behaves when this dependency is absent

### trust_class
- **Type:** Enum
- **Allowed values:**
  - `TRUSTED` — The slice operates within a fully verified trust boundary with strong isolation guarantees.
  - `VERIFIED` — The slice has been reviewed and its trust boundary has been assessed, but some trust assumptions remain.
  - `PROVISIONAL` — The slice is operating under provisional trust while full verification is pending. Requires enhanced monitoring.
  - `UNTRUSTED` — The slice has not been trust-verified. It may only operate in sandboxed environments.
- **Description:** The trust classification determines what level of access and isolation applies to this slice.

### transfer_class
- **Type:** Enum
- **Allowed values:**
  - `NON_TRANSFERABLE` — This slice cannot be handed off to another party. It is bound to Construction OS.
  - `LICENSE_ONLY` — This slice may be licensed for use by another party but ownership remains with Construction OS.
  - `WHITE_LABELABLE` — This slice may be rebranded and presented under another party's name.
  - `BUYOUT_READY` — This slice has met all transfer gate conditions and may be purchased by another party. Requires transfer gate pass.
  - `FULL_HANDOFF_READY` — This slice may be completely handed over to another party with all artifacts, documentation, and operational knowledge. Requires transfer gate pass.
- **Description:** Governs what commercial and operational transactions are permitted for this slice.

### detachability_level
- **Type:** Enum
- **Allowed values:**
  - `FULLY_DETACHABLE` — This slice can be removed immediately with no side effects on Construction OS core or other slices.
  - `DETACHABLE_WITH_MIGRATION` — This slice can be removed, but some data or configuration migration is required first. The migration steps are documented.
  - `DETACHABLE_WITH_NOTICE` — This slice can be removed, but dependent systems or tenants must be notified and given time to adjust. The notice period and dependencies are documented.
- **Description:** Declares how easily this slice can be disconnected from the mirror and Construction OS.

### version
- **Type:** String (semantic versioning)
- **Format:** `MAJOR.MINOR.PATCH`
- **Description:** The current version of this slice declaration. Version changes follow semantic versioning rules.

### parity_eligibility
- **Type:** Boolean
- **Description:** Whether this slice is subject to parity verification. Most slices are parity-eligible. A slice may be ineligible only if it provides a capability that has no corresponding source system truth to verify against (e.g., a transformation-only slice).

### promotion_eligibility
- **Type:** Enum
- **Allowed values:**
  - `MIRROR_ONLY` — This slice is inherently tied to the mirror's source system and cannot be promoted to core.
  - `CORE_PROMOTABLE` — This slice's functionality could potentially be promoted into Construction OS core if it passes the promotion gate.
- **Description:** Whether the functionality provided by this slice is a candidate for promotion into Construction OS core.

---

## How Slices Attach to Mirrors

### Attachment Rules

1. **Every slice belongs to exactly one mirror.** A slice cannot be shared across mirrors. If two mirrors need similar functionality, each must declare its own slice.

2. **Slices are declared in the mirror manifest.** The `enabled_slices` field in `mirror-manifest.yaml` lists all slices that are part of the mirror. Each slice must have a corresponding full declaration.

3. **Slice dependencies may reference other slices within the same mirror.** Cross-mirror slice dependencies are forbidden — if a slice needs something from another mirror, the dependency must be mediated through a Construction OS core interface.

4. **Slices inherit the mirror's trust boundary.** A slice cannot have a weaker trust boundary than its parent mirror. A slice may have a stricter trust boundary (additional restrictions beyond the mirror level).

5. **Slice lifecycle is bounded by mirror lifecycle.** A slice cannot be OPERATIONAL if its parent mirror is not ACTIVE. When a mirror transitions to FROZEN, all its slices transition to DISABLED or UNAVAILABLE. When a mirror transitions to RETIRED, all its slices are permanently deactivated.

### Attachment Process

1. **Declaration** — The slice is declared with all required fields in the slice declaration document.
2. **Registration** — The slice ID is registered and the slice is added to the mirror manifest's `enabled_slices` list.
3. **Dependency Validation** — The slice's dependency graph is validated to ensure all dependencies are declared and available.
4. **Trust Verification** — The slice's trust class is verified against the mirror's trust boundary.
5. **Activation** — The slice transitions from PENDING_ACTIVATION to OPERATIONAL upon successful first run.

### Detachment Process

1. **Impact Assessment** — Identify all dependents of the slice (other slices, tenants using the capability).
2. **Notification** — If detachability level requires notice, notify all affected parties.
3. **Migration** — If detachability level requires migration, execute documented migration steps.
4. **Disablement** — Set the slice to DISABLED status.
5. **Removal** — Remove the slice from the mirror manifest's `enabled_slices` list.
6. **Verification** — Verify that Construction OS core and remaining slices are unaffected.
7. **Registry Update** — Record the detachment in the registry.

---

## Slice Declaration Example

```yaml
slice_id: SLICE-MIRROR-PROCORE-001
purpose: "Reflects project schedule milestones from Procore into Construction OS project timeline view"
version: "1.0.0"

inputs:
  - input_id: procore-milestones
    source: "Procore Project Schedule API"
    format: "application/json; schema=procore-milestone-v2"
    frequency: "periodic:15m"
    required: true

outputs:
  - output_id: cos-timeline-milestones
    destination: "Construction OS Reflection Surface: project-timeline"
    format: "application/json; schema=cos-milestone-reflection-v1"
    freshness_guarantee: "30m"

required_dependencies:
  - dependency_id: procore-api-access
    dependency_type: EXTERNAL_SERVICE
    description: "Authenticated access to Procore Project Schedule API"
    failure_impact: "Slice becomes UNAVAILABLE; no milestone data reflected"

optional_dependencies:
  - dependency_id: cos-notification-service
    dependency_type: PLATFORM_SERVICE
    description: "Construction OS notification service for alerting on milestone changes"
    failure_impact: "Milestone changes are reflected but notifications are not sent"
    degradation_description: "Silent reflection without change alerts"

trust_class: VERIFIED
transfer_class: NON_TRANSFERABLE
detachability_level: FULLY_DETACHABLE
parity_eligibility: true
promotion_eligibility: MIRROR_ONLY
```

---

## Constraints

1. A slice with undeclared dependencies violates GHC-05 and GHC-13, and is a forbidden pattern (pattern 5).
2. A slice containing billing, tenant UI, auth shell, customer dashboard behavior, or presentation logic violates GHC-06.
3. A slice classified as BUYOUT_READY or FULL_HANDOFF_READY must have passed the transfer gate (GHC-08).
4. A slice classified as CORE_PROMOTABLE for promotion eligibility must pass the promotion gate before any of its functionality enters Construction OS core (GHC-07).
5. All slice declarations must be machine-readable and included in or referenced from the mirror manifest.
