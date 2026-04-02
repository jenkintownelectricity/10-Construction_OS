# Project Posture Classification v0.1

**Status:** ACTIVE
**Classification:** POSTURE_CLASSIFICATION
**Authority:** 10-Construction_OS
**System:** Stake in the Game — One Truth, Many Lenses
**Date:** 2026-04-02

---

## Purpose

Defines the complete set of posture states used to assess a project's current position on any given topic. Posture is the system's structured answer to "where does this stand right now?" — derived from evidence, claims, reconciliation, and governing rules.

---

## Core Principle

Posture is an assessment, not an opinion. Posture detection uses deterministic rules from config where they exist and falls back to NEEDS_REVIEW where they do not. Any heuristic interpretation must be explicitly labeled HEURISTIC. No silent inference may be presented as deterministic truth.

---

## Posture States — Complete Enumeration

### Scope Posture

| State | Definition |
|-------|-----------|
| IN_SCOPE | Item is within the contracted scope of work |
| OUT_OF_SCOPE | Item is outside the contracted scope of work |
| UNCLEAR_SCOPE | Scope determination cannot be made from available evidence |

### Responsibility Posture

| State | Definition |
|-------|-----------|
| DESIGN_RESPONSIBILITY_PUSH | Responsibility is being shifted from designer to contractor or vice versa |
| WARRANTY_RISK | Current trajectory creates warranty exposure for one or more parties |

### Prerequisite / Dependency Posture

| State | Definition |
|-------|-----------|
| MISSING_PREREQUISITE | A required upstream deliverable or condition has not been met |
| PENDING_UPSTREAM_RESPONSE | Action is blocked waiting for a response from an upstream party |

### Schedule / Performance Posture

| State | Definition |
|-------|-----------|
| CONTRACTOR_OVERDUE | Contractor obligation is past its required date |
| CONTRACTOR_NOT_YET_DUE | Contractor obligation exists but the due date has not passed |
| SCHEDULE_RISK | Current trajectory indicates probable schedule impact |

### Direction / Approval Posture

| State | Definition |
|-------|-----------|
| CONFLICTING_DIRECTION | Two or more directives from authoritative sources contradict each other |
| APPROVED_BUT_REVERSED | A previously approved item has been subsequently reversed or countermanded |

### Field / Observation Posture

| State | Definition |
|-------|-----------|
| FIELD_CONDITION_VARIANCE | Observed field condition does not match documented or intended condition |

### Submittal Posture

| State | Definition |
|-------|-----------|
| SUBMITTAL_PENDING_REVIEW | Submittal has been submitted and awaits reviewer action |
| SUBMITTAL_BLOCKED_BY_MISSING_INPUT | Submittal cannot proceed because required input is absent |

### Documentation Posture

| State | Definition |
|-------|-----------|
| DOCUMENT_GAP | A required document does not exist in the project record |
| DOCUMENTATION_MISMATCH | Two or more documents that should agree contain conflicting information |

### Communication Posture

| State | Definition |
|-------|-----------|
| COMMUNICATION_RISK | Communication pattern indicates risk of misalignment or missed direction |

### Fallback

| State | Definition |
|-------|-----------|
| NEEDS_REVIEW | No deterministic posture can be assigned — requires human review |

---

## Posture Record Metadata

```
posture_id:           string (unique)
topic_reference:      string (what this posture is about — item, scope element, submittal, etc.)
posture_state:        enum (one of the states above)
detection_method:     enum (RULE_BASED, HEURISTIC, MANUAL_ASSIGNMENT)
confidence:           float (0.0–1.0) — required when detection_method is HEURISTIC
supporting_evidence:  list of evidence_ids
supporting_claims:    list of claim_ids
detection_rule:       string (rule reference — populated when RULE_BASED)
detected_date:        ISO-8601 date
last_updated:         ISO-8601 date
notes:                string (optional context)
```

---

## Posture Detection Rules

1. **Rule-based detection** is preferred. Config contains mapping rules that evaluate project state against posture conditions.
2. **Heuristic detection** is permitted when no rule exists but pattern recognition suggests a posture. Must be labeled `HEURISTIC` with confidence score.
3. **Manual assignment** is permitted when a human reviewer sets posture directly.
4. **Fallback to NEEDS_REVIEW** occurs when:
   - No rule matches
   - Heuristic confidence is below threshold
   - Multiple posture states could apply with no clear winner
5. **No silent inference** — if the system cannot determine posture deterministically, it must say so.

---

## Posture Is Not Judgment

- Posture states describe position, not fault
- CONTRACTOR_OVERDUE does not assign blame — it states a schedule fact
- DESIGN_RESPONSIBILITY_PUSH does not determine who is right — it flags the dynamic
- WARRANTY_RISK does not predict outcome — it identifies exposure

---

## Limitations

- Posture detection is only as complete as the rule set in config
- Heuristic posture is probabilistic and may be wrong
- Posture does not auto-update unless the detection pipeline is triggered
- Multiple posture states may apply to the same topic simultaneously — this is valid, not an error

---

## References

- CLAIM_SPINE_DOCTRINE_v0.1.md — claims that inform posture detection
- PROJECT_EVIDENCE_SPINE_DOCTRINE_v0.1.md — evidence that feeds posture assessment
- RECONCILIATION_SPINE_DOCTRINE_v0.1.md — reconciliation divergence triggers posture evaluation
- CONTRACTOR_LENS_REPLY_DRAFTING_DOCTRINE_v0.1.md — reply drafting consumes posture
