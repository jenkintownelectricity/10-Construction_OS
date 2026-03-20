"""
Tests for mirror_activation_gate.py — MirrorActivationGate with FAIL-CLOSED semantics.

The activation gate MUST be fail-closed: if ANY check fails, activation is DENIED.
"""

from __future__ import annotations

import unittest
from typing import Any

from runtime.mirror_control.mirror_activation_gate import (
    ActivationCheck,
    ActivationResult,
    ActivationVerdict,
    MirrorActivationGate,
)


def _make_valid_inputs() -> dict[str, Any]:
    """Return a complete set of inputs that should pass all gate checks."""
    return {
        "mirror_id": "mirror-test",
        "manifest": {
            "mirror_id": "mirror-test",
            "version": "1.0.0",
            "slices": ["slice-a", "slice-b"],
            "trust_boundary": "boundary-alpha",
        },
        "enabled_slices": ["slice-a", "slice-b"],
        "declared_slices": ["slice-a", "slice-b", "slice-c"],
        "dependency_graph": {
            "nodes": ["slice-a", "slice-b", "slice-c"],
            "edges": {"slice-a": ["slice-b"], "slice-b": [], "slice-c": []},
        },
        "trust_boundary": "boundary-alpha",
        "reflection_statuses": {
            "ref-1": "active",
            "ref-2": "staged",
        },
        "parity_fixtures": [
            {"fixture_id": "f-1", "name": "test"},
        ],
        "drift_record_schema": {"type": "object"},
        "breakaway_conditions": [
            {"condition_id": "c-1", "name": "No shared state"},
        ],
        "truth_ownership": "source-prime",
        "mirror_source_code": [
            "def compute(x): return x * 2",
            "class Handler: pass",
        ],
        "lifecycle_state": "active",
        "lifecycle_evidence": {
            "state": "active",
            "parity_verified": True,
        },
        "registry_entry": {
            "mirror_id": "mirror-test",
            "registered_at": "2025-01-01T00:00:00Z",
        },
    }


class TestActivationCheck(unittest.TestCase):
    """Tests for the ActivationCheck dataclass."""

    def test_check_to_dict(self) -> None:
        check = ActivationCheck(
            check_id="test-check",
            rule_number=1,
            name="Test Check",
            passed=True,
            details="All good",
        )
        d = check.to_dict()
        self.assertEqual(d["check_id"], "test-check")
        self.assertTrue(d["passed"])


class TestActivationResult(unittest.TestCase):
    """Tests for the ActivationResult dataclass."""

    def test_result_properties(self) -> None:
        checks = [
            ActivationCheck("c1", 1, "Check 1", True),
            ActivationCheck("c2", 2, "Check 2", False, details="Failed"),
        ]
        result = ActivationResult(
            mirror_id="m-1",
            verdict=ActivationVerdict.DENY,
            checks=checks,
        )
        self.assertFalse(result.passed)
        self.assertEqual(len(result.failed_checks), 1)
        self.assertEqual(len(result.passed_checks), 1)
        self.assertTrue(result.fail_closed)

    def test_result_to_dict(self) -> None:
        result = ActivationResult(
            mirror_id="m-1",
            verdict=ActivationVerdict.ALLOW,
            checks=[ActivationCheck("c1", 1, "Check 1", True)],
            summary="All passed",
        )
        d = result.to_dict()
        self.assertEqual(d["verdict"], "allow")
        self.assertEqual(d["passed_count"], 1)
        self.assertEqual(d["failed_count"], 0)


