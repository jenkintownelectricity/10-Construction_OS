"""
Detail Selector — Wave 14 Subsystem 2.

Selects canonical detail families based on classified condition and material context.
Returns only IDs that exist in the frozen kernel detail families.
"""

from typing import Any

# Frozen canonical detail families from Wave 13A Construction_Kernel
CANONICAL_DETAIL_FAMILIES: dict[str, dict[str, str]] = {
    "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01": {
        "condition": "PARAPET",
        "assembly_family": "EPDM",
        "system": "LOW_SLOPE",
        "class": "TERMINATION",
    },
    "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01": {
        "condition": "VERTICAL_WALL",
        "assembly_family": "TPO",
        "system": "LOW_SLOPE",
        "class": "TERMINATION",
    },
    "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01": {
        "condition": "ROOF_TO_WALL",
        "assembly_family": "PVC",
        "system": "LOW_SLOPE",
        "class": "TRANSITION",
    },
    "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01": {
        "condition": "ROOF_TO_EDGE",
        "assembly_family": "TPO",
        "system": "LOW_SLOPE",
        "class": "EDGE",
    },
    "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01": {
        "condition": "PIPE",
        "assembly_family": "EPDM",
        "system": "LOW_SLOPE",
        "class": "PENETRATION",
    },
    "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01": {
        "condition": "CURB",
        "assembly_family": "TPO",
        "system": "LOW_SLOPE",
        "class": "PENETRATION",
    },
    "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01": {
        "condition": "DRAIN",
        "assembly_family": "TPO",
        "system": "LOW_SLOPE",
        "class": "DRAINAGE",
    },
    "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01": {
        "condition": "SCUPPER",
        "assembly_family": "SBS",
        "system": "LOW_SLOPE",
        "class": "DRAINAGE",
    },
    "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01": {
        "condition": "EXPANSION_JOINT",
        "assembly_family": "EPDM",
        "system": "LOW_SLOPE",
        "class": "JOINT",
    },
}


class DetailSelection:
    """Result of selecting a detail family."""

    def __init__(
        self,
        canonical_detail_id: str | None,
        status: str,
        reason: str,
        ambiguity_flags: list[str] | None = None,
    ):
        self.canonical_detail_id = canonical_detail_id
        self.status = status
        self.reason = reason
        self.ambiguity_flags = ambiguity_flags or []


def select_detail(
    kernel_condition: str,
    material_context: str | None = None,
) -> DetailSelection:
    """
    Select a canonical detail family for a given kernel condition and material context.
    Returns only canonical IDs. Never fabricates.
    Deterministic for identical inputs.
    """
    candidates = [
        (did, info)
        for did, info in sorted(CANONICAL_DETAIL_FAMILIES.items())
        if info["condition"] == kernel_condition
    ]

    if not candidates:
        return DetailSelection(
            canonical_detail_id=None,
            status="UNRESOLVED",
            reason=f"No canonical detail family found for condition '{kernel_condition}'.",
        )

    # Filter by material context if provided
    if material_context:
        material_matches = [
            (did, info) for did, info in candidates
            if info["assembly_family"] == material_context
        ]
        if material_matches:
            if len(material_matches) == 1:
                did, _ = material_matches[0]
                return DetailSelection(
                    canonical_detail_id=did,
                    status="RESOLVED",
                    reason=f"Exact match: condition='{kernel_condition}', material='{material_context}'.",
                )
            else:
                # Multiple matches — take first deterministically but flag ambiguity
                did, _ = material_matches[0]
                return DetailSelection(
                    canonical_detail_id=did,
                    status="RESOLVED",
                    reason=f"Multiple matches for condition='{kernel_condition}', material='{material_context}'. Selected first by canonical ID sort.",
                    ambiguity_flags=[f"MULTIPLE_MATCHES:{len(material_matches)}"],
                )
        else:
            # Material context provided but no match — flag but still try condition-only
            ambiguity = [f"MATERIAL_MISMATCH:{material_context}"]
            if len(candidates) == 1:
                did, info = candidates[0]
                return DetailSelection(
                    canonical_detail_id=did,
                    status="RESOLVED",
                    reason=f"Condition match only: condition='{kernel_condition}'. Material '{material_context}' did not match assembly_family '{info['assembly_family']}'.",
                    ambiguity_flags=ambiguity,
                )
            else:
                did, _ = candidates[0]
                return DetailSelection(
                    canonical_detail_id=did,
                    status="RESOLVED",
                    reason=f"Condition match with material mismatch: condition='{kernel_condition}', requested='{material_context}'. Selected first by canonical ID sort.",
                    ambiguity_flags=ambiguity + [f"MULTIPLE_CANDIDATES:{len(candidates)}"],
                )

    # No material context — select by condition only
    if len(candidates) == 1:
        did, _ = candidates[0]
        return DetailSelection(
            canonical_detail_id=did,
            status="RESOLVED",
            reason=f"Single canonical match for condition='{kernel_condition}'.",
        )
    else:
        did, _ = candidates[0]
        return DetailSelection(
            canonical_detail_id=did,
            status="RESOLVED",
            reason=f"Multiple candidates for condition='{kernel_condition}'. Selected first by canonical ID sort.",
            ambiguity_flags=[f"MULTIPLE_CANDIDATES:{len(candidates)}"],
        )
