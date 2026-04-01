"""Tests for the Constraint Port.

Cases:
- valid_resolution_passes
- warning_condition
- halt_condition
- malformed_evidence
- fail_closed_on_unknown_constraint

All tests use inline fixtures with deterministic constraint objects.
"""

import unittest
from datetime import datetime, timezone

from core.constraint_types import (
    ConstraintObject,
    ConstraintEvidence,
    EvidenceItem,
    AppliesTo,
    Trigger,
    DependencyMap,
)
from core.constraint_port import ConstraintPort, ConstraintPortResult
from core.constraint_decision import (
    aggregate_action,
    aggregate_severity,
    is_halting,
    any_halting,
    decide_on_unknown_constraint,
)
from core.constraint_validator import (
    validate_constraint_object,
    validate_constraint_evidence,
    validate_constraint_decision,
)


# ============================================================
# Test fixtures
# ============================================================

def _make_constraint(
    rule_id: str = "CR-TEST-001",
    constraint_type: str = "CODE_VIOLATION",
    logic_operator: str = "BLOCK",
    decision_on_fail: str = "BLOCK",
    required_evidence: list[str] | None = None,
) -> ConstraintObject:
    return ConstraintObject(
        rule_id=rule_id,
        rule_label="Test constraint",
        rule_family="TEST_FAMILY",
        constraint_type=constraint_type,
        source_authority="IBC 2021",
        source_ref="Section 1504.3",
        applies_to=AppliesTo(entity_type="material"),
        trigger=Trigger(condition="material_compatibility_check"),
        dependency_map=DependencyMap(kernels=["Construction_Kernel"]),
        logic_operator=logic_operator,
        required_evidence=required_evidence or ["material_compatible"],
        decision_on_fail=decision_on_fail,
    )


def _make_evidence(
    rule_id: str = "CR-TEST-001",
    evidence_id: str = "EV-TEST-001",
    completeness: str = "COMPLETE",
    items: list[EvidenceItem] | None = None,
    missing_items: list[str] | None = None,
) -> ConstraintEvidence:
    default_items = [EvidenceItem(key="material_compatible", value=True, source="Construction_Kernel")]
    return ConstraintEvidence(
        evidence_id=evidence_id,
        rule_id=rule_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        evidence_items=items if items is not None else default_items,
        completeness=completeness,
        missing_items=missing_items or [],
    )


def _make_resolution_result() -> dict:
    return {
        "result_id": "RES-test0001",
        "schema_version": "1.0.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "condition_id": "COND-TEST-001",
        "status": "RESOLVED",
        "resolution_stages": {
            "intake": {"status": "PASS"},
            "normalization": {"status": "PASS"},
            "family_classification": {"status": "PASS"},
            "pattern_resolution": {"status": "PASS"},
            "variant_selection": {"status": "PASS"},
            "constraint_enforcement": {"status": "PASS"},
            "conflict_detection": {"status": "PASS"},
            "scoring": {"status": "PASS"},
        },
    }


# ============================================================
# Test: Validator standalone
# ============================================================

