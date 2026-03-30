# Object Model Overview — Construction Material Kernel

## Core Object Hierarchy

The material kernel organizes truth into seven primary object types, each governed by a dedicated JSON Schema with `additionalProperties: false`.

```
Material Class
  └── Material Form
        └── Material Property
        └── Material Performance
        └── Hygrothermal Property
        └── Weathering Behavior
  └── Compatibility Record (links two Material Classes/Forms)
```

## Object Definitions

### Material Class

The root classification entity. Identifies a material by its polymer or composition family. Enum-controlled: thermoplastic, thermoset, elastomer, bituminous, cementitious, metallic, mineral_fiber, cellular_plastic, composite, fluid_applied, sheet_applied, spray_applied.

### Material Form

The physical delivery form of a material class. A thermoplastic class may have sheet and membrane forms. Enum-controlled: sheet, liquid, foam, rigid_board, batt, loose_fill, paste, tape, coating, membrane, panel.

### Material Property

A single measured physical property attached to a material. Includes value, unit, test method reference, and optional test conditions. Examples: tensile strength (psi), elongation (%), vapor permeance (perms).

### Material Performance

An aggregate performance record that may reference multiple properties. Includes performance class, test results, and optional service life estimates with climate and geometry context.

### Compatibility Record

A pairwise relationship between two materials. Result is enum-controlled: compatible, incompatible, conditional, untested. Conditional records require a conditions field describing constraints.

### Weathering Behavior

A degradation record for a material under specific exposure. Exposure type is enum-controlled: uv, thermal_cycling, moisture, freeze_thaw, chemical, biological. Includes degradation rate and optional service life impact.

### Hygrothermal Property

A moisture-transport or thermal-moisture property. Type is enum-controlled: vapor_permeance, moisture_absorption, capillary_coefficient, sorption_isotherm, thermal_conductivity_wet.

## Cross-Object References

All objects reference each other by ID pointers, never by embedding. A Material Property points to its parent material via `material_ref`. A Compatibility Record points to two materials via `material_a_ref` and `material_b_ref`. Standards references use `test_method_ref` pointers.

## Schema Governance

Every object type has a frozen schema. Schema changes require version increment and baseline advancement. No object may contain fields not defined in its schema.
