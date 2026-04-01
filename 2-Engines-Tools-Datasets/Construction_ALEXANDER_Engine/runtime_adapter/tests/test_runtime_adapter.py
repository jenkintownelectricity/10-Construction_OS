"""Tests for the Alexander Runtime Adapter.

Cases:
- valid_condition_resolves
- invalid_condition_signature
- invalid_resolution_result
- missing_kernel_reference
- fail_closed_on_engine_error

All tests use mock engine/kernel to isolate adapter behavior
from the full ALEXANDER pipeline.
"""

import unittest
from datetime import datetime, timezone
from typing import Any

from runtime_adapter.alexander_runtime_adapter import AlexanderRuntimeAdapter
from runtime_adapter.runtime_resolution_types import (
    RESOLUTION_RESULT_SCHEMA_VERSION,
    RESOLUTION_STAGES_REQUIRED,
)
from runtime_adapter.runtime_resolution_validator import (
    validate_condition_signature,
    validate_resolution_result,
)


# ============================================================
# Test fixtures
# ============================================================

def _make_valid_condition() -> dict[str, Any]:
    """Create a valid ConditionSignature dict matching the authoritative schema."""
    return {
        "condition_id": "COND-TEST-001",
        "schema_version": "1.0.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "condition_type": "roof_edge",
        "location_context": {
            "zone_id": "ZONE-A1",
            "interface_condition": "roof_to_wall",
        },
    }


def _make_valid_resolution_result(condition_id: str = "COND-TEST-001") -> dict[str, Any]:
    """Create a valid ResolutionResult dict matching the authoritative schema."""
    stages = {}
    for stage_name in RESOLUTION_STAGES_REQUIRED:
        stages[stage_name] = {"status": "PASS"}

    return {
        "result_id": "RES-test0001",
        "schema_version": RESOLUTION_RESULT_SCHEMA_VERSION,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "condition_id": condition_id,
        "status": "RESOLVED",
        "pattern_family_id": "FAM-ROOF-EDGE",
        "pattern_id": "PAT-ROOF-EDGE-001",
        "variant_id": "VAR-ROOF-EDGE-001-A",
        "artifact_intent_id": "ART-ROOF-EDGE-001",
        "fail_reasons": [],
        "conflicts": [],
        "constraint_violations": [],
        "score": {
            "total_score": 0.95,
            "breakdown": {
                "family_confidence": 0.98,
                "pattern_fit": 0.95,
                "variant_match": 0.92,
                "constraint_compliance": 1.0,
                "conflict_free": 1.0,
            },
        },
        "resolution_stages": stages,
        "correlation_refs": [],
        "source_repo": "Construction_ALEXANDER_Engine",
    }


class MockEngine:
    """Mock engine that returns a configurable resolution result."""

    def __init__(self, result: dict[str, Any] | None = None, error: Exception | None = None):
        self._result = result
        self._error = error
        self.last_condition = None
        self.last_kernel = None

    def resolve(self, condition: dict[str, Any], kernel: Any) -> dict[str, Any]:
        self.last_condition = condition
        self.last_kernel = kernel
        if self._error is not None:
            raise self._error
        if self._result is not None:
            return self._result
        return _make_valid_resolution_result(condition.get("condition_id", "unknown"))


class MockKernel:
    """Mock kernel placeholder."""
    pass


# ============================================================
# Test: Input validation (standalone)
# ============================================================

class TestConditionSignatureValidation(unittest.TestCase):

    def test_valid_condition_has_no_errors(self):
        errors = validate_condition_signature(_make_valid_condition())
        self.assertEqual(errors, [])

    def test_non_dict_input_fails(self):
        errors = validate_condition_signature("not a dict")
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "INVALID_INPUT_TYPE")

    def test_missing_required_fields(self):
        errors = validate_condition_signature({})
        codes = [e.code for e in errors]
        self.assertTrue(all(c == "MISSING_REQUIRED_FIELD" for c in codes))
        missing_fields = {e.details.get("field") for e in errors}
        self.assertIn("condition_id", missing_fields)
        self.assertIn("condition_type", missing_fields)
        self.assertIn("location_context", missing_fields)

    def test_invalid_condition_type_enum(self):
        cond = _make_valid_condition()
        cond["condition_type"] = "invalid_type"
        errors = validate_condition_signature(cond)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "INVALID_ENUM_VALUE")

    def test_empty_condition_id_fails(self):
        cond = _make_valid_condition()
        cond["condition_id"] = ""
        errors = validate_condition_signature(cond)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "INVALID_FIELD_VALUE")

    def test_bad_schema_version_format(self):
        cond = _make_valid_condition()
        cond["schema_version"] = "v1"
        errors = validate_condition_signature(cond)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "INVALID_FIELD_VALUE")

    def test_missing_zone_id(self):
        cond = _make_valid_condition()
        cond["location_context"] = {}
        errors = validate_condition_signature(cond)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "MISSING_REQUIRED_FIELD")
        self.assertIn("zone_id", errors[0].message)

    def test_invalid_interface_condition(self):
        cond = _make_valid_condition()
        cond["location_context"]["interface_condition"] = "nonexistent"
        errors = validate_condition_signature(cond)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "INVALID_ENUM_VALUE")


