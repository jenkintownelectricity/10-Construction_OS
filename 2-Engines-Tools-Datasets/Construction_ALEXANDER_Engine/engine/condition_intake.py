"""
Condition Intake Module.

Validates ConditionSignature shape before any processing.
Fail-closed: rejects invalid, incomplete, or malformed conditions.
"""

from engine.config import (
    VALID_CONDITION_TYPES,
    FAIL_INVALID_CONDITION,
    FAIL_MISSING_REQUIRED_FIELD,
    FAIL_UNKNOWN_CONDITION_TYPE,
)

REQUIRED_FIELDS = [
    "condition_id",
    "schema_version",
    "timestamp_utc",
    "condition_type",
    "location_context",
]

REQUIRED_LOCATION_FIELDS = ["zone_id"]


def validate_condition_signature(condition: dict) -> dict:
    """
    Validate a ConditionSignature dict.

    Returns:
        {"valid": True, "condition": condition} on success
        {"valid": False, "fail_reason": {...}} on failure
    """
    if not isinstance(condition, dict):
        return _fail(
            FAIL_INVALID_CONDITION,
            "intake",
            "ConditionSignature must be a dict",
        )

    # Check required top-level fields
    for field in REQUIRED_FIELDS:
        if field not in condition or condition[field] is None:
            return _fail(
                FAIL_MISSING_REQUIRED_FIELD,
                "intake",
                f"Missing required field: {field}",
                {"field": field},
            )
        if isinstance(condition[field], str) and not condition[field].strip():
            return _fail(
                FAIL_MISSING_REQUIRED_FIELD,
                "intake",
                f"Empty required field: {field}",
                {"field": field},
            )

    # Validate condition_type
    if condition["condition_type"] not in VALID_CONDITION_TYPES:
        return _fail(
            FAIL_UNKNOWN_CONDITION_TYPE,
            "intake",
            f"Unknown condition_type: {condition['condition_type']}",
            {"condition_type": condition["condition_type"],
             "valid_types": sorted(VALID_CONDITION_TYPES)},
        )

    # Validate location_context
    loc = condition["location_context"]
    if not isinstance(loc, dict):
        return _fail(
            FAIL_INVALID_CONDITION,
            "intake",
            "location_context must be a dict",
        )
    for field in REQUIRED_LOCATION_FIELDS:
        if field not in loc or not loc[field]:
            return _fail(
                FAIL_MISSING_REQUIRED_FIELD,
                "intake",
                f"Missing required location field: {field}",
                {"field": f"location_context.{field}"},
            )

    # Validate schema_version format
    sv = condition["schema_version"]
    if not isinstance(sv, str):
        return _fail(
            FAIL_INVALID_CONDITION,
            "intake",
            "schema_version must be a string",
        )

    # Validate condition_id is non-empty string
    cid = condition["condition_id"]
    if not isinstance(cid, str) or not cid.strip():
        return _fail(
            FAIL_INVALID_CONDITION,
            "intake",
            "condition_id must be a non-empty string",
        )

    return {"valid": True, "condition": condition}


def _fail(code: str, stage: str, message: str, details: dict = None) -> dict:
    reason = {"code": code, "stage": stage, "message": message}
    if details:
        reason["details"] = details
    return {"valid": False, "fail_reason": reason}
