"""Tests for QAEngine — Wave 8A structural validation.

Validates that the QA engine can be instantiated and exposes detection
methods for all 7 issue classes.
"""

import pytest

from runtime.qa.qa_engine import QAEngine


# ---------------------------------------------------------------------------
# QAEngine instantiation
# ---------------------------------------------------------------------------

class TestQAEngineInstantiation:
    """Verify QAEngine can be created with a contract_loader."""

    def test_instantiate_with_contract_loader(self):
        engine = QAEngine(contract_loader="mock_loader")
        assert engine is not None
        assert engine._contract_loader == "mock_loader"

    def test_instantiate_without_args(self):
        engine = QAEngine()
        assert engine is not None

    def test_instantiate_with_config(self):
        engine = QAEngine(config={"strict": True})
        assert engine._config == {"strict": True}


# ---------------------------------------------------------------------------
# 7 issue class detection methods
# ---------------------------------------------------------------------------

ISSUE_CLASS_METHODS = [
    "detect_missing_details",
    "detect_incompatible_materials",
    "detect_unresolved_interfaces",
    "detect_scope_conflicts",
    "detect_parameter_gaps",
    "detect_missing_ownership",
    "detect_readiness_blockers",
]


class TestQAEngineDetectionMethods:
    """Verify QAEngine has detection methods for all 7 issue classes."""

    @pytest.mark.parametrize("method_name", ISSUE_CLASS_METHODS)
    def test_detection_method_exists(self, method_name):
        engine = QAEngine()
        assert hasattr(engine, method_name), f"QAEngine missing method: {method_name}"

    @pytest.mark.parametrize("method_name", ISSUE_CLASS_METHODS)
    def test_detection_method_is_callable(self, method_name):
        engine = QAEngine()
        method = getattr(engine, method_name)
        assert callable(method), f"QAEngine.{method_name} is not callable"

    def test_all_seven_methods_present(self):
        engine = QAEngine()
        for method_name in ISSUE_CLASS_METHODS:
            assert hasattr(engine, method_name), f"Missing: {method_name}"
        assert len(ISSUE_CLASS_METHODS) == 7, "Expected exactly 7 issue classes"

    def test_run_checks_method_exists(self):
        engine = QAEngine()
        assert callable(getattr(engine, "run_checks", None))
