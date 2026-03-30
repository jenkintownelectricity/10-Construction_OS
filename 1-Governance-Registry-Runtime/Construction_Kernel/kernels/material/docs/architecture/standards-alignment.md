# Standards Alignment — Construction Material Kernel

## Alignment Principle

This kernel aligns with ASTM International test methods as the primary standards framework for material property definition. Standards are referenced by citation only. No copyrighted standards text is stored, reproduced, or paraphrased in this kernel.

## Primary Standards Organizations

| Organization | Role in Material Kernel |
|---|---|
| ASTM International | Test methods defining material properties |
| AAMA | Window and curtain wall material test methods |
| UL | Fire classification test methods |
| FM Global | Roofing material approval test methods |
| CSA | Canadian material standards (future scope) |

## ASTM Test Method Categories

### Membrane Materials (Division 07 50 00)
- ASTM D751 — Coated fabrics (tensile, tear, adhesion)
- ASTM D4434 — PVC roofing membranes
- ASTM D6878 — TPO roofing membranes
- ASTM D4637 — EPDM roofing membranes
- ASTM D6162/D6163 — SBS/APP modified bitumen

### Insulation Materials (Division 07 20 00)
- ASTM C518 — Thermal transmission (heat flow meter)
- ASTM C578 — Rigid cellular polystyrene
- ASTM C1289 — Polyisocyanurate board
- ASTM C665 — Mineral fiber blanket insulation
- ASTM E96 — Water vapor transmission

### Flashing and Sealant Materials (Division 07 60 00/90 00)
- ASTM C920 — Elastomeric sealants
- ASTM D1970 — Self-adhered flashing
- ASTM E96 — Vapor permeance of flashing materials

### Fire Performance
- ASTM E84 — Surface burning characteristics (flame spread, smoke developed)
- ASTM E108 — Fire resistance of roof coverings
- UL 790 — Standard test methods for fire tests of roof coverings

## How Standards References Are Stored

Each material property record includes a `test_method_ref` field that points to a standards reference record. The standards reference record contains only: standard ID, title, edition, and applicability. The kernel never interprets what a test method measures — it only records which test method was used to generate a property value.

## Standards Version Tracking

When a test method is revised (e.g., ASTM D6878-17 to D6878-23), both versions may exist as separate standards reference records. Material properties tested under the older version retain their original reference. New properties reference the updated standard.
