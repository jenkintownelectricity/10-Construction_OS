# Drift Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Purpose

This directory contains drift detection artifacts for the `gcp_shopdrawing` mirror. Drift is the divergence between what the mirror reflects and what the source system actually contains. Drift detection is how the mirror knows it is still accurate.

---

## What Is Drift

Drift occurs when the mirror's reflected data no longer faithfully represents the source system's state. Drift is not the same as staleness (a timing issue). Drift is a fidelity issue -- the data is wrong, not just late.

### Types of Drift

| Type | Description | Example |
|------|-------------|---------|
| Schema drift | GCP changes its data model and the mediation layer has not adapted | GCP adds a new required field; mirror produces records missing that field |
| Value drift | Mediation transforms produce incorrect values | A vocabulary mapping is wrong, causing status values to be misclassified |
| Completeness drift | Records that should be reflected are missing | A new GCP entity type is not recognized by the sync agent |
| Semantic drift | Data is structurally correct but semantically wrong | A rule's condition is syntactically valid but logically different from source |

### Drift vs. Staleness

- **Staleness:** The data is correct but old. The sync agent has not run recently. Fix: run sync.
- **Drift:** The data is incorrect regardless of when it was synced. The mediation or source has changed. Fix: investigate root cause.

---

## Drift Detection Mechanisms

### Automated Detection

1. **Parity checks** (every 6 hours): Compare sampled reflected records against source records. Measure schema, value, completeness, and timeliness parity.

2. **Schema monitoring** (every sync cycle): Validate that GCP API responses match the expected schema. Flag unexpected fields, missing fields, or type changes.

3. **Reconciliation** (daily): Full comparison of mirror state against GCP state. Identifies records that are present in one but not the other.

4. **Vocabulary monitoring** (weekly): Check for unmapped enumeration values in mediation logs. New values at GCP may not have OS vocabulary mappings.

### Manual Detection

- Consumer reports of incorrect data.
- Platform team inspection during routine review.
- Post-incident investigation revealing data discrepancies.

---

## Drift Tolerance

Each slice has a defined drift tolerance (see `parity-baseline.yaml`):

| Slice | Drift Tolerance | Current Parity | Status |
|-------|----------------|----------------|--------|
| detail_normalization | 0.05 | 0.96 | Within tolerance |
| rules_engine | 0.08 | 0.91 | Within tolerance |
| validation | 0.06 | 0.93 | Within tolerance |
| artifact_manifest | 0.04 | 0.96 | Within tolerance |
| lineage | 0.02 | 0.98 | Within tolerance |

---

## Directory Structure

```
drift/
  events/                  # Individual drift event records
  investigations/          # Root cause investigations for drift events
  reports/                 # Periodic drift summary reports
  baselines/               # Historical parity baseline snapshots
```

---

## Drift Response Procedure

1. **Detect:** Automated monitoring or manual observation identifies drift.
2. **Classify:** Determine drift type (schema, value, completeness, semantic).
3. **Assess:** Measure the magnitude and scope. How many records? Which slices?
4. **Investigate:** Identify root cause (GCP change, mediation bug, sync issue).
5. **Remediate:** Fix at the appropriate layer. Do not mask drift with workarounds.
6. **Verify:** Re-measure parity to confirm remediation.
7. **Document:** Record the event, cause, and resolution in this directory.

If drift exceeds tolerance for 7 consecutive days without a resolution path, a breakaway evaluation is triggered (see `breakaway-conditions.md`).