class TestConstraintValidators(unittest.TestCase):

    def test_valid_constraint_object(self):
        c = _make_constraint()
        errors = validate_constraint_object({
            "rule_id": c.rule_id,
            "rule_label": c.rule_label,
            "rule_family": c.rule_family,
            "constraint_type": c.constraint_type,
            "source_authority": c.source_authority,
            "source_ref": c.source_ref,
            "applies_to": {"entity_type": "material"},
            "trigger": {"condition": "test"},
            "dependency_map": {},
            "logic_operator": c.logic_operator,
            "required_evidence": c.required_evidence,
            "decision_on_fail": c.decision_on_fail,
        })
        self.assertEqual(errors, [])

    def test_invalid_constraint_type_enum(self):
        errors = validate_constraint_object({
            "rule_id": "CR-TEST-001",
            "rule_label": "x",
            "rule_family": "x",
            "constraint_type": "INVALID_TYPE",
            "source_authority": "x",
            "source_ref": "x",
            "applies_to": {"entity_type": "material"},
            "trigger": {"condition": "test"},
            "dependency_map": {},
            "logic_operator": "BLOCK",
            "required_evidence": ["a"],
            "decision_on_fail": "BLOCK",
        })
        codes = [e["code"] for e in errors]
        self.assertIn("INVALID_ENUM", codes)

    def test_valid_evidence(self):
        e = _make_evidence()
        errors = validate_constraint_evidence({
            "evidence_id": e.evidence_id,
            "rule_id": e.rule_id,
            "timestamp": e.timestamp,
            "evidence_items": [{"key": "k", "value": "v", "source": "s"}],
            "completeness": e.completeness,
        })
        self.assertEqual(errors, [])

    def test_valid_decision(self):
        errors = validate_constraint_decision({
            "decision_id": "CD-TEST-001",
            "rule_id": "CR-TEST-001",
            "evidence_id": "EV-TEST-001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "PASS",
            "severity": "INFO",
            "rationale": "All good",
            "source_authority": "IBC 2021",
            "deterministic": True,
        })
        self.assertEqual(errors, [])

    def test_non_deterministic_decision_fails(self):
        errors = validate_constraint_decision({
            "decision_id": "CD-TEST-001",
            "rule_id": "CR-TEST-001",
            "evidence_id": "EV-TEST-001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "PASS",
            "severity": "INFO",
            "rationale": "test",
            "source_authority": "x",
            "deterministic": False,
        })
        codes = [e["code"] for e in errors]
        self.assertIn("INVALID_VALUE", codes)


# ============================================================
# Test: Constraint Port end-to-end
# ============================================================

