"""
Renderer Layer

Renders deterministic outputs from Drawing Instruction IR.
All renderers consume the same IR. No renderer may invent construction logic.
Renderers decide geometric emission only.
"""

from __future__ import annotations

from typing import Any

from runtime.drawing_engine.ir_emitter import IRInstruction


def render_svg(
    detail_id: str,
    instructions: list[IRInstruction],
    width: int = 800,
    height: int = 600,
) -> dict[str, Any]:
    """
    Render Drawing Instruction IR to SVG output.

    Translates construction-semantic IR into SVG elements.
    The renderer makes geometric decisions only — it does not
    invent construction logic or modify semantic content.

    Returns a dict with svg_content and render_status.
    """
    elements: list[str] = []
    y_offset = 60
    component_positions: dict[str, int] = {}

    for instruction in instructions:
        inst_type = instruction.instruction_type

        if inst_type == "define_view_boundary":
            elements.append(
                f'  <rect x="10" y="10" width="{width - 20}" height="{height - 20}" '
                f'fill="none" stroke="#000" stroke-width="2"/>'
            )
            elements.append(
                f'  <text x="{width // 2}" y="35" text-anchor="middle" '
                f'font-size="14" font-weight="bold">'
                f'{instruction.target_reference.replace("_", " ").title()}</text>'
            )

        elif inst_type == "draw_component":
            component_positions[instruction.target_reference] = y_offset
            fill = _material_color(instruction.material_reference)
            elements.append(
                f'  <rect x="80" y="{y_offset}" width="600" height="30" '
                f'fill="{fill}" stroke="#333" stroke-width="1"/>'
            )
            elements.append(
                f'  <text x="90" y="{y_offset + 20}" font-size="11">'
                f'{instruction.target_reference}</text>'
            )
            y_offset += 40

        elif inst_type == "draw_profile":
            component_positions[instruction.target_reference] = y_offset
            elements.append(
                f'  <polygon points="80,{y_offset} 680,{y_offset} '
                f'680,{y_offset + 25} 690,{y_offset + 35} '
                f'70,{y_offset + 35} 80,{y_offset + 25}" '
                f'fill="#C0C0C0" stroke="#333" stroke-width="1"/>'
            )
            elements.append(
                f'  <text x="90" y="{y_offset + 20}" font-size="11">'
                f'{instruction.target_reference}</text>'
            )
            y_offset += 45

        elif inst_type == "place_material_tag":
            tag_y = component_positions.get(instruction.target_reference, y_offset)
            elements.append(
                f'  <text x="700" y="{tag_y + 15}" font-size="9" fill="#666">'
                f'{instruction.material_reference}</text>'
            )

        elif inst_type == "place_symbol":
            sym_params = instruction.parameters
            sym_y = component_positions.get(instruction.target_reference, y_offset)
            spacing = sym_params.get("spacing", "12in")
            elements.append(
                f'  <text x="700" y="{sym_y + 15}" font-size="9" fill="#900">'
                f'[{sym_params.get("type", "fastener")} @ {spacing}]</text>'
            )

        elif inst_type == "place_dimension":
            dim_params = instruction.parameters
            elements.append(
                f'  <text x="50" y="{y_offset}" font-size="9" fill="#006">'
                f'{dim_params.get("type", "dim")}: {dim_params.get("value", "")}</text>'
            )
            y_offset += 15

        elif inst_type == "place_annotation":
            ann_params = instruction.parameters
            elements.append(
                f'  <text x="{width // 2}" y="{height - 20}" text-anchor="middle" '
                f'font-size="12" font-style="italic">'
                f'{ann_params.get("text", "")}</text>'
            )

    svg_content = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
        f'  <style>text {{ font-family: monospace; }}</style>\n'
        + "\n".join(elements)
        + "\n</svg>"
    )

    return {
        "render_status": "success",
        "format": "svg",
        "detail_id": detail_id,
        "svg_content": svg_content,
        "instruction_count": len(instructions),
        "element_count": len(elements),
    }


def render_dxf_stub(
    detail_id: str,
    instructions: list[IRInstruction],
) -> dict[str, Any]:
    """
    Stub DXF renderer consuming the same IR.

    Produces a DXF-compatible instruction summary.
    Full DXF entity emission deferred to future implementation.
    """
    dxf_instructions: list[dict[str, Any]] = []

    for instruction in instructions:
        dxf_instructions.append({
            "ir_type": instruction.instruction_type,
            "target": instruction.target_reference,
            "material": instruction.material_reference,
            "params": instruction.parameters,
        })

    return {
        "render_status": "stub",
        "format": "dxf",
        "detail_id": detail_id,
        "dxf_instructions": dxf_instructions,
        "instruction_count": len(instructions),
    }


def _material_color(material_ref: str) -> str:
    """Map canonical material class to a display color for SVG rendering."""
    color_map = {
        "epdm_membrane": "#2C2C2C",
        "tpo_membrane": "#E8E8E8",
        "pvc_membrane": "#D0D0D0",
        "galvanized_steel": "#C0C0C0",
        "stainless_steel": "#A8A8A8",
        "aluminum_sheet": "#B8B8B8",
        "polyiso_insulation": "#FFE4B5",
        "xps_insulation": "#87CEEB",
        "mineral_wool_insulation": "#DAA520",
        "polyurethane_sealant": "#8B4513",
        "silicone_sealant": "#D3D3D3",
        "steel_deck": "#808080",
        "concrete_deck": "#A9A9A9",
        "gypsum_board": "#FAFAD2",
    }
    return color_map.get(material_ref, "#CCCCCC")
