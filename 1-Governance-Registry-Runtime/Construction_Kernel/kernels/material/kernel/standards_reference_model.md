# Standards Reference Model — Construction Material Kernel

## Purpose

This model defines how ASTM test methods and material standards are referenced within the kernel. Standards are cited by identifier and title only. No copyrighted text is stored or reproduced.

## Standards Reference Structure

Each standards reference record contains:

| Field | Required | Description |
|---|---|---|
| reference_id | Yes | Unique identifier for this reference |
| standard_id | Yes | Standard designation (e.g., "ASTM D6878") |
| title | Yes | Official standard title |
| applicability | Yes | What the standard measures or defines |
| test_method | No | Specific test procedure within the standard |
| edition | No | Year or edition (e.g., "2023") |
| notes | No | Kernel-internal notes on usage |

## Key ASTM Standards for Division 07 Materials

### Membrane Materials
| Standard | Applicability |
|---|---|
| ASTM D4434 | PVC roofing membrane properties |
| ASTM D6878 | TPO roofing membrane properties |
| ASTM D4637 | EPDM roofing membrane properties |
| ASTM D6162 | SBS modified bitumen cap sheet properties |
| ASTM D6163 | APP modified bitumen cap sheet properties |
| ASTM D751 | Coated fabric test methods (tensile, tear) |

### Insulation Materials
| Standard | Applicability |
|---|---|
| ASTM C578 | Rigid cellular polystyrene insulation |
| ASTM C1289 | Faced rigid polyisocyanurate insulation |
| ASTM C665 | Mineral fiber blanket thermal insulation |
| ASTM C518 | Thermal transmission by heat flow meter |

### Properties and Performance
| Standard | Applicability |
|---|---|
| ASTM E96 | Water vapor transmission of materials |
| ASTM E84 | Surface burning characteristics |
| ASTM E108 | Fire tests of roof coverings |
| ASTM D1970 | Self-adhered polymer modified bitumen sheet |
| ASTM C920 | Elastomeric joint sealants |

## Citation Rules

1. Standards are referenced by designation and title — never by content
2. Test method references in property records point to standards reference records by ID
3. When a standard is revised, a new reference record is created; existing property records retain original references
4. Standards from multiple organizations (ASTM, AAMA, UL, FM) follow the same reference structure
5. The kernel records which standard was used, not what the standard requires