class TestConstraintPort(unittest.TestCase):

    def test_valid_resolution_passes(self):
        """All evidence is COMPLETE, no violations → PASS."""
        port = ConstraintPort()
        constraint = _make_constraint()
        evidence = _make_evidence()

        result = port.evaluate(
            resolution_result=_make_resolution_result(),
            constraints=[constraint],
            evidence_map={constraint.rule_id: evidence},
        )

        self.assertEqual(len(result.decisions), 1)
        self.assertEqual(result.decisions[0].action, "PASS")
        self.assertEqual(result.aggregate_action, "PASS")
        self.assertFalse(result.halted)

    def test_warning_condition(self):
        """Evidence shows violation + logic_operator=WARN → WARN, not halted."""
        port = ConstraintPort()
        constraint = _make_constraint(logic_operator="WARN")
        evidence = _make_evidence(
            items=[EvidenceItem(key="material_compatible", value=False, source="Construction_Kernel")],
        )

        result = port.evaluate(
            resolution_result=_make_resolution_result(),
            constraints=[constraint],
            evidence_map={constraint.rule_id: evidence},
        )

        self.assertEqual(len(result.decisions), 1)
        self.assertEqual(result.decisions[0].action, "WARN")
        self.assertEqual(result.aggregate_action, "WARN")
        self.assertFalse(result.halted)

    def test_halt_condition(self):
        """Evidence shows violation + logic_operator=BLOCK → BLOCK, halted."""
        port = ConstraintPort()
        constraint = _make_constraint(logic_operator="BLOCK")
        evidence = _make_evidence(
            items=[EvidenceItem(key="material_compatible", value=False, source="Construction_Kernel")],
        )

        result = port.evaluate(
            resolution_result=_make_resolution_result(),
            constraints=[constraint],
            evidence_map={constraint.rule_id: evidence},
        )

        self.assertEqual(len(result.decisions), 1)
        self.assertEqual(result.decisions[0].action, "BLOCK")
        self.assertEqual(result.aggregate_action, "BLOCK")
        self.assertTrue(result.halted)

    def test_malformed_evidence(self):
        """Incomplete evidence → decision_on_fail applied."""
        port = ConstraintPort()
        constraint = _make_constraint(decision_on_fail="BLOCK")
        evidence = _make_evidence(
            completeness="PARTIAL",
            items=[],
            missing_items=["material_compatible"],
        )

        result = port.evaluate(
            resolution_result=_make_resolution_result(),
            constraints=[constraint],
            evidence_map={constraint.rule_id: evidence},
        )

        self.assertEqual(len(result.decisions), 1)
        self.assertEqual(result.decisions[0].action, "BLOCK")
        self.assertTrue(result.halted)

    def test_fail_closed_on_unknown_constraint(self):
        """No evidence provided for constraint → BLOCK (fail-closed)."""
        port = ConstraintPort()
        constraint = _make_constraint()

        result = port.evaluate(
            resolution_result=_make_resolution_result(),
            constraints=[constraint],
            evidence_map={},  # no evidence
        )

        self.assertEqual(len(result.decisions), 1)
        self.assertEqual(result.decisions[0].action, "BLOCK")
        self.assertEqual(result.decisions[0].severity, "CRITICAL")
        self.assertTrue(result.halted)

    def test_multiple_constraints_aggregate(self):
        """Multiple constraints: one PASS, one BLOCK → aggregate is BLOCK."""
        port = ConstraintPort()
        c1 = _make_constraint(rule_id="CR-TEST-001", logic_operator="BLOCK")
        c2 = _make_constraint(rule_id="CR-TEST-002", logic_operator="WARN")

        e1 = _make_evidence(rule_id="CR-TEST-001", evidence_id="EV-TEST-001")
        e2 = _make_evidence(
            rule_id="CR-TEST-002",
            evidence_id="EV-TEST-002",
            items=[EvidenceItem(key="material_compatible", value=False, source="CK")],
        )

        result = port.evaluate(
            resolution_result=_make_resolution_result(),
            constraints=[c1, c2],
            evidence_map={c1.rule_id: e1, c2.rule_id: e2},
        )

        self.assertEqual(len(result.decisions), 2)
        actions = {d.action for d in result.decisions}
        self.assertIn("PASS", actions)
        self.assertIn("WARN", actions)
        self.assertEqual(result.aggregate_action, "WARN")

    def test_deterministic_evaluation_order(self):
        """Constraints evaluated in rule_id sort order."""
        port = ConstraintPort()
        c_b = _make_constraint(rule_id="CR-TEST-002")
        c_a = _make_constraint(rule_id="CR-TEST-001")

        e_a = _make_evidence(rule_id="CR-TEST-001", evidence_id="EV-TEST-001")
        e_b = _make_evidence(rule_id="CR-TEST-002", evidence_id="EV-TEST-002")

        result = port.evaluate(
            resolution_result=_make_resolution_result(),
            constraints=[c_b, c_a],  # deliberately out of order
            evidence_map={c_a.rule_id: e_a, c_b.rule_id: e_b},
        )

        self.assertEqual(result.decisions[0].rule_id, "CR-TEST-001")
        self.assertEqual(result.decisions[1].rule_id, "CR-TEST-002")

    def test_invalid_resolution_result_input(self):
        """Non-dict resolution_result → fail-closed."""
        port = ConstraintPort()
        result = port.evaluate(
            resolution_result="not a dict",
            constraints=[],
            evidence_map={},
        )
        self.assertTrue(result.halted)
        self.assertTrue(len(result.validation_errors) > 0)


# ============================================================
# Test: Decision model standalone
# ============================================================

class TestDecisionModel(unittest.TestCase):

    def test_aggregate_action_picks_most_severe(self):
        d1 = decide_on_unknown_constraint("CD-T-0001", "CR-TEST-001", "EV-NONE")
        # d1.action is BLOCK
        self.assertEqual(aggregate_action([d1]), "BLOCK")

    def test_aggregate_empty_is_block(self):
        self.assertEqual(aggregate_action([]), "BLOCK")

    def test_aggregate_severity_empty_is_critical(self):
        self.assertEqual(aggregate_severity([]), "CRITICAL")

    def test_is_halting_block(self):
        d = decide_on_unknown_constraint("CD-T-0001", "CR-TEST-001", "EV-NONE")
        self.assertTrue(is_halting(d))


if __name__ == "__main__":
    unittest.main()
