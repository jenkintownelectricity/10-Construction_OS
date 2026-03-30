"""Generation validator for Construction Runtime v0.2.

Checks: geometry completeness, annotation completeness, layer assignments,
deliverable structure, SVG render readiness.
Fails closed.
"""

from typing import Any

from standards import error_codes
from standards.layer_standards import ALL_LAYERS
from runtime.models.drawing_instruction import SUPPORTED_ENTITY_TYPES


def validate_generation(instruction_set_dict: dict[str, Any]) -> dict[str, Any]:
    """Validate a DrawingInstructionSet (as dict) for generation readiness.

    Returns structured validation result with stage='generation'.
    """
    warnings: list[str] = []
    errors: list[dict[str, str]] = []

    if not instruction_set_dict:
        errors.append({
            "code": error_codes.GENERATION_GEOMETRY_INCOMPLETE,
            "message": "Instruction set is empty.",
            "path": "",
        })
        return {"is_valid": False, "stage": "generation", "warnings": warnings, "errors": errors}

    # Check entities
    entities = instruction_set_dict.get("entities", [])
    if not entities:
        errors.append({
            "code": error_codes.GENERATION_GEOMETRY_INCOMPLETE,
            "message": "No entities in instruction set.",
            "path": "entities",
        })

    for i, entity in enumerate(entities):
        etype = entity.get("entity_type", "")
        if etype not in SUPPORTED_ENTITY_TYPES:
            errors.append({
                "code": error_codes.GENERATION_SVG_UNSUPPORTED_ENTITY,
                "message": f"Unsupported entity type: '{etype}'.",
                "path": f"entities[{i}].entity_type",
            })

        layer = entity.get("layer", "")
        if not layer:
            errors.append({
                "code": error_codes.GENERATION_LAYER_MAPPING_MISSING,
                "message": f"Entity at index {i} has no layer.",
                "path": f"entities[{i}].layer",
            })
        elif layer not in ALL_LAYERS:
            warnings.append(f"Entity at index {i} uses non-standard layer '{layer}'.")

    # Check layers list
    layers = instruction_set_dict.get("layers", [])
    if not layers:
        warnings.append("No layers declared in instruction set.")

    # Check sheet metadata
    sheet = instruction_set_dict.get("sheet_metadata", {})
    if not sheet:
        errors.append({
            "code": error_codes.GENERATION_GEOMETRY_INCOMPLETE,
            "message": "Missing sheet_metadata.",
            "path": "sheet_metadata",
        })
    else:
        if sheet.get("width", 0) <= 0 or sheet.get("height", 0) <= 0:
            errors.append({
                "code": error_codes.GEOMETRY_NEGATIVE_DIMENSION,
                "message": "Sheet dimensions must be positive.",
                "path": "sheet_metadata",
            })

    # Check annotation completeness
    annotations = instruction_set_dict.get("text_annotations", [])
    for i, ann in enumerate(annotations):
        if not ann.get("text", "").strip():
            warnings.append(f"Text annotation at index {i} has empty text.")

    return {"is_valid": len(errors) == 0, "stage": "generation", "warnings": warnings, "errors": errors}
