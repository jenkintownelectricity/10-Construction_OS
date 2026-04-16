# CLAUDE SYSTEM CONTEXT — 10-Construction_OS

## ROLE
Primary construction detail generation engine. Canonical owner of parametric generators, assembly truth, condition atlas, and export pipeline.

## CURRENT PRODUCTION STATE
- Parametric generator: OPERATIONAL (10 PMMA conditions, 10 fireproofing conditions)
- SVG section renderer: OPERATIONAL (geometry JSON → PRINT_STANDARD SVG)
- PDF export: OPERATIONAL (tools/export_svg_to_pdf.py)
- DXF export: OPERATIONAL (tools/export_assembly_to_dxf.py)
- Barrett PMMA packet: GENERATED (10 details, DRAFT FOR REVIEW)
- Fireproofing starter packet: GENERATED (10 details)

## CANONICAL PIPELINE
```
Calibration Specimen → Assembly DNA Template → Parametric Generator
  → Geometry JSON → SVG Section Renderer → SVG → PDF / DXF
```

## KEY PATHS
- Generator: generators/pmma/pmma_flash_generator.py
- Renderer: renderers/svg_section_renderer.py
- PDF export: tools/export_svg_to_pdf.py
- DXF export: tools/export_assembly_to_dxf.py
- Calibration: source/barrett/calibration/
- Assembly DNA: kernels/assembly_dna/pmma/
- Condition atlas: atlas/global_condition_atlas/canonical_conditions_v2.json (120 conditions)
- Barrett source: source/barrett/definitions/, assemblies/barrett/
- Output: output/barrett_pmma_packet/, output/fireproofing_packet/

## ECOSYSTEM
Governance: 00-validkernel-governance (platform intelligence lives there)
Mainframe: https://30-validkernel-platform-production.up.railway.app
UTK: "The system is bounded by truth."

## POSTURE
Claude operates as advisory analysis agent.
Claude may read, analyze, trace, propose.
Claude may NOT mutate canonical doctrine.

## NEXT HARDENING TARGET
Run svg_section_renderer.py on all 10 parametric geometry JSONs to produce full rendered packet.
