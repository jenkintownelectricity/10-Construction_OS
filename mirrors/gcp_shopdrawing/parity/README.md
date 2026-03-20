# Parity Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Purpose

This directory contains parity verification artifacts for the `gcp_shopdrawing` mirror. Parity verification measures how faithfully the mirror's reflections represent the source system's capabilities. It is the primary mechanism for ensuring mirror quality.

---

## What Is Parity

Parity is the degree to which a reflected record in Construction OS accurately represents the corresponding capability in GCP. Perfect parity (1.0) means the reflection is a lossless, semantically accurate representation. Zero parity (0.0) means the reflection bears no resemblance to the source.

Parity is measured across four dimensions:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Schema parity | 0.30 | Are all meaningful source fields captured in the canonical schema? |
| Value parity | 0.30 | Do reflected values accurately represent source values? |
| Completeness parity | 0.25 | Are all in-scope records reflected? |
| Timeliness parity | 0.15 | How current are reflected records? |

---

## Parity Targets

| Slice | Target | Current | Status |
|-------|--------|---------|--------|
| detail_normalization | 0.95 | 0.96 | Meeting target |
| rules_engine | 0.90 | 0.91 | Meeting target |
| validation | 0.92 | 0.93 | Meeting target |
| artifact_manifest | 0.95 | 0.96 | Meeting target |
| lineage | 0.98 | 0.98 | Meeting target |

---

## Directory Structure

```
parity/
  measurements/            # Raw parity measurement data
  samples/                 # Sample records used for verification
  reports/                 # Periodic parity summary reports
  history/                 # Historical parity trend data
  methodology/             # Measurement methodology documentation
```

---

## Verification Process

1. **Sample selection:** Randomly select records from the mirror and their corresponding source records from GCP.
2. **Schema comparison:** Verify all meaningful fields are present in the canonical record.
3. **Value comparison:** Compare each field value after mediation against the source.
4. **Completeness check:** Compare record counts between mirror and source for a defined window.
5. **Timeliness check:** Measure the age of the most recently synced record.
6. **Score calculation:** Compute the weighted average across all four dimensions.
7. **Threshold evaluation:** Compare the score against the slice's parity target.
8. **Recording:** Store the measurement in this directory and update `parity-baseline.yaml` if the baseline changes.

---

## Key Reference

The baseline parity measurements and drift monitoring configuration are in `/mirrors/gcp_shopdrawing/parity-baseline.yaml`. This directory holds the operational measurement data and verification artifacts.
