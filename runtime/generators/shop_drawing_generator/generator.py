"""Shop drawing generator.

Generates structured drawing instructions, DXF-compatible export instructions,
and JSON-friendly preview output from validated assembly data.

Structured output first, render/export second.
"""

from typing import Any

from runtime.models.deliverable_model import DeliverableModel


def generate_shop_drawing(assembly_engine_output: dict[str, Any]) -> DeliverableModel:
    """Generate a shop drawing deliverable from assembly engine output.

    Sequence:
        1. Accept validated assembly runtime model
        2. Generate structured drawing instructions
        3. Generate DXF-compatible export instructions
        4. Generate JSON-friendly preview output
        5. Emit DeliverableModel

    Args:
        assembly_engine_output: Output from the assembly engine.

    Returns:
        A DeliverableModel containing structured drawing data.
    """
    assembly_name = assembly_engine_output.get("assembly_name", "unnamed")
    components = assembly_engine_output.get("components", [])
    geometry = assembly_engine_output.get("geometry", {})
    constraints = assembly_engine_output.get("constraints", [])

    # Step 2: Structured drawing instructions
    drawing_instructions = _build_drawing_instructions(
        assembly_name, components, geometry, constraints
    )

    # Step 3: DXF-compatible export instructions
    dxf_instructions = _build_dxf_export_instructions(
        assembly_name, components, geometry
    )

    # Step 4: JSON-friendly preview
    preview = _build_json_preview(assembly_name, components, geometry, constraints)

    return DeliverableModel(
        deliverable_type="shop_drawing",
        payload={
            "drawing_instructions": drawing_instructions,
            "dxf_export": dxf_instructions,
            "preview": preview,
        },
        export_targets=["json", "dxf"],
    )


def _build_drawing_instructions(
    name: str,
    components: list[dict],
    geometry: dict,
    constraints: list[dict],
) -> list[dict[str, Any]]:
    """Build structured drawing instructions for each component."""
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


def _build_dxf_export_instructions(
    name: str,
    components: list[dict],
    geometry: dict,
) -> dict[str, Any]:
    """Build DXF-compatible export instructions."""
    return {
        "format": "dxf",
        "filename": f"{name.replace(' ', '_').lower()}_shop_drawing.dxf",
        "layers": [
            {"name": "COMPONENTS", "item_count": len(components)},
            {"name": "DIMENSIONS", "has_data": bool(geometry.get("dimensions"))},
            {"name": "ANNOTATIONS", "has_data": True},
        ],
    }


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
