"""End-to-end integration tests for the Governed Pipeline.

Cases:
- end_to_end_valid_condition: full chain → APPROVED
- end_to_end_halt_condition: constraint BLOCK → BLOCKED
- end_to_end_invalid_signature: bad input → FAILED
- application_consumer_receives_governed_result_only
- receipt and signal generation

These tests wire Wave 3 (RuntimeAdapter) + Wave 4 (ConstraintPort) +
Wave 5 (GovernedResult) with mock engine/kernel/provider.
"""

import unittest
from datetime import datetime, timezone
from typing import Any

from runtime_adapter.alexander_runtime_adapter import AlexanderRuntimeAdapter
from runtime_adapter.runtime_resolution_types import (
    RESOLUTION_RESULT_SCHEMA_VERSION,
    RESOLUTION_STAGES_REQUIRED,
    RuntimeAdapterResult,
)

from core.constraint_types import (
    ConstraintObject,
    ConstraintEvidence,
    EvidenceItem,
    AppliesTo,
    Trigger,
    DependencyMap,
)
from core.constraint_port import ConstraintPort

from governed_result.governed_result_types import (
    GovernedResult,
    GOVERNED_STATUSES,
)
from governed_result.governed_pipeline import GovernedPipeline, GovernedPipelineOutput
from governed_result.governed_result_transformer import transform
from governed_result.governed_result_receipt import generate_receipt, generate_signal


# ============================================================
# Mock fixtures
# ============================================================

def _make_valid_condition() -> dict[str, Any]:
    return {
        "condition_id": "COND-INT-001",
        "schema_version": "1.0.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "condition_type": "roof_edge",
        "location_context": {
            "zone_id": "ZONE-INT-A1",
            "interface_condition": "roof_to_wall",
        },
    }


def _make_valid_resolution_result(condition_id: str = "COND-INT-001") -> dict[str, Any]:
    stages = {}
    for stage_name in RESOLUTION_STAGES_REQUIRED:
        stages[stage_name] = {"status": "PASS"}
    return {
        "result_id": "RES-int0001",
        "schema_version": RESOLUTION_RESULT_SCHEMA_VERSION,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "condition_id": condition_id,
        "status": "RESOLVED",
        "pattern_family_id": "FAM-ROOF-EDGE",
        "pattern_id": "PAT-ROOF-EDGE-001",
        "variant_id": "VAR-ROOF-EDGE-001-A",
        "artifact_intent_id": None,
        "fail_reasons": [],
        "conflicts": [],
        "constraint_violations": [],
        "score": {"total_score": 0.95, "breakdown": {
            "family_confidence": 0.98, "pattern_fit": 0.95,
            "variant_match": 0.92, "constraint_compliance": 1.0,
            "conflict_free": 1.0,
        }},
        "resolution_stages": stages,
        "correlation_refs": [],
        "source_repo": "Construction_ALEXANDER_Engine",
    }


class MockEngine:
    def __init__(self, result=None, error=None):
        self._result = result
        self._error = error

    def resolve(self, condition, kernel):
        if self._error:
            raise self._error
        if self._result:
            return self._result
        return _make_valid_resolution_result(condition.get("condition_id", "unknown"))


class MockKernel:
    pass


def _make_constraint_pass() -> ConstraintObject:
    return ConstraintObject(
        rule_id="CR-INT-001",
        rule_label="Integration test constraint",
        rule_family="TEST_FAMILY",
        constraint_type="CODE_VIOLATION",
        source_authority="IBC 2021",
        source_ref="Section 1504.3",
        applies_to=AppliesTo(entity_type="material"),
        trigger=Trigger(condition="material_compatibility_check"),
        dependency_map=DependencyMap(kernels=["Construction_Kernel"]),
        logic_operator="BLOCK",
        required_evidence=["material_compatible"],
        decision_on_fail="BLOCK",
    )


def _make_evidence_pass(rule_id="CR-INT-001") -> ConstraintEvidence:
    return ConstraintEvidence(
        evidence_id="EV-INT-001",
        rule_id=rule_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        evidence_items=[EvidenceItem(key="material_compatible", value=True, source="CK")],
        completeness="COMPLETE",
    )


def _make_evidence_fail(rule_id="CR-INT-001") -> ConstraintEvidence:
    return ConstraintEvidence(
        evidence_id="EV-INT-002",
        rule_id=rule_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        evidence_items=[EvidenceItem(key="material_compatible", value=False, source="CK")],
        completeness="COMPLETE",
    )


class MockConstraintProvider:
    def __init__(self, constraints, evidence_map):
        self._constraints = constraints
        self._evidence_map = evidence_map

    def get_constraints(self, resolution_result):
        return self._constraints, self._evidence_map


# ============================================================
# Integration tests
# ============================================================

