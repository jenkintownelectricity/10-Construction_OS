"""DXF artifact renderer.

Renders geometry primitives to DXF format (AutoCAD R2000, inches).
Consumes primitives only — no classification or resolution logic.

Uses native DXF group code generation (no external dependencies).
Follows ezdxf conventions: INSUNITS=1 (inches), ACADVER=AC1015.
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
from runtime.artifact_renderer.renderer_errors import UnsupportedPrimitiveError


RENDERER_ID = "artifact_dxf_renderer_v18"
OUTPUT_FORMAT = "DXF"

# DXF layer color map (ACI colors)
LAYER_COLORS = {
    "A-COMP": 1,       # Red
    "A-DETAIL": 2,     # Yellow
    "A-DIMS": 3,       # Green
    "A-TEXT": 7,        # White
    "A-HATCH": 8,       # Gray
    "A-ANNO": 5,        # Blue
    "A-HIDDEN": 9,      # Light gray
    "A-CENTER": 4,      # Cyan
}


class DxfRenderer:
    """Renders geometry primitives to DXF format."""

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
        """Render primitives to DXF content string.

        Args:
            primitives: List of geometry primitives.
            sheet: Sheet metadata (width, height, unit).
            layers: Layer names to define.
            metadata: Title block and provenance metadata.

        Returns:
            Tuple of (dxf_content, list_of_errors).
        """
        errors: list[dict[str, str]] = []
        lines: list[str] = []

        lines.extend(self._write_header(sheet))
        lines.extend(self._write_tables(layers))
        lines.extend(self._write_entities(primitives, sheet, errors))
        lines.extend(self._write_title_block(metadata, sheet))
        lines.append("0")
        lines.append("EOF")

        return "\n".join(lines), errors

    def _write_header(self, sheet: dict[str, Any]) -> list[str]:
        width = sheet.get("width", 36.0)
        height = sheet.get("height", 24.0)
        return [
            "0", "SECTION",
            "2", "HEADER",
            "9", "$ACADVER", "1", "AC1015",
            "9", "$INSUNITS", "70", "1",
            "9", "$EXTMIN", "10", "0.0", "20", "0.0",
            "9", "$EXTMAX", "10", str(width), "20", str(height),
            "0", "ENDSEC",
        ]

    def _write_tables(self, layers: list[str]) -> list[str]:
        lines = ["0", "SECTION", "2", "TABLES", "0", "TABLE", "2", "LAYER"]
        for layer_name in layers:
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

    def _write_entities(
        self,
        primitives: list[Primitive],
        sheet: dict[str, Any],
        errors: list[dict[str, str]],
    ) -> list[str]:
        lines = ["0", "SECTION", "2", "ENTITIES"]

        for prim in primitives:
            prim_lines = self._primitive_to_dxf(prim, errors)
            lines.extend(prim_lines)

        lines.extend(["0", "ENDSEC"])
        return lines

    def _primitive_to_dxf(
        self,
        prim: Primitive,
        errors: list[dict[str, str]],
    ) -> list[str]:
        ptype = prim.primitive_type

        if ptype == "LINE":
            return self._line_to_dxf(prim)
        if ptype == "ARC":
            return self._arc_to_dxf(prim)
        if ptype == "POLYLINE":
            return self._polyline_to_dxf(prim)
        if ptype == "RECTANGLE":
            return self._rectangle_to_dxf(prim)
        if ptype == "TEXT":
            return self._text_to_dxf(prim)
        if ptype == "HATCH":
            return self._hatch_to_dxf(prim)
        if ptype == "DIMENSION":
            return self._dimension_to_dxf(prim)
        if ptype == "CALLOUT":
            return self._callout_to_dxf(prim)

        errors.append({
            "code": "DXF_UNSUPPORTED_PRIMITIVE",
            "message": f"Unsupported primitive type: '{ptype}'.",
        })
        return []

    def _line_to_dxf(self, prim: LinePrimitive) -> list[str]:
        return [
            "0", "LINE", "8", prim.layer,
            "10", str(prim.start.x), "20", str(prim.start.y),
            "11", str(prim.end.x), "21", str(prim.end.y),
        ]

    def _arc_to_dxf(self, prim: ArcPrimitive) -> list[str]:
        if prim.is_full_circle():
            return [
                "0", "CIRCLE", "8", prim.layer,
                "10", str(prim.center.x), "20", str(prim.center.y),
                "40", str(prim.radius),
            ]
        return [
            "0", "ARC", "8", prim.layer,
            "10", str(prim.center.x), "20", str(prim.center.y),
            "40", str(prim.radius),
            "50", str(prim.start_angle),
            "51", str(prim.end_angle),
        ]

    def _polyline_to_dxf(self, prim: PolylinePrimitive) -> list[str]:
        lines = ["0", "LWPOLYLINE", "8", prim.layer]
        lines.extend(["90", str(len(prim.points))])
        lines.extend(["70", "1" if prim.closed else "0"])
        for pt in prim.points:
            lines.extend(["10", str(pt.x), "20", str(pt.y)])
        return lines

    def _rectangle_to_dxf(self, prim: RectanglePrimitive) -> list[str]:
        corners = prim.corners()
        lines = ["0", "LWPOLYLINE", "8", prim.layer, "90", "4", "70", "1"]
        for c in corners:
            lines.extend(["10", str(c.x), "20", str(c.y)])
        return lines

    def _text_to_dxf(self, prim: TextPrimitive) -> list[str]:
        lines = [
            "0", "TEXT", "8", prim.layer,
            "10", str(prim.position.x), "20", str(prim.position.y),
            "40", str(prim.height),
            "1", prim.text,
        ]
        if prim.rotation:
            lines.extend(["50", str(prim.rotation)])
        return lines

    def _hatch_to_dxf(self, prim: HatchPrimitive) -> list[str]:
        lines = [
            "0", "HATCH", "8", prim.layer,
            "2", prim.pattern,
            "70", "0",
            "41", str(prim.scale),
            "52", str(prim.angle),
            "91", "1",
            "92", "1",
            "93", str(len(prim.boundary)),
        ]
        for pt in prim.boundary:
            lines.extend(["10", str(pt.x), "20", str(pt.y)])
        return lines

    def _dimension_to_dxf(self, prim: DimensionPrimitive) -> list[str]:
        mid_x = (prim.start.x + prim.end.x) / 2
        mid_y = (prim.start.y + prim.end.y) / 2 + prim.offset
        label = prim.text or f"{prim.measured_value():.{prim.precision}f} {prim.unit}"
        return [
            "0", "LINE", "8", prim.layer,
            "10", str(prim.start.x), "20", str(prim.start.y),
            "11", str(prim.end.x), "21", str(prim.end.y),
            "0", "TEXT", "8", prim.layer,
            "10", str(mid_x), "20", str(mid_y),
            "40", "0.125",
            "1", label,
        ]

    def _callout_to_dxf(self, prim: CalloutPrimitive) -> list[str]:
        return [
            "0", "LINE", "8", prim.layer,
            "10", str(prim.anchor.x), "20", str(prim.anchor.y),
            "11", str(prim.leader_end.x), "21", str(prim.leader_end.y),
            "0", "CIRCLE", "8", prim.layer,
            "10", str(prim.anchor.x), "20", str(prim.anchor.y),
            "40", str(prim.bubble_radius),
            "0", "TEXT", "8", prim.layer,
            "10", str(prim.anchor.x), "20", str(prim.anchor.y),
            "40", "0.1",
            "1", prim.text,
        ]

    def _write_title_block(self, metadata: dict[str, Any], sheet: dict[str, Any]) -> list[str]:
        title = metadata.get("title", {})
        detail_id = title.get("detail_id", "")
        display_name = title.get("display_name", "")
        if not detail_id:
            return []

        width = sheet.get("width", 36.0)
        return [
            "0", "SECTION", "2", "ENTITIES",
            "0", "TEXT", "8", "A-TEXT",
            "10", str(width - 6.0), "20", "0.5",
            "40", "0.2",
            "1", detail_id,
            "0", "TEXT", "8", "A-TEXT",
            "10", str(width - 6.0), "20", "0.25",
            "40", "0.125",
            "1", display_name,
            "0", "ENDSEC",
        ]
