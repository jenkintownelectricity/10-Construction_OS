# Reflections Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Purpose

This directory tracks the state and quality of individual reflections produced by the `gcp_shopdrawing` mirror. A reflection is a single data element or capability that crosses the trust boundary from GCP into Construction OS in canonical form.

---

## What Is a Reflection

A reflection is the smallest unit of mirrored data. Each reflection:

- Belongs to exactly one slice.
- Has a canonical schema defining its structure in Construction OS terms.
- Has a source entity mapping defining where it comes from in GCP.
- Has a parity score indicating how faithfully it represents the source.
- Is either ACTIVE (data is flowing) or STAGED (defined but not flowing).

Reflections are inventoried in `/mirrors/gcp_shopdrawing/reflection-inventory.yaml`. This directory holds operational tracking artifacts for individual reflections.

---

## Reflection Tracking

### Per-Reflection Artifacts

When a reflection requires operational attention (quality issues, schema evolution, consumer feedback), create a tracking file:

```
reflections/
  {reflection_id}/
    quality-log.yaml       # Historical quality measurements
    schema-evolution.md    # Schema change history and migration notes
    consumer-registry.yaml # Known consumers of this reflection
    issues/                # Open issues affecting this reflection
```

### Reflection Quality States

| State | Description |
|-------|-------------|
| HEALTHY | Parity within target. No open issues. |
| DEGRADED | Parity below target but above critical. Investigation underway. |
| QUARANTINED | Records failing mediation. Not being delivered to consumers. |
| STALE | Data has not been refreshed within the expected window. |

### Monitoring

Reflections are monitored through the parity baseline system (see `parity-baseline.yaml`). Individual reflection quality is tracked here when aggregate slice-level monitoring identifies issues that need per-reflection investigation.

### Current Active Reflections: 25

- 6 from `detail_normalization`
- 5 from `rules_engine`
- 4 from `validation`
- 5 from `artifact_manifest`
- 5 from `lineage`

See `reflection-inventory.yaml` for the complete list with descriptions and parity scores.
