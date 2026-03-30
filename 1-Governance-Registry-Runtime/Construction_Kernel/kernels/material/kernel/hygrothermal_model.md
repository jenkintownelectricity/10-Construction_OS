# Hygrothermal Model — Construction Material Kernel

## Purpose

This model defines how moisture transport and thermal-moisture interaction properties are recorded. Hygrothermal properties govern how materials handle water vapor, liquid moisture, and the interaction between moisture and thermal performance.

## Hygrothermal Property Record Structure

| Field | Type | Required | Description |
|---|---|---|---|
| property_id | string | Yes | Unique identifier |
| material_ref | string | Yes | ID of the parent material |
| property_type | enum | Yes | vapor_permeance, moisture_absorption, capillary_coefficient, sorption_isotherm, thermal_conductivity_wet |
| value | number/string | Yes | Measured value |
| unit | string | Yes | Unit of measurement |
| status | enum | Yes | active, draft, deprecated |
| test_method_ref | string | No | Standards reference for test method |
| temperature | string | No | Temperature at which measured |
| rh_conditions | string | No | Relative humidity conditions |
| notes | string | No | Additional context |

## Property Types

### Vapor Permeance
Rate of water vapor transmission through a material. Measured in perms (US) per ASTM E96. Two test methods: desiccant (dry cup) and water (wet cup), which may yield different values for the same material.

| Material Class | Typical Permeance | Classification |
|---|---|---|
| Polyethylene sheet (6 mil) | 0.06 perms | Vapor barrier (Class I) |
| Self-adhered membrane | 0.05-0.1 perms | Vapor barrier (Class I) |
| Kraft-faced insulation | 0.4-1.0 perms | Vapor retarder (Class II) |
| Latex paint (2 coats) | 5-10 perms | Vapor retarder (Class III) |
| Unfaced mineral wool | >50 perms | Vapor open |

### Moisture Absorption
Mass of water absorbed expressed as percentage of dry weight. Measured per ASTM D2247 or ASTM C209. Indicates material's tendency to take on moisture during service.

### Capillary Coefficient
Rate of liquid water uptake through capillary action. Measured as water absorption coefficient (kg/m2 s^0.5). Relevant for cementitious and mineral fiber materials.

### Sorption Isotherm
Equilibrium moisture content as a function of relative humidity at constant temperature. Characterizes how much moisture a material holds at different humidity levels.

### Thermal Conductivity (Wet)
Thermal conductivity of a material in a moisture-laden state. Generally higher than dry-state conductivity. Indicates R-value loss when material absorbs moisture.

## Condition Sensitivity

Hygrothermal properties are condition-sensitive:
- Vapor permeance changes with temperature and humidity differential
- Moisture absorption depends on exposure duration and water contact method
- Thermal conductivity increases with moisture content

## Rules

1. All hygrothermal values must state temperature and RH conditions
2. Wet-cup and dry-cup permeance are separate records (different test conditions)
3. The kernel does not model vapor drive or moisture transport through assemblies
4. Hygrothermal simulation input data may be sourced from this kernel, but simulation is not performed here
5. Variable permeance materials (smart vapor retarders) require multiple records at different RH levels
