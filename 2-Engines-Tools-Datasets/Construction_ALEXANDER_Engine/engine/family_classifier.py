"""
Pattern Family Classifier Module.

Classifies a normalized condition into a PatternFamily using
governed family definitions from the kernel.

Fail-closed: no match → UNRESOLVED, ambiguous match → BLOCKED.
"""

from engine.config import (
    CONDITION_TYPE_MAP,
    FAIL_NO_FAMILY_MATCH,
    FAIL_AMBIGUOUS_FAMILY,
    FAIL_MISSING_TRUTH,
)
from contracts.pattern_kernel_consumer import PatternKernelConsumer


def classify_family(
    normalized: dict,
    kernel: PatternKernelConsumer,
) -> dict:
    """
    Classify a normalized condition into a PatternFamily.

    Returns:
        {"matched": True, "family": {...}, "family_id": "...", "confidence": float}
        {"matched": False, "fail_reason": {...}}
    """
    condition_type = normalized.get("condition_type", "")

    # Map condition_type to domain key
    domain_key = CONDITION_TYPE_MAP.get(condition_type)

    if domain_key is None:
        # condition_type is 'interface' or 'transition' — try interface_condition
        interface_cond = normalized.get("interface_condition")
        if interface_cond:
            domain_key = _interface_to_domain(interface_cond)

    if domain_key is None:
        return _fail(
            FAIL_NO_FAMILY_MATCH,
            "family_classification",
            f"Cannot map condition_type '{condition_type}' to a pattern family domain",
            {"condition_type": condition_type},
        )

    # Query kernel for matching families
    candidates = kernel.get_families_by_domain_key(domain_key)

    if not candidates:
        return _fail(
            FAIL_MISSING_TRUTH,
            "family_classification",
            f"No pattern family found in kernel for domain key '{domain_key}'",
            {"domain_key": domain_key},
        )

    if len(candidates) == 1:
        family = candidates[0]
        return {
            "matched": True,
            "family": family,
            "family_id": family["id"],
            "confidence": 1.0,
        }

    # Multiple candidates — attempt to disambiguate by name/description match
    scored = []
    for fam in candidates:
        score = _score_family_match(fam, normalized)
        scored.append((score, fam))
    scored.sort(key=lambda x: x[0], reverse=True)

    if scored[0][0] > scored[1][0]:
        family = scored[0][1]
        return {
            "matched": True,
            "family": family,
            "family_id": family["id"],
            "confidence": min(scored[0][0], 1.0),
        }

    # Truly ambiguous
    return _fail(
        FAIL_AMBIGUOUS_FAMILY,
        "family_classification",
        f"Ambiguous family match: {len(candidates)} candidates for domain '{domain_key}'",
        {"candidates": [c["id"] for c in candidates]},
    )


def _interface_to_domain(interface_condition: str) -> str | None:
    """Map atlas interface condition types to kernel domain keys."""
    mapping = {
        "roof_to_wall": "PARAPET",
        "parapet": "PARAPET",
        "penetration": "PIPE",
        "fenestration": None,
        "below_grade": None,
        "expansion_joint": "JOINT",
        "deck_to_wall": None,
        "roof_edge": "EDGE",
        "curb": "PIPE",
        "drain": "DRAIN",
    }
    return mapping.get(interface_condition)


def _score_family_match(family: dict, normalized: dict) -> float:
    """Score how well a family matches the normalized condition."""
    score = 0.5  # base score for domain key match
    name = family.get("name", "").lower()
    desc = family.get("description", "").lower()
    ctype = normalized.get("condition_type", "").lower()

    if ctype in name:
        score += 0.3
    if ctype in desc:
        score += 0.2

    return score


def _fail(code: str, stage: str, message: str, details: dict = None) -> dict:
    reason = {"code": code, "stage": stage, "message": message}
    if details:
        reason["details"] = details
    return {"matched": False, "fail_reason": reason}
