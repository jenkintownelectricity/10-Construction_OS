# Tests Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Purpose

This directory contains test suites, test fixtures, and test results for the `gcp_shopdrawing` mirror. Testing verifies that the mirror correctly reflects GCP's shop drawing capabilities through the trust boundary into Construction OS canonical format.

---

## Test Categories

### 1. Schema Mediation Tests

**What they verify:** The trust boundary's mediation layer correctly transforms GCP-native data into Construction OS canonical format.

**Test approach:**
- Provide known GCP-native input payloads.
- Assert that the mediation layer produces the expected canonical output.
- Test all field mappings, vocabulary translations, ID transformations, and timestamp normalizations.
- Test edge cases: null values, empty arrays, maximum-length strings, special characters, Unicode.

**Coverage target:** Every field in every active reflection must have at least one mediation test.

### 2. Parity Verification Tests

**What they verify:** Reflected records accurately represent source records.

**Test approach:**
- Fetch a sample of records from both GCP and the mirror.
- Compare each canonical field against the expected transformation of the GCP field.
- Measure parity scores and compare against targets.

**Coverage target:** Minimum 100 records per slice per test run.

### 3. Sync Agent Tests

**What they verify:** The sync agent correctly fetches data from GCP, handles errors, respects rate limits, and maintains cursor state.

**Test approach:**
- Unit tests for cursor management, pagination, error handling, and retry logic.
- Integration tests against a GCP API mock that simulates normal operation, errors, rate limiting, and schema changes.
- End-to-end tests in staging against the actual GCP API (rate-limited to avoid production impact).

**Coverage target:** All sync modes (incremental, event-triggered, full reconciliation, backfill, manual).

### 4. Trust Boundary Tests

**What they verify:** The trust boundary correctly enforces isolation guarantees.

**Test approach:**
- Attempt to pass prohibited data types through the boundary. Assert rejection.
- Verify that no GCP-native identifiers, field names, or enumeration values appear on the egress side.
- Verify that PII is stripped and replaced with opaque tokens.
- Verify audit logging for every crossing event.

**Coverage target:** Every prohibition in `trust-boundary.md` must have a test.

### 5. Breakaway Tests

**What they verify:** The mirror can be detached without damage.

**Test approach:**
- Disable the sync agent.
- Verify all consumers continue to operate on static data.
- Verify no errors, no missing data, no consumer-side failures.
- Verify that reflected data remains queryable and intact.

**Coverage target:** All registered consumers tested during breakaway dry run.

### 6. Dependency Tests

**What they verify:** Slice dependencies are correctly enforced.

**Test approach:**
- Attempt to activate a slice whose dependencies are not ACTIVE. Assert rejection.
- Deactivate a dependency slice. Assert that dependent slices are flagged.
- Verify the dependency graph (`slice-dependency-graph.json`) has no cycles.

**Coverage target:** Every edge in the dependency graph.

---

## Directory Structure

```
tests/
  mediation/               # Schema mediation test suites
  parity/                  # Parity verification test suites
  sync-agent/              # Sync agent unit and integration tests
  trust-boundary/          # Trust boundary enforcement tests
  breakaway/               # Breakaway dry run test results
  dependency/              # Slice dependency validation tests
  fixtures/                # Shared test fixtures (sample GCP payloads, expected outputs)
  results/                 # Test execution results and history
```

---

## Test Fixtures

Test fixtures are sample data that represent realistic GCP payloads and their expected canonical transformations. Fixtures are maintained for each active slice:

| Slice | Fixture Count | Description |
|-------|---------------|-------------|
| detail_normalization | 10+ | Sample detail records across all supported trades |
| rules_engine | 10+ | Sample rules of each category and severity |
| validation | 10+ | Sample validation results including pass, fail, warning |
| artifact_manifest | 10+ | Sample artifacts of each type and release state |
| lineage | 10+ | Sample lineage chains with various revision and approval patterns |

---

## Test Execution

| Environment | Frequency | Scope |
|-------------|-----------|-------|
| Development | On every change | Unit tests, mediation tests |
| Staging | Daily | Full suite including sync agent integration tests |
| Production | Weekly | Parity verification only (read-only against live data) |

---

## Test Requirements for Slice Activation

Before any slice moves from STAGED to ACTIVE, the following test requirements must be met:

1. All schema mediation tests pass for the slice's reflections.
2. Parity verification tests produce scores at or above the slice's parity target.
3. Trust boundary tests confirm no prohibited data leaks for the slice's data types.
4. Dependency tests confirm all prerequisite slices are ACTIVE and healthy.
5. Three consecutive sync cycles complete successfully in staging.

These requirements are enforced through the activation checklist in `mirror-activation-checklist.md`.
