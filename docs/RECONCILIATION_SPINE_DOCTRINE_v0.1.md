# Reconciliation Spine Doctrine v0.1

**Status:** ACTIVE
**Classification:** RECONCILIATION_DOCTRINE
**Authority:** 10-Construction_OS
**System:** Stake in the Game — One Truth, Many Lenses
**Date:** 2026-04-02

---

## Purpose

Defines the rules governing reconciliation — the governed comparison between intent and reality within the Construction OS project intelligence system. Reconciliation is the mechanism that detects divergence between what was planned, what was approved, what was asserted, what was observed, and what was documented.

---

## Core Principle

Reconciliation compares states. It does not resolve conflicts. When states diverge, the system produces a divergence record and surfaces it for human review. No automatic resolution of claim conflicts occurs.

---

## Reconciliation States

| State | Definition |
|-------|-----------|
| ALIGNED | All consumed states agree — no divergence detected |
| INTENT_ONLY | An intended state exists but no corresponding approved, observed, or documented state |
| REALITY_ONLY | An observed or documented state exists with no corresponding intent or approval |
| ASSERTED_NOT_EVIDENCED | A claim has been made but no supporting evidence exists |
| OBSERVED_NOT_APPROVED | A field condition has been observed that was never formally approved |
| DOCUMENTED_BUT_NOT_OBSERVED | Documentation says something should be present but field observation does not confirm it |
| CLAIM_CONFLICT | Two or more claims about the same topic contradict each other |
| NEEDS_REVIEW | Reconciliation cannot determine alignment — requires human review |

---

## Consumed States

Reconciliation operates by comparing up to five state dimensions for any given topic:

```
intended_state:     What the design/contract documents say should happen
approved_state:     What has been formally approved (submittals, RFIs, change orders)
asserted_state:     What a party claims to be true (via claim spine)
observed_state:     What has been seen in the field (photos, inspections, field notes)
documented_state:   What project records say happened (daily logs, correspondence, meeting minutes)
```

Not all dimensions are required for every reconciliation. A reconciliation is valid with as few as two dimensions present.

---

## Reconciliation Record Metadata

```
reconciliation_id:    string (unique)
topic_reference:      string (what is being reconciled)
intended_state:       state_reference or NULL
approved_state:       state_reference or NULL
asserted_state:       state_reference or NULL (links to claim_ids)
observed_state:       state_reference or NULL (links to evidence_ids)
documented_state:     state_reference or NULL (links to document_record_ids)
reconciliation_state: enum (one of the states above)
divergence_records:   list of divergence_record_ids (populated when not ALIGNED)
reconciled_date:      ISO-8601 date
last_updated:         ISO-8601 date
resolution_status:    enum (OPEN, UNDER_REVIEW, RESOLVED_BY_HUMAN, RESOLVED_BY_RULE)
resolution_basis:     string (populated when resolved)
```

---

## Divergence Records

When reconciliation state is anything other than ALIGNED, a divergence record is produced:

```
divergence_id:        string (unique)
reconciliation_id:    string (parent reference)
divergence_type:      enum (MISSING_STATE, CONFLICTING_STATE, UNSUPPORTED_ASSERTION, UNAPPROVED_OBSERVATION, UNDOCUMENTED_INTENT)
dimension_a:          string (first state dimension involved)
dimension_b:          string (second state dimension involved, or NULL)
description:          string (plain language summary of the divergence)
severity:             enum (LOW, MEDIUM, HIGH, CRITICAL)
created_date:         ISO-8601 date
```

---

## Reconciliation Rules

1. **Comparison is symmetric** — INTENT_ONLY and REALITY_ONLY are both valid divergence types; neither is privileged
2. **All five dimensions are checked** when present; missing dimensions are noted but do not block reconciliation
3. **CLAIM_CONFLICT is never auto-resolved** — when claims contradict, the system surfaces both and waits for human decision
4. **OBSERVED_NOT_APPROVED triggers posture detection** — feeds into FIELD_CONDITION_VARIANCE posture
5. **ASSERTED_NOT_EVIDENCED triggers evidence request** — system flags the gap but does not reject the claim
6. **Reconciliation is re-run** when any consumed state changes — not on a schedule, on state change
7. **NEEDS_REVIEW** is assigned when:
   - Dimensions are ambiguous
   - Multiple reconciliation states could apply
   - Confidence in state comparison is below threshold

---

## What Reconciliation Does NOT Do

1. Does not determine who is right — it identifies where states disagree
2. Does not auto-resolve claim conflicts — surfaces divergence for human review
3. Does not assign fault or liability — it maps discrepancies
4. Does not replace audit — it is a detection layer, not a compliance engine

---

## Limitations

- Reconciliation quality depends on completeness of state dimensions; missing states produce incomplete pictures
- State comparison is string/semantic matching — nuanced contractual interpretation is beyond automated comparison
- Divergence severity is rule-assigned and may not reflect true project impact
- Re-reconciliation on state change requires reliable change detection in upstream systems

---

## References

- PROJECT_EVIDENCE_SPINE_DOCTRINE_v0.1.md — observed and documented states come from evidence
- CLAIM_SPINE_DOCTRINE_v0.1.md — asserted states come from claims
- PROJECT_POSTURE_CLASSIFICATION_v0.1.md — reconciliation divergence feeds posture detection
- PROJECT_CONTEXT_MODEL_v0.1.md — context model provides the records being reconciled
