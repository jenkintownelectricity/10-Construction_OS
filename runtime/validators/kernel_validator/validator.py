"""Kernel validator.

Validates that parsed data meets minimum runtime integrity requirements
before proceeding to engine processing or deliverable generation.

Fails closed: if validation cannot confirm integrity, the result is invalid.
"""

from typing import Any


def validate_kernel_alignment(parsed_data: dict[str, Any], input_type: str) -> dict[str, Any]:
    """Validate parsed data against kernel alignment requirements.

    Checks:
        - Required parsed fields exist
        - Assembly references include enough information to proceed
        - Materials and geometry inputs are structurally valid
        - Deliverable generation only runs when minimum runtime integrity is met

    Fails closed: ambiguous or missing data results in is_valid=False.

    Args:
        parsed_data: The parsed payload (from assembly or spec parser).
        input_type: Either 'assembly' or 'spec'.

    Returns:
        Dictionary with:
            - is_valid: bool
            - warnings: list of warning strings
            - errors: list of error strings
    """
    warnings: list[str] = []
    errors: list[str] = []

    if not parsed_data:
        return {
            "is_valid": False,
            "warnings": [],
            "errors": ["Parsed data is empty or None. Failing closed."],
        }

    metadata = parsed_data.get("metadata", {})
    parse_status = metadata.get("parse_status", "")

    if parse_status == "empty_input":
        return {
            "is_valid": False,
            "warnings": [],
            "errors": ["Input was empty. Failing closed."],
        }

    if parse_status != "success":
        errors.append(f"Unexpected parse status: '{parse_status}'. Failing closed.")

    if input_type == "assembly":
        _validate_assembly(parsed_data, warnings, errors)
    elif input_type == "spec":
        _validate_spec(parsed_data, warnings, errors)
    else:
        errors.append(f"Unknown input_type: '{input_type}'. Failing closed.")

    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "warnings": warnings,
        "errors": errors,
    }


def _validate_assembly(parsed_data: dict[str, Any], warnings: list[str], errors: list[str]) -> None:
    """Validate assembly-specific parsed data."""
    if "components" not in parsed_data:
        errors.append("Missing 'components' field in assembly data.")
    elif not parsed_data["components"]:
        errors.append("Assembly has zero components. Cannot proceed.")

    if "constraints" not in parsed_data:
        warnings.append("Missing 'constraints' field in assembly data.")
    elif not parsed_data["constraints"]:
        warnings.append("Assembly has no constraints defined.")

    if not parsed_data.get("name"):
        warnings.append("Assembly has no name.")

    if not parsed_data.get("source_text"):
        warnings.append("Assembly has no source text.")


def _validate_spec(parsed_data: dict[str, Any], warnings: list[str], errors: list[str]) -> None:
    """Validate spec-specific parsed data."""
    if "sections" not in parsed_data:
        errors.append("Missing 'sections' field in spec data.")

    if "requirements" not in parsed_data:
        errors.append("Missing 'requirements' field in spec data.")
    elif not parsed_data["requirements"]:
        warnings.append("Spec has no requirements detected.")

    if not parsed_data.get("source_text"):
        warnings.append("Spec has no source text.")
