# Standards Reference Model — Construction Assembly Kernel

## Purpose

Defines how this kernel references standards, test methods, and code requirements. Standards are referenced by citation only — no standards text is reproduced.

## Reference Mechanism

All standards references use the `reference_id` values from the shared standards registry at `Construction_Reference_Intelligence/shared/shared_standards_registry.json`.

### In Assembly Records

The `standards_refs` array on `assembly_system` objects lists applicable standards:

```json
"standards_refs": ["IBC", "ASHRAE_90_1", "NFPA_285"]
```

### In Tested Assembly Records

The `test_standard_ref` field identifies the specific test method:

```json
"test_standard_ref": "NFPA_285"
```

### In Continuity Requirements

Requirements may reference the code section driving the obligation in the `conditions` field.

## Standards Categories Relevant to Assembly Truth

### Building Codes (Mandatory Compliance)

- **IBC**: Fire resistance ratings, weather protection, structural requirements for assemblies
- **ASHRAE 90.1**: Thermal performance requirements by climate zone. Drives insulation type, thickness, and position in assemblies.

### Fire Test Standards

- **NFPA 285**: Exterior wall assembly fire propagation. Tests complete wall assembly including all layers.
- **ASTM E119 / UL 263**: Fire endurance testing for rated assemblies.
- **ASTM E84**: Surface burning characteristics of building materials (component-level, not assembly-level).

### Wind Uplift Standards

- **FM 4450 / FM 4470**: Approval standard for Class 1 roof systems. Tests wind uplift resistance of complete roof assembly.
- **UL 580**: Wind uplift classification for roof assemblies.
- **SPRI ES-1**: Edge securement test for low-slope membrane roof systems.

### Water and Air Test Standards

- **ASTM E331**: Water penetration of exterior wall assemblies under uniform air pressure.
- **ASTM E2357**: Air leakage rate of building enclosure assemblies using fan pressurization.
- **AAMA 501.1 / 503**: Wall assembly water infiltration and structural testing.

### Thermal Performance Standards

- **ASTM C518**: Steady-state thermal transmission by heat flow meter apparatus.
- **ASTM C1549**: Determination of solar reflectance.

## Governing Relationships

From the shared standards registry, standards have defined governing relationships:

| Relationship | Meaning |
|---|---|
| mandatory_compliance | Assembly must comply; no exception |
| mandatory_compliance_where_applicable | Assembly must comply when conditions trigger applicability |
| test_method_authority | Defines the accepted test procedure |
| advisory | Guidance for best practice; not mandatory |
| classification_authority | Defines classification system used for organizing |

## Limitations

- This kernel records which standards apply and what test results were achieved.
- It does not interpret code intent, track code adoption by jurisdiction, or determine applicability thresholds.
- Jurisdiction-specific requirements (local amendments, AHJ interpretations) are outside kernel scope.
