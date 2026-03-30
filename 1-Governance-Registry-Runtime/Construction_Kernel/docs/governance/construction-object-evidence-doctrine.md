# Construction Object Evidence Doctrine

## Purpose

Define governed evidence rules used to support identity continuity and truth extraction within the Construction domain. Evidence is the traceable basis for all identity determinations and truth assertions.

---

## Evidence Principle

Every identity determination and truth assertion must be supported by traceable evidence. Evidence must link to a source artifact. Unsupported assertions are governance violations.

---

## Evidence Types

The following are recognized evidence types within the Construction domain:

- Design drawings
- Shop drawings
- Submittals
- Specifications
- RFIs (Requests for Information)
- Field photos
- Inspection reports
- Laser scans
- As-built documentation
- Sensor data
- Survey data
- Material test reports
- Change orders
- Field observation records

This list is not exhaustive. New evidence types may be admitted through governed determination.

---

## Evidence Strength

Not all evidence carries equal weight for identity determination. Evidence strength depends on:

- Proximity to the object (direct observation vs. derived reference)
- Temporal proximity to the event in question
- Authority of the producing agent
- Independence of the observation
- Completeness of the record

Evidence strength must be considered during governed identity evaluation. The system must not treat all evidence types as equivalent for identity continuity claims.

---

## Evidence Traceability Rule

Every piece of evidence must link to a traceable source artifact. The source artifact must be identifiable, locatable, and version-stable at the time of reference. Evidence without traceable source is not valid for governed determinations.

Traceability requires:

- Source artifact identifier
- Source artifact version or timestamp
- Extraction method or observation context
- Producing agent or authority

---

## Evidence Conflict Rule

Conflicting evidence must be preserved. Conflicting evidence must not be silently replaced, overwritten, or discarded.

When evidence conflicts:

- All conflicting evidence must be retained in the record
- Resolution must occur through governed determination
- The determination must record which evidence was accepted, which was set aside, and the basis for the decision
- The resolution itself becomes part of the auditable evidence record

Silent replacement of conflicting evidence is a governance violation.

---

## Safety Note

- This document defines construction-domain governance only
- No runtime code, schemas, or implementations are modified
- This doctrine is specific to the Construction domain and does not modify root ValidKernel governance
