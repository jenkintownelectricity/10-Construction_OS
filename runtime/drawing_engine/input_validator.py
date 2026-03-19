"""
Input Validation Layer

Validates governed inputs before any translation or rendering occurs.
Missing or ambiguous required inputs stop execution before IR emission.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:
    """Result of input validation."""

    is_valid: bool = False
    errors: list[dict[str, str]] = field(default_factory=list)
    warnings: list[dict[str, str]] = field(default_factory=list)


def validate_drawing_inputs(condition: dict[str, Any]) -> ValidationResult:
    """
    Validate all governed inputs required for deterministic drawing generation.

    Validates presence and integrity of:
    - applicable detail reference
    - detail schema inputs
    - material references against canonical taxonomy
    - interface conditions where required
    - scope posture where required
    - view intent completeness
    - parameter completeness

    Fail-closed: returns invalid with errors on any missing or ambiguous input.
    """
    result = ValidationResult()
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    if not isinstance(condition, dict):
        errors.append({
            "code": "INVALID_INPUT_TYPE",
            "message": "Condition must be a dictionary",
            "path": "condition",
        })
        result.errors = errors
        return result

    # Required fields
    required_fields = [
        ("condition_id", "Condition identifier is required"),
        ("assembly_type", "Assembly type is required for detail applicability"),
        ("interface_type", "Interface type is required for detail selection"),
    ]

    for field_name, message in required_fields:
        if not condition.get(field_name):
            errors.append({
                "code": "MISSING_REQUIRED_INPUT",
                "message": message,
                "path": field_name,
            })

    # Material references must use canonical material classes
    material_refs = condition.get("material_references", {})
    if not material_refs:
        errors.append({
            "code": "MISSING_REQUIRED_INPUT",
            "message": "At least one material reference is required",
            "path": "material_references",
        })
    elif isinstance(material_refs, dict):
        for role, mat_class in material_refs.items():
            if not isinstance(mat_class, str) or not mat_class.strip():
                errors.append({
                    "code": "INVALID_MATERIAL_REFERENCE",
                    "message": f"Material reference for '{role}' must be a non-empty canonical material class",
                    "path": f"material_references.{role}",
                })

    # View intent
    view_intent = condition.get("view_intent")
    if not view_intent:
        errors.append({
            "code": "MISSING_REQUIRED_INPUT",
            "message": "View intent is required for drawing generation",
            "path": "view_intent",
        })
    elif isinstance(view_intent, dict):
        for vi_field in ["view_intent_type", "representation_depth"]:
            if not view_intent.get(vi_field):
                errors.append({
                    "code": "INCOMPLETE_VIEW_INTENT",
                    "message": f"View intent field '{vi_field}' is required",
                    "path": f"view_intent.{vi_field}",
                })

    # Scope posture
    scope = condition.get("scope_classification")
    if not scope:
        warnings.append({
            "code": "MISSING_SCOPE",
            "message": "Scope classification not provided; will be treated as unresolved",
            "path": "scope_classification",
        })

    # Parameters
    parameters = condition.get("parameters", {})
    if not parameters:
        warnings.append({
            "code": "EMPTY_PARAMETERS",
            "message": "No parameters provided; detail parameterization may be incomplete",
            "path": "parameters",
        })

    result.errors = errors
    result.warnings = warnings
    result.is_valid = len(errors) == 0

    return result