# ============================================================
# Test: Output validation (standalone)
# ============================================================

class TestResolutionResultValidation(unittest.TestCase):

    def test_valid_result_has_no_errors(self):
        errors = validate_resolution_result(_make_valid_resolution_result())
        self.assertEqual(errors, [])

    def test_non_dict_output_fails(self):
        errors = validate_resolution_result(42)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "INVALID_OUTPUT_TYPE")

    def test_wrong_schema_version_fails(self):
        result = _make_valid_resolution_result()
        result["schema_version"] = "2.0.0"
        errors = validate_resolution_result(result)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "SCHEMA_VERSION_MISMATCH")

    def test_invalid_status_enum(self):
        result = _make_valid_resolution_result()
        result["status"] = "UNKNOWN_STATUS"
        errors = validate_resolution_result(result)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "INVALID_ENUM_VALUE")

    def test_missing_resolution_stages(self):
        result = _make_valid_resolution_result()
        del result["resolution_stages"]
        errors = validate_resolution_result(result)
        missing_fields = {e.details.get("field") for e in errors}
        self.assertIn("resolution_stages", missing_fields)

    def test_wrong_source_repo_fails(self):
        result = _make_valid_resolution_result()
        result["source_repo"] = "SomeOtherEngine"
        errors = validate_resolution_result(result)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "INVALID_SOURCE_REPO")


# ============================================================
# Test: Adapter end-to-end
# ============================================================

class TestAlexanderRuntimeAdapter(unittest.TestCase):

    def test_valid_condition_resolves(self):
        """Happy path: valid condition → engine resolves → valid output returned."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)

        condition = _make_valid_condition()
        result = adapter.resolve_condition(condition)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.resolution_result)
        self.assertEqual(result.adapter_errors, [])
        self.assertEqual(result.resolution_result["status"], "RESOLVED")
        self.assertEqual(result.resolution_result["condition_id"], condition["condition_id"])
        # Verify engine received the condition and kernel
        self.assertEqual(engine.last_condition, condition)
        self.assertIs(engine.last_kernel, kernel)

    def test_invalid_condition_signature(self):
        """Invalid input → adapter rejects before engine invocation."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)

        bad_condition = {"condition_type": "nonexistent_type"}
        result = adapter.resolve_condition(bad_condition)

        self.assertFalse(result.success)
        self.assertIsNone(result.resolution_result)
        self.assertTrue(len(result.adapter_errors) > 0)
        # Engine should NOT have been called
        self.assertIsNone(engine.last_condition)

    def test_invalid_resolution_result(self):
        """Engine returns malformed output → adapter rejects."""
        bad_result = {"status": "INVALID", "schema_version": "9.9.9"}
        engine = MockEngine(result=bad_result)
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)

        condition = _make_valid_condition()
        result = adapter.resolve_condition(condition)

        self.assertFalse(result.success)
        self.assertIsNone(result.resolution_result)
        self.assertTrue(len(result.adapter_errors) > 0)
        error_codes = {e.code for e in result.adapter_errors}
        self.assertTrue(
            error_codes & {"SCHEMA_VERSION_MISMATCH", "INVALID_ENUM_VALUE", "MISSING_REQUIRED_FIELD"}
        )

    def test_missing_kernel_reference(self):
        """Engine returns result with missing condition_id → adapter catches."""
        result_missing_cid = _make_valid_resolution_result()
        del result_missing_cid["condition_id"]
        engine = MockEngine(result=result_missing_cid)
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)

        condition = _make_valid_condition()
        result = adapter.resolve_condition(condition)

        self.assertFalse(result.success)
        self.assertIsNone(result.resolution_result)
        missing_fields = {e.details.get("field") for e in result.adapter_errors}
        self.assertIn("condition_id", missing_fields)

    def test_fail_closed_on_engine_error(self):
        """Engine raises exception → adapter returns structured error."""
        engine = MockEngine(error=RuntimeError("kernel corrupted"))
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)

        condition = _make_valid_condition()
        result = adapter.resolve_condition(condition)

        self.assertFalse(result.success)
        self.assertIsNone(result.resolution_result)
        self.assertEqual(len(result.adapter_errors), 1)
        self.assertEqual(result.adapter_errors[0].code, "ENGINE_INVOCATION_FAILED")
        self.assertIn("kernel corrupted", result.adapter_errors[0].message)


if __name__ == "__main__":
    unittest.main()
