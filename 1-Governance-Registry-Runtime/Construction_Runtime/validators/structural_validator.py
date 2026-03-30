"""Structural validator for Construction Runtime v0.2.

Checks: missing required fields, malformed units, enum violations, invalid data types.
Fails closed.
"""

from typing import Any

from standards import error_codes


VALID_UNITS = {"in", "ft", "mm", "cm", "m"}
VALID_PARSE_STATUSES = {"success", "empty_input"}


def validate_structural(parsed_data: dict[str, Any], input_type: str) -> dict[str, Any]:
    """Run structural validation on parsed data.

    Returns:
        {
            "is_valid": bool,
            "stage": "structural",
            "warnings": [],
            "errors": [{"code": str, "message": str, "path": str}]
        }
    """
    warnings: list[str] = []
    errors: list[dict[str, str]] = []

    if not parsed_data:
        errors.append({
            "code": error_codes.VALIDATION_EMPTY_DATA,
            "message": "Parsed data is empty or None.",
            "path": "",
        })
        return {"is_valid": False, "stage": "structural", "warnings": warnings, "errors": errors}

    # Metadata checks
    metadata = parsed_data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append({
            "code": error_codes.MODEL_MISSING_FIELD,
            "message": "Missing or invalid 'metadata' field.",
            "path": "metadata",
        })
    else:
        status = metadata.get("parse_status", "")
        if status not in VALID_PARSE_STATUSES:
            errors.append({
                "code": error_codes.MODEL_ENUM_VIOLATION,
                "message": f"Invalid parse_status: '{status}'.",
                "path": "metadata.parse_status",
            })
        if status == "empty_input":
            errors.append({
                "code": error_codes.PARSE_EMPTY_INPUT,
                "message": "Input was empty.",
                "path": "metadata.parse_status",
            })

    if not parsed_data.get("source_text"):
        warnings.append("No source_text present.")

    if input_type == "assembly":
        _validate_assembly_structure(parsed_data, warnings, errors)
    elif input_type == "spec":
        _validate_spec_structure(parsed_data, warnings, errors)
    else:
        errors.append({
            "code": error_codes.VALIDATION_UNKNOWN_INPUT_TYPE,
            "message": f"Unknown input_type: '{input_type}'.",
            "path": "input_type",
        })

    return {"is_valid": len(errors) == 0, "stage": "structural", "warnings": warnings, "errors": errors}


def _validate_assembly_structure(data: dict, warnings: list, errors: list) -> None:
    if "components" not in data:
        errors.append({"code": error_codes.MODEL_MISSING_FIELD, "message": "Missing 'components'.", "path": "components"})
    elif not isinstance(data["components"], list):
        errors.append({"code": error_codes.MODEL_INVALID_TYPE, "message": "'components' must be a list.", "path": "components"})
    elif not data["components"]:
        errors.append({"code": error_codes.PARSE_COMPONENT_UNNAMED, "message": "Assembly has zero components.", "path": "components"})
    else:
        for i, comp in enumerate(data["components"]):
            if not isinstance(comp, dict):
                errors.append({"code": error_codes.MODEL_INVALID_TYPE, "message": f"Component at index {i} is not a dict.", "path": f"components[{i}]"})
            elif not comp.get("name"):
                errors.append({"code": error_codes.PARSE_COMPONENT_UNNAMED, "message": f"Component at index {i} has no name.", "path": f"components[{i}].name"})

    if "constraints" not in data:
        warnings.append("Missing 'constraints' field.")
    elif not data["constraints"]:
        warnings.append("No constraints defined.")

    if not data.get("name"):
        warnings.append("Assembly has no name.")


def _validate_spec_structure(data: dict, warnings: list, errors: list) -> None:
    if "sections" not in data:
        errors.append({"code": error_codes.MODEL_MISSING_FIELD, "message": "Missing 'sections'.", "path": "sections"})
    if "requirements" not in data:
        errors.append({"code": error_codes.MODEL_MISSING_FIELD, "message": "Missing 'requirements'.", "path": "requirements"})
    elif not data["requirements"]:
        warnings.append("No requirements detected.")
    if "product_references" not in data:
        warnings.append("Missing 'product_references' field.")
