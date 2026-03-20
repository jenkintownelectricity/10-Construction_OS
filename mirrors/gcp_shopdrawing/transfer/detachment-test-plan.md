# Detachment Test Plan — gcp_shopdrawing

**Mirror ID:** gcp_shopdrawing
**Plan Version:** 1.0.0
**Date:** 2026-03-20

## Purpose

This test plan verifies that the `gcp_shopdrawing` mirror can be cleanly detached from the canonical Construction Kernel without leaving orphaned references, broken contracts, or corrupted state in either the mirror or the kernel.

## Scope

- All 5 ACTIVE slices and their associated contracts, schemas, fixtures, and mappings
- Dependency graph integrity post-detachment
- Lineage record completeness after separation
- STAGED slice cleanup

## Pre-Conditions

1. Mirror is in a known-good state (all L0.6 validity checks pass except drift baseline).
2. No in-flight sync operations are active.
3. Parity baseline has been recorded.
4. All ACTIVE slice fixtures have been executed at least once.

## Test Cases

### TC-01: Contract Unbinding

**Objective:** Verify all mirror-specific contracts are removed without affecting canonical contracts.

| Step | Action                                               | Expected Result                                   |
|------|------------------------------------------------------|---------------------------------------------------|
| 1    | List all contracts bound to gcp_shopdrawing          | 5 ACTIVE + 10 STAGED contracts returned           |
| 2    | Execute detachment for ACTIVE contracts              | Contracts marked DETACHED, canonical unaffected    |
| 3    | Verify canonical contract registry                   | No references to gcp_shopdrawing remain            |
| 4    | Verify mirror contract registry                      | All contracts show DETACHED status                 |

### TC-02: Schema Deregistration

**Objective:** Verify mirror-local schemas are deregistered cleanly.

| Step | Action                                               | Expected Result                                   |
|------|------------------------------------------------------|---------------------------------------------------|
| 1    | Enumerate all schemas registered by this mirror      | 10 ACTIVE schemas + 20 STAGED schemas listed      |
| 2    | Deregister all mirror schemas                        | Schemas removed from registry                      |
| 3    | Confirm no dangling schema references in kernel      | Zero orphaned references found                     |

### TC-03: Fixture Isolation

**Objective:** Verify fixtures remain self-contained and do not reference kernel state post-detachment.

| Step | Action                                               | Expected Result                                   |
|------|------------------------------------------------------|---------------------------------------------------|
| 1    | Run all 15 ACTIVE fixtures in isolated mode          | All fixtures execute without kernel calls          |
| 2    | Verify fixture outputs match pre-detachment baselines| Outputs are identical to parity baseline           |
| 3    | Confirm no fixture writes to kernel state stores     | Zero write operations to canonical stores          |

### TC-04: Mapping Cleanup

**Objective:** Verify GCP-specific mappings are removed without corrupting canonical mappings.

| Step | Action                                               | Expected Result                                   |
|------|------------------------------------------------------|---------------------------------------------------|
| 1    | List all GCP mappings in canonical mapping registry  | 5 ACTIVE + 10 STAGED mappings listed               |
| 2    | Remove all GCP mappings                              | Mappings deleted from registry                     |
| 3    | Run canonical mapping integrity check                | All remaining mappings valid                       |

### TC-05: Dependency Graph Severance

**Objective:** Verify the dependency graph remains valid after mirror node removal.

| Step | Action                                               | Expected Result                                   |
|------|------------------------------------------------------|---------------------------------------------------|
| 1    | Remove all gcp_shopdrawing nodes from global graph   | 15 nodes removed                                   |
| 2    | Validate remaining graph is acyclic                  | DAG property maintained                            |
| 3    | Confirm no edges reference removed nodes             | Zero dangling edges                                |

### TC-06: Lineage Record Sealing

**Objective:** Verify lineage records are sealed with terminal entries upon detachment.

| Step | Action                                               | Expected Result                                   |
|------|------------------------------------------------------|---------------------------------------------------|
| 1    | Enumerate all lineage chains involving this mirror   | All chains identified                              |
| 2    | Append DETACHED terminal entry to each chain         | Terminal entries written successfully               |
| 3    | Verify chains are read-only post-sealing             | Write attempts rejected                            |

### TC-07: STAGED Slice Cleanup

**Objective:** Verify STAGED slices are removed without residue.

| Step | Action                                               | Expected Result                                   |
|------|------------------------------------------------------|---------------------------------------------------|
| 1    | List all STAGED slices                               | 10 STAGED slices returned                          |
| 2    | Delete STAGED slice registrations                    | All 10 removed                                     |
| 3    | Confirm no STAGED artifacts remain in any registry   | Zero residual entries                              |

### TC-08: Post-Detachment Kernel Health

**Objective:** Verify the canonical kernel operates normally after detachment.

| Step | Action                                               | Expected Result                                   |
|------|------------------------------------------------------|---------------------------------------------------|
| 1    | Run kernel self-test suite                           | All tests pass                                     |
| 2    | Verify other mirrors unaffected                      | No status changes in sibling mirrors               |
| 3    | Confirm kernel logs show clean detachment            | DETACH_COMPLETE event logged                       |

## Pass Criteria

- All 8 test cases pass without errors.
- Zero orphaned references in any registry.
- Canonical kernel self-test passes at 100%.
- Detachment completes within the designated maintenance window.

## Rollback Procedure

If detachment fails at any step:

1. Halt the detachment process immediately.
2. Restore mirror state from the pre-detachment snapshot.
3. Re-register any contracts/schemas that were partially removed.
4. Validate the dependency graph integrity.
5. Log the failure and escalate for root-cause analysis.
