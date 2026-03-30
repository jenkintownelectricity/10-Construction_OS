"""
Variant Generator — Wave 14 Subsystem 3.

Generates derived parameterized detail variants from canonical detail families.
Canonical detail IDs remain unchanged. Variants produce derived payloads only.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

CONTRACT_VERSION = "14.3.0"

CANONICAL_DETAIL_FAMILIES = frozenset([
    "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
    "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01",
    "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01",
    "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01",
    "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01",
    "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01",
    "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01",
    "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01",
    "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01",
])

# Parameter definitions with allowed ranges
PARAMETER_DEFINITIONS: dict[str, dict[str, Any]] = {
    "parapet_height": {"min": 4, "max": 96, "unit": "inches"},
    "membrane_thickness": {"min": 0.030, "max": 0.120, "unit": "inches"},
    "pipe_diameter": {"min": 0.5, "max": 24, "unit": "inches"},
    "curb_size": {"min": 6, "max": 72, "unit": "inches"},
    "drain_diameter": {"min": 2, "max": 12, "unit": "inches"},
    "reglet_depth": {"min": 0.25, "max": 2.0, "unit": "inches"},
    "joint_width": {"min": 0.5, "max": 6, "unit": "inches"},
    "overflow_size": {"min": 2, "max": 12, "unit": "inches"},
}

# Applicable parameters per condition type (derived from detail family condition)
CONDITION_PARAMETERS: dict[str, list[str]] = {
    "PARAPET": ["parapet_height", "membrane_thickness"],
    "VERTICAL_WALL": ["membrane_thickness"],
    "ROOF_TO_WALL": ["membrane_thickness", "reglet_depth"],
    "ROOF_TO_EDGE": ["membrane_thickness"],
    "PIPE": ["pipe_diameter", "membrane_thickness"],
    "CURB": ["curb_size", "membrane_thickness"],
    "DRAIN": ["drain_diameter", "membrane_thickness"],
    "SCUPPER": ["overflow_size", "membrane_thickness"],
    "EXPANSION_JOINT": ["joint_width", "membrane_thickness"],
}

# Map canonical detail IDs to their condition
DETAIL_CONDITION_MAP: dict[str, str] = {
    "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01": "PARAPET",
    "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01": "VERTICAL_WALL",
    "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01": "ROOF_TO_WALL",
    "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01": "ROOF_TO_EDGE",
    "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01": "PIPE",
    "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01": "CURB",
    "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01": "DRAIN",
    "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01": "SCUPPER",
    "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01": "EXPANSION_JOINT",
}

# Prohibited parameter combinations
PROHIBITED_COMBINATIONS: list[dict[str, Any]] = [
    {
        "description": "Thin membrane with tall parapet is structurally unsound",
        "condition": "PARAPET",
        "rule": lambda p: p.get("membrane_thickness", 999) < 0.045 and p.get("parapet_height", 0) > 48,
    },
    {
        "description": "Large pipe with thin membrane exceeds reinforcement limits",
        "condition": "PIPE",
        "rule": lambda p: p.get("pipe_diameter", 0) > 12 and p.get("membrane_thickness", 999) < 0.045,
    },
]


class VariantGenerationError(Exception):
    """Raised when variant generation fails."""


def generate_variant(
    canonical_detail_id: str,
    parameters: dict[str, float],
    variant_sequence: int = 1,
) -> dict[str, Any]:
    """
    Generate a single derived variant from a canonical detail.

    Args:
        canonical_detail_id: Must exist in CANONICAL_DETAIL_FAMILIES.
        parameters: Dict of parameter name to value.
        variant_sequence: Sequence number for variant ID (1-999).

    Returns:
        Variant payload dict.

    Raises:
        VariantGenerationError: On invalid input.
    """
    if canonical_detail_id not in CANONICAL_DETAIL_FAMILIES:
        raise VariantGenerationError(
            f"Canonical detail ID '{canonical_detail_id}' not found in frozen kernel families."
        )

    condition = DETAIL_CONDITION_MAP.get(canonical_detail_id)
    if not condition:
        raise VariantGenerationError(
            f"No condition mapping for '{canonical_detail_id}'."
        )

    # Validate parameters
    allowed_params = set(CONDITION_PARAMETERS.get(condition, []))
    for param_name, value in sorted(parameters.items()):
        if param_name not in PARAMETER_DEFINITIONS:
            raise VariantGenerationError(
                f"Unknown parameter '{param_name}'."
            )
        if param_name not in allowed_params:
            raise VariantGenerationError(
                f"Parameter '{param_name}' not applicable to condition '{condition}'. "
                f"Allowed: {sorted(allowed_params)}"
            )
        pdef = PARAMETER_DEFINITIONS[param_name]
        if value < pdef["min"] or value > pdef["max"]:
            raise VariantGenerationError(
                f"Parameter '{param_name}' value {value} outside allowed range "
                f"[{pdef['min']}, {pdef['max']}]."
            )

    # Check prohibited combinations
    for prohibition in PROHIBITED_COMBINATIONS:
        if prohibition["condition"] == condition and prohibition["rule"](parameters):
            raise VariantGenerationError(
                f"Prohibited parameter combination: {prohibition['description']}"
            )

    variant_id = f"{canonical_detail_id}-V{variant_sequence:03d}"

    return {
        "variant_id": variant_id,
        "canonical_detail_id": canonical_detail_id,
        "parameters": dict(sorted(parameters.items())),
        "provenance": {
            "canonical_detail_id": canonical_detail_id,
            "generation_source": "variant_generator",
            "contract_version": CONTRACT_VERSION,
        },
    }


def generate_variant_manifest(
    variants: list[dict[str, Any]],
    manifest_id: str = "variant-manifest",
) -> dict[str, Any]:
    """
    Build a variant manifest from a list of generated variants.
    Deterministic ordering and checksumming.
    """
    sorted_variants = sorted(variants, key=lambda v: v["variant_id"])

    manifest = {
        "manifest_id": manifest_id,
        "contract_version": CONTRACT_VERSION,
        "generation_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "variants": sorted_variants,
        "summary": {
            "total_variants": len(sorted_variants),
            "canonical_details_referenced": sorted(set(
                v["canonical_detail_id"] for v in sorted_variants
            )),
        },
    }

    content_for_checksum = json.dumps(
        sorted_variants, sort_keys=True, separators=(",", ":")
    )
    manifest["checksum"] = hashlib.sha256(content_for_checksum.encode("utf-8")).hexdigest()

    return manifest
