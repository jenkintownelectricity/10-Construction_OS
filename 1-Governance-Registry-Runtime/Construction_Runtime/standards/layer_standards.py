"""Layer standards for Construction Runtime v0.2.

Canonical layer names for DXF and SVG output.
All entity-to-layer mappings must reference these constants.
"""

SCHEMA_VERSION = "0.2"

# Standard architectural layers
LAYER_WALL = "A-WALL"
LAYER_ROOF = "A-ROOF"
LAYER_INSULATION = "A-INSUL"
LAYER_FASTENER = "A-FAST"
LAYER_DIMENSIONS = "A-DIMS"
LAYER_TEXT = "A-TEXT"
LAYER_DETAIL = "A-DETAIL"
LAYER_COMPONENTS = "A-COMP"
LAYER_CONSTRAINTS = "A-CONST"
LAYER_TITLEBLOCK = "A-TBLK"

ALL_LAYERS = [
    LAYER_WALL,
    LAYER_ROOF,
    LAYER_INSULATION,
    LAYER_FASTENER,
    LAYER_DIMENSIONS,
    LAYER_TEXT,
    LAYER_DETAIL,
    LAYER_COMPONENTS,
    LAYER_CONSTRAINTS,
    LAYER_TITLEBLOCK,
]

# Default layer colors (AutoCAD ACI color index)
LAYER_COLORS = {
    LAYER_WALL: 7,       # white
    LAYER_ROOF: 1,       # red
    LAYER_INSULATION: 4, # cyan
    LAYER_FASTENER: 3,   # green
    LAYER_DIMENSIONS: 2, # yellow
    LAYER_TEXT: 7,        # white
    LAYER_DETAIL: 5,      # blue
    LAYER_COMPONENTS: 6,  # magenta
    LAYER_CONSTRAINTS: 8, # dark gray
    LAYER_TITLEBLOCK: 7,  # white
}


def is_valid_layer(layer_name: str) -> bool:
    """Check if a layer name is in the standard set."""
    return layer_name in ALL_LAYERS
