"""SVG artifact renderer.

Renders geometry primitives to SVG format.
SVG must match DXF/PDF instruction fidelity — same primitives, same output.

SVG uses a top-left origin with Y-axis flipped relative to DXF.
Scale factor: drawing units (inches) to SVG pixels = 30.0.
"""

from typing import Any
import math

from runtime.artifact_renderer.geometry_primitives import (
    Primitive,
    LinePrimitive,
    ArcPrimitive,
    PolylinePrimitive,
    RectanglePrimitive,
    TextPrimitive,
    HatchPrimitive,
    DimensionPrimitive,
    CalloutPrimitive,
    SUPPORTED_PRIMITIVES,
)
from runtime.artifact_renderer.artifact_contract import RendererCapability


RENDERER_ID = "artifact_svg_renderer_v18"
OUTPUT_FORMAT = "SVG"
SVG_SCALE = 30.0
DEFAULT_STROKE_WIDTH = 1.0
DEFAULT_FONT_FAMILY = "monospace"

LAYER_COLORS = {
    "A-COMP": "#FF0000",
    "A-DETAIL": "#FFFF00",
    "A-DIMS": "#00FF00",
    "A-TEXT": "#FFFFFF",
    "A-HATCH": "#808080",
    "A-ANNO": "#0000FF",
    "A-HIDDEN": "#C0C0C0",
    "A-CENTER": "#00FFFF",
}


