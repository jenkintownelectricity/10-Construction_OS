"""Kernel validator v0.2 (backward-compatible wrapper).

Delegates to the multi-layer validation system in validators/
while preserving the v0.1 API surface for existing callers.
"""

from typing import Any

from validators.structural_validator import validate_structural
from validators.domain_validator import validate_domain


def validate_kernel_alignment(parsed_data: dict[str, Any], input_type: str) -> dict[str, Any]:
    """Validate parsed data against kernel alignment requirements.

    v0.2: Delegates to structural + domain validators.
    Returns v0.1-compatible format: {is_valid, warnings, errors}.
    """
    # Run structural validation
    structural = validate_structural(parsed_data, input_type)

    # Flatten structured errors to strings for v0.1 compat
    warnings: list[str] = list(structural["warnings"])
    errors: list[str] = [e["message"] for e in structural["errors"]]

    if not structural["is_valid"]:
        return {"is_valid": False, "warnings": warnings, "errors": errors}

    # Run domain validation
    domain = validate_domain(parsed_data, input_type)
    warnings.extend(domain["warnings"])
    errors.extend(e["message"] for e in domain["errors"])

    return {
        "is_valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
    }
