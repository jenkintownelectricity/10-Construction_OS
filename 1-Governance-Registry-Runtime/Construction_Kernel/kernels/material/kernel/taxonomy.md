# Taxonomy — Construction Material Kernel

## Material Class Taxonomy

Materials are classified by their primary composition or application method. The taxonomy uses a controlled enum sourced from the shared family taxonomy registry.

### Primary Material Classes

| Class ID | Name | Description | Division 07 Examples |
|---|---|---|---|
| thermoplastic | Thermoplastic | Heat-weldable polymer membranes | TPO, PVC roofing membranes |
| thermoset | Thermoset | Chemically cured polymer membranes | EPDM roofing membranes |
| elastomer | Elastomer | Flexible rubber-based materials | Sealants, gaskets, flashings |
| bituminous | Bituminous | Asphalt or coal-tar based materials | Modified bitumen, BUR, dampproofing |
| cementitious | Cementitious | Portland cement based materials | Stucco, fiber cement, fireproofing |
| metallic | Metallic | Metal sheet and panel materials | Flashing, roof panels, copings |
| mineral_fiber | Mineral Fiber | Inorganic fiber insulation | Fiberglass batts, mineral wool boards |
| cellular_plastic | Cellular Plastic | Closed or open cell foam insulation | Polyiso, XPS, EPS boards |
| composite | Composite | Multi-material engineered products | Composite panels, coverboards |
| fluid_applied | Fluid Applied | Liquid-applied coatings and membranes | Air barriers, waterproofing, coatings |
| sheet_applied | Sheet Applied | Self-adhered or mechanically attached sheets | Peel-and-stick membranes, vapor retarders |
| spray_applied | Spray Applied | Field-sprayed materials | SPF insulation, spray fireproofing |

### Material Form Types

| Form ID | Description |
|---|---|
| sheet | Flat flexible material in rolls or sheets |
| liquid | Liquid applied by spray, roller, or trowel |
| foam | Cellular material (rigid or flexible) |
| rigid_board | Rigid flat panel or board |
| batt | Semi-rigid blanket insulation |
| loose_fill | Granular or fibrous loose material |
| paste | Thick viscous material applied by gun or trowel |
| tape | Narrow strip with adhesive backing |
| coating | Thin liquid film applied to surfaces |
| membrane | Continuous waterproof or air-barrier layer |
| panel | Rigid structural or semi-structural panel |

## Taxonomy Rules

1. Every material record must have exactly one `primary_material_class` from the enum above
2. Material class values are sourced from `shared_taxonomy.json`
3. A material class may have multiple applicable form types
4. Taxonomy is append-only — new classes require shared registry update
5. Taxonomy does not encode hierarchy — all classes are peers at the top level

## Control Layer Mapping by Class

| Material Class | Typical Control Layers |
|---|---|
| thermoplastic | Water, air |
| thermoset | Water |
| elastomer | Water, air (sealants at joints) |
| bituminous | Water, vapor |
| cellular_plastic | Thermal |
| mineral_fiber | Thermal, fire |
| fluid_applied | Water, air, vapor |
| sheet_applied | Water, air, vapor |
| spray_applied | Thermal, air |