class TestGovernedPipelineIntegration(unittest.TestCase):

    def test_end_to_end_valid_condition(self):
        """Full chain: valid condition → resolved → constraints pass → APPROVED."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)
        port = ConstraintPort()

        constraint = _make_constraint_pass()
        evidence = _make_evidence_pass()
        provider = MockConstraintProvider(
            constraints=[constraint],
            evidence_map={constraint.rule_id: evidence},
        )

        pipeline = GovernedPipeline(
            runtime_adapter=adapter,
            constraint_port=port,
            constraint_provider=provider,
        )

        output = pipeline.resolve_governed(_make_valid_condition())

        self.assertIsInstance(output, GovernedPipelineOutput)
        self.assertIsInstance(output.governed_result, GovernedResult)
        self.assertEqual(output.governed_result.status, "APPROVED")
        self.assertIsNotNone(output.governed_result.resolution_summary)
        self.assertIsNotNone(output.governed_result.constraint_summary)
        self.assertFalse(output.governed_result.constraint_summary.halted)
        self.assertEqual(output.governed_result.errors, [])

    def test_end_to_end_halt_condition(self):
        """Full chain: valid condition → resolved → constraint BLOCKS → BLOCKED."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)
        port = ConstraintPort()

        constraint = _make_constraint_pass()
        evidence = _make_evidence_fail()  # violation
        provider = MockConstraintProvider(
            constraints=[constraint],
            evidence_map={constraint.rule_id: evidence},
        )

        pipeline = GovernedPipeline(
            runtime_adapter=adapter,
            constraint_port=port,
            constraint_provider=provider,
        )

        output = pipeline.resolve_governed(_make_valid_condition())

        self.assertEqual(output.governed_result.status, "BLOCKED")
        self.assertTrue(output.governed_result.constraint_summary.halted)
        self.assertIn("CR-INT-001", output.governed_result.constraint_summary.blocking_rules)

    def test_end_to_end_invalid_signature(self):
        """Bad input → adapter rejects → FAILED GovernedResult."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)
        port = ConstraintPort()

        pipeline = GovernedPipeline(
            runtime_adapter=adapter,
            constraint_port=port,
        )

        bad_condition = {"condition_type": "nonexistent"}
        output = pipeline.resolve_governed(bad_condition)

        self.assertEqual(output.governed_result.status, "FAILED")
        self.assertTrue(len(output.governed_result.errors) > 0)

    def test_application_consumer_receives_governed_result_only(self):
        """Application consumer only sees GovernedResult — no engine internals."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)
        port = ConstraintPort()

        pipeline = GovernedPipeline(
            runtime_adapter=adapter,
            constraint_port=port,
        )

        output = pipeline.resolve_governed(_make_valid_condition())

        # GovernedResult is the only output type
        gr = output.governed_result
        self.assertIsInstance(gr, GovernedResult)

        # No engine internals exposed
        self.assertFalse(hasattr(gr, "resolution_pipeline"))
        self.assertFalse(hasattr(gr, "engine"))
        self.assertFalse(hasattr(gr, "kernel"))

        # Status is a governed status, not an engine status
        self.assertIn(gr.status, GOVERNED_STATUSES)

        # Source chain is present
        self.assertIn("Construction_ALEXANDER_Engine", gr.source_chain)
        self.assertIn("Constraint_Port", gr.source_chain)
        self.assertIn("Governed_Result_Surface", gr.source_chain)

    def test_receipt_generation(self):
        """GovernedResult produces a valid receipt."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)
        port = ConstraintPort()

        pipeline = GovernedPipeline(
            runtime_adapter=adapter,
            constraint_port=port,
        )

        output = pipeline.resolve_governed(_make_valid_condition())

        receipt = output.receipt
        self.assertEqual(receipt["receipt_type"], "governed_result")
        self.assertEqual(receipt["receipt_version"], "1.0.0")
        self.assertEqual(receipt["governed_result_id"], output.governed_result.governed_result_id)
        self.assertEqual(receipt["status"], output.governed_result.status)
        self.assertIn("source_chain", receipt)

    def test_signal_generation(self):
        """GovernedResult produces a valid signal."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)
        port = ConstraintPort()

        pipeline = GovernedPipeline(
            runtime_adapter=adapter,
            constraint_port=port,
        )

        output = pipeline.resolve_governed(_make_valid_condition())

        signal = output.signal
        self.assertEqual(signal["signal_type"], "governed_result_ready")
        self.assertEqual(signal["governed_result_id"], output.governed_result.governed_result_id)
        self.assertEqual(signal["status"], output.governed_result.status)

    def test_no_constraint_provider_still_produces_result(self):
        """Without constraint provider, result based on resolution alone."""
        engine = MockEngine()
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)
        port = ConstraintPort()

        pipeline = GovernedPipeline(
            runtime_adapter=adapter,
            constraint_port=port,
            constraint_provider=None,
        )

        output = pipeline.resolve_governed(_make_valid_condition())

        self.assertEqual(output.governed_result.status, "APPROVED")
        self.assertIsNone(output.governed_result.constraint_summary)

    def test_engine_error_produces_failed_result(self):
        """Engine exception → FAILED GovernedResult."""
        engine = MockEngine(error=RuntimeError("engine crash"))
        kernel = MockKernel()
        adapter = AlexanderRuntimeAdapter(engine=engine, kernel=kernel)
        port = ConstraintPort()

        pipeline = GovernedPipeline(
            runtime_adapter=adapter,
            constraint_port=port,
        )

        output = pipeline.resolve_governed(_make_valid_condition())

        self.assertEqual(output.governed_result.status, "FAILED")
        self.assertTrue(len(output.governed_result.errors) > 0)


# ============================================================
# Transformer standalone tests
# ============================================================

class TestGovernedResultTransformer(unittest.TestCase):

    def test_invalid_adapter_result_produces_failed(self):
        result = transform(adapter_result="not valid")
        self.assertEqual(result.status, "FAILED")

    def test_failed_adapter_produces_failed(self):
        adapter_result = RuntimeAdapterResult(
            success=False,
            resolution_result=None,
            adapter_errors=[],
        )
        result = transform(adapter_result=adapter_result)
        self.assertEqual(result.status, "FAILED")


if __name__ == "__main__":
    unittest.main()
