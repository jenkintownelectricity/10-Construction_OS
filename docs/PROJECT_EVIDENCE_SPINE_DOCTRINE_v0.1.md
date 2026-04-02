# Project Evidence Spine Doctrine v0.1

**Status:** ACTIVE
**Classification:** EVIDENCE_DOCTRINE
**Authority:** 10-Construction_OS
**System:** Stake in the Game — One Truth, Many Lenses
**Date:** 2026-04-02

---

## Purpose

Defines the rules governing how project evidence is ingested, classified, and consumed within the Construction OS project intelligence system. Evidence is the supporting infrastructure for the Reality Plane — it is raw material from which truth spine events are extracted.

---

## Core Principle

Evidence does not replace kernel truth. Evidence validates, qualifies, or challenges it. The truth spine remains the canonical record; evidence is the substrate that feeds it.

---

## Evidence Surfaces

Evidence enters the system from the following surface types:

| Surface | Examples |
|---------|----------|
| Photos | Field photos, progress photos, drone captures |
| Inspection Reports | Third-party inspection results, punch lists |
| Field Notes | Superintendent daily logs, foreman notes |
| Emails | Correspondence between project parties |
| Submittals | Shop drawings, product data, samples |
| RFIs | Requests for information and responses |
| Meeting Minutes | OAC meeting notes, coordination logs |
| Change Documents | Change orders, bulletins, directives |

These surfaces are raw material. They are not truth until processed.

---

## Evidence Quality Tiers

| Tier | Definition | Example |
|------|-----------|---------|
| PRIMARY | Direct observation by a known party at a known time | Field photo with GPS/timestamp, inspector on-site report |
| SECONDARY | Documented record produced as part of project process | Submitted RFI response, approved shop drawing, email chain |
| TERTIARY | Inferred or derived from other evidence | Calculated schedule impact, cross-referenced discrepancy |

Quality tier affects weight in claim evaluation but does not automatically disqualify evidence.

---

## Required Evidence Metadata

Every evidence record must carry:

```
evidence_id:          string (unique)
source_type:          enum (PHOTO, INSPECTION_REPORT, FIELD_NOTE, EMAIL, SUBMITTAL, RFI, MEETING_MINUTES, CHANGE_DOCUMENT, OTHER)
source_date:          ISO-8601 date
source_party:         party_id reference
extraction_method:    enum (MANUAL_ENTRY, OCR_EXTRACTION, STRUCTURED_IMPORT, API_INGEST, HEURISTIC_EXTRACTION)
quality_tier:         enum (PRIMARY, SECONDARY, TERTIARY)
extraction_confidence: float (0.0–1.0) — required when extraction_method is HEURISTIC_EXTRACTION or OCR_EXTRACTION
linked_truth_events:  list of truth_event_ids (may be empty at ingestion)
status:               enum (INGESTED, PROCESSED, LINKED, CHALLENGED, SUPERSEDED)
```

---

## Evidence-to-Truth Extraction Rules

1. Evidence is ingested in raw form with metadata attached
2. Extraction produces candidate facts from evidence content
3. Candidate facts are matched against existing truth spine events or create new ones
4. Extraction method is always recorded — no silent transformation
5. Heuristic extractions must be labeled `HEURISTIC` and carry confidence scores
6. No heuristic output may be presented as deterministic truth

---

## NEEDS_REVIEW Fallback

When evidence is:
- Incomplete or ambiguous
- Contradicted by other evidence of equal or higher tier
- Extracted via heuristic with confidence below threshold
- Missing required metadata fields

The system assigns `NEEDS_REVIEW` status. No further automated processing occurs until human review resolves the flag.

---

## What Evidence Does NOT Do

1. Evidence does not override kernel truth — it informs it
2. Evidence does not resolve claims — it supports or challenges them
3. Evidence does not determine project posture — it feeds posture detection
4. Evidence does not generate legal conclusions — it surfaces facts

---

## Limitations

- OCR and heuristic extraction are best-effort; confidence scores are estimates, not guarantees
- Photo evidence without metadata (GPS, timestamp) is downgraded to TERTIARY
- Email evidence relies on correct party identification; misattribution is a known risk
- Evidence linking to truth events is not retroactive without explicit re-processing

---

## References

- PROJECT_CONTEXT_MODEL_v0.1.md — object families that consume evidence
- CLAIM_SPINE_DOCTRINE_v0.1.md — claims that reference evidence
- RECONCILIATION_SPINE_DOCTRINE_v0.1.md — reconciliation that compares evidence states
