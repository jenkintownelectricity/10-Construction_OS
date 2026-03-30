"""Unit tests for condition intake validation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.condition_intake import validate_condition_signature


def _valid_condition():
    return {
        "condition_id": "COND-001",
        "schema_version": "1.0.0",
        "timestamp_utc": "2026-03-22T12:00:00Z",
        "condition_type": "roof_edge",
        "location_context": {
            "zone_id": "zone-A1",
        },
    }


def test_valid_condition_passes():
    result = validate_condition_signature(_valid_condition())
    assert result["valid"] is True
    assert result["condition"] == _valid_condition()


def test_non_dict_fails():
    result = validate_condition_signature("not a dict")
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "INVALID_CONDITION"


def test_missing_condition_id_fails():
    c = _valid_condition()
    del c["condition_id"]
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "MISSING_REQUIRED_FIELD"


def test_missing_schema_version_fails():
    c = _valid_condition()
    del c["schema_version"]
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "MISSING_REQUIRED_FIELD"


def test_missing_timestamp_fails():
    c = _valid_condition()
    del c["timestamp_utc"]
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "MISSING_REQUIRED_FIELD"


def test_missing_condition_type_fails():
    c = _valid_condition()
    del c["condition_type"]
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "MISSING_REQUIRED_FIELD"


def test_missing_location_context_fails():
    c = _valid_condition()
    del c["location_context"]
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "MISSING_REQUIRED_FIELD"


def test_unknown_condition_type_fails():
    c = _valid_condition()
    c["condition_type"] = "unknown_type"
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "UNKNOWN_CONDITION_TYPE"


def test_missing_zone_id_fails():
    c = _valid_condition()
    c["location_context"] = {}
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "MISSING_REQUIRED_FIELD"


def test_empty_condition_id_fails():
    c = _valid_condition()
    c["condition_id"] = "   "
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "MISSING_REQUIRED_FIELD"


def test_location_context_not_dict_fails():
    c = _valid_condition()
    c["location_context"] = "not a dict"
    result = validate_condition_signature(c)
    assert result["valid"] is False
    assert result["fail_reason"]["code"] == "INVALID_CONDITION"


def test_all_valid_condition_types():
    valid_types = ["roof_edge", "parapet", "drain", "penetration", "expansion_joint", "interface", "transition"]
    for ct in valid_types:
        c = _valid_condition()
        c["condition_type"] = ct
        result = validate_condition_signature(c)
        assert result["valid"] is True, f"Expected valid for type '{ct}'"
