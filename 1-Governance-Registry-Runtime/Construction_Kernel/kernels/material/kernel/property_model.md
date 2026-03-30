# Property Model — Construction Material Kernel

## Purpose

This model defines how physical properties are recorded. A property is a single measured characteristic of a material, expressed as a value with units, linked to a test method and evidence source.

## Property Record Structure

| Field | Type | Required | Description |
|---|---|---|---|
| property_id | string | Yes | Unique property identifier |
| material_ref | string | Yes | ID of the parent material |
| property_name | string | Yes | Name of the property |
| value | number/string | Yes | Measured value |
| unit | string | Yes | Unit of measurement |
| test_method_ref | string | Yes | Reference to standards record |
| status | enum | Yes | active, draft, deprecated |
| conditions | string | No | Test conditions (temp, RH, age) |
| temperature_range | object | No | Applicable temperature range |
| notes | string | No | Additional context |

## Property Categories

### Mechanical Properties
| Property | Unit | Typical Test Method |
|---|---|---|
| Tensile strength | psi or MPa | ASTM D751, D412 |
| Elongation at break | % | ASTM D751, D412 |
| Tear resistance | lbf or N | ASTM D751 (tongue tear) |
| Puncture resistance | lbf or N | ASTM D5602, ASTM E154 |
| Compressive strength | psi | ASTM D1621 |

### Thermal Properties
| Property | Unit | Typical Test Method |
|---|---|---|
| Thermal resistance (R-value) | ft2 hr degF/BTU | ASTM C518 |
| Thermal conductivity | BTU in/hr ft2 degF | ASTM C518 |
| Linear thermal expansion | in/in/degF | ASTM D696 |

### Moisture Properties
| Property | Unit | Typical Test Method |
|---|---|---|
| Water vapor permeance | perms (US) | ASTM E96 |
| Moisture absorption | % by weight | ASTM D2247 |
| Water penetration resistance | pass/fail | ASTM D5957 |

### Fire Properties
| Property | Unit | Typical Test Method |
|---|---|---|
| Flame spread index | dimensionless | ASTM E84 |
| Smoke developed index | dimensionless | ASTM E84 |
| Fire resistance rating | hours | ASTM E119 |

### Dimensional Properties
| Property | Unit | Typical Test Method |
|---|---|---|
| Thickness | mils or mm | ASTM D751 |
| Density | pcf or kg/m3 | ASTM D1622 |
| Dimensional stability | % change | ASTM D1204 |

## Property Value Rules

1. Values are numeric except for pass/fail or classification results
2. Units must be stated explicitly — no implied units
3. Test conditions must be stated when they affect the value
4. Multiple values for the same property under different conditions are separate records
5. Property values must match the precision of the source evidence
