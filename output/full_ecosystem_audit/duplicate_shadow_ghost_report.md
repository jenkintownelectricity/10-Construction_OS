# Duplicate / Shadow / Ghost Path Report

## Duplicate SVG Generators (4 instances)

| Repo | File | Size | Language | Status |
|------|------|------|----------|--------|
| Construction_Runtime | generator/svg_writer.py | 6.1KB | Python | WIRED_BUT_UNREACHABLE (needs DrawingInstructionSet) |
| WLV Vision OS | apps/workstation/export/SVGExportRenderer.ts | 3.9KB | TypeScript | LIVE but requires running web app |
| ShopDrawing_Compiler | engines/export/svg_exporter.ts | 2.9KB | TypeScript | WIRED_BUT_UNREACHABLE (no proven e2e) |
| 10-Construction_OS | Direct SVG generation in print/ | N/A | Parametric | LIVE — currently the only one producing actual artifacts |

**Canonical owner:** 10-Construction_OS (for batch) / WLV (for interactive)

## Duplicate DXF Generators (4 instances)

| Repo | File | Size | Language | Status |
|------|------|------|----------|--------|
| GPC_Shop_Drawings | src/dxf_generator.py | 28.8KB | Python | MOST MATURE — real CAD geometry |
| Construction_Runtime | generator/dxf_writer.py | 5.5KB | Python | PARTIAL — needs DrawingInstructionSet |
| WLV Vision OS | apps/workstation/export/DXFExportRenderer.ts | 6.6KB | TypeScript | LIVE but requires web app |
| ShopDrawing_Compiler | engines/export/dxf_exporter.ts | 2.7KB | TypeScript | WIRED_BUT_UNREACHABLE |

**Canonical owner for production DXF:** GPC_Shop_Drawings (most mature code)
**Canonical owner for batch DXF from JSON:** 10-Construction_OS tools/export_assembly_to_dxf.py (ezdxf)

## Duplicate PDF Generators (3 instances)

| Repo | File | Size | Language | Status |
|------|------|------|----------|--------|
| WLV Vision OS | apps/workstation/export/PDFExportRenderer.ts | 4.3KB | TypeScript | LIVE but requires web app |
| ShopDrawing_Compiler | engines/export/pdf_exporter.ts | 3.2KB | TypeScript | WIRED_BUT_UNREACHABLE |
| 10-Construction_OS | tools/export_svg_to_pdf.py | 6.7KB | Python | LIVE — producing actual PDFs now |

**Canonical owner:** 10-Construction_OS (for batch PDF)

## Duplicate Assembly/Condition Resolution

| Repo | Mechanism | Status |
|------|-----------|--------|
| Construction_OS | assemblies/barrett/ + atlas/ | LIVE — actual source data |
| Construction_Assembly_Kernel | kernel/ + assemblies/ | PARTIAL — schemas only |
| Construction_ALEXANDER_Engine | 8-stage pipeline | LIVE but advisory, not consumed |
| Construction_Atlas | condition_nodes/ + detail_renderer/ | LIVE web UI, not batch |

## Ghost Repos (no real content)

| Repo | Evidence |
|------|----------|
| 50-validkernel-architect-reasoning-workspace | README only (550 bytes) |
| 60-validkernel-schematic-digital-twin | README only (691 bytes) |

## Shadow / Stale Paths

| Path | Problem |
|------|---------|
| Construction_OS_Sales_Command_Center generators/ | Declared not implemented |
| vkbus event routing | Framework skeleton, incomplete |
| ALEXANDER → WLV handoff contract | Contract exists, invocation does not |
