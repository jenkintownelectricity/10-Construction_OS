# Standards Model — Construction Material Kernel

## Purpose

This model defines how ASTM and other test method standards are represented in the kernel. Standards define the test methods by which material properties are measured. The kernel references standards by citation; it never reproduces standards content.

## Standards Record Structure

| Field | Type | Required | Description |
|---|---|---|---|
| reference_id | string | Yes | Unique identifier |
| standard_id | string | Yes | Standard designation (e.g., ASTM D6878) |
| title | string | Yes | Official standard title |
| applicability | string | Yes | What the standard measures or defines |
| test_method | string | No | Specific test within multi-part standard |
| edition | string | No | Year or edition identifier |
| notes | string | No | Internal usage notes |

## Standards Organization Coverage

| Organization | Scope in This Kernel |
|---|---|
| ASTM International | Primary — material property test methods |
| AAMA | Window and curtain wall material tests |
| UL | Fire classification and safety tests |
| FM Global | Roofing material approval tests |
| NRCA | Roofing material guidelines (informational) |
| SPRI | Single-ply roofing material guidelines |

## Standards-to-Property Linkage

Every material property record contains a `test_method_ref` field that points to a standards reference record. This linkage establishes:

1. Which test method generated the property value
2. What conditions the test method prescribes
3. Which edition of the standard was in effect

## Standards Versioning

When a standard is revised:
- A new standards reference record is created for the new edition
- Existing property records retain their original standards reference
- New property records reference the current edition
- Both editions coexist in the kernel

## Division 07 Standards Map

| Subdivision | Key Standards |
|---|---|
| 07 10 00 Waterproofing | ASTM D1970, ASTM D4586 |
| 07 20 00 Insulation | ASTM C518, C578, C1289, C665 |
| 07 50 00 Membrane roofing | ASTM D4434, D4637, D6878, D6162, D6163 |
| 07 60 00 Flashing | ASTM D1970, ASTM B370 |
| 07 90 00 Sealants | ASTM C920, ASTM C1193 |

## Standards Integrity Rules

1. Standards are cited by designation and official title only
2. No copyrighted text, tables, or figures from standards are stored
3. Standards references do not interpret what a test method measures
4. Standards editions are tracked to ensure property values align with the correct version
5. Non-ASTM standards follow the same reference structure
