"""Shop drawing generator v0.2.

Generates deliverables via DrawingInstructionSet → DXF + SVG dual output.
Consumes geometry engine output, not raw assembly data.

v0.2: Uses DrawingInstructionSet as intermediate representation.
Backward-compatible: still returns DeliverableModel with payload.
"""

import uuid
from typing import Any

from runtime.models.deliverable_model import DeliverableModel, DeliverableFormat
from runtime.models.drawing_instruction import DrawingInstructionSet
from geometry.geometry_engine import build_drawing_instructions
from generator.dxf_writer import write_dxf
from generator.svg_writer import write_svg
from validators.generation_validator import validate_generation


def generate_shop_drawing(assembly_engine_output: dict[str, Any]) -> DeliverableModel:
    """Generate a shop drawing deliverable from assembly engine output.

    v0.2 flow:
        1. Build DrawingInstructionSet via geometry engine
        2. Validate instruction set for generation readiness
        3. Generate DXF via dxf_writer
        4. Generate SVG via svg_writer
        5. Build JSON preview
        6. Emit DeliverableModel with all formats

    Falls back to v0.1 behavior if geometry engine fails.

    Args:
        assembly_engine_output: Output from the assembly engine.

    Returns:
        A DeliverableModel containing DXF, SVG, and JSON preview.
    """
    deliverable_id = f"detail_{uuid.uuid4().hex[:6]}"
    assembly_name = assembly_engine_output.get("assembly_name", "unnamed")
    components = assembly_engine_output.get("components", [])
    constraints = assembly_engine_output.get("constraints", [])
    geometry = assembly_engine_output.get("geometry", {})

    # Step 1: Build DrawingInstructionSet
    instruction_set, geo_result = build_drawing_instructions(assembly_engine_output)

    dxf_format = DeliverableFormat(status="skipped")
    svg_format = DeliverableFormat(status="skipped")
    json_format = DeliverableFormat(status="pending")

    if instruction_set is not None:
        # Step 2: Validate
        gen_validation = validate_generation(instruction_set.to_dict())

        if gen_validation["is_valid"]:
            # Step 3: DXF
            dxf_content, dxf_errors = write_dxf(instruction_set)
            if not dxf_errors:
                dxf_format = DeliverableFormat(content=dxf_content, status="generated")
            else:
                dxf_format = DeliverableFormat(status="failed")

            # Step 4: SVG
            svg_content, svg_errors = write_svg(instruction_set)
            if not svg_errors:
                svg_format = DeliverableFormat(content=svg_content, status="generated")
            else:
                svg_format = DeliverableFormat(status="failed")

    # Step 5: JSON preview (always generated)
    preview = _build_json_preview(assembly_name, components, geometry, constraints)
    json_format = DeliverableFormat(
        content=str(preview),
        status="generated",
    )

    # Step 6: Build v0.1-compatible payload + v0.2 formats
    drawing_instructions = _build_v1_drawing_instructions(
        assembly_name, components, geometry, constraints
    )

    return DeliverableModel(
        deliverable_type="shop_drawing",
        deliverable_id=deliverable_id,
        deliverable_version="0.2",
        payload={
            "drawing_instructions": drawing_instructions,
            "preview": preview,
        },
        export_targets=["json", "dxf", "svg"],
        formats={
            "dxf": dxf_format,
            "svg": svg_format,
            "json_preview": json_format,
        },
    )


def _build_v1_drawing_instructions(
    name: str,
    components: list[dict],
    geometry: dict,
    constraints: list[dict],
) -> list[dict[str, Any]]:
    """Build v0.1-compatible drawing instructions for payload backward compat."""
    instructions = []
    instructions.append({
        "action": "title_block",
        "assembly_name": name,
        "component_count": len(components),
    })
    for i, comp in enumerate(components):
        instructions.append({
            "action": "draw_component",
            "index": i,
            "name": comp.get("name", f"component_{i}"),
            "type": comp.get("type", "unknown"),
        })
    if geometry.get("dimensions"):
        instructions.append({
            "action": "apply_dimensions",
            "dimensions": geometry["dimensions"],
        })
    for constraint in constraints:
        instructions.append({
            "action": "annotate_constraint",
            "type": constraint.get("type", ""),
            "description": constraint.get("description", ""),
        })
    return instructions


def _build_json_preview(
    name: str,
    components: list[dict],
    geometry: dict,
    constraints: list[dict],
) -> dict[str, Any]:
    """Build a JSON-friendly preview of the shop drawing."""
    return {
        "assembly_name": name,
        "component_names": [c.get("name", "") for c in components],
        "has_geometry": bool(geometry.get("dimensions") or geometry.get("spatial_refs")),
        "constraint_count": len(constraints),
        "export_ready": len(components) > 0,
    }
