# Evidence-to-Object Map — Construction Assembly Kernel

## Purpose

Maps evidence types to the kernel objects they support, validate, or challenge.

## Evidence Type Mapping

### lab_test

| Target Object | Evidence Role |
|---|---|
| tested_assembly_record | Primary evidence — test report validates the tested configuration |
| assembly_system | Supporting evidence — tested configuration validates the assembly design |

### field_observation

| Target Object | Evidence Role |
|---|---|
| assembly_system | Validates as-built configuration matches design intent |
| transition_condition | Confirms transition detail was properly executed |
| penetration_condition | Confirms seal method was properly installed |
| edge_condition | Confirms edge treatment was properly secured |

### inspection_report

| Target Object | Evidence Role |
|---|---|
| assembly_system | Third-party verification of layer stack installation |
| transition_condition | Inspection of critical transitions |
| penetration_condition | Inspection of penetration seals |
| tie_in_condition | Inspection of new-to-existing connections |

### commissioning_report

| Target Object | Evidence Role |
|---|---|
| assembly_system | BECx verification of complete assembly performance |
| continuity_requirement | Verification that continuity requirements are met |

### manufacturer_data

| Target Object | Evidence Role |
|---|---|
| assembly_system | Manufacturer's tested assembly listing supports configuration |
| assembly_component | Product data sheet confirms component properties |
| tested_assembly_record | Manufacturer's test data supports test result |

### forensic_report

| Target Object | Evidence Role |
|---|---|
| assembly_system | Post-failure analysis identifies assembly defects |
| transition_condition | Forensic finding at failed transition |
| penetration_condition | Forensic finding at failed penetration |

### sensor_data

| Target Object | Evidence Role |
|---|---|
| assembly_system | Moisture or thermal monitoring validates assembly performance |
| continuity_requirement | Sensor data confirms or denies continuity |

### warranty_claim

| Target Object | Evidence Role |
|---|---|
| assembly_system | Warranty claim documents assembly failure |
| tested_assembly_record | Claim may challenge validity of tested configuration |

## Evidence Priority by Object Type

| Object Type | Primary Evidence | Secondary Evidence |
|---|---|---|
| tested_assembly_record | lab_test | manufacturer_data |
| assembly_system (active) | field_observation, inspection_report | manufacturer_data, commissioning_report |
| transition_condition (critical) | field_observation, inspection_report | lab_test (mock-up) |
| penetration_condition | inspection_report | field_observation |
| continuity_requirement | commissioning_report | sensor_data, inspection_report |
