# Generator / Engine / Renderer Organization Rules

## Canonical Folder Boundaries

```
10-Construction_OS/
  generators/     ← condition → geometry JSON (parametric functions)
  renderers/      ← geometry JSON → SVG sheet (coordinate rendering)
  tools/          ← export utilities (SVG→PDF, JSON→DXF)
  schemas/        ← validation schemas
  kernels/        ← assembly DNA templates
  source/         ← calibration specimens, manufacturer data
  registries/     ← active runtime registry (generator registry)
  output/         ← generated artifacts (SVG, PDF, DXF, reports)
  receipts/       ← execution lineage records
```

## What Belongs Where

| Module | Folder | Responsibility |
|--------|--------|---------------|
| Parametric generator | generators/ | Condition → normalized geometry JSON |
| SVG section renderer | renderers/ | Geometry JSON → print-ready SVG |
| PDF export | tools/ | SVG → combined PDF packet |
| DXF export | tools/ | Assembly JSON → layered DXF |
| Assembly DNA | kernels/ | Rules, layer stacks, constraints |
| Calibration data | source/ | Measured dimensions from CAD/field |
| Condition maps | source/ | Condition→generator mapping |

## What Must NOT Be Mixed

1. **Generators must not render.** They produce geometry JSON, not SVG markup.
2. **Renderers must not generate geometry.** They consume coordinates, not conditions.
3. **Tools must not contain business logic.** They convert formats, not resolve assemblies.
4. **No hidden exporters in UI repos.** WLV may have interactive exporters for its workstation, but batch production exports live in Construction_OS tools/.
5. **No shadow packet compilers.** One packet compilation path. One.

## Naming Rules

- Generators: `{system}_{family}_generator.py` (e.g., `pmma_flash_generator.py`)
- Renderers: `svg_section_renderer.py` (generic, reads any geometry JSON)
- Export tools: `export_{input}_to_{output}.py` (e.g., `export_svg_to_pdf.py`)
- Schemas: `{subject}.schema.json` (e.g., `barrett_pmma_measured_geometry.schema.json`)

## Canonical Ownership

| Function | Owner | NOT owned by |
|----------|-------|-------------|
| Batch SVG generation | Construction_OS renderers/ | WLV, ShopDrawing_Compiler |
| Batch PDF compilation | Construction_OS tools/ | WLV, ShopDrawing_Compiler |
| Batch DXF export | Construction_OS tools/ | GPC (reference), Runtime (reference) |
| Interactive editing | WLV apps/workstation/ | Construction_OS |
| Pattern resolution | ALEXANDER engine/ | Construction_OS |
