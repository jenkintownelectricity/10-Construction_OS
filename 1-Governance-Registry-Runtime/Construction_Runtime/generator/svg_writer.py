"""SVG writer for Construction Runtime v0.2.

Consumes DrawingInstructionSet only. Produces SVG markup string.
SVG derives from the same instruction set as DXF.
"""

from typing import Any

from runtime.models.drawing_instruction import DrawingInstructionSet, DrawingEntity
from standards.svg_standards import (
    DEFAULT_VIEWBOX_WIDTH,
    DEFAULT_VIEWBOX_HEIGHT,
    DEFAULT_STROKE_WIDTH,
    DEFAULT_FONT_SIZE,
    DEFAULT_FONT_FAMILY,
    SUPPORTED_ENTITIES,
    get_layer_color,
)
from standards import error_codes

SCHEMA_VERSION = "0.2"

# Scale factor: drawing units (inches) to SVG pixels
SVG_SCALE = 30.0


def write_svg(instruction_set: DrawingInstructionSet) -> tuple[str, list[dict[str, str]]]:
    """Generate SVG content from a DrawingInstructionSet.

    Args:
        instruction_set: The canonical drawing instruction set.

    Returns:
        Tuple of (svg_content_string, list_of_errors).
    """
    errors: list[dict[str, str]] = []

    sheet = instruction_set.sheet_metadata
    vw = sheet.width * SVG_SCALE
    vh = sheet.height * SVG_SCALE

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'viewBox="0 0 {vw} {vh}" '
                 f'width="{vw}" height="{vh}" '
                 f'style="background:#fff">')

    # Group entities by layer
    layers_used = instruction_set.get_all_used_layers()
    for layer in sorted(layers_used):
        color = get_layer_color(layer)
        parts.append(f'  <g id="{layer}" stroke="{color}" fill="none" '
                     f'stroke-width="{DEFAULT_STROKE_WIDTH}">')

        # Entities on this layer
        for entity in instruction_set.entities:
            if entity.layer != layer:
                continue
            svg_elem = _entity_to_svg(entity, color, errors)
            if svg_elem:
                parts.append(f'    {svg_elem}')

        # Dimensions on this layer
        for dim in instruction_set.dimensions:
            if dim.layer != layer:
                continue
            sx, sy = dim.start[0] * SVG_SCALE, (sheet.height - dim.start[1]) * SVG_SCALE
            ex, ey = dim.end[0] * SVG_SCALE, (sheet.height - dim.end[1]) * SVG_SCALE
            parts.append(f'    <line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" '
                         f'stroke="{color}" stroke-dasharray="4,2" />')
            if dim.label:
                mx, my = (sx + ex) / 2, (sy + ey) / 2 - 5
                parts.append(f'    <text x="{mx}" y="{my}" fill="{color}" '
                             f'font-size="{DEFAULT_FONT_SIZE * 0.8}" '
                             f'font-family="{DEFAULT_FONT_FAMILY}" '
                             f'text-anchor="middle">{_escape(dim.label)}</text>')

        # Text annotations on this layer
        for ann in instruction_set.text_annotations:
            if ann.layer != layer:
                continue
            ax = ann.position[0] * SVG_SCALE
            ay = (sheet.height - ann.position[1]) * SVG_SCALE
            transform = f' transform="rotate({-ann.rotation},{ax},{ay})"' if ann.rotation else ""
            parts.append(f'    <text x="{ax}" y="{ay}" fill="{color}" '
                         f'font-size="{ann.font_size}" '
                         f'font-family="{DEFAULT_FONT_FAMILY}"{transform}>'
                         f'{_escape(ann.text)}</text>')

        parts.append('  </g>')

    parts.append('</svg>')

    return "\n".join(parts), errors


def _entity_to_svg(entity: DrawingEntity, color: str, errors: list) -> str | None:
    """Convert a single DrawingEntity to an SVG element string."""
    props = entity.properties
    etype = entity.entity_type

    # We flip Y because SVG has top-left origin
    def sy(y: float) -> float:
        return 24.0 * SVG_SCALE - y * SVG_SCALE  # default sheet height = 24

    if etype == "LINE":
        x1, y1 = props.get("x1", 0) * SVG_SCALE, sy(props.get("y1", 0))
        x2, y2 = props.get("x2", 0) * SVG_SCALE, sy(props.get("y2", 0))
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'

    if etype == "RECT":
        x = props.get("x", 0) * SVG_SCALE
        y_bottom = props.get("y", 0)
        w = props.get("width", 0) * SVG_SCALE
        h = props.get("height", 0) * SVG_SCALE
        y_svg = sy(y_bottom + props.get("height", 0))
        return f'<rect x="{x}" y="{y_svg}" width="{w}" height="{h}" />'

    if etype == "CIRCLE":
        cx = props.get("cx", 0) * SVG_SCALE
        cy_val = sy(props.get("cy", 0))
        r = props.get("radius", 1) * SVG_SCALE
        return f'<circle cx="{cx}" cy="{cy_val}" r="{r}" />'

    if etype == "POLYLINE":
        points = props.get("points", [])
        pts_str = " ".join(f"{p[0] * SVG_SCALE},{sy(p[1])}" for p in points)
        return f'<polyline points="{pts_str}" />'

    if etype == "TEXT":
        x = props.get("x", 0) * SVG_SCALE
        y_val = sy(props.get("y", 0))
        text = _escape(str(props.get("text", "")))
        height = props.get("height", 0.125) * SVG_SCALE
        return f'<text x="{x}" y="{y_val}" fill="{color}" font-size="{height}">{text}</text>'

    if etype == "DIMENSION":
        x = props.get("x", 0) * SVG_SCALE
        y_val = sy(props.get("y", 0))
        text = _escape(str(props.get("text", "")))
        return f'<text x="{x}" y="{y_val}" fill="{color}" font-size="10">{text}</text>'

    if etype == "CALLOUT":
        x = props.get("x", 0) * SVG_SCALE
        y_val = sy(props.get("y", 0))
        text = _escape(str(props.get("text", "")))
        return (f'<g><circle cx="{x}" cy="{y_val}" r="12" fill="none" />'
                f'<text x="{x}" y="{y_val + 4}" text-anchor="middle" '
                f'fill="{color}" font-size="10">{text}</text></g>')

    errors.append({
        "code": error_codes.GENERATION_SVG_UNSUPPORTED_ENTITY,
        "message": f"Cannot render entity type '{etype}' to SVG.",
        "path": f"entity.{etype}",
    })
    return None


def _escape(text: str) -> str:
    """Escape text for SVG/XML."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))
