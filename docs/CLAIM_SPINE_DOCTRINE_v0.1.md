# Claim Spine Doctrine v0.1

**Status:** ACTIVE
**Classification:** CLAIM_DOCTRINE
**Authority:** 10-Construction_OS
**System:** Stake in the Game — One Truth, Many Lenses
**Date:** 2026-04-02

---

## Purpose

Defines the rules governing how claims are created, tracked, evaluated, and resolved within the Construction OS project intelligence system. Claims are assertions about project state made by a party. The system surfaces facts and evaluates claims against evidence — it does not render legal judgment.

---

## Core Principle

A claim is an assertion, not a fact. Claims must be linked to evidence. The system evaluates claims deterministically where rules exist and assigns NEEDS_REVIEW where ambiguity remains. Humans decide outcomes.

---

## Claim Definition

A claim is a formal assertion by a project party regarding:
- Scope inclusion or exclusion
- Responsibility assignment
- Schedule impact
- Cost impact
- Compliance with contract documents
- Quality of work performed
- Completeness of deliverables

---

## Claim States

| State | Definition |
|-------|-----------|
| ASSERTED | Claim has been made by a party but not yet linked to evidence |
| EVIDENCED | Claim has been linked to one or more evidence records |
| CONTESTED | A counter-claim or contradicting evidence has been registered |
| RESOLVED | Claim evaluation is complete — deterministic rules produced a result |
| ACCEPTED | Human review has accepted the claim |
| REJECTED | Human review has rejected the claim |

State transitions:

```
ASSERTED → EVIDENCED     (evidence linked)
ASSERTED → CONTESTED     (counter-claim registered)
EVIDENCED → CONTESTED    (contradicting evidence or counter-claim)
EVIDENCED → RESOLVED     (deterministic evaluation complete)
CONTESTED → RESOLVED     (deterministic evaluation complete)
CONTESTED → NEEDS_REVIEW (ambiguity — no deterministic resolution)
RESOLVED → ACCEPTED      (human approval)
RESOLVED → REJECTED      (human rejection)
NEEDS_REVIEW → ACCEPTED  (human decision after review)
NEEDS_REVIEW → REJECTED  (human decision after review)
```

---

## Required Claim Metadata

Every claim record must carry:

```
claim_id:             string (unique)
claimant_party_id:    party_id reference
claim_type:           enum (SCOPE, RESPONSIBILITY, SCHEDULE, COST, COMPLIANCE, QUALITY, COMPLETENESS, OTHER)
severity:             enum (LOW, MEDIUM, HIGH, CRITICAL)
evidence_ids:         list of evidence_id references (may be empty at ASSERTED)
status:               enum (ASSERTED, EVIDENCED, CONTESTED, RESOLVED, ACCEPTED, REJECTED, NEEDS_REVIEW)
assertion_date:       ISO-8601 date
assertion_summary:    string (plain language description)
contract_references:  list of document section references (optional)
counter_claim_ids:    list of claim_ids that contest this claim (may be empty)
resolution_basis:     string (rule reference or HUMAN_JUDGMENT — populated at RESOLVED/ACCEPTED/REJECTED)
```

---

## Counter-Claims

- A counter-claim is itself a claim with its own claim_id
- Counter-claims must reference the claim_id they contest via `counter_claim_ids`
- Both the original claim and counter-claim carry independent evidence
- The system does not automatically prefer one claim over another
- When claims conflict, status moves to CONTESTED and evaluation proceeds

---

## Claim Evaluation Rules

1. **Deterministic evaluation** applies when:
   - Contract language is unambiguous on the topic
   - Evidence clearly supports or refutes the assertion
   - A governing rule in config maps the claim type to a resolution

2. **NEEDS_REVIEW** applies when:
   - Contract language is ambiguous or silent
   - Evidence is contradictory or insufficient
   - Multiple valid interpretations exist
   - Claim involves subjective quality assessment

3. **No silent resolution** — every evaluation must record its basis:
   - Rule-based: cite the rule
   - Evidence-based: cite the evidence_ids
   - Human: record HUMAN_JUDGMENT

---

## What Claims Do NOT Do

1. Claims do not constitute legal findings — the system surfaces, humans decide
2. Claims do not override truth spine events — they assert interpretations of them
3. Claims do not auto-resolve when contested — human review is required
4. Claims do not expire — they remain in their last state until acted upon

---

## Limitations

- Claim severity is assigned by the claimant and may not reflect objective impact
- Evidence linking is only as good as the evidence ingestion pipeline
- Counter-claim relationships are manually declared; the system does not auto-detect contradictions
- Deterministic evaluation depends on rule coverage in config — gaps produce NEEDS_REVIEW

---

## References

- PROJECT_EVIDENCE_SPINE_DOCTRINE_v0.1.md — evidence that supports claims
- RECONCILIATION_SPINE_DOCTRINE_v0.1.md — reconciliation that consumes claim states
- PROJECT_POSTURE_CLASSIFICATION_v0.1.md — posture detection informed by claims
