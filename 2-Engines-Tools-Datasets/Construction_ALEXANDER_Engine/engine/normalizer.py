"""
Condition Normalizer Module.

Deterministic normalization of validated ConditionSignature into
a canonical internal form for downstream processing.
"""


def normalize_condition(condition: dict) -> dict:
    """
    Normalize a validated ConditionSignature into canonical form.

    Deterministic: same input always produces same output.

    Returns:
        {"valid": True, "normalized": {...}} on success
        {"valid": False, "fail_reason": {...}} on failure
    """
    try:
        normalized = {
            "condition_id": condition["condition_id"].strip(),
            "condition_type": condition["condition_type"].strip().lower(),
            "schema_version": condition["schema_version"].strip(),
            "timestamp_utc": condition["timestamp_utc"].strip(),
            "zone_id": condition["location_context"]["zone_id"].strip(),
            "spatial_object_id": _get_str(condition, "location_context", "spatial_object_id"),
            "interface_condition": _get_str(condition, "location_context", "interface_condition"),
            "adjacencies": _get_list(condition, "location_context", "adjacencies"),
            "dimensions": _normalize_dimensions(condition.get("dimensions")),
            "system_type": _strip_or_none(condition.get("system_type")),
            "material_preferences": _normalize_string_list(condition.get("material_preferences")),
            "method_preference": _strip_or_none(condition.get("method_preference")),
            "manufacturer_refs": _normalize_string_list(condition.get("manufacturer_refs")),
            "climate_context": _normalize_climate(condition.get("climate_context")),
            "code_requirements": condition.get("code_requirements", []),
            "correlation_refs": condition.get("correlation_refs", []),
        }
        return {"valid": True, "normalized": normalized}
    except Exception as e:
        return {
            "valid": False,
            "fail_reason": {
                "code": "INVALID_CONDITION",
                "stage": "normalization",
                "message": f"Normalization failed: {str(e)}",
            },
        }


def _get_str(d: dict, *keys: str) -> str | None:
    """Navigate nested dict and return stripped string or None."""
    current = d
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    if isinstance(current, str):
        s = current.strip()
        return s if s else None
    return None


def _get_list(d: dict, *keys: str) -> list:
    """Navigate nested dict and return list or empty list."""
    current = d
    for key in keys:
        if not isinstance(current, dict):
            return []
        current = current.get(key)
    return list(current) if isinstance(current, list) else []


def _strip_or_none(val) -> str | None:
    if isinstance(val, str):
        s = val.strip()
        return s if s else None
    return None


def _normalize_string_list(val) -> list:
    if not isinstance(val, list):
        return []
    return [s.strip().lower() for s in val if isinstance(s, str) and s.strip()]


def _normalize_dimensions(dims) -> dict:
    if not isinstance(dims, dict):
        return {}
    result = {}
    for key, val in dims.items():
        if isinstance(val, (int, float)):
            result[key] = float(val)
    return result


def _normalize_climate(climate) -> dict:
    if not isinstance(climate, dict):
        return {}
    result = {}
    if "wind_zone" in climate and isinstance(climate["wind_zone"], int):
        result["wind_zone"] = climate["wind_zone"]
    if "moisture_exposure" in climate and isinstance(climate["moisture_exposure"], str):
        result["moisture_exposure"] = climate["moisture_exposure"].strip().lower()
    if "climate_zone" in climate and isinstance(climate["climate_zone"], str):
        result["climate_zone"] = climate["climate_zone"].strip()
    if "freeze_thaw" in climate and isinstance(climate["freeze_thaw"], bool):
        result["freeze_thaw"] = climate["freeze_thaw"]
    return result