class TestMirrorActivationGate(unittest.TestCase):
    """Tests for the MirrorActivationGate class -- FAIL-CLOSED semantics."""

    def setUp(self) -> None:
        self.gate = MirrorActivationGate()

    # ---- FAIL-CLOSED: all checks pass -> ALLOW ----

    def test_all_checks_pass_allows_activation(self) -> None:
        inputs = _make_valid_inputs()
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.ALLOW)
        self.assertTrue(result.passed)
        self.assertEqual(len(result.failed_checks), 0)

    # ---- FAIL-CLOSED: each individual check failure -> DENY ----

    def test_deny_when_manifest_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["manifest"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_manifest_incomplete(self) -> None:
        inputs = _make_valid_inputs()
        inputs["manifest"] = {"mirror_id": "m-1"}
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_manifest_slices_not_list(self) -> None:
        inputs = _make_valid_inputs()
        inputs["manifest"]["slices"] = "not-a-list"
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_enabled_slices_not_declared(self) -> None:
        inputs = _make_valid_inputs()
        inputs["enabled_slices"] = ["slice-a", "slice-undeclared"]
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_enabled_slices_none(self) -> None:
        inputs = _make_valid_inputs()
        inputs["enabled_slices"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_dependency_graph_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["dependency_graph"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_dependency_graph_has_cycle(self) -> None:
        inputs = _make_valid_inputs()
        inputs["dependency_graph"] = {
            "nodes": ["a", "b", "c"],
            "edges": {"a": ["b"], "b": ["c"], "c": ["a"]},
        }
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_trust_boundary_undefined(self) -> None:
        inputs = _make_valid_inputs()
        inputs["trust_boundary"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_trust_boundary_empty(self) -> None:
        inputs = _make_valid_inputs()
        inputs["trust_boundary"] = ""
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_reflection_statuses_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["reflection_statuses"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_reflection_statuses_empty(self) -> None:
        inputs = _make_valid_inputs()
        inputs["reflection_statuses"] = {}
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_reflection_statuses_invalid(self) -> None:
        inputs = _make_valid_inputs()
        inputs["reflection_statuses"] = {"ref-1": "bogus_status"}
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_parity_fixtures_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["parity_fixtures"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_parity_fixtures_empty(self) -> None:
        inputs = _make_valid_inputs()
        inputs["parity_fixtures"] = []
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_drift_schema_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["drift_record_schema"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_breakaway_conditions_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["breakaway_conditions"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_breakaway_conditions_empty(self) -> None:
        inputs = _make_valid_inputs()
        inputs["breakaway_conditions"] = []
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_truth_ownership_undefined(self) -> None:
        inputs = _make_valid_inputs()
        inputs["truth_ownership"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_forbidden_patterns_found(self) -> None:
        inputs = _make_valid_inputs()
        inputs["mirror_source_code"] = [
            "from app import config",
            "flask.Flask(__name__)",
        ]
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_source_code_not_provided(self) -> None:
        inputs = _make_valid_inputs()
        inputs["mirror_source_code"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_lifecycle_state_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["lifecycle_state"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_lifecycle_evidence_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["lifecycle_evidence"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_lifecycle_state_invalid(self) -> None:
        inputs = _make_valid_inputs()
        inputs["lifecycle_state"] = "invalid_state"
        inputs["lifecycle_evidence"] = {"state": "invalid_state"}
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_lifecycle_inconsistent(self) -> None:
        inputs = _make_valid_inputs()
        inputs["lifecycle_state"] = "active"
        inputs["lifecycle_evidence"] = {"state": "frozen"}
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_active_without_parity_evidence(self) -> None:
        inputs = _make_valid_inputs()
        inputs["lifecycle_state"] = "active"
        inputs["lifecycle_evidence"] = {"state": "active", "parity_verified": False}
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_registry_entry_missing(self) -> None:
        inputs = _make_valid_inputs()
        inputs["registry_entry"] = None
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_registry_entry_empty(self) -> None:
        inputs = _make_valid_inputs()
        inputs["registry_entry"] = {}
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    def test_deny_when_registry_entry_incomplete(self) -> None:
        inputs = _make_valid_inputs()
        inputs["registry_entry"] = {"mirror_id": "m-1"}
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(result.verdict, ActivationVerdict.DENY)

    # ---- FAIL-CLOSED: default (no args) -> DENY ----

    def test_deny_on_empty_evaluation(self) -> None:
        """With no arguments provided, all checks fail and gate denies."""
        result = self.gate.evaluate_activation(mirror_id="empty-mirror")
        self.assertEqual(result.verdict, ActivationVerdict.DENY)
        self.assertGreater(len(result.failed_checks), 0)

    # ---- Individual check methods ----

    def test_check_manifest_valid(self) -> None:
        check = self.gate.check_manifest({
            "mirror_id": "m-1",
            "version": "1.0",
            "slices": ["a"],
            "trust_boundary": "tb",
        })
        self.assertTrue(check.passed)

    def test_check_manifest_none(self) -> None:
        check = self.gate.check_manifest(None)
        self.assertFalse(check.passed)

    def test_check_trust_boundary_valid(self) -> None:
        check = self.gate.check_trust_boundary("boundary-1")
        self.assertTrue(check.passed)

    def test_check_trust_boundary_none(self) -> None:
        check = self.gate.check_trust_boundary(None)
        self.assertFalse(check.passed)

    def test_check_reflection_statuses_valid(self) -> None:
        check = self.gate.check_reflection_statuses({"r1": "active", "r2": "frozen"})
        self.assertTrue(check.passed)

    def test_check_reflection_statuses_invalid_value(self) -> None:
        check = self.gate.check_reflection_statuses({"r1": "exploded"})
        self.assertFalse(check.passed)

    def test_check_fixtures_valid(self) -> None:
        check = self.gate.check_fixtures([{"fixture_id": "f-1"}])
        self.assertTrue(check.passed)

    def test_check_fixtures_empty(self) -> None:
        check = self.gate.check_fixtures([])
        self.assertFalse(check.passed)

    def test_check_forbidden_patterns_clean(self) -> None:
        check = self.gate.check_forbidden_patterns(["def foo(): return 1"])
        self.assertTrue(check.passed)

    def test_check_forbidden_patterns_dirty(self) -> None:
        check = self.gate.check_forbidden_patterns(["import app"])
        self.assertFalse(check.passed)

    def test_check_forbidden_patterns_localhost(self) -> None:
        check = self.gate.check_forbidden_patterns(["url = 'localhost:8080'"])
        self.assertFalse(check.passed)

    def test_check_registry_entry_valid(self) -> None:
        check = self.gate.check_registry_entry({
            "mirror_id": "m-1",
            "registered_at": "2025-01-01T00:00:00Z",
        })
        self.assertTrue(check.passed)

    def test_check_slice_validity_valid(self) -> None:
        check = self.gate.check_slice_validity({
            "nodes": ["a", "b"],
            "edges": {"a": ["b"], "b": []},
        })
        self.assertTrue(check.passed)

    def test_check_slice_validity_missing_fields(self) -> None:
        check = self.gate.check_slice_validity({"nodes": ["a"]})
        self.assertFalse(check.passed)

    def test_check_parity_baseline_valid(self) -> None:
        check = self.gate.check_parity_baseline({"type": "object"})
        self.assertTrue(check.passed)

    def test_check_parity_baseline_empty(self) -> None:
        check = self.gate.check_parity_baseline({})
        self.assertFalse(check.passed)

    # ---- Summary content ----

    def test_allow_summary_contains_mirror_id(self) -> None:
        inputs = _make_valid_inputs()
        result = self.gate.evaluate_activation(**inputs)
        self.assertIn("mirror-test", result.summary)

    def test_deny_summary_lists_failed_checks(self) -> None:
        result = self.gate.evaluate_activation(mirror_id="m-denied")
        self.assertIn("DENIED", result.summary)

    # ---- Verify 12 checks always run ----

    def test_always_runs_12_checks(self) -> None:
        inputs = _make_valid_inputs()
        result = self.gate.evaluate_activation(**inputs)
        self.assertEqual(len(result.checks), 12)

    def test_always_runs_12_checks_even_on_empty(self) -> None:
        result = self.gate.evaluate_activation(mirror_id="empty")
        self.assertEqual(len(result.checks), 12)


if __name__ == "__main__":
    unittest.main()
