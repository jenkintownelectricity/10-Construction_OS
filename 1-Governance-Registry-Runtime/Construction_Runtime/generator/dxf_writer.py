"""DXF writer for Construction Runtime v0.2.

Consumes DrawingInstructionSet only. Produces DXF-format string output.
"""

from typing import Any

from runtime.models.drawing_instruction import DrawingInstructionSet, DrawingEntity
from standards.layer_standards import LAYER_COLORS, is_valid_layer
from standards import error_codes

SCHEMA_VERSION = "0.2"


def write_dxf(instruction_set: DrawingInstructionSet) -> tuple[str, list[dict[str, str]]]:
    """Generate DXF content from a DrawingInstructionSet.

    Args:
        instruction_set: The canonical drawing instruction set.

    Returns:
        Tuple of (dxf_content_string, list_of_errors).
    """
    errors: list[dict[str, str]] = []
    lines: list[str] = []

    # DXF header
    lines.extend(_write_header(instruction_set))

    # Tables section — layers
    lines.extend(_write_tables(instruction_set, errors))

    # Entities section
    lines.extend(_write_entities(instruction_set, errors))

    # EOF
    lines.append("0")
    lines.append("EOF")

    return "\n".join(lines), errors


def _write_header(inst: DrawingInstructionSet) -> list[str]:
    """Write DXF HEADER section."""
    sheet = inst.sheet_metadata
    return [
        "0", "SECTION",
        "2", "HEADER",
        "9", "$ACADVER", "1", "AC1015",
        "9", "$INSUNITS", "70", "1",  # inches
        "9", "$EXTMIN", "10", "0.0", "20", "0.0",
        "9", "$EXTMAX", "10", str(sheet.width), "20", str(sheet.height),
        "0", "ENDSEC",
    ]


def _write_tables(inst: DrawingInstructionSet, errors: list) -> list[str]:
    """Write DXF TABLES section with layer definitions."""
    lines = ["0", "SECTION", "2", "TABLES", "0", "TABLE", "2", "LAYER"]

    for layer_name in inst.layers:
        color = LAYER_COLORS.get(layer_name, 7)
        lines.extend([
            "0", "LAYER",
            "2", layer_name,
            "70", "0",
            "62", str(color),
            "6", "CONTINUOUS",
        ])

    lines.extend(["0", "ENDTAB", "0", "ENDSEC"])
    return lines


def _write_entities(inst: DrawingInstructionSet, errors: list) -> list[str]:
    """Write DXF ENTITIES section."""
    lines = ["0", "SECTION", "2", "ENTITIES"]

    for entity in inst.entities:
        entity_lines = _entity_to_dxf(entity, errors)
        lines.extend(entity_lines)

    # Dimensions as lines with text
    for dim in inst.dimensions:
        lines.extend([
            "0", "LINE",
            "8", dim.layer,
            "10", str(dim.start[0]), "20", str(dim.start[1]),
            "11", str(dim.end[0]), "21", str(dim.end[1]),
        ])
        if dim.label:
            mid_x = (dim.start[0] + dim.end[0]) / 2
            mid_y = (dim.start[1] + dim.end[1]) / 2
            lines.extend([
                "0", "TEXT",
                "8", dim.layer,
                "10", str(mid_x), "20", str(mid_y + 0.25),
                "40", "0.125",
                "1", dim.label,
            ])

    # Text annotations
    for ann in inst.text_annotations:
        lines.extend([
            "0", "TEXT",
            "8", ann.layer,
            "10", str(ann.position[0]), "20", str(ann.position[1]),
            "40", str(ann.font_size / 72.0),
            "1", ann.text,
        ])
        if ann.rotation:
            lines.extend(["50", str(ann.rotation)])

    lines.extend(["0", "ENDSEC"])
    return lines


def _entity_to_dxf(entity: DrawingEntity, errors: list) -> list[str]:
    """Convert a single DrawingEntity to DXF lines."""
    props = entity.properties
    layer = entity.layer

    if entity.entity_type == "LINE":
        return [
            "0", "LINE", "8", layer,
            "10", str(props.get("x1", 0)), "20", str(props.get("y1", 0)),
            "11", str(props.get("x2", 0)), "21", str(props.get("y2", 0)),
        ]

    if entity.entity_type == "RECT":
        x, y = props.get("x", 0), props.get("y", 0)
        w, h = props.get("width", 0), props.get("height", 0)
        return [
            "0", "LWPOLYLINE", "8", layer,
            "90", "4", "70", "1",
            "10", str(x), "20", str(y),
            "10", str(x + w), "20", str(y),
            "10", str(x + w), "20", str(y + h),
            "10", str(x), "20", str(y + h),
        ]

    if entity.entity_type == "CIRCLE":
        return [
            "0", "CIRCLE", "8", layer,
            "10", str(props.get("cx", 0)), "20", str(props.get("cy", 0)),
            "40", str(props.get("radius", 1)),
        ]

    if entity.entity_type == "TEXT":
        return [
            "0", "TEXT", "8", layer,
            "10", str(props.get("x", 0)), "20", str(props.get("y", 0)),
            "40", str(props.get("height", 0.125)),
            "1", str(props.get("text", "")),
        ]

    if entity.entity_type == "POLYLINE":
        lines = ["0", "LWPOLYLINE", "8", layer]
        points = props.get("points", [])
        lines.extend(["90", str(len(points)), "70", "0"])
        for pt in points:
            lines.extend(["10", str(pt[0]), "20", str(pt[1])])
        return lines

    if entity.entity_type in ("DIMENSION", "CALLOUT"):
        # Represented as text in basic DXF
        return [
            "0", "TEXT", "8", layer,
            "10", str(props.get("x", 0)), "20", str(props.get("y", 0)),
            "40", "0.125",
            "1", str(props.get("text", entity.entity_type)),
        ]

    errors.append({
        "code": error_codes.GENERATION_SVG_UNSUPPORTED_ENTITY,
        "message": f"Unsupported entity type for DXF: '{entity.entity_type}'.",
        "path": f"entity.{entity.entity_type}",
    })
    return []
