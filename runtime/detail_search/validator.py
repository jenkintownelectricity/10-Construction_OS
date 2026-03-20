"""
Detail Search Validator — Wave 15.

Validates search results for determinism and correctness.
"""

from typing import Any


class DetailSearchValidationError(Exception):
    """Raised when search validation fails."""


def validate_search_result(result: dict[str, Any]) -> dict[str, Any]:
    """Validate a search result for structural correctness."""
    checks: list[dict[str, Any]] = []

    # Check 1: Required keys
    required = {"results", "query", "search_type", "tier", "total_results", "deterministic"}
    missing = required - set(result.keys())
    checks.append({
        "check": "structure_completeness",
        "passed": len(missing) == 0,
        "detail": f"Missing: {sorted(missing)}" if missing else "Complete.",
    })

    # Check 2: Count consistency
    count_ok = len(result.get("results", [])) == result.get("total_results", -1)
    checks.append({
        "check": "count_consistency",
        "passed": count_ok,
        "detail": "Count matches." if count_ok else "Count mismatch.",
    })

    # Check 3: Tier 0 is deterministic
    if result.get("tier") == 0:
        checks.append({
            "check": "tier0_deterministic",
            "passed": result.get("deterministic") is True,
            "detail": "Tier 0 marked deterministic." if result.get("deterministic") else "Tier 0 not deterministic.",
        })

    # Check 4: No duplicate detail_ids
    ids = [r["detail_id"] for r in result.get("results", []) if "detail_id" in r]
    has_dupes = len(ids) != len(set(ids))
    checks.append({
        "check": "no_duplicates",
        "passed": not has_dupes,
        "detail": "No duplicates." if not has_dupes else "Duplicate detail_ids found.",
    })

    all_passed = all(c["passed"] for c in checks)
    return {
        "subsystem": "detail_search",
        "wave": "15",
        "status": "PASS" if all_passed else "FAIL",
        "checks": checks,
    }
