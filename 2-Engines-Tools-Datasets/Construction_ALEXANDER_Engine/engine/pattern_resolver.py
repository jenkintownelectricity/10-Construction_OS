"""
Pattern Resolver Module.

Narrows pattern candidates within a selected family based on
condition context, interface conditions, and detail intents.

Fail-closed: no match → UNRESOLVED, ambiguous → BLOCKED.
"""

from engine.config import (
    FAIL_NO_PATTERN_MATCH,
    FAIL_AMBIGUOUS_PATTERN,
    FAIL_MISSING_TRUTH,
)
from contracts.pattern_kernel_consumer import PatternKernelConsumer


def resolve_pattern(
    normalized: dict,
    family_id: str,
    kernel: PatternKernelConsumer,
) -> dict:
    """
    Resolve a specific pattern within the classified family.

    Returns:
        {"matched": True, "pattern": {...}, "pattern_id": "...", "candidates": [...], "confidence": float}
        {"matched": False, "fail_reason": {...}, "candidates": [...]}
    """
    patterns = kernel.get_patterns_for_family(family_id)

    if not patterns:
        return _fail(
            FAIL_MISSING_TRUTH,
            "pattern_resolution",
            f"No patterns found in kernel for family '{family_id}'",
            {"family_id": family_id},
            candidates=[],
        )

    if len(patterns) == 1:
        pat = patterns[0]
        return {
            "matched": True,
            "pattern": pat,
            "pattern_id": pat["id"],
            "candidates": [pat["id"]],
            "confidence": 1.0,
        }

    # Score each pattern against the condition
    scored = []
    for pat in patterns:
        score = _score_pattern(pat, normalized)
        scored.append((score, pat))
    scored.sort(key=lambda x: x[0], reverse=True)

    all_ids = [s[1]["id"] for s in scored]

    # Check if there's a clear winner
    if scored[0][0] > scored[1][0] and scored[0][0] > 0:
        pat = scored[0][1]
        return {
            "matched": True,
            "pattern": pat,
            "pattern_id": pat["id"],
            "candidates": all_ids,
            "confidence": min(scored[0][0], 1.0),
        }

    # If all scores are 0, no match
    if scored[0][0] == 0:
        return _fail(
            FAIL_NO_PATTERN_MATCH,
            "pattern_resolution",
            f"No pattern matched condition context within family '{family_id}'",
            {"family_id": family_id, "candidates": all_ids},
            candidates=all_ids,
        )

    # Ambiguous — tied top scores
    return _fail(
        FAIL_AMBIGUOUS_PATTERN,
        "pattern_resolution",
        f"Ambiguous pattern match: top {len([s for s in scored if s[0] == scored[0][0]])} candidates tied",
        {"family_id": family_id, "candidates": all_ids},
        candidates=all_ids,
    )


def _score_pattern(pattern: dict, normalized: dict) -> float:
    """Score pattern fit against normalized condition."""
    score = 0.0
    pat_name = pattern.get("name", "").lower()
    pat_desc = pattern.get("description", "").lower()
    pat_text = pat_name + " " + pat_desc
    detail_intents = [d.lower() if isinstance(d, str) else "" for d in pattern.get("detail_intents", [])]

    condition_type = normalized.get("condition_type", "")
    interface_cond = normalized.get("interface_condition", "")
    system_type = normalized.get("system_type", "")
    method_pref = normalized.get("method_preference", "")

    # Name/description matching — check both exact and word-level
    if condition_type:
        ct_words = set(condition_type.replace("_", " ").split())
        if condition_type in pat_name or condition_type.replace("_", " ") in pat_name:
            score += 0.2
        elif ct_words and ct_words.issubset(set(pat_text.split())):
            score += 0.15

    # Interface condition matching — word-level
    if interface_cond:
        ic_lower = interface_cond.lower()
        ic_words = set(ic_lower.replace("_", " ").split())
        if ic_lower in pat_text or ic_lower.replace("_", " ") in pat_text:
            score += 0.3
        elif ic_words and ic_words.issubset(set(pat_text.split())):
            score += 0.2

    # System type matching
    if system_type:
        st_lower = system_type.lower()
        st_words = set(st_lower.replace("_", " ").split())
        if st_lower in pat_desc:
            score += 0.1
        elif st_words.intersection(set(pat_text.split())):
            score += 0.05

    # Method preference matching — check pattern text and variant method hints
    if method_pref:
        mp_lower = method_pref.lower()
        if mp_lower in pat_name or mp_lower in pat_desc:
            score += 0.2
        for di in detail_intents:
            if mp_lower in di:
                score += 0.1
                break

    # Material preference matching — word-level
    mat_prefs = normalized.get("material_preferences", [])
    if mat_prefs:
        for mp in mat_prefs:
            mp_words = set(mp.split())
            if mp in pat_desc:
                score += 0.1
                break
            elif mp_words.intersection(set(pat_desc.split())):
                score += 0.05
                break

    return score


def _fail(code, stage, message, details=None, candidates=None):
    reason = {"code": code, "stage": stage, "message": message}
    if details:
        reason["details"] = details
    result = {"matched": False, "fail_reason": reason}
    if candidates is not None:
        result["candidates"] = candidates
    return result