class SvgRenderer:
    """Renders geometry primitives to SVG markup."""

    def renderer_id(self) -> str:
        return RENDERER_ID

    def output_format(self) -> str:
        return OUTPUT_FORMAT

    def capability(self) -> RendererCapability:
        return RendererCapability(
            renderer_id=RENDERER_ID,
            output_format=OUTPUT_FORMAT,
            supported_primitives=sorted(SUPPORTED_PRIMITIVES),
            version="18.0",
        )

    def render(
        self,
        primitives: list[Primitive],
        sheet: dict[str, Any],
        layers: list[str],
        metadata: dict[str, Any],
    ) -> tuple[str, list[dict[str, str]]]:
        errors: list[dict[str, str]] = []
        width = sheet.get("width", 36.0)
        height = sheet.get("height", 24.0)
        vw = width * SVG_SCALE
        vh = height * SVG_SCALE

        parts: list[str] = []
        parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {vw} {vh}" '
            f'width="{vw}" height="{vh}" '
            f'style="background:#fff">'
        )

        # Group primitives by layer
        layer_prims: dict[str, list[Primitive]] = {}
        for prim in primitives:
            layer = getattr(prim, "layer", "")
            if layer not in layer_prims:
                layer_prims[layer] = []
            layer_prims[layer].append(prim)

        for layer in sorted(layer_prims.keys()):
            color = LAYER_COLORS.get(layer, "#FFFFFF")
            parts.append(
                f'  <g id="{_escape_attr(layer)}" stroke="{color}" '
                f'fill="none" stroke-width="{DEFAULT_STROKE_WIDTH}">'
            )
            for prim in layer_prims[layer]:
                elem = self._primitive_to_svg(prim, color, height, errors)
                if elem:
                    parts.append(f"    {elem}")
            parts.append("  </g>")

        # Title block
        title = metadata.get("title", {})
        if title.get("detail_id"):
            parts.append(self._title_block_svg(title, vw, vh))

        parts.append("</svg>")
        return "\n".join(parts), errors

    def _primitive_to_svg(
        self,
        prim: Primitive,
        color: str,
        sheet_height: float,
        errors: list[dict[str, str]],
    ) -> str | None:
        ptype = prim.primitive_type

        def sy(y: float) -> float:
            return (sheet_height - y) * SVG_SCALE

        if ptype == "LINE":
            return self._line_to_svg(prim, sy)
        if ptype == "ARC":
            return self._arc_to_svg(prim, sy)
        if ptype == "POLYLINE":
            return self._polyline_to_svg(prim, sy)
        if ptype == "RECTANGLE":
            return self._rectangle_to_svg(prim, sy)
        if ptype == "TEXT":
            return self._text_to_svg(prim, color, sy)
        if ptype == "HATCH":
            return self._hatch_to_svg(prim, color, sy)
        if ptype == "DIMENSION":
            return self._dimension_to_svg(prim, color, sy)
        if ptype == "CALLOUT":
            return self._callout_to_svg(prim, color, sy)

        errors.append({
            "code": "SVG_UNSUPPORTED_PRIMITIVE",
            "message": f"Unsupported primitive type: '{ptype}'.",
        })
        return None

    def _line_to_svg(self, prim: LinePrimitive, sy) -> str:
        x1 = prim.start.x * SVG_SCALE
        y1 = sy(prim.start.y)
        x2 = prim.end.x * SVG_SCALE
        y2 = sy(prim.end.y)
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'

    def _arc_to_svg(self, prim: ArcPrimitive, sy) -> str:
        cx = prim.center.x * SVG_SCALE
        cy = sy(prim.center.y)
        r = prim.radius * SVG_SCALE

        if prim.is_full_circle():
            return f'<circle cx="{cx}" cy="{cy}" r="{r}" />'

        # SVG arc path
        sa = math.radians(prim.start_angle)
        ea = math.radians(prim.end_angle)
        x1 = cx + r * math.cos(sa)
        y1 = cy - r * math.sin(sa)
        x2 = cx + r * math.cos(ea)
        y2 = cy - r * math.sin(ea)
        large = 1 if prim.sweep_angle() > 180 else 0
        return (
            f'<path d="M {x1} {y1} A {r} {r} 0 {large} 0 {x2} {y2}" />'
        )

    def _polyline_to_svg(self, prim: PolylinePrimitive, sy) -> str:
        pts = " ".join(f"{p.x * SVG_SCALE},{sy(p.y)}" for p in prim.points)
        if prim.closed:
            return f'<polygon points="{pts}" />'
        return f'<polyline points="{pts}" />'

    def _rectangle_to_svg(self, prim: RectanglePrimitive, sy) -> str:
        x = prim.origin.x * SVG_SCALE
        y_svg = sy(prim.origin.y + prim.height)
        w = prim.width * SVG_SCALE
        h = prim.height * SVG_SCALE
        return f'<rect x="{x}" y="{y_svg}" width="{w}" height="{h}" />'

    def _text_to_svg(self, prim: TextPrimitive, color: str, sy) -> str:
        x = prim.position.x * SVG_SCALE
        y = sy(prim.position.y)
        size = prim.height * SVG_SCALE
        transform = ""
        if prim.rotation:
            transform = f' transform="rotate({-prim.rotation},{x},{y})"'
        return (
            f'<text x="{x}" y="{y}" fill="{color}" '
            f'font-size="{size}" font-family="{DEFAULT_FONT_FAMILY}"'
            f'{transform}>{_escape(prim.text)}</text>'
        )

    def _hatch_to_svg(self, prim: HatchPrimitive, color: str, sy) -> str:
        pts = " ".join(f"{p.x * SVG_SCALE},{sy(p.y)}" for p in prim.boundary)
        # Deterministic pattern ID from boundary hash
        boundary_key = "|".join(f"{p.x},{p.y}" for p in prim.boundary)
        pattern_id = f"hatch-{hash(boundary_key) & 0xFFFFFFFF:08x}"
        return (
            f'<defs><pattern id="{pattern_id}" width="8" height="8" '
            f'patternUnits="userSpaceOnUse" patternTransform="rotate({prim.angle})">'
            f'<line x1="0" y1="0" x2="0" y2="8" stroke="{color}" stroke-width="0.5"/>'
            f'</pattern></defs>'
            f'<polygon points="{pts}" fill="url(#{pattern_id})" />'
        )

    def _dimension_to_svg(self, prim: DimensionPrimitive, color: str, sy) -> str:
        x1 = prim.start.x * SVG_SCALE
        y1 = sy(prim.start.y)
        x2 = prim.end.x * SVG_SCALE
        y2 = sy(prim.end.y)
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - prim.offset * SVG_SCALE
        label = prim.text or f"{prim.measured_value():.{prim.precision}f} {prim.unit}"
        return (
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke-dasharray="4,2" />'
            f'<text x="{mx}" y="{my}" fill="{color}" '
            f'font-size="10" font-family="{DEFAULT_FONT_FAMILY}" '
            f'text-anchor="middle">{_escape(label)}</text>'
        )

    def _callout_to_svg(self, prim: CalloutPrimitive, color: str, sy) -> str:
        ax = prim.anchor.x * SVG_SCALE
        ay = sy(prim.anchor.y)
        lx = prim.leader_end.x * SVG_SCALE
        ly = sy(prim.leader_end.y)
        r = prim.bubble_radius * SVG_SCALE
        return (
            f'<line x1="{ax}" y1="{ay}" x2="{lx}" y2="{ly}" />'
            f'<circle cx="{ax}" cy="{ay}" r="{r}" />'
            f'<text x="{ax}" y="{ay + 4}" fill="{color}" '
            f'font-size="10" text-anchor="middle">{_escape(prim.text)}</text>'
        )

    def _title_block_svg(self, title: dict[str, Any], vw: float, vh: float) -> str:
        detail_id = title.get("detail_id", "")
        display_name = title.get("display_name", "")
        x = vw - 180
        y = vh - 30
        return (
            f'  <g id="title-block">'
            f'<text x="{x}" y="{y}" fill="#333" font-size="14" '
            f'font-family="{DEFAULT_FONT_FAMILY}">{_escape(detail_id)}</text>'
            f'<text x="{x}" y="{y + 16}" fill="#666" font-size="10" '
            f'font-family="{DEFAULT_FONT_FAMILY}">{_escape(display_name)}</text>'
            f'</g>'
        )


def _escape(text: str) -> str:
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def _escape_attr(text: str) -> str:
    return _escape(text)
