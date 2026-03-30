"""
Material Detector — Wave 14 Subsystem 5.

Detects material hints from field observations.
Advisory only — never kernel truth.
"""

from typing import Any

KNOWN_MATERIAL_CLASSES = frozenset([
    "SBS", "APP", "TPO", "PVC", "EPDM", "KEE",
    "HDPE", "LDPE", "PIB", "PU", "Acrylic",
    "Silicone", "Bitumen", "PMMA", "Epoxy", "Hybrid",
])


def detect_material_hints(
    observation: str,
    evidence_ref: str,
) -> dict[str, Any]:
    """
    Detect material hints from a field observation description.
    Returns advisory-only material hints with confidence.
    """
    detected: list[str] = []
    observation_upper = observation.upper()

    for material in sorted(KNOWN_MATERIAL_CLASSES):
        if material.upper() in observation_upper:
            detected.append(material)

    if not detected:
        return {
            "detected_materials": [],
            "confidence": 0.0,
            "evidence_refs": [evidence_ref],
            "advisory_only": True,
            "status": "UNKNOWN",
            "reason": "No known material classes detected in observation.",
        }

    return {
        "detected_materials": sorted(detected),
        "confidence": 0.5,  # keyword match only — moderate confidence
        "evidence_refs": [evidence_ref],
        "advisory_only": True,
        "status": "DETECTED",
        "reason": f"Keyword match detected: {', '.join(sorted(detected))}",
    }
