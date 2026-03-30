"""
Scan Validation — Wave 14 Subsystem 5.

Validates field scan outputs for contract compliance.
Ensures advisory_only flag is always set.
Ensures no scanner output can mutate kernel truth.
"""

from typing import Any

VALID_DETECTION_STATUSES = frozenset(["DETECTED", "UNKNOWN"])


def validate_scan_result(result: dict[str, Any]) -> list[str]:
    """
    Validate a field scan result for contract compliance.
    Returns list of validation errors. Empty means valid.
    """
    errors: list[str] = []

    # Advisory-only must be true
    if result.get("advisory_only") is not True:
        errors.append("advisory_only must be true. Scanner output cannot be kernel truth.")

    # Required fields
    for field in ("evidence_refs", "confidence"):
        if field not in result:
            errors.append(f"Missing required field: {field}")

    # Confidence must be numeric and in range
    confidence = result.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)):
            errors.append("confidence must be numeric.")
        elif confidence < 0 or confidence > 1:
            errors.append(f"confidence {confidence} outside valid range [0, 1].")

    # Evidence refs must be present
    evidence_refs = result.get("evidence_refs", [])
    if not isinstance(evidence_refs, list) or len(evidence_refs) == 0:
        errors.append("evidence_refs must be a non-empty list.")

    # Detection status if present
    status = result.get("detection_status")
    if status and status not in VALID_DETECTION_STATUSES:
        errors.append(f"Invalid detection_status: '{status}'. Must be one of {sorted(VALID_DETECTION_STATUSES)}.")

    return errors


def validate_scan_batch(results: list[dict[str, Any]]) -> list[str]:
    """Validate a batch of scan results."""
    errors: list[str] = []
    for i, result in enumerate(results):
        result_errors = validate_scan_result(result)
        for err in result_errors:
            errors.append(f"Scan result {i}: {err}")
    return errors
