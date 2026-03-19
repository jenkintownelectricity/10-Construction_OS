"""
IR Emission Layer

Emits Drawing Instruction IR from governed detail logic plus resolved parameters.
IR is construction-semantic and engine-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class IRInstruction:
    """A single Drawing Instruction IR instruction."""

    instruction_type: str = ""
    target_reference: str = ""
    material_reference: str = ""
    position_context: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    representation_intent: str = ""


@dataclass
class IREmissionResult:
    """Result of IR emission."""

    emitted: bool = False
    detail_id: str = ""
    instructions: list[IRInstruction] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)


def emit_ir(
    detail_id: str,
    components: list[dict[str, Any]],
    relationships: list[dict[str, str]],
    parameters: dict[str, Any],
    view_intent: dict[str, Any],
) -> IREmissionResult:
    """
    Emit Drawing Instruction IR from resolved detail logic.

    Emits only construction-semantic IR referencing canonical components
    and relationships. Avoids renderer-specific logic.

    Fail-closed: if required references are incomplete, returns unemitted.
    """
    result = IREmissionResult(detail_id=detail_id)
    instructions: list[IRInstruction] = []
    errors: list[dict[str, str]] = []

    if not components:
        errors.append({
            "code": "IR_EMISSION_FAILURE",
            "message": "No components available for IR emission",
            "path": "components",
        })
        result.errors = errors
        return result

    # View boundary instruction
    view_type = view_intent.get("view_intent_type", "detail_view")
    depth = view_intent.get("representation_depth", "component_level")

    instructions.append(IRInstruction(
        instruction_type="define_view_boundary",
        target_reference=detail_id,
        parameters={"type": view_type, "depth": depth},
        representation_intent=depth,
    ))

    instructions.append(IRInstruction(
        instruction_type="set_representation_depth",
        parameters={"depth": depth},
    ))

    # Component instructions
    for component in components:
        name = component.get("name", "")
        material = component.get("material", "")
        role = component.get("role", "")

        if not name:
            errors.append({
                "code": "IR_EMISSION_FAILURE",
                "message": "Component missing name",
                "path": "components",
            })
            continue

        # Determine instruction type based on role
        if role == "edge_profile":
            inst_type = "draw_profile"
        else:
            inst_type = "draw_component"

        instructions.append(IRInstruction(
            instruction_type=inst_type,
            target_reference=name,
            material_reference=material,
            position_context=f"detail:{detail_id}",
            parameters={"role": role},
            representation_intent=depth,
        ))

        # Material tag
        if material:
            instructions.append(IRInstruction(
                instruction_type="place_material_tag",
                target_reference=name,
                material_reference=material,
            ))

    # Relationship instructions
    for rel in relationships:
        source = rel.get("source", "")
        rel_type = rel.get("type", "")
        target = rel.get("target", "")

        if not all([source, rel_type, target]):
            continue

        instructions.append(IRInstruction(
            instruction_type="draw_relationship",
            target_reference=f"{source}->{target}",
            parameters={"relationship_type": rel_type, "source": source, "target": target},
        ))

    # Fastener symbols
    for component in components:
        if component.get("role") == "fastener":
            spacing = parameters.get("fastener_spacing", "12in")
            instructions.append(IRInstruction(
                instruction_type="place_symbol",
                target_reference=component.get("name", ""),
                material_reference=component.get("material", ""),
                parameters={"type": "fastener", "spacing": spacing},
            ))

    # Dimension instructions from parameters
    for param_key, param_value in parameters.items():
        if param_key.endswith("_dimension") or param_key in ("overlap", "height", "extension"):
            instructions.append(IRInstruction(
                instruction_type="place_dimension",
                parameters={"type": param_key, "value": str(param_value)},
            ))

    # Annotation for detail title
    instructions.append(IRInstruction(
        instruction_type="place_annotation",
        target_reference=detail_id,
        parameters={"text": detail_id.replace("_", " ").title()},
    ))

    result.instructions = instructions
    result.errors = errors
    result.emitted = len(errors) == 0

    return result
