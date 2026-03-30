"""SVG standards for Construction Runtime v0.2.

Constants and utilities for SVG preview generation.
"""

SCHEMA_VERSION = "0.2"

DEFAULT_VIEWBOX_WIDTH = 1200
DEFAULT_VIEWBOX_HEIGHT = 800
DEFAULT_STROKE_WIDTH = 1
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT_FAMILY = "monospace"

# SVG-supported entity types
SUPPORTED_ENTITIES = {"LINE", "POLYLINE", "RECT", "CIRCLE", "TEXT", "DIMENSION", "CALLOUT"}

# Layer-to-SVG-color mapping
LAYER_SVG_COLORS = {
    "A-WALL": "#333333",
    "A-ROOF": "#CC0000",
    "A-INSUL": "#00CCCC",
    "A-FAST": "#00CC00",
    "A-DIMS": "#CCCC00",
    "A-TEXT": "#333333",
    "A-DETAIL": "#0000CC",
    "A-COMP": "#CC00CC",
    "A-CONST": "#888888",
    "A-TBLK": "#333333",
}

DEFAULT_COLOR = "#000000"


def get_layer_color(layer: str) -> str:
    """Get the SVG color for a given layer."""
    return LAYER_SVG_COLORS.get(layer, DEFAULT_COLOR)
