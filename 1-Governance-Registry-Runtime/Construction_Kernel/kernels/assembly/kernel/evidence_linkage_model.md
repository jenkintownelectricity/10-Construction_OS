# Evidence Linkage Model — Construction Assembly Kernel

## Purpose

Defines how assembly truth records link to supporting evidence. Every assembly configuration, test result, and continuity claim should be traceable to evidence. Evidence is referenced by pointer, never duplicated into this kernel.

## Evidence Types Relevant to Assembly Truth

From the shared evidence registry (`shared_evidence_registry.json`):

| Evidence Type | Assembly Relevance |
|---|---|
| lab_test | Test reports for fire rating, wind uplift, air leakage, water penetration |
| field_observation | Site verification of installed assembly configuration |
| inspection_report | Third-party inspection of assembly installation quality |
| commissioning_report | Building enclosure commissioning (BECx) verification results |
| manufacturer_data | Assembly installation guides, tested configurations, warranty requirements |
| forensic_report | Post-failure analysis documenting assembly defects |
| sensor_data | Moisture monitoring, thermal imaging of installed assemblies |
| warranty_claim | Documentation of assembly failures under warranty |

## Linkage Points in Kernel Objects

### tested_assembly_record

Most direct evidence linkage. Each tested assembly record includes:
- `test_standard_ref` — which test method was used
- `result` — test outcome (pass/fail, rating achieved)
- `evidence_ref` — pointer to the test report or lab documentation
- `lab_ref` — testing laboratory identifier
- `test_date` — date of test

### assembly_system

Assembly systems may reference evidence through:
- `tested_assembly_refs` — pointers to tested assembly records that validate the configuration
- `notes` — may cite evidence sources for unusual configurations

### transition_condition

Transitions at critical and high risk levels should include:
- `evidence_refs` — pointers to mock-up test results, field inspection reports, or detail review documentation

### penetration_condition

Penetration seal verification evidence:
- Evidence of seal method effectiveness from manufacturer test data or field testing

## Evidence Quality Tiers

From the shared evidence registry:

| Tier | Definition | Example |
|---|---|---|
| primary | Direct measurement or observation from qualified source | NFPA 285 test report from accredited lab |
| secondary | Published data, authoritative but not project-specific | Manufacturer's tested assembly listing |
| tertiary | Professional opinion, requires corroboration | Consultant's recommendation for untested detail |

## Evidence Obligations

| Record Type | Evidence Requirement |
|---|---|
| tested_assembly_record | Mandatory — must reference test report |
| assembly_system (active) | Recommended — should reference tested assembly or field verification |
| assembly_system (draft) | Not required — may be promoted when evidence is available |
| transition_condition (critical/high risk) | Recommended — mock-up or inspection evidence |
| penetration_condition | Recommended — seal verification evidence |
| continuity_requirement | Optional — may reference code section or analysis |

## Mock-Up Testing

Mock-up tests are a primary evidence source for assembly transitions and details:
- ASTM E331 mock-up tests for wall assembly water resistance
- AAMA 501.1 field tests for installed fenestration
- Project-specific mock-ups for complex transitions

Mock-up results link to transition_condition and penetration_condition records.

## Limitations

- Evidence is referenced, not stored. This kernel holds pointers, not documents.
- Evidence quality assessment is the responsibility of the intelligence layer.
- Conflicting evidence is recorded; resolution is not automated.
