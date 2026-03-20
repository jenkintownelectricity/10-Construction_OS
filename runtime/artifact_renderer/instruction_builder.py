"""Instruction builder: Detail DNA -> Geometry Primitives -> Instruction Set.

Translates resolved detail DNA and variant parameters into a typed
instruction set of geometry primitives. This is the bridge between
kernel-resolved detail families and the renderer pipeline.

Authority: Construction_Runtime
Input: Detail DNA resolution + variant parameters
Output: List of geometry primitives organized by layer
"""

from typing import Any
import uuid

from runtime.artifact_renderer.geometry_primitives import (
    Point2D,
    LinePrimitive,
    ArcPrimitive,
    PolylinePrimitive,
    RectanglePrimitive,
    TextPrimitive,
    HatchPrimitive,
    DimensionPrimitive,
    CalloutPrimitive,
    Primitive,
    SUPPORTED_PRIMITIVES,
    validate_primitive,
)
from runtime.artifact_renderer.renderer_errors import InvalidInstructionSetError


BUILDER_VERSION = "18.0"


def build_instruction_set(
    detail_dna: dict[str, Any],
    variant_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a rendering instruction set from Detail DNA.

    Args:
        detail_dna: Resolved detail DNA dictionary from the kernel.
        variant_params: Optional variant parameter overrides.

    Returns:
        Instruction set dictionary with primitives, layers, and metadata.

    Raises:
        InvalidInstructionSetError: If the instruction set cannot be built.
    """
    variant_params = variant_params or {}
    detail_id = detail_dna.get("detail_id", "")
    if not detail_id:
        raise InvalidInstructionSetError("detail_dna missing 'detail_id'.")

    primitives = _extract_primitives(detail_dna, variant_params)

    # Validate all primitives
    all_errors = []
    for prim in primitives:
        errs = validate_primitive(prim)
        all_errors.extend(errs)

    if all_errors:
        raise InvalidInstructionSetError(
            f"Primitives failed validation: {len(all_errors)} error(s).",
            errors=all_errors,
        )

    layers = _collect_layers(primitives)
    instruction_set_id = f"IS-{detail_id}-{uuid.uuid4().hex[:8]}"

    return {
        "instruction_set_id": instruction_set_id,
        "builder_version": BUILDER_VERSION,
        "detail_id": detail_id,
        "variant_id": detail_dna.get("variant_id", ""),
        "assembly_family": detail_dna.get("assembly_family", ""),
        "primitives": primitives,
        "layers": layers,
        "sheet": {
            "width": detail_dna.get("sheet_width", 36.0),
            "height": detail_dna.get("sheet_height", 24.0),
            "unit": "in",
            "scale": detail_dna.get("scale", "1:1"),
        },
        "title": {
            "detail_id": detail_id,
            "display_name": detail_dna.get("display_name", ""),
            "assembly_family": detail_dna.get("assembly_family", ""),
        },
        "provenance": {
            "source_detail_id": detail_id,
            "builder_version": BUILDER_VERSION,
            "resolved_by": "Construction_Runtime",
            "wave": "18",
        },
    }


def _extract_primitives(
    detail_dna: dict[str, Any],
    variant_params: dict[str, Any],
) -> list[Primitive]:
    """Extract geometry primitives from detail DNA entities."""
    primitives: list[Primitive] = []
    entities = detail_dna.get("entities", [])

    for entity in entities:
        prim = _entity_to_primitive(entity, variant_params)
        if prim is not None:
            primitives.append(prim)

    return primitives


def _entity_to_primitive(
    entity: dict[str, Any],
    variant_params: dict[str, Any],
) -> Primitive | None:
    """Convert a single detail DNA entity to a geometry primitive."""
    etype = entity.get("type", "").upper()
    layer = entity.get("layer", "A-DETAIL")
    props = entity.get("properties", {})
    lineweight = props.get("lineweight", 0.25)

    # Apply variant parameter overrides
    for key, value in variant_params.items():
        if key in props:
            props[key] = value

    if etype == "LINE":
        return LinePrimitive(
            start=Point2D(props.get("x1", 0.0), props.get("y1", 0.0)),
            end=Point2D(props.get("x2", 0.0), props.get("y2", 0.0)),
            layer=layer,
            lineweight=lineweight,
        )

    if etype == "ARC":
        return ArcPrimitive(
            center=Point2D(props.get("cx", 0.0), props.get("cy", 0.0)),
            radius=props.get("radius", 1.0),
            start_angle=props.get("start_angle", 0.0),
            end_angle=props.get("end_angle", 360.0),
            layer=layer,
            lineweight=lineweight,
        )

    if etype == "POLYLINE":
        points = [Point2D(p[0], p[1]) for p in props.get("points", [])]
        return PolylinePrimitive(
            points=points,
            closed=props.get("closed", False),
            layer=layer,
            lineweight=lineweight,
        )

    if etype == "RECTANGLE":
        return RectanglePrimitive(
            origin=Point2D(props.get("x", 0.0), props.get("y", 0.0)),
            width=props.get("width", 0.0),
            height=props.get("height", 0.0),
            layer=layer,
            lineweight=lineweight,
        )

    if etype == "TEXT":
        return TextPrimitive(
            text=props.get("text", ""),
            position=Point2D(props.get("x", 0.0), props.get("y", 0.0)),
            height=props.get("height", 0.125),
            rotation=props.get("rotation", 0.0),
            layer=layer,
            font=props.get("font", "standard"),
            alignment=props.get("alignment", "left"),
        )

    if etype == "HATCH":
        boundary = [Point2D(p[0], p[1]) for p in props.get("boundary", [])]
        return HatchPrimitive(
            boundary=boundary,
            pattern=props.get("pattern", "ANSI31"),
            scale=props.get("scale", 1.0),
            angle=props.get("angle", 0.0),
            layer=layer,
        )

    if etype == "DIMENSION":
        return DimensionPrimitive(
            start=Point2D(props.get("x1", 0.0), props.get("y1", 0.0)),
            end=Point2D(props.get("x2", 0.0), props.get("y2", 0.0)),
            offset=props.get("offset", 0.5),
            text=props.get("text", ""),
            unit=props.get("unit", "in"),
            layer=layer,
            precision=props.get("precision", 2),
        )

    if etype == "CALLOUT":
        return CalloutPrimitive(
            anchor=Point2D(props.get("ax", 0.0), props.get("ay", 0.0)),
            leader_end=Point2D(props.get("lx", 0.0), props.get("ly", 0.0)),
            text=props.get("text", ""),
            bubble_radius=props.get("bubble_radius", 0.25),
            layer=layer,
        )

    # Unsupported entity type — fail closed
    return None


def _collect_layers(primitives: list[Primitive]) -> list[str]:
    """Collect unique layers from primitives in sorted order."""
    layers = set()
    for prim in primitives:
        if hasattr(prim, "layer") and prim.layer:
            layers.add(prim.layer)
    return sorted(layers)


def primitives_to_drawing_instruction_set(
    instruction_set: dict[str, Any],
) -> dict[str, Any]:
    """Convert primitives-based instruction set to DrawingInstructionSet format.

    Bridges the new primitive-based format with the existing v0.2
    DrawingInstructionSet consumed by legacy generators.
    """
    entities = []
    dimensions = []
    text_annotations = []
    primitives = instruction_set.get("primitives", [])

    for prim in primitives:
        ptype = prim.primitive_type

        if ptype == "LINE":
            entities.append({
                "entity_type": "LINE",
                "layer": prim.layer,
                "properties": {
                    "x1": prim.start.x, "y1": prim.start.y,
                    "x2": prim.end.x, "y2": prim.end.y,
                },
            })
        elif ptype == "ARC":
            entities.append({
                "entity_type": "CIRCLE" if prim.is_full_circle() else "ARC",
                "layer": prim.layer,
                "properties": {
                    "cx": prim.center.x, "cy": prim.center.y,
                    "radius": prim.radius,
                    "start_angle": prim.start_angle,
                    "end_angle": prim.end_angle,
                },
            })
        elif ptype == "POLYLINE":
            entities.append({
                "entity_type": "POLYLINE",
                "layer": prim.layer,
                "properties": {
                    "points": [p.to_tuple() for p in prim.points],
                    "closed": prim.closed,
                },
            })
        elif ptype == "RECTANGLE":
            entities.append({
                "entity_type": "RECT",
                "layer": prim.layer,
                "properties": {
                    "x": prim.origin.x, "y": prim.origin.y,
                    "width": prim.width, "height": prim.height,
                },
            })
        elif ptype == "TEXT":
            text_annotations.append({
                "text": prim.text,
                "position": prim.position.to_tuple(),
                "font_size": prim.height * 72,
                "layer": prim.layer,
                "rotation": prim.rotation,
            })
        elif ptype == "HATCH":
            entities.append({
                "entity_type": "HATCH",
                "layer": prim.layer,
                "properties": {
                    "boundary": [p.to_tuple() for p in prim.boundary],
                    "pattern": prim.pattern,
                    "scale": prim.scale,
                    "angle": prim.angle,
                },
            })
        elif ptype == "DIMENSION":
            dimensions.append({
                "dim_type": "linear",
                "start": prim.start.to_tuple(),
                "end": prim.end.to_tuple(),
                "value": prim.measured_value(),
                "unit": prim.unit,
                "label": prim.text or f"{prim.measured_value():.{prim.precision}f} {prim.unit}",
                "layer": prim.layer,
                "provenance": {},
            })
        elif ptype == "CALLOUT":
            entities.append({
                "entity_type": "CALLOUT",
                "layer": prim.layer,
                "properties": {
                    "x": prim.anchor.x, "y": prim.anchor.y,
                    "text": prim.text,
                    "leader_x": prim.leader_end.x,
                    "leader_y": prim.leader_end.y,
                },
            })

    sheet = instruction_set.get("sheet", {})
    title = instruction_set.get("title", {})

    return {
        "instruction_version": "0.2",
        "entities": entities,
        "dimensions": dimensions,
        "text_annotations": text_annotations,
        "layers": instruction_set.get("layers", []),
        "sheet_metadata": {
            "width": sheet.get("width", 36.0),
            "height": sheet.get("height", 24.0),
            "unit": sheet.get("unit", "in"),
            "scale": sheet.get("scale", "1:1"),
        },
        "title_block_data": {
            "project_name": "",
            "assembly_name": title.get("assembly_family", ""),
            "drawing_number": title.get("detail_id", ""),
            "revision": "0",
            "date": "",
            "schema_version": "0.2",
        },
        "provenance": instruction_set.get("provenance", {}),
    }
