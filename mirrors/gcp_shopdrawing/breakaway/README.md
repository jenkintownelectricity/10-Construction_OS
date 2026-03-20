# Breakaway Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Doctrine

> Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

---

## Purpose

This directory contains operational artifacts for the breakaway process. Breakaway is the controlled detachment of this mirror from GCP. It is a design-time guarantee, not an emergency procedure. Every artifact in this directory supports the ability to cleanly sever the mirror relationship at any time.

Breakaway readiness is not optional. It is a structural requirement. A mirror that cannot break away cleanly is a hard-wired integration wearing a mirror's label.

---

## What This Directory Contains

### Breakaway Readiness

- **Readiness assessments:** Periodic evaluations of whether the mirror can break away cleanly right now.
- **Dry run results:** Records of breakaway dry runs where the sync agent is disabled in a staging environment to verify consumer resilience.
- **Consumer dependency map:** Which consumers depend on this mirror's reflections and what happens to them during breakaway.

### Breakaway Execution

- **Runbooks:** Step-by-step procedures for each phase of breakaway (assessment, preparation, execution, completion).
- **Credential inventory:** List of mirror-specific credentials that must be revoked during breakaway (no actual secrets stored here).
- **Communication templates:** Pre-written notifications for stakeholders at each breakaway phase.

### Post-Breakaway

- **Archive manifests:** What gets archived when the mirror detaches.
- **Data retention plan:** How long reflected data is kept after breakaway and in what form.
- **Replacement planning:** Templates for planning a replacement mirror if the source system changes.

---

## Directory Structure

```
breakaway/
  readiness/               # Periodic readiness assessment results
  dry-runs/                # Dry run execution logs and results
  consumer-map/            # Consumer dependency documentation
  runbooks/                # Breakaway procedure runbooks
  credentials/             # Credential inventory (no actual secrets)
  communications/          # Notification templates
  archive/                 # Post-breakaway archive manifests
```

---

## Breakaway Readiness Schedule

| Activity | Frequency | Last Completed |
|----------|-----------|----------------|
| Readiness self-assessment | Monthly | Pending (new mirror) |
| Consumer dependency review | Quarterly | Pending (new mirror) |
| Dry run (staging) | Every 90 days | Pending (new mirror) |
| Credential inventory review | Quarterly | Pending (new mirror) |

---

## Key Reference

The full breakaway conditions, triggers, procedures, and guarantees are documented in `/mirrors/gcp_shopdrawing/breakaway-conditions.md`. This directory holds the operational artifacts that support those procedures.
