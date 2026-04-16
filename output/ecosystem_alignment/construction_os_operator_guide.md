# Construction_OS Operator Guide

## Role
10-Construction_OS is the DETAIL COMPILER — the canonical production system for generating construction detail packets.

## How to Run the Pipeline

### Step 1: Select Condition
Choose from 120 canonical conditions in `atlas/global_condition_atlas/canonical_conditions_v2.json` or from the 10 Barrett PMMA conditions in `source/barrett/condition_maps/barrett_pmma_condition_family_map.json`.

### Step 2: Generate Geometry
```bash
python3 generators/pmma/pmma_flash_generator.py \
  source/barrett/calibration/barrett_pmma_calibration_specimen_001.json \
  output/barrett_pmma_parametric_test/json
```
Produces normalized geometry JSON for all 10 conditions.

### Step 3: Render SVG Sheets
```bash
python3 renderers/svg_section_renderer.py \
  output/barrett_pmma_parametric_test/json/barrett_pmma_equipment_curb_001_geometry.json \
  output/barrett_pmma_parametric_rendered/svg/05_equipment_curb_rendered.svg
```
Or render all 10 in a loop.

### Step 4: Compile PDF
```bash
pip install cairosvg pypdf
python3 tools/export_svg_to_pdf.py \
  --input output/barrett_pmma_parametric_rendered/svg/ \
  --output output/barrett_pmma_parametric_rendered/pdf/Barrett_PMMA_Parametric_Rendered_Packet_v1.pdf
```

### Step 5: Export DXF
```bash
pip install ezdxf
python3 tools/export_assembly_to_dxf.py \
  --input output/barrett_pmma_packet/json/ \
  --output output/barrett_pmma_packet/dxf/
```

## How to Validate Outputs
Each rendered SVG must pass:
1. White background (#FFFFFF)
2. 2+ rect elements (real geometry)
3. 3+ total geometry elements
4. "Barrett PMMA" in title
5. "DETAIL ATLAS" in titleblock
6. "CALLOUT KEY" present
7. SVG > 2000 bytes

## How to Publish Artifacts
1. Push to branch: `git push -u origin claude/emergency-system-reconstruction-4hLpM`
2. Create PR for merge to main
3. For client delivery: use PDF from `output/*/client/` folder
