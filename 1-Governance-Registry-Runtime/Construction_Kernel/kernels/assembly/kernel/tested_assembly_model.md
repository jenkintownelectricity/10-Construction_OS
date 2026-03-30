# Tested Assembly Model — Construction Assembly Kernel

## Definition

A tested assembly record documents a specific assembly configuration validated by a specific test under a specific standard. The truth is narrow and precise: this exact configuration, tested by this method, produced this result. No extrapolation, no interpolation, no inference to untested configurations.

## Tested Assembly Record Structure

| Property | Required | Description |
|---|---|---|
| record_id | Yes | Unique identifier |
| title | Yes | Human-readable description of the tested configuration |
| test_type | Yes | fire_rating, wind_uplift, structural, air_leakage, water_penetration, thermal |
| test_standard_ref | Yes | Reference ID of the test method standard |
| result | Yes | Test outcome (pass/fail, rating, classification, measured value) |
| status | Yes | active, draft, deprecated |
| assembly_ref | No | Pointer to the assembly system record this test validates |
| test_date | No | Date the test was performed |
| lab_ref | No | Testing laboratory identifier |
| evidence_ref | No | Pointer to the test report |

## Test Types

### fire_rating

Assembly tested for fire resistance or fire propagation characteristics.
- **NFPA 285**: Exterior wall assembly fire propagation. Tests the complete wall assembly including all layers. Result is pass/fail.
- **ASTM E119 / UL 263**: Fire endurance test. Result is hourly fire-resistance rating (1-hour, 2-hour, etc.).
- **UL design numbers**: Specific tested configurations listed in UL directories.

### wind_uplift

Assembly tested for resistance to wind uplift forces.
- **FM 4450 / FM 4470**: Factory Mutual approval. Result is FM classification (Class 1) with specific wind uplift rating (1-60, 1-90, 1-120, etc.).
- **UL 580**: Wind uplift classification. Result is UL class (30, 60, 90).
- **SPRI ES-1**: Edge securement test. Result is pass/fail for specific edge detail at specified wind speed.

### air_leakage

Assembly tested for air leakage rate.
- **ASTM E2357**: Air leakage of building enclosure assembly. Result is air leakage rate in CFM/SF at specified pressure differential.
- **ASTM E783**: Air leakage of fenestration assemblies.

### water_penetration

Assembly tested for resistance to water infiltration.
- **ASTM E331**: Water penetration of exterior wall assemblies. Result is pass/fail at specified pressure and duration.
- **AAMA 501.1**: Water penetration of installed fenestration.

### structural

Assembly tested for structural adequacy under specified loads.
- **ASTM E330**: Structural performance of exterior windows under uniform air pressure.

### thermal

Assembly tested for thermal performance.
- **ASTM C518**: Thermal transmission by heat flow meter. Result is R-value or thermal conductivity.
- **Hot-box testing**: Full-assembly thermal performance including thermal bridges.

## Immutability

Tested assembly records have `immutable` revision posture. Once a test result is recorded, it cannot be changed. If a test is re-run, a new record is created.

## Configuration Specificity

A tested assembly record is valid only for the exact configuration tested. Changing any component — substrate, insulation type or thickness, membrane, adhesive, fastener pattern — potentially invalidates the test result.

The kernel records tested configurations with sufficient detail to determine whether a proposed assembly matches the tested configuration. The `assembly_ref` links to the full layer stack of the tested configuration.

## Common Tested Assembly Configurations

### NFPA 285 Wall Assembly

Tested configuration includes: substrate (steel stud + gypsum sheathing), air barrier (self-adhered membrane), insulation (polyiso, 3" thick), cladding attachment (metal clips), cladding (aluminum composite panel). Changing any component requires re-testing.

### FM Approved Roof Assembly

Tested configuration includes: deck type (steel, 22 ga), vapor retarder, insulation (polyiso, 2 layers, staggered joints), cover board (high-density polyiso), membrane (60-mil TPO, fully adhered). FM approval specifies exact products and attachment.

## Limitations

- Test results apply only to the tested configuration. Substitution analysis is outside kernel scope.
- Test method interpretation and applicability determination are outside kernel scope.
- Product-specific test listings (FM, UL) are maintained by those organizations, not by this kernel.
