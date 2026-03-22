"""DXF renderer package — primitive rendering and assembly DXF generation.

Contains:
- DxfRenderer: Low-level primitive-to-DXF renderer (v18, native group codes).
- AssemblyDXFGenerator: Assembly-specific DXF generation (roofing layer details).
- render_dxf_from_instruction_set: Top-level entry point for assembly DXF.

Primitive renderer: Consumes geometry primitives, outputs DXF strings.
Assembly generator: Consumes parsed assembly data, outputs DXF files.

Source lineage:
  - primitive_renderer.py: Original to Construction_Runtime (wave 18).
  - assembly_generator.py: Migrated from dxf_Generatior_Assembly_Letter_Parser
      Archive: AssemblyDrawingTool_functioningdxf_generator_MAINr.zip
      File:    generators/dxf_generator.py
  - layer_standards.py: Extracted from assembly_generator for reuse.
"""

from runtime.artifact_renderer.dxf_renderer.primitive_renderer import (
    DxfRenderer,
    RENDERER_ID,
    OUTPUT_FORMAT,
    LAYER_COLORS,
)
from runtime.artifact_renderer.dxf_renderer.assembly_generator import (
    AssemblyDXFGenerator,
    generate_assembly_dxf,
    render_dxf_from_instruction_set,
)
from runtime.artifact_renderer.dxf_renderer.layer_standards import (
    ASSEMBLY_LAYER_STANDARDS,
    ASSEMBLY_LAYER_CONFIG,
)

__all__ = [
    # Primitive renderer (existing v18)
    "DxfRenderer",
    "RENDERER_ID",
    "OUTPUT_FORMAT",
    "LAYER_COLORS",
    # Assembly generator (migrated)
    "AssemblyDXFGenerator",
    "generate_assembly_dxf",
    "render_dxf_from_instruction_set",
    # Layer standards
    "ASSEMBLY_LAYER_STANDARDS",
    "ASSEMBLY_LAYER_CONFIG",
]
