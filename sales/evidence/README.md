# Evidence Index

## Barrett PMMA Packet

| Artifact | Path | Description |
|----------|------|-------------|
| Combined PDF | `output/barrett_pmma_packet/client/Barrett_PMMA_Detail_Packet_v1.pdf` | 10-page print-ready packet |
| Print SVGs | `output/barrett_pmma_packet/print/*.svg` | 10 individual detail sheets |
| Assembly JSONs | `output/barrett_pmma_packet/json/*.json` | 10 canonical assembly records |
| DXF files | `output/barrett_pmma_packet/dxf/*.dxf` | 10 layered CAD files |

## Parametric Renderer Proof

| Artifact | Path | Description |
|----------|------|-------------|
| Rendered SVG | `output/barrett_pmma_parametric_rendered/svg/barrett_pmma_equipment_curb_001_rendered.svg` | Equipment curb rendered from geometry JSON |
| Geometry JSON | `output/barrett_pmma_parametric_test/json/barrett_pmma_equipment_curb_001_geometry.json` | Source geometry payload |
| Render report | `output/barrett_pmma_parametric_rendered/report/equipment_curb_render_report.md` | 13/13 validation checks PASS |

## Why These Outputs Matter

These are not mockups or wireframes. They are real generated construction detail sheets produced from structured manufacturer data through a parametric pipeline. The equipment curb SVG was rendered directly from a geometry JSON payload — proving the system can produce details without manual drawing.
