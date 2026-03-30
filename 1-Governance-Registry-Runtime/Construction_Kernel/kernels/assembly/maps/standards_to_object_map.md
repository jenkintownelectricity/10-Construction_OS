# Standards-to-Object Map — Construction Assembly Kernel

## Purpose

Maps standards references to the kernel objects they govern or validate.

## Standards Mapping

### IBC — International Building Code

| IBC Section | Kernel Object | Relationship |
|---|---|---|
| Chapter 14 (Exterior Walls) | assembly_system (wall_assembly) | Governs wall assembly requirements |
| Chapter 15 (Roof Assemblies) | assembly_system (roof_assembly) | Governs roof assembly requirements |
| Table 601 / 602 (Fire Resistance) | tested_assembly_record (fire_rating) | Defines required fire ratings |
| Section 1402.2 (Weather Protection) | continuity_requirement (bulk_water_control) | Drives water control continuity |
| Section 1503 (Weather Protection) | assembly_system (roof_assembly) | Requires weather protection |

### NFPA 285

| Requirement | Kernel Object | Relationship |
|---|---|---|
| Exterior wall fire propagation test | tested_assembly_record (fire_rating) | Test validates wall assembly |
| Component-specific tested configuration | assembly_system (wall_assembly) | Assembly must match tested configuration |
| Floor-line fire barrier | transition_condition (expansion_joint) | Fire continuity at floor lines |

### ASHRAE 90.1

| Section | Kernel Object | Relationship |
|---|---|---|
| Section 5 (Building Envelope) | assembly_system (all types) | Thermal performance requirements |
| Table 5.5 (Insulation Requirements) | assembly_layer (thermal_control) | Minimum insulation R-values |
| Air barrier requirements | continuity_requirement (air_control) | Air barrier continuity obligation |
| Continuous insulation (ci) | assembly_layer (thermal_control) | Layer position requirements |

### FM 4450 / FM 4470

| Requirement | Kernel Object | Relationship |
|---|---|---|
| Wind uplift classification | tested_assembly_record (wind_uplift) | Test validates roof assembly |
| Assembly approval | assembly_system (roof_assembly) | Configuration must match FM listing |

### SPRI ES-1

| Requirement | Kernel Object | Relationship |
|---|---|---|
| Edge securement test | edge_condition | Edge detail must meet ES-1 |
| Wind speed classification | edge_condition | Edge treatment rated for wind zone |

### ASTM Test Methods

| Standard | Kernel Object | Relationship |
|---|---|---|
| ASTM E2357 (Air Leakage) | tested_assembly_record (air_leakage) | Test method for air barrier testing |
| ASTM E331 (Water Penetration) | tested_assembly_record (water_penetration) | Test method for water resistance |
| ASTM E119 (Fire Endurance) | tested_assembly_record (fire_rating) | Test method for fire rating |
| ASTM C518 (Thermal) | tested_assembly_record (thermal) | Test method for R-value |
