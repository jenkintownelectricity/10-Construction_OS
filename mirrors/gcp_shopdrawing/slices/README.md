# Slices Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Purpose

This directory contains the operational artifacts for each slice in the `gcp_shopdrawing` mirror. A slice is an independently activatable unit of capability reflection. Each slice reflects a specific aspect of GCP's shop drawing capabilities into Construction OS.

---

## Slice Management

### What Is a Slice

A slice is the atomic unit of mirror capability. Each slice:

- Reflects one coherent capability from the source system.
- Has its own lifecycle (STAGED or ACTIVE).
- Has its own parity target and drift tolerance.
- Can be activated or deactivated independently (respecting dependency order).
- Produces one or more reflections (see `reflection-inventory.yaml`).

### Slice Lifecycle

```
STAGED  --(activation checklist passes)-->  ACTIVE
ACTIVE  --(deactivation decision)-------->  STAGED
ACTIVE  --(mirror breakaway)------------->  DETACHED
```

A slice begins as STAGED when the mirror is created. It moves to ACTIVE when all activation criteria are met (see `mirror-activation-checklist.md`). It can return to STAGED if deactivated, or move to DETACHED if the entire mirror breaks away.

### Current Slice Status

| Slice | Status | Dependencies |
|-------|--------|-------------|
| `detail_normalization` | ACTIVE | None (foundation) |
| `rules_engine` | ACTIVE | detail_normalization |
| `validation` | ACTIVE | detail_normalization, rules_engine |
| `artifact_manifest` | ACTIVE | detail_normalization |
| `lineage` | ACTIVE | detail_normalization |
| `approval_workflow` | STAGED | validation, lineage |
| `rfi_linkage` | STAGED | detail_normalization + external RFI mirror |
| `clash_detection` | STAGED | detail_normalization |
| `submittal_packaging` | STAGED | artifact_manifest |
| `trade_coordination` | STAGED | detail_normalization, clash_detection |
| `fabrication_release` | STAGED | validation, approval_workflow |
| `markup_capture` | STAGED | artifact_manifest |
| `schedule_linkage` | STAGED | lineage + external schedule mirror |

### Directory Structure

When a slice is activated, it should have a subdirectory here containing:

```
slices/
  {slice_id}/
    slice-config.yaml      # Slice-specific configuration
    schema/                 # Canonical schemas for this slice's reflections
    transforms/             # Mediation transform definitions
    fixtures/               # Test fixtures for parity verification
    CHANGELOG.md            # Slice-level change history
```

### Adding a New Slice

1. Create the subdirectory structure above.
2. Define schemas for all reflections the slice will produce.
3. Define mediation transforms for the trust boundary.
4. Create test fixtures for parity verification.
5. Run the slice activation checklist from `mirror-activation-checklist.md`.
6. Update `mirror-manifest.yaml`, `reflection-inventory.yaml`, and `slice-dependency-graph.json`.

### Deactivating a Slice

1. Verify no other ACTIVE slices depend on this slice.
2. Notify all consumers of this slice's reflections.
3. Stop sync for this slice's source endpoints.
4. Mark the slice as STAGED in all manifest files.
5. Reflected data remains available as static (last-known-good) data.
