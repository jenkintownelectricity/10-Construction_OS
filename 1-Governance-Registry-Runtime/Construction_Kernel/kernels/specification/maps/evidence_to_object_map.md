# Evidence-to-Object Map — Construction Specification Kernel

## How Evidence Maps to Specification Objects

This map shows how different evidence types relate to specification entities. The kernel records what evidence is required; the evidence itself is stored outside the kernel.

## Evidence-to-Entity Relationships

### Testing Requirements --> Test Evidence

| Testing Requirement Type | Evidence Type | Evidence Example |
|---|---|---|
| field_test | field_observation, inspection_report | Adhesion test results per ASTM D4541 |
| lab_test | lab_test | Laboratory air leakage test per ASTM E2357 |
| mock_up | field_observation, inspection_report | Mock-up evaluation report |
| preconstruction | lab_test, manufacturer_data | Preconstruction compatibility testing |

### Submittal Requirements --> Submittal Evidence

| Submittal Type | Evidence Type | Evidence Example |
|---|---|---|
| product_data | manufacturer_data | Product data sheet with performance values |
| shop_drawing | manufacturer_data | Detailed installation drawings |
| sample | field_observation | Physical material sample |
| test_report | lab_test | Independent lab test report |
| certificate | manufacturer_data | Manufacturer certification letter |
| warranty | manufacturer_data | Executed warranty document |
| mix_design | manufacturer_data | Concrete or coating mix proportions |

### Qualification Requirements --> Qualification Evidence

| Qualification Type | Evidence Type | Evidence Example |
|---|---|---|
| manufacturer | manufacturer_data | Manufacturer experience documentation |
| installer | manufacturer_data, inspection_report | Installer certification and project list |
| testing_agency | manufacturer_data | Testing agency accreditation certificate |
| inspector | manufacturer_data | Inspector certification documentation |

### Warranty Requirements --> Warranty Evidence

| Warranty Type | Evidence Type | Evidence Example |
|---|---|---|
| manufacturer_standard | manufacturer_data | Standard warranty document |
| manufacturer_extended | manufacturer_data | Extended warranty agreement |
| system_warranty | manufacturer_data | System warranty with inspection sign-off |
| nol | manufacturer_data | No-dollar-limit warranty document |
| workmanship | manufacturer_data | Contractor workmanship warranty |

## Evidence Chain Integrity

The specification kernel records step 1 of the evidence chain (what is required). Steps 2-4 occur outside the kernel:

1. **Specification states evidence requirement** (this kernel)
2. **Evidence is produced** (outside kernel)
3. **Evidence is reviewed** (outside kernel)
4. **Compliance is determined** (intelligence layer)
