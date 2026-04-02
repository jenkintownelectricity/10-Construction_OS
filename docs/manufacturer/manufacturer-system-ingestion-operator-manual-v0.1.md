# Manufacturer System Ingestion Operator Manual v0.1

## Authority
10-Construction_OS (domain execution plane)

## Audience
Internal operators preparing manufacturer systems for platform onboarding.

## Purpose
Exact operational workflow for onboarding a manufacturer's detail system in under 10 minutes.

---

## 1. Overview

The operator's role is to take a manufacturer's submitted DXF detail package and produce:
1. Parsed raw JSON geometry records
2. Layer-to-ownership mappings
3. Assembly family definition packs
4. Readiness classifications

**Target: sub-10-minute turnaround per manufacturer.**

---

## 2. Golden DXF Selection

Select the FIRST representative detail from the manufacturer's package:

**Selection Criteria (in priority order):**
1. Lowest layer count
2. Cleanest geometry (fewest noise entities)
3. Most representative of the primary system
4. Simplest condition type (field membrane or standard parapet)
5. Fewest INSERT/BLOCK entities

**Example:** For Barrett Black Pearl, select a simple field waterproofing detail showing:
- Black Pearl Sheet layer
- Substrate/slab context
- Minimal annotation

---

## 3. Progressive Batch Ingestion

| Batch | Count | Criteria | Gate |
|-------|-------|----------|------|
| First | 5 | Cleanest, lowest layer count | Taxonomy confirmed before proceeding |
| Second | 5 | Moderate complexity | First batch taxonomy stable |
| Third | 10 | Includes noisier/complex details | Second batch taxonomy stable |

**Rule:** Do NOT proceed to the next batch until the current batch's layer taxonomy is confirmed.

---

## 4. Semantic Layer Mapping

For each unique layer in the parsed DXF JSON:

| Layer Name | → Ownership Class | → Semantic Role |
|------------|-------------------|-----------------|
| RAM Black Pearl Sheet | SYSTEM_OWNED | membrane |
| Protection Course | SYSTEM_OWNED | protection |
| Others | CONTEXT_ONLY | unclassified_context |
| Text | ANNOTATION | annotation |
| Defpoints | ANNOTATION | annotation |

**Default Rules:**
- If layer name matches a known product → SYSTEM_OWNED
- If layer name is "Others" → CONTEXT_ONLY
- If layer name is "Text" / "Defpoints" → ANNOTATION
- If MULTILEADER/TEXT/MTEXT entity → ANNOTATION regardless of layer
- If unknown → CONTEXT_ONLY, flag for review

**Ambiguity Rule:** If you cannot confidently classify a layer as SYSTEM_OWNED, mark it CONTEXT_ONLY. Never promote without evidence.

---

## 5. Ownership Mapping Rules

### SYSTEM_OWNED
The layer/entity represents material that the manufacturer's system is responsible for:
- Membranes, sheets, coatings
- Primers, adhesives
- Flashings
- Reinforcement / fleece
- Protection courses (when system-owned)
- Termination components

### CONTEXT_ONLY
The layer/entity is shown for context but is NOT part of the system:
- Substrate, concrete, steel
- Walls, masonry
- Adjacent construction
- Overburden, pavers
- "Others" layer (always defaults here)

### ANNOTATION
Text, dimensions, leaders — not geometry:
- Text, MTEXT entities
- MULTILEADER entities
- Dimension entities
- "Text" and "Defpoints" layers

---

## 6. Assembly Definition Creation

Create a family definition JSON following `schemas/manufacturer/manufacturer_family_definition.schema.json`:

```json
{
  "family_id": "FAM-<MFR>-<SYSTEM>",
  "manufacturer_id": "MFR-<MFR>-001",
  "manufacturer_name": "...",
  "system_name": "...",
  "system_description": "...",
  "product_components": [...],
  "owned_layers": [...],
  "context_layers": [...],
  "annotation_layers": [...],
  "supported_conditions": [...],
  "representative_sources": [...],
  "readiness": "READY|PARTIAL|BLOCKED|NO_SOURCE",
  "readiness_blockers": [...]
}
```

**Save to:** `source/<manufacturer>/definitions/<family>.definition.json`

---

## 7. Readiness Classification

| State | Criteria |
|-------|----------|
| READY | Family defined, components listed, layers mapped to ownership, at least 1 DXF parsed, conditions defined |
| PARTIAL | Family defined but missing layer confirmation, DXF parse, or condition mapping |
| BLOCKED | Cannot proceed — missing critical evidence (no DXF, incompatible format, unresolvable ambiguity) |
| NO_SOURCE | No source evidence exists at all |

---

## 8. Operator Checklist

- [ ] 1. Create manufacturer record (MFR-<ID>)
- [ ] 2. Select golden DXF (lowest layer count, cleanest)
- [ ] 3. Parse DXF to raw JSON (ingestor tool)
- [ ] 4. Inventory layers from parsed JSON
- [ ] 5. Map each layer to ownership class
- [ ] 6. Map each layer to semantic role
- [ ] 7. Create family definition JSON
- [ ] 8. List product components with roles
- [ ] 9. Define supported condition types
- [ ] 10. Classify readiness (READY/PARTIAL/BLOCKED)
- [ ] 11. Document blockers if any
- [ ] 12. Generate onboarding receipt

---

## 9. Sub-10-Minute Timing Breakdown

| Step | Time | Action |
|------|------|--------|
| 1 | 30s | Create manufacturer record |
| 2 | 1m | Select golden DXF |
| 3 | 1m | Parse to raw JSON (automated) |
| 4 | 3m | Layer mapping + ownership classification |
| 5 | 2m | Family definition + components |
| 6 | 1m | Readiness classification |
| 7 | 30s | Receipt generation |
| **Total** | **~9m** | |

---

## 10. Exploratory Concept UI

> **EXPLORATORY CONCEPT — NOT YET IMPLEMENTED**
>
> This section describes a potential 4-panel manufacturer intake UI.
> It is conceptual only and must not be treated as a required implementation.

### Panel 1 — Source Details
- DXF file list with parse status
- Entity counts per file
- Layer counts per file
- Source path reference

### Panel 2 — Layer Roles
- Table: Layer Name → Ownership Class → Semantic Role
- Color coding: SYSTEM_OWNED (green), CONTEXT_ONLY (gray), ANNOTATION (blue)
- Override controls for operator adjustment
- Ambiguity flags

### Panel 3 — Assembly Definitions
- Family components list with roles
- Condition support checkboxes
- Layer ownership mapping summary
- Cross-family relationship notes

### Panel 4 — Review and Readiness
- Readiness classification selector
- Blocker list
- Receipt preview
- Submit for onboarding

---

## 11. Applying This Flow to Other Manufacturers

This exact flow works for any manufacturer:

| Manufacturer | Expected Families | Notes |
|-------------|-------------------|-------|
| Carlisle | TPO, PVC, EPDM, Fluid Applied | Different layer naming conventions |
| GAF | TPO, BUR, Modified Bitumen | May use different DXF conventions |
| Siplast | SBS Modified Bitumen, APP | Similar to Barrett SBS family |
| Tremco | Fluid Applied, Sheet | May include primers/coatings |

The platform does NOT need rebuilding for each manufacturer.
Only the family definitions and layer mappings change.
