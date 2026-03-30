# Evidence Linkage Model — Construction Material Kernel

## Purpose

Every material property in this kernel traces to a published evidence source. This model defines evidence types, linkage structure, and quality requirements.

## Evidence Types

| Type | Code | Description |
|---|---|---|
| Laboratory test report | LAB | Independent laboratory test results per ASTM methods |
| Manufacturer TDS | TDS | Manufacturer technical data sheet with published properties |
| Field performance study | FLD | Documented field performance observation or study |
| Forensic analysis report | FOR | Post-failure material analysis report |
| Accelerated weathering test | AWX | Xenon arc, QUV, or equivalent accelerated aging data |
| Peer-reviewed publication | PUB | Published building science research |

## Evidence Linkage Structure

Each material property record includes an `evidence_ref` field containing:

- **evidence_type** — one of the codes above
- **source_id** — unique identifier for the evidence document
- **source_title** — human-readable title of the evidence source
- **date** — date of evidence document or test
- **relevance** — how this evidence supports the property value

## Evidence Quality Hierarchy

| Rank | Evidence Type | Confidence |
|---|---|---|
| 1 | Independent laboratory test report | Highest |
| 2 | Peer-reviewed publication | High |
| 3 | Manufacturer TDS (with test method citation) | High |
| 4 | Accelerated weathering test report | Moderate-High |
| 5 | Field performance study | Moderate |
| 6 | Manufacturer TDS (without test method) | Low |
| 7 | Forensic analysis report | Context-dependent |

## Evidence Rules

1. **No unsourced properties** — every property value must have at least one evidence reference
2. **Test method alignment** — evidence must reference the same test method as the property record
3. **Date currency** — evidence older than 15 years should be flagged for review
4. **Manufacturer TDS preference** — when both TDS and lab data exist, lab data takes precedence for property values
5. **Contradiction handling** — when evidence sources conflict, the ambiguity flag is set and both sources are recorded

## Evidence Gaps

When a material is expected to have a property but no evidence exists, the property record is not created. The absence of a property record signals a data gap. The intelligence layer surfaces evidence gaps for resolution. Empty or placeholder property values are not permitted.

## Linkage to Other Kernels

Evidence linkage is a material-kernel function. The Chemistry Kernel may reference the same evidence documents for chemical analysis. Evidence documents are not duplicated across kernels — each kernel records its own evidence linkage to the shared document identifier.
