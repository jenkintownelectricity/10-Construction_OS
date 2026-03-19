# Construction Object Evidence and Matching Basis

## Purpose

Define how evidence supports object identity determination within the Construction domain. This document specifies evidence surfaces, matching signals, matching posture, and the evidence decision surface.

---

## Evidence Surfaces

Evidence for identity determination is drawn from the following surfaces:

| Surface | Description |
|---|---|
| Documents | Design drawings, shop drawings, submittals, specifications, RFIs, change orders |
| Extracted data | Structured facts extracted from document surfaces |
| Field observations | Inspection reports, field photos, observation records |
| Sensor measurements | Laser scans, survey data, sensor readings, material test results |

Evidence surfaces provide raw material for identity evaluation. No single evidence surface is authoritative in isolation.

---

## Matching Signals

The following signals may support identity determination when evaluated together:

| Signal | Description |
|---|---|
| Location similarity | Objects occupy the same or proximate spatial position |
| Geometry similarity | Objects share geometric properties or dimensional characteristics |
| Material similarity | Objects share material specifications or observed material properties |
| Relational structure | Objects share relationships to the same surrounding objects |
| Temporal proximity | Objects appear in successive revisions within a plausible continuity window |

---

## Matching Posture

Matching signals may support identity determination. Matching signals must not automatically establish identity.

- Signals are inputs to governed evaluation, not deterministic rules.
- High signal alignment suggests but does not prove continuity.
- Low signal alignment suggests but does not prove discontinuity.
- No combination of signals bypasses the requirement for governed identity evaluation.

---

## Evidence Decision Surface

Identity continuity requires governed evaluation of evidence. The decision surface operates as follows:

1. Evidence is collected from available evidence surfaces.
2. Matching signals are evaluated across revision boundaries.
3. Signal evaluation produces candidate matches, not final determinations.
4. Governed evaluation considers candidate matches, evidence strength, and conflict.
5. A governed determination establishes, disputes, or denies identity continuity.

Matching systems may propose candidate matches but must not establish final identity. Final identity determination is a governed operation, not an automated computation.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Governance doctrine for evidence rules: `Construction_Kernel/docs/governance/construction-object-evidence-doctrine.md`
