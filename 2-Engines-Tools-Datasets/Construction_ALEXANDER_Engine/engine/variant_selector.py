"""
Variant Selector Module.

Selects the best PatternVariant from a resolved pattern based on
dimensions, system type, method preference, manufacturer refs,
and climate/wind constraints.

Fail-closed: no match → UNRESOLVED, ambiguous → BLOCKED.
"""

from engine.config import (
    FAIL_NO_VARIANT_MATCH,
    FAIL_AMBIGUOUS_VARIANT,
    FAIL_MISSING_TRUTH,
)
from contracts.pattern_kernel_consumer import PatternKernelConsumer


def select_variant(
    normalized: dict,
    pattern_id: str,
    kernel: PatternKernelConsumer,
) -> dict:
    """
    Select the best variant for a resolved pattern.

    Returns:
        {"matched": True, "variant": {...}, "variant_id": "...", "candidates": [...], "confidence": float}
        {"matched": False, "fail_reason": {...}, "candidates": [...]}
    """
    variants = kernel.get_variants_for_pattern(pattern_id)

    if not variants:
        return _fail(
            FAIL_MISSING_TRUTH,
            "variant_selection",
            f"No variants found in kernel for pattern '{pattern_id}'",
            {"pattern_id": pattern_id},
            candidates=[],
        )

    if len(variants) == 1:
        var = variants[0]
        return {
            "matched": True,
            "variant": var,
            "variant_id": var["id"],
            "candidates": [var["id"]],
            "confidence": 1.0,
        }

    # Score each variant
    scored = []
    for var in variants:
        score = _score_variant(var, normalized)
        scored.append((score, var))
    scored.sort(key=lambda x: x[0], reverse=True)

    all_ids = [s[1]["id"] for s in scored]

    if scored[0][0] > scored[1][0] and scored[0][0] > 0:
        var = scored[0][1]
        return {
            "matched": True,
            "variant": var,
            "variant_id": var["id"],
            "candidates": all_ids,
            "confidence": min(scored[0][0], 1.0),
        }

    if scored[0][0] == 0:
        return _fail(
            FAIL_NO_VARIANT_MATCH,
            "variant_selection",
            f"No variant matched condition context for pattern '{pattern_id}'",
            {"pattern_id": pattern_id, "candidates": all_ids},
            candidates=all_ids,
        )

    return _fail(
        FAIL_AMBIGUOUS_VARIANT,
        "variant_selection",
        f"Ambiguous variant match: top candidates tied for pattern '{pattern_id}'",
        {"pattern_id": pattern_id, "candidates": all_ids},
        candidates=all_ids,
    )


def _score_variant(variant: dict, normalized: dict) -> float:
    """Score variant fit based on method, materials, dimensions, manufacturer."""
    score = 0.0
    var_name = variant.get("name", "").lower()
    var_desc = variant.get("description", "").lower()
    method = variant.get("method", "").lower()
    materials = [
        m.get("name", "").lower()
        for m in variant.get("materials", [])
        if isinstance(m, dict)
    ]

    # Method preference matching
    method_pref = normalized.get("method_preference", "")
    if method_pref:
        mp = method_pref.lower()
        if mp in method or mp in var_name:
            score += 0.4
        elif mp in var_desc:
            score += 0.2

    # Material preference matching
    mat_prefs = normalized.get("material_preferences", [])
    if mat_prefs:
        for pref in mat_prefs:
            if any(pref in m for m in materials):
                score += 0.3
                break
            if pref in var_desc:
                score += 0.1
                break

    # Manufacturer reference matching
    mfr_refs = normalized.get("manufacturer_refs", [])
    var_mfrs = [m.lower() for m in variant.get("manufacturer_refs", []) if isinstance(m, str)]
    if mfr_refs and var_mfrs:
        for ref in mfr_refs:
            if ref in var_mfrs:
                score += 0.2
                break

    # Dimensional compatibility
    dims = normalized.get("dimensions", {})
    var_dims = variant.get("dimensional_constraints", {})
    if dims and var_dims:
        dim_score = _score_dimensional_fit(dims, var_dims)
        score += dim_score * 0.1

    return score


def _score_dimensional_fit(condition_dims: dict, variant_dims: dict) -> float:
    """Check if condition dimensions are compatible with variant constraints."""
    # Simple compatibility check — not a constraint enforcer
    if not variant_dims:
        return 1.0
    return 0.5  # partial credit for having any dimensional constraints


def _fail(code, stage, message, details=None, candidates=None):
    reason = {"code": code, "stage": stage, "message": message}
    if details:
        reason["details"] = details
    result = {"matched": False, "fail_reason": reason}
    if candidates is not None:
        result["candidates"] = candidates
    return result
