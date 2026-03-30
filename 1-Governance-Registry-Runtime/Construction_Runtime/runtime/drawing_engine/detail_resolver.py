"""
Detail Resolution Layer

Resolves canonical detail logic from governed applicability rules.
Selects only governed canonical detail logic. Rejects unresolved or
conflicting matches. Rejects uncontrolled variant creation.

Applicability rules are loaded from Construction_Kernel governed contracts.
Runtime does not define applicability rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from runtime.drawing_engine.contract_loader import (
    ContractLoadError,
    load_applicability_rules,
)


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


def _load_governed_rules() -> list[dict[str, Any]]:
    """
    Load applicability rules from governed kernel contracts.

    Fail-closed: if contracts are missing or malformed, returns
    an empty list and the caller will produce an appropriate error.
    """
    try:
        return load_applicability_rules()
    except ContractLoadError as exc:
        # Re-raise as a resolution-level error so the pipeline fails closed
        raise


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

    Rules are loaded from Construction_Kernel governed contracts.
    Fail-closed: if no governed detail applies, contracts are missing,
    or multiple ambiguous matches exist, returns unresolved with errors.
    """
    result = DetailResolutionResult()

    # Load governed rules from kernel contracts — fail closed on error
    try:
        governed_rules = _load_governed_rules()
    except ContractLoadError as exc:
        result.errors.append({
            "code": "GOVERNED_CONTRACT_LOAD_FAILURE",
            "message": str(exc),
            "path": "detail_applicability",
        })
        return result

    # Find matching rules
    matches: list[dict[str, Any]] = []
    for rule in governed_rules:
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
