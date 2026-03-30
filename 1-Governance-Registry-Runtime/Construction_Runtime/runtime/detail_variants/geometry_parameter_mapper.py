"""
Geometry Parameter Mapper — Wave 14 Subsystem 3.

Maps geometry hints and field measurements to variant parameters.
Validates parameter applicability per condition type.
"""

from typing import Any

from runtime.detail_variants.variant_generator import (
    CONDITION_PARAMETERS,
    DETAIL_CONDITION_MAP,
    PARAMETER_DEFINITIONS,
)


class ParameterMappingError(Exception):
    """Raised when parameter mapping fails."""


def map_geometry_to_parameters(
    canonical_detail_id: str,
    geometry_hints: dict[str, Any],
) -> dict[str, float]:
    """
    Map geometry hints to variant parameters for a specific canonical detail.

    Args:
        canonical_detail_id: The canonical detail to map parameters for.
        geometry_hints: Raw geometry data (e.g., measured dimensions).

    Returns:
        Dict of validated parameter name to value.

    Raises:
        ParameterMappingError: If mapping fails or produces invalid values.
    """
    condition = DETAIL_CONDITION_MAP.get(canonical_detail_id)
    if not condition:
        raise ParameterMappingError(
            f"No condition mapping for '{canonical_detail_id}'."
        )

    allowed = set(CONDITION_PARAMETERS.get(condition, []))
    mapped: dict[str, float] = {}

    # Direct mapping: geometry hint keys that match parameter names
    for param_name in sorted(allowed):
        if param_name in geometry_hints:
            value = geometry_hints[param_name]
            if not isinstance(value, (int, float)):
                raise ParameterMappingError(
                    f"Parameter '{param_name}' must be numeric, got {type(value).__name__}."
                )
            pdef = PARAMETER_DEFINITIONS[param_name]
            if value < pdef["min"] or value > pdef["max"]:
                raise ParameterMappingError(
                    f"Parameter '{param_name}' value {value} outside allowed range "
                    f"[{pdef['min']}, {pdef['max']}]."
                )
            mapped[param_name] = float(value)

    return mapped


def get_applicable_parameters(canonical_detail_id: str) -> list[dict[str, Any]]:
    """
    Return the list of applicable parameters for a canonical detail,
    including their allowed ranges.
    """
    condition = DETAIL_CONDITION_MAP.get(canonical_detail_id)
    if not condition:
        return []

    params = CONDITION_PARAMETERS.get(condition, [])
    result = []
    for p in sorted(params):
        pdef = PARAMETER_DEFINITIONS.get(p, {})
        result.append({
            "parameter": p,
            "min": pdef.get("min"),
            "max": pdef.get("max"),
            "unit": pdef.get("unit", ""),
        })
    return result
