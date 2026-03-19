"""
Detail Resolution Layer

Resolves canonical detail logic from governed applicability rules.
Selects only governed canonical detail logic. Rejects unresolved or
conflicting matches. Rejects uncontrolled variant creation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DetailResolutionResult:
    """Result of detail resolution."""

    resolved: bool = False
    detail_id: str = ""
    detail_family: str = ""
    components: list[dict[str, Any]] = field(default_factory=list)
    relationships: list[dict[str, str]] = field(default_factory=list)
    parameter_bindings: dict[str, Any] = field(default_factory=dict)
    errors: list[dict[str, str]] = field(default_factory=list)


# Canonical detail applicability rules
# Each rule matches a condition pattern to a canonical detail logic definition.
APPLICABILITY_RULES: list[dict[str, Any]] = [
    {
        "rule_id": "RULE_EPDM_PARAPET_STD",
        "condition_pattern": {
            "interface_type": "roof_to_parapet",
            "membrane_class": "epdm_membrane",
        },
        "applies_detail": "EPDM_PARAPET_FLASHING_STANDARD",
        "detail_family": "parapet_flashing",
        "priority": 1,
        "components": [
            {"name": "membrane_extension", "role": "waterproofing", "material_param": "membrane_type"},
            {"name": "base_flashing", "role": "waterproofing", "material_param": "membrane_type"},
            {"name": "termination_bar", "role": "fastener", "material": "galvanized_steel"},
            {"name": "counterflashing", "role": "protection", "material": "galvanized_steel"},
            {"name": "sealant", "role": "sealant", "material": "polyurethane_sealant"},
        ],
        "relationships": [
            {"source": "membrane_extension", "type": "overlaps", "target": "base_flashing"},
            {"source": "base_flashing", "type": "fastened_to", "target": "substrate"},
            {"source": "termination_bar", "type": "fastened_to", "target": "substrate"},
            {"source": "termination_bar", "type": "covers", "target": "membrane_extension"},
            {"source": "counterflashing", "type": "covers", "target": "termination_bar"},
            {"source": "sealant", "type": "seals", "target": "counterflashing"},
        ],
    },
    {
        "rule_id": "RULE_TPO_PARAPET_STD",
        "condition_pattern": {
            "interface_type": "roof_to_parapet",
            "membrane_class": "tpo_membrane",
        },
        "applies_detail": "TPO_PARAPET_FLASHING_STANDARD",
        "detail_family": "parapet_flashing",
        "priority": 1,
        "components": [
            {"name": "membrane_extension", "role": "waterproofing", "material_param": "membrane_type"},
            {"name": "base_flashing", "role": "waterproofing", "material_param": "membrane_type"},
            {"name": "termination_bar", "role": "fastener", "material": "galvanized_steel"},
            {"name": "counterflashing", "role": "protection", "material": "galvanized_steel"},
            {"name": "sealant", "role": "sealant", "material": "polyurethane_sealant"},
        ],
        "relationships": [
            {"source": "membrane_extension", "type": "overlaps", "target": "base_flashing"},
            {"source": "base_flashing", "type": "fastened_to", "target": "substrate"},
            {"source": "termination_bar", "type": "fastened_to", "target": "substrate"},
            {"source": "termination_bar", "type": "covers", "target": "membrane_extension"},
            {"source": "counterflashing", "type": "covers", "target": "termination_bar"},
            {"source": "sealant", "type": "seals", "target": "counterflashing"},
        ],
    },
    {
        "rule_id": "RULE_EPDM_EDGE_STD",
        "condition_pattern": {
            "interface_type": "roof_edge",
            "membrane_class": "epdm_membrane",
        },
        "applies_detail": "EPDM_ROOF_EDGE_STANDARD",
        "detail_family": "roof_edge",
        "priority": 1,
        "components": [
            {"name": "membrane_extension", "role": "waterproofing", "material_param": "membrane_type"},
            {"name": "metal_edge", "role": "edge_profile", "material": "galvanized_steel"},
            {"name": "cleat", "role": "fastener", "material": "galvanized_steel"},
            {"name": "sealant", "role": "sealant", "material": "polyurethane_sealant"},
        ],
        "relationships": [
            {"source": "membrane_extension", "type": "overlaps", "target": "metal_edge"},
            {"source": "cleat", "type": "fastened_to", "target": "substrate"},
            {"source": "metal_edge", "type": "covers", "target": "cleat"},
            {"source": "sealant", "type": "seals", "target": "membrane_extension"},
        ],
    },
    {
        "rule_id": "RULE_TPO_EDGE_STD",
        "condition_pattern": {
            "interface_type": "roof_edge",
            "membrane_class": "tpo_membrane",
        },
        "applies_detail": "TPO_ROOF_EDGE_STANDARD",
        "detail_family": "roof_edge",
        "priority": 1,
        "components": [
            {"name": "membrane_extension", "role": "waterproofing", "material_param": "membrane_type"},
            {"name": "metal_edge", "role": "edge_profile", "material": "galvanized_steel"},
            {"name": "cleat", "role": "fastener", "material": "galvanized_steel"},
            {"name": "sealant", "role": "sealant", "material": "polyurethane_sealant"},
        ],
        "relationships": [
            {"source": "membrane_extension", "type": "overlaps", "target": "metal_edge"},
            {"source": "cleat", "type": "fastened_to", "target": "substrate"},
            {"source": "metal_edge", "type": "covers", "target": "cleat"},
            {"source": "sealant", "type": "seals", "target": "membrane_extension"},
        ],
    },
    {
        "rule_id": "RULE_PIPE_PENETRATION_STD",
        "condition_pattern": {
            "interface_type": "penetration",
        },
        "applies_detail": "PIPE_PENETRATION_FLASHING_STANDARD",
        "detail_family": "penetration_flashing",
        "priority": 10,
        "components": [
            {"name": "pipe_sleeve", "role": "penetrating_element", "material_param": "penetration_material"},
            {"name": "flashing_base", "role": "waterproofing", "material_param": "membrane_type"},
            {"name": "pipe_boot", "role": "seal", "material_param": "membrane_type"},
            {"name": "clamp", "role": "fastener", "material": "stainless_fastener"},
            {"name": "sealant", "role": "sealant", "material": "polyurethane_sealant"},
        ],
        "relationships": [
            {"source": "flashing_base", "type": "overlaps", "target": "membrane_extension"},
            {"source": "pipe_boot", "type": "surrounds", "target": "pipe_sleeve"},
            {"source": "clamp", "type": "fastened_to", "target": "pipe_boot"},
            {"source": "sealant", "type": "seals", "target": "pipe_boot"},
        ],
    },
]


def _matches_pattern(condition: dict[str, Any], pattern: dict[str, Any]) -> bool:
    """Check if a condition matches an applicability rule pattern."""
    for key, value in pattern.items():
        condition_value = condition.get(key)
        if condition_value is None:
            # Also check inside material_references
            condition_value = condition.get("material_references", {}).get(
                key.replace("_class", ""), ""
            )
        if condition_value != value:
            return False
    return True


def resolve_detail(condition: dict[str, Any]) -> DetailResolutionResult:
    """
    Resolve canonical detail logic from governed applicability rules.

    Fail-closed: if no governed detail applies or multiple ambiguous
    matches exist, returns unresolved with errors.
    """
    result = DetailResolutionResult()

    # Find matching rules
    matches: list[dict[str, Any]] = []
    for rule in APPLICABILITY_RULES:
        if _matches_pattern(condition, rule["condition_pattern"]):
            matches.append(rule)

    if not matches:
        result.errors.append({
            "code": "UNRESOLVED_DETAIL_APPLICABILITY",
            "message": (
                f"No governed detail applies for interface_type="
                f"'{condition.get('interface_type', 'unknown')}' with given materials"
            ),
            "path": "detail_applicability",
        })
        return result

    # Sort by priority (lower = higher priority)
    matches.sort(key=lambda r: r.get("priority", 100))

    # Check for ambiguous matches at same priority
    if len(matches) > 1 and matches[0]["priority"] == matches[1]["priority"]:
        result.errors.append({
            "code": "CONFLICTING_DETAIL_APPLICABILITY",
            "message": (
                f"Multiple detail rules match at same priority: "
                f"{[m['rule_id'] for m in matches[:3]]}"
            ),
            "path": "detail_applicability",
        })
        return result

    # Select best match
    selected = matches[0]
    result.resolved = True
    result.detail_id = selected["applies_detail"]
    result.detail_family = selected["detail_family"]
    result.components = selected["components"]
    result.relationships = selected["relationships"]

    return result
