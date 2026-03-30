"""Assembly DXF layer standards — roofing detail layer configuration.

Defines layer naming, hatch patterns, and drawing standards for
roofing assembly detail drawings.

Source lineage:
  Migrated from dxf_Generatior_Assembly_Letter_Parser
  Archive: AssemblyDrawingTool_functioningdxf_generator_MAINr.zip
  File:    generators/dxf_generator.py (self.standards dict)
"""

from typing import Any


ASSEMBLY_LAYER_STANDARDS: dict[str, dict[str, Any]] = {
    "deck": {
        "outline_layer": "00 LDS Deck Outline",
        "hatch_layer": "00 LDS Deck Hatch",
        "hatch_pattern": "AR-CONC",
        "hatch_scale": 0.01,
        "default_height": 3.0,
    },
    "insulation": {
        "outline_layer": "00 LDS Insulation {} Outline",
        "hatch_layer": "00 LDS Insulation {} Hatch",
        "hatch_pattern": "NET",
        "hatch_scale": 0.25,
        "hatch_angle": 0,
    },
    "coverboard": {
        "outline_layer": "00 LDS Coverboard {} Outline",
        "hatch_layer": "00 LDS Coverboard {} Hatch",
        "hatch_pattern": "ANSI31",
        "hatch_scale": 0.22,
        "hatch_angle": 0,
    },
    "vapor_barrier": {
        "outline_layer": "00 LDS Vapor Barrier Outline",
        "hatch_layer": "00 LDS Vapor Barrier Hatch",
        "hatch_pattern": "SOLID",
        "default_height": 0.0625,
    },
    "membrane": {
        "layer": "00 LDS Membrane 1",
        "adhesive_layer": "00 LDS Membrane 1 Adhesive",
        "line_offset": 0.125,
        "line_weight": 0.1,
        "color_rgb": (39, 170, 187),
    },
    "text": {
        "layer": "00 LDS Text",
        "height": 0.125,
        "font": "Arial",
    },
}


ASSEMBLY_LAYER_CONFIG: list[tuple[str, str | tuple[int, int, int]]] = [
    ("00 LDS Deck Outline", "BYLAYER"),
    ("00 LDS Deck Hatch", "BYLAYER"),
    ("00 LDS Vapor Barrier Outline", "BYLAYER"),
    ("00 LDS Vapor Barrier Hatch", "BYLAYER"),
    ("00 LDS Membrane 1", (39, 170, 187)),
    ("00 LDS Membrane 1 Adhesive", (39, 170, 187)),
    ("00 LDS Text", "BYLAYER"),
    ("00 LDS Insulation 1 Outline", "BYLAYER"),
    ("00 LDS Insulation 1 Hatch", "BYLAYER"),
    ("00 LDS Coverboard 1 Outline", "BYLAYER"),
    ("00 LDS Coverboard 1 Hatch", "BYLAYER"),
    ("00 LDS Insulation 2 Outline", "BYLAYER"),
    ("00 LDS Insulation 2 Hatch", "BYLAYER"),
    ("00 LDS Coverboard 2 Outline", "BYLAYER"),
    ("00 LDS Coverboard 2 Hatch", "BYLAYER"),
    ("00 LDS Insulation 3 Outline", "BYLAYER"),
    ("00 LDS Insulation 3 Hatch", "BYLAYER"),
    ("00 LDS Coverboard 3 Outline", "BYLAYER"),
    ("00 LDS Coverboard 3 Hatch", "BYLAYER"),
]
