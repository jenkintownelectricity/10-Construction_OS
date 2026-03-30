# Standards-to-Object Map — Construction Material Kernel

## Purpose
Maps ASTM and other test method standards to the kernel objects they define or measure.

## Membrane Material Standards

| Standard | Object Type | Properties Defined |
|---|---|---|
| ASTM D6878 | Material Class (thermoplastic/TPO) | Tensile, elongation, tear, puncture, weathering |
| ASTM D4434 | Material Class (thermoplastic/PVC) | Tensile, elongation, tear, dimensional stability |
| ASTM D4637 | Material Class (thermoset/EPDM) | Tensile, elongation, tear, ozone resistance |
| ASTM D6162 | Material Class (bituminous/SBS mod bit) | Tensile, elongation, tear, low-temp flexibility |
| ASTM D6163 | Material Class (bituminous/APP mod bit) | Tensile, elongation, tear, heat resistance |
| ASTM D751 | Material Property | Tensile, tear, adhesion test methods for coated fabrics |

## Insulation Standards

| Standard | Object Type | Properties Defined |
|---|---|---|
| ASTM C1289 | Material Class (cellular_plastic/polyiso) | R-value, compressive, dimensional stability |
| ASTM C578 | Material Class (cellular_plastic/XPS, EPS) | R-value, compressive, moisture absorption |
| ASTM C665 | Material Class (mineral_fiber/batt) | R-value, density, moisture resistance |
| ASTM C518 | Material Property | Thermal resistance test method |

## General Property Standards

| Standard | Object Type | Properties Defined |
|---|---|---|
| ASTM E96 | Hygrothermal Property | Water vapor permeance |
| ASTM E84 | Material Property | Flame spread index, smoke developed index |
| ASTM E108 | Material Performance | Fire resistance of roof coverings |
| ASTM D1970 | Material Class (sheet_applied) | Self-adhered membrane properties |
| ASTM C920 | Material Class (elastomer/sealant) | Sealant movement, adhesion, hardness |

## Weathering Standards

| Standard | Object Type | Properties Defined |
|---|---|---|
| ASTM G154 | Weathering Behavior | Fluorescent UV condensation exposure |
| ASTM G155 | Weathering Behavior | Xenon arc exposure |
| ASTM D4811 | Weathering Behavior | Non-bituminous roof covering weathering |

## Mapping Rules

1. Each property record's `test_method_ref` must map to a standards reference record
2. Material class standards (D6878, D4434, etc.) define minimum property requirements
3. Test method standards (D751, E96, etc.) define how properties are measured
4. Multiple properties may reference the same test method standard
