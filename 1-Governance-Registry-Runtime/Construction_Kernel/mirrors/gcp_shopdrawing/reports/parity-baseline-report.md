# Parity Baseline Report

**Mirror:** gcp_shopdrawing
**Report Date:** 2026-03-20
**Baseline Version:** 1.0.0

---

## Summary

| Metric | Value |
|--------|-------|
| Total Fixtures | 15 |
| Passing | 11 |
| Partial Match | 4 |
| Failing | 0 |
| Overall Parity | 73% (PARTIAL) |

---

## Detail Normalization (3 fixtures)

| Fixture | Result | Notes |
|---------|--------|-------|
| fixture-001-steel-beam-detail | PASS | All fields normalize correctly |
| fixture-002-concrete-column-detail | PARTIAL | Reinforcement schedule format differs; 14/16 fields match |
| fixture-003-curtain-wall-panel-detail | PASS | All fields normalize correctly |

## Rules Engine (3 fixtures)

| Fixture | Result | Notes |
|---------|--------|-------|
| fixture-001-beam-compliance-check | PASS | All 8 compliance rules evaluate correctly |
| fixture-002-column-compliance-check | PARTIAL | Seismic category mapping differs for SDC-E |
| fixture-003-panel-compliance-check | PASS | All thermal and structural rules pass |

## Validation (3 fixtures)

| Fixture | Result | Notes |
|---------|--------|-------|
| fixture-001-valid-submission | PASS | Correctly identifies valid submission |
| fixture-002-invalid-submission | PASS | Correctly identifies all 3 validation errors |
| fixture-003-partial-submission | PASS | Correctly identifies 2 missing required fields |

## Artifact Manifest (3 fixtures)

| Fixture | Result | Notes |
|---------|--------|-------|
| fixture-001-drawing-artifact | PASS | Manifest entry created correctly |
| fixture-002-calculation-artifact | PARTIAL | Page count extraction differs for multi-section calcs |
| fixture-003-material-cert-artifact | PASS | Certificate metadata captured correctly |

## Lineage (3 fixtures)

| Fixture | Result | Notes |
|---------|--------|-------|
| fixture-001-detail-lineage-chain | PASS | Chain integrity verified |
| fixture-002-artifact-lineage-chain | PARTIAL | Timestamp precision differs (ms vs µs) |
| fixture-003-rule-lineage-chain | PASS | Chain integrity verified |

---

## Remediation Plan

1. **Concrete column reinforcement format** — Align normalization rule for rebar schedule notation
2. **Seismic category SDC-E mapping** — Add SDC-E case to seismic category mapping table
3. **Multi-section calculation page count** — Update page extraction logic for compound documents
4. **Timestamp precision alignment** — Standardize on millisecond precision at mirror boundary
