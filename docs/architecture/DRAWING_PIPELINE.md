# Drawing Pipeline

## End-to-End Flow

```
Assembly DNA Template (rules + layer stack + geometry constraints)
    ↓
Calibration Specimen (measured dimensions from CAD/field)
    ↓
Parametric Generator (10 condition functions)
    ↓
Geometry JSON (normalized coordinate payload: rects, lines, paths, callouts, dims)
    ↓
SVG Section Renderer (reads JSON, draws geometry, applies layer styles)
    ↓
PRINT_STANDARD SVG (white bg, black linework, titleblock, callout key)
    ↓
PDF Export (cairosvg + pypdf → combined multi-page packet)
    ↓
DXF Export (ezdxf → layered CAD file per condition)
```

## Stage Details

### 1. Assembly DNA Template
- File: `kernels/assembly_dna/pmma/barrett_pmma_flash_template.json`
- Contains: geometry rules (min turnup, cant dimensions, reinforcement widths), layer stack (primer → resin → fleece → seal coat), condition family map, export defaults

### 2. Calibration Specimen
- File: `source/barrett/calibration/barrett_pmma_calibration_specimen_001.json`
- Contains: measured dimensions for each condition (slab thickness, curb height, etc.)
- Source: Barrett CAD detail LF-CU-01 + Barrett TDS

### 3. Parametric Generator
- File: `generators/pmma/pmma_flash_generator.py`
- Functions: `generate_parapet()`, `generate_edge()`, `generate_primary_drain()`, `generate_pipe_penetration()`, `generate_equipment_curb()`, `generate_inside_corner()`, `generate_outside_corner()`, `generate_crack_control_joint()`, `generate_tile_overburden()`, `generate_expansion_joint()`
- Output: Normalized geometry JSON with elements[], dimensions[], callouts[]

### 4. SVG Section Renderer
- File: `renderers/svg_section_renderer.py`
- Input: Geometry JSON
- Layer styles: substrate (stippled fill), insulation (diagonal hatch), membrane (solid black), fleece (dashed), metal (gray fill)
- Output: 1056x816 SVG sheet (11x17 landscape)

### 5. PDF Export
- File: `tools/export_svg_to_pdf.py`
- Engine: cairosvg + pypdf
- Output: Combined multi-page PDF packet

### 6. DXF Export
- File: `tools/export_assembly_to_dxf.py`
- Engine: ezdxf (R2010 format)
- Layers: SUBSTRATE, INSULATION, MEMBRANE, REINFORCEMENT, PRIMER, METAL, DIMENSIONS, TEXT, TITLEBLOCK
