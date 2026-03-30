"""
Condition Detector — Wave 14 Subsystem 5.

Detects construction conditions from field inputs.
All outputs are advisory only — never kernel truth.
Fail-closed on unsupported or ambiguous inputs.
"""

from typing import Any

SUPPORTED_CONDITION_TYPES = frozenset([
    "ROOF_FIELD", "PARAPET", "EDGE", "DRAIN",
    "SCUPPER", "CURB", "PIPE_PENETRATION", "EXPANSION_JOINT",
])

MINIMUM_CONFIDENCE_THRESHOLD = 0.3


class ConditionDetectionError(Exception):
    """Raised when detection encounters a fatal error."""


def detect_condition_from_manual(
    condition_type: str,
    label: str,
    evidence_ref: str,
    confidence: float = 1.0,
    geometry_hints: dict[str, Any] | None = None,
    material_hints: list[str] | None = None,
) -> dict[str, Any]:
    """
    Create a detected condition from manual field entry.
    Returns advisory-only detection result.
    """
    if condition_type not in SUPPORTED_CONDITION_TYPES:
        raise ConditionDetectionError(
            f"Unsupported condition type '{condition_type}'. "
            f"Supported: {sorted(SUPPORTED_CONDITION_TYPES)}"
        )

    if confidence < MINIMUM_CONFIDENCE_THRESHOLD:
        return {
            "detected_condition_type": condition_type,
            "detected_material_hints": material_hints or [],
            "detected_geometry_hints": geometry_hints or {},
            "confidence": confidence,
            "evidence_refs": [evidence_ref],
            "advisory_only": True,
            "detection_status": "UNKNOWN",
            "detection_reason": f"Confidence {confidence} below minimum threshold {MINIMUM_CONFIDENCE_THRESHOLD}.",
        }

    return {
        "detected_condition_type": condition_type,
        "detected_material_hints": sorted(material_hints or []),
        "detected_geometry_hints": geometry_hints or {},
        "confidence": confidence,
        "evidence_refs": [evidence_ref],
        "advisory_only": True,
        "detection_status": "DETECTED",
        "detection_reason": f"Manual entry: {label}",
    }


def detect_condition_from_image(
    image_ref: str,
    hints: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Stub for image-based condition detection.
    In Wave 14, image detection is not yet implemented.
    Returns UNKNOWN per fail-closed rule.
    """
    return {
        "detected_condition_type": "UNKNOWN",
        "detected_material_hints": [],
        "detected_geometry_hints": {},
        "confidence": 0.0,
        "evidence_refs": [image_ref],
        "advisory_only": True,
        "detection_status": "UNKNOWN",
        "detection_reason": "Image-based detection not yet implemented. Fail-closed.",
    }


def detect_condition_from_lidar(
    lidar_ref: str,
    hints: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Stub for lidar-based condition detection.
    In Wave 14, lidar detection is not yet implemented.
    Returns UNKNOWN per fail-closed rule.
    """
    return {
        "detected_condition_type": "UNKNOWN",
        "detected_material_hints": [],
        "detected_geometry_hints": {},
        "confidence": 0.0,
        "evidence_refs": [lidar_ref],
        "advisory_only": True,
        "detection_status": "UNKNOWN",
        "detection_reason": "Lidar-based detection not yet implemented. Fail-closed.",
    }
