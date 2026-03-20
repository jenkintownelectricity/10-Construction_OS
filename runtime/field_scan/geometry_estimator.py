"""
Geometry Estimator — Wave 14 Subsystem 5.

Estimates geometry parameters from field observations.
Advisory only — uncertain estimates return UNKNOWN.
"""

from typing import Any

ESTIMATABLE_PARAMETERS = frozenset([
    "parapet_height", "membrane_thickness", "pipe_diameter",
    "curb_size", "drain_diameter", "reglet_depth",
    "joint_width", "overflow_size",
])


def estimate_geometry(
    raw_measurements: dict[str, Any],
    evidence_ref: str,
) -> dict[str, Any]:
    """
    Estimate geometry parameters from raw field measurements.
    Returns advisory-only geometry hints.
    """
    estimated: dict[str, float] = {}
    unknown_params: list[str] = []

    for param_name, value in sorted(raw_measurements.items()):
        if param_name not in ESTIMATABLE_PARAMETERS:
            unknown_params.append(param_name)
            continue
        if not isinstance(value, (int, float)):
            unknown_params.append(param_name)
            continue
        if value <= 0:
            unknown_params.append(param_name)
            continue
        estimated[param_name] = float(value)

    confidence = len(estimated) / max(len(raw_measurements), 1) if raw_measurements else 0.0

    return {
        "estimated_parameters": estimated,
        "unknown_parameters": sorted(unknown_params),
        "confidence": round(confidence, 3),
        "evidence_refs": [evidence_ref],
        "advisory_only": True,
        "status": "ESTIMATED" if estimated else "UNKNOWN",
        "reason": (
            f"Estimated {len(estimated)} parameters from field measurements."
            if estimated else
            "No valid parameters could be estimated from field measurements."
        ),
    }
