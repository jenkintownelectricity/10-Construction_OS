"""
Scoring Engine Module.

Produces machine-readable score breakdowns for resolution results.
Deterministic scoring based on classification confidence, fit metrics,
constraint compliance, and conflict status.
"""

from engine.config import FAIL_SCORING_FAILURE


def score_resolution(
    family_result: dict,
    pattern_result: dict,
    variant_result: dict,
    constraint_result: dict,
    conflict_result: dict,
) -> dict:
    """
    Score the overall resolution quality.

    Returns:
        {"scored": True, "score": {"total_score": float, "breakdown": {...}}}
        {"scored": False, "fail_reason": {...}, "score": None}
    """
    try:
        breakdown = {}

        # Family confidence
        breakdown["family_confidence"] = family_result.get("confidence", 0.0) if family_result.get("matched") else 0.0

        # Pattern fit
        breakdown["pattern_fit"] = pattern_result.get("confidence", 0.0) if pattern_result.get("matched") else 0.0

        # Variant match
        breakdown["variant_match"] = variant_result.get("confidence", 0.0) if variant_result.get("matched") else 0.0

        # Constraint compliance (1.0 if passed, 0.0 if violations)
        if constraint_result.get("passed"):
            breakdown["constraint_compliance"] = 1.0
        else:
            violation_count = len(constraint_result.get("violations", []))
            breakdown["constraint_compliance"] = max(0.0, 1.0 - (violation_count * 0.25))

        # Conflict free (1.0 if no conflicts, reduced by severity)
        if not conflict_result.get("has_conflicts"):
            breakdown["conflict_free"] = 1.0
        else:
            conflicts = conflict_result.get("conflicts", [])
            critical_count = sum(1 for c in conflicts if c.get("severity") == "critical")
            warning_count = sum(1 for c in conflicts if c.get("severity") != "critical")
            breakdown["conflict_free"] = max(
                0.0,
                1.0 - (critical_count * 0.5) - (warning_count * 0.2),
            )

        # Total score is weighted average
        weights = {
            "family_confidence": 0.15,
            "pattern_fit": 0.25,
            "variant_match": 0.25,
            "constraint_compliance": 0.20,
            "conflict_free": 0.15,
        }
        total = sum(breakdown[k] * weights[k] for k in weights)
        total = round(min(max(total, 0.0), 1.0), 4)

        return {
            "scored": True,
            "score": {
                "total_score": total,
                "breakdown": breakdown,
            },
        }

    except Exception as e:
        return {
            "scored": False,
            "fail_reason": {
                "code": FAIL_SCORING_FAILURE,
                "stage": "scoring",
                "message": f"Scoring failed: {str(e)}",
            },
            "score": None,
        }
