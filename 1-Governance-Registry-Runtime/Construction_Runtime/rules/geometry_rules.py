"""Geometry rules for Construction Runtime v0.2.

Defines rules for panel layout, spacing, overlap detection,
edge offsets, joint placement, and dimension chains.
"""

SCHEMA_VERSION = "0.2"

# Authority status values for derived dimensions
AUTHORITY_EXPLICIT = "explicit"
AUTHORITY_DERIVED = "derived"
AUTHORITY_INFERRED = "inferred"
AUTHORITY_UNAPPROVED = "unapproved"

# Default construction geometry rules
DEFAULT_EDGE_OFFSET_IN = 1.5       # inches
DEFAULT_JOINT_WIDTH_IN = 0.5       # inches
DEFAULT_MIN_SPACING_IN = 3.0       # inches
DEFAULT_MIN_PANEL_WIDTH_IN = 6.0   # inches
MAX_PANEL_ASPECT_RATIO = 10.0


def validate_dimension(value: float, unit: str) -> tuple[bool, str]:
    """Validate a single dimension value.

    Returns (is_valid, error_message).
    """
    if value < 0:
        return False, f"Negative dimension: {value} {unit}"
    if value == 0:
        return False, f"Zero dimension: {value} {unit}"
    return True, ""


def check_overlap(rect_a: dict, rect_b: dict) -> bool:
    """Check if two axis-aligned rectangles overlap.

    Each rect: {"x": float, "y": float, "width": float, "height": float}
    """
    a_right = rect_a["x"] + rect_a["width"]
    a_top = rect_a["y"] + rect_a["height"]
    b_right = rect_b["x"] + rect_b["width"]
    b_top = rect_b["y"] + rect_b["height"]

    if rect_a["x"] >= b_right or rect_b["x"] >= a_right:
        return False
    if rect_a["y"] >= b_top or rect_b["y"] >= a_top:
        return False
    return True


def compute_panel_layout(
    run_length: float,
    panel_width: float,
    joint_width: float = DEFAULT_JOINT_WIDTH_IN,
    edge_offset: float = DEFAULT_EDGE_OFFSET_IN,
) -> dict:
    """Compute a linear panel layout along a run.

    Returns layout dict with provenance metadata.
    """
    if run_length <= 0 or panel_width <= 0:
        return {
            "panels": [],
            "error": "Invalid dimensions",
            "provenance": {"authority_status": AUTHORITY_UNAPPROVED},
        }

    usable_length = run_length - (2 * edge_offset)
    if usable_length <= 0:
        return {
            "panels": [],
            "error": "Run length too short after edge offsets",
            "provenance": {"authority_status": AUTHORITY_UNAPPROVED},
        }

    effective_panel = panel_width + joint_width
    panel_count = int(usable_length / effective_panel)
    if panel_count < 1:
        panel_count = 1

    actual_joint = (usable_length - (panel_count * panel_width)) / max(panel_count - 1, 1) if panel_count > 1 else 0

    panels = []
    x = edge_offset
    for i in range(panel_count):
        panels.append({
            "index": i,
            "x": round(x, 4),
            "width": panel_width,
        })
        x += panel_width + (actual_joint if i < panel_count - 1 else 0)

    return {
        "panels": panels,
        "panel_count": panel_count,
        "run_length": run_length,
        "usable_length": round(usable_length, 4),
        "actual_joint_width": round(actual_joint, 4),
        "provenance": {
            "authority_status": AUTHORITY_DERIVED,
            "derivation": "run_length / panel_count",
            "source": "geometry_rules.compute_panel_layout",
        },
    }
