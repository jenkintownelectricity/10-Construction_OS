# Evidence-to-Object Map

## Purpose

Documents how lab tests, manufacturer SDS documents, and field observations map to chemistry kernel records.

## Evidence Types

| Evidence Prefix | Source Type | Description |
|---|---|---|
| `EVD-LAB-` | Laboratory test | Controlled test results per ASTM or equivalent methods. |
| `EVD-FIELD-` | Field observation | Documented field condition, failure, or performance observation. |
| `EVD-MFR-TDS-` | Manufacturer TDS | Technical data sheet from product manufacturer. |
| `EVD-MFR-SDS-` | Manufacturer SDS | Safety data sheet from product manufacturer. |
| `EVD-MFR-GUIDE-` | Manufacturer guide | Application guide or installation instructions. |

## Evidence Consumers

| Chemistry Object | Evidence Field | Usage |
|---|---|---|
| Adhesion Rule | `evidence_refs` | Lab adhesion tests and field peel observations supporting adhesion status. |
| Incompatibility Rule | `evidence_refs` | Lab compatibility tests and field failure reports documenting adverse interactions. |
| Degradation Mechanism | `evidence_refs` | Accelerated aging tests and field condition surveys documenting deterioration. |
| Chemical Hazard Record | `sds_ref` | Manufacturer SDS providing hazard classification and precaution data. |
| Chemical Hazard Record | `regulatory_refs` | Regulatory citations (OSHA, EPA) governing hazard classification. |

## Evidence Quality Requirements

- Laboratory evidence must cite the test method (e.g., ASTM C794).
- Field evidence must include date, location context, and observer qualification.
- Manufacturer data must include product name, revision date, and document number.
- Critical severity incompatibility rules require at least one evidence reference.

## Data Flow

1. Evidence records are created and maintained outside the chemistry kernel.
2. Chemistry kernel records reference evidence by string ID only.
3. Evidence IDs are not validated by the kernel schema; integrity is enforced by governance.
4. Consumers trace chemistry claims back to evidence for audit and dispute resolution.

## Notes

- Evidence records are not stored in this kernel. They reside in an evidence registry or document management system.
- The kernel trusts evidence references at authoring time. Broken references are detected by external validation.
