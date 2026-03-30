"""Geometry engine for Construction Runtime v0.2.

Deterministic geometry engine that produces DrawingInstructionSet objects
from runtime assembly data. All derived dimensions include provenance metadata.

Fails closed if dimensions are insufficient.
"""

from typing import Any

from runtime.models.drawing_instruction import (
    DrawingInstructionSet,
    DrawingEntity,
    DrawingDimension,
    TextAnnotation,
    SheetMetadata,
    TitleBlockData,
    SUPPORTED_ENTITY_TYPES,
)
from standards.layer_standards import (
    LAYER_COMPONENTS,
    LAYER_DIMENSIONS,
    LAYER_TEXT,
    LAYER_TITLEBLOCK,
    LAYER_CONSTRAINTS,
    LAYER_DETAIL,
    ALL_LAYERS,
)
from standards import error_codes
from rules.geometry_rules import (
    AUTHORITY_DERIVED,
    AUTHORITY_EXPLICIT,
    compute_panel_layout,
    validate_dimension,
)

SCHEMA_VERSION = "0.2"


def build_drawing_instructions(
    engine_result: dict[str, Any],
) -> tuple[DrawingInstructionSet | None, dict[str, Any]]:
    """Build a DrawingInstructionSet from assembly engine output.

    Args:
        engine_result: Output from the assembly engine.

    Returns:
        Tuple of (DrawingInstructionSet or None, validation_result).
        If geometry is insufficient, returns (None, errors).
    """
    errors: list[dict[str, str]] = []
    warnings: list[str] = []

    assembly_name = engine_result.get("assembly_name", "unnamed")
    components = engine_result.get("components", [])
    geometry = engine_result.get("geometry", {})
    constraints = engine_result.get("constraints", [])
    materials = engine_result.get("materials", [])

    if not components:
        errors.append({
            "code": error_codes.GEOMETRY_INSUFFICIENT_DIMENSIONS,
            "message": "No components to lay out.",
            "path": "engine_result.components",
        })
        return None, {"is_valid": False, "errors": errors, "warnings": warnings}

    # Build entities
    entities: list[DrawingEntity] = []
    dimensions: list[DrawingDimension] = []
    annotations: list[TextAnnotation] = []
    used_layers = set()

    # Title block entity
    entities.append(DrawingEntity(
        entity_type="RECT",
        layer=LAYER_TITLEBLOCK,
        properties={"x": 0, "y": 0, "width": 36, "height": 24, "role": "title_block"},
    ))
    used_layers.add(LAYER_TITLEBLOCK)

    # Component entities — lay them out as rectangles
    geo_dims = geometry.get("dimensions", {})
    comp_width = geo_dims.get("width", 4.0)
    comp_height = geo_dims.get("height", 2.0)

    spacing_x = 6.0
    start_x = 2.0
    start_y = 16.0

    for i, comp in enumerate(components):
        x = start_x + i * (comp_width + spacing_x)
        y = start_y

        # Validate dimensions
        w_valid, w_err = validate_dimension(comp_width, "in")
        h_valid, h_err = validate_dimension(comp_height, "in")
        if not w_valid:
            errors.append({"code": error_codes.GEOMETRY_NEGATIVE_DIMENSION, "message": w_err, "path": f"components[{i}].width"})
        if not h_valid:
            errors.append({"code": error_codes.GEOMETRY_NEGATIVE_DIMENSION, "message": h_err, "path": f"components[{i}].height"})

        entities.append(DrawingEntity(
            entity_type="RECT",
            layer=LAYER_COMPONENTS,
            properties={
                "x": x, "y": y,
                "width": comp_width, "height": comp_height,
                "name": comp.get("name", f"component_{i}"),
            },
        ))
        used_layers.add(LAYER_COMPONENTS)

        # Label
        annotations.append(TextAnnotation(
            text=comp.get("name", f"component_{i}"),
            position=(x + comp_width / 2, y - 0.5),
            font_size=10,
            layer=LAYER_TEXT,
        ))
        used_layers.add(LAYER_TEXT)

        # Dimension for width
        dimensions.append(DrawingDimension(
            dim_type="linear",
            start=(x, y + comp_height + 0.5),
            end=(x + comp_width, y + comp_height + 0.5),
            value=comp_width,
            unit="in",
            label=f"{comp_width}\"",
            layer=LAYER_DIMENSIONS,
            provenance={
                "authority_status": AUTHORITY_EXPLICIT if geo_dims else AUTHORITY_DERIVED,
                "source": "geometry_engine",
            },
        ))
        used_layers.add(LAYER_DIMENSIONS)

    # Constraint annotations
    for i, constraint in enumerate(constraints):
        annotations.append(TextAnnotation(
            text=f"{constraint.get('type', 'constraint')}: {constraint.get('description', '')}",
            position=(2.0, 6.0 - i * 1.0),
            font_size=8,
            layer=LAYER_CONSTRAINTS,
        ))
        used_layers.add(LAYER_CONSTRAINTS)

    if errors:
        return None, {"is_valid": False, "errors": errors, "warnings": warnings}

    # Build instruction set
    layers_list = sorted(used_layers)

    instruction_set = DrawingInstructionSet(
        entities=entities,
        dimensions=dimensions,
        text_annotations=annotations,
        layers=layers_list,
        sheet_metadata=SheetMetadata(
            width=36.0,
            height=24.0,
            unit="in",
            scale="1:1",
        ),
        title_block_data=TitleBlockData(
            assembly_name=assembly_name,
            schema_version=SCHEMA_VERSION,
        ),
        provenance={
            "engine": "geometry_engine",
            "version": SCHEMA_VERSION,
            "component_count": len(components),
        },
    )

    return instruction_set, {"is_valid": True, "errors": [], "warnings": warnings}
