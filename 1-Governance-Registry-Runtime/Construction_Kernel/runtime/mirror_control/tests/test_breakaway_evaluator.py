"""
Tests for breakaway_evaluator.py — BreakawayCondition, BreakawayRecord, BreakawayEvaluator.
"""

from __future__ import annotations

import unittest

from runtime.mirror_control.breakaway_evaluator import (
    BreakawayCondition,
    BreakawayEvaluator,
    BreakawayRecord,
    BreakawayVerdict,
)


class TestBreakawayCondition(unittest.TestCase):
    """Tests for the BreakawayCondition dataclass."""

    def test_condition_creation(self) -> None:
        cond = BreakawayCondition(
            condition_id="c-001",
            name="Test Condition",
            description="A test condition",
            required=True,
        )
        self.assertFalse(cond.met)
        self.assertEqual(cond.details, "")

    def test_condition_to_dict_roundtrip(self) -> None:
        cond = BreakawayCondition(
            condition_id="c-002",
            name="Roundtrip",
            description="Test roundtrip",
            check_fn_name="check_roundtrip",
            required=False,
            met=True,
            details="All good",
        )
        d = cond.to_dict()
        restored = BreakawayCondition.from_dict(d)
        self.assertEqual(restored.condition_id, "c-002")
        self.assertTrue(restored.met)
        self.assertFalse(restored.required)


class TestBreakawayRecord(unittest.TestCase):
    """Tests for the BreakawayRecord dataclass."""

    def test_record_creation(self) -> None:
        record = BreakawayRecord(
            record_id="breakaway-aabbccddee11",
            mirror_id="mirror-x",
            source_id="source-y",
            verdict=BreakawayVerdict.APPROVED,
            non_destructive=True,
        )
        self.assertNotEqual(record.evaluated_at, "")
        self.assertEqual(record.verdict, BreakawayVerdict.APPROVED)

    def test_record_to_dict_roundtrip(self) -> None:
        cond = BreakawayCondition(
            condition_id="c-1",
            name="Cond 1",
            description="desc",
            met=True,
        )
        record = BreakawayRecord(
            record_id="breakaway-112233445566",
            mirror_id="m1",
            source_id="s1",
            verdict=BreakawayVerdict.DENIED,
            conditions=[cond],
            non_destructive=False,
            notes="Blocked",
        )
        d = record.to_dict()
        restored = BreakawayRecord.from_dict(d)
        self.assertEqual(restored.verdict, BreakawayVerdict.DENIED)
        self.assertEqual(len(restored.conditions), 1)
        self.assertEqual(restored.notes, "Blocked")


class TestBreakawayEvaluator(unittest.TestCase):
    """Tests for the BreakawayEvaluator class."""

    def setUp(self) -> None:
        self.evaluator = BreakawayEvaluator(
            mirror_id="mirror-alpha",
            source_id="source-prime",
        )

    def test_standard_conditions_loaded(self) -> None:
        self.assertGreater(len(self.evaluator.conditions), 0)
        ids = {c.condition_id for c in self.evaluator.conditions}
        self.assertIn("no-shared-state", ids)
        self.assertIn("no-source-callbacks", ids)
        self.assertIn("clean-interface-boundary", ids)

    def test_set_condition_met(self) -> None:
        result = self.evaluator.set_condition_met(
            "no-shared-state", True, "Verified no shared state"
        )
        self.assertTrue(result)
        cond = [c for c in self.evaluator.conditions if c.condition_id == "no-shared-state"][0]
        self.assertTrue(cond.met)

    def test_set_condition_met_not_found(self) -> None:
        result = self.evaluator.set_condition_met("nonexistent", True)
        self.assertFalse(result)

    def test_check_conditions_partition(self) -> None:
        self.evaluator.set_condition_met("no-shared-state", True)
        met, unmet = self.evaluator.check_conditions()
        met_ids = {c.condition_id for c in met}
        self.assertIn("no-shared-state", met_ids)
        self.assertGreater(len(unmet), 0)

    def test_add_custom_condition(self) -> None:
        custom = BreakawayCondition(
            condition_id="custom-1",
            name="Custom Check",
            description="A custom check",
            required=True,
        )
        self.evaluator.add_condition(custom)
        ids = {c.condition_id for c in self.evaluator.conditions}
        self.assertIn("custom-1", ids)

    def test_verify_non_destructive_clean(self) -> None:
        is_safe, issues = self.evaluator.verify_non_destructive()
        self.assertTrue(is_safe)
        self.assertEqual(len(issues), 0)

    def test_verify_non_destructive_writes_to_source(self) -> None:
        is_safe, issues = self.evaluator.verify_non_destructive(
            mirror_writes_to_source=True,
        )
        self.assertFalse(is_safe)
        self.assertGreater(len(issues), 0)

    def test_verify_non_destructive_shared_resources(self) -> None:
        is_safe, issues = self.evaluator.verify_non_destructive(
            shared_resources=["shared_db", "shared_cache"],
        )
        self.assertFalse(is_safe)

    def test_verify_non_destructive_source_depends_on_mirror(self) -> None:
        is_safe, issues = self.evaluator.verify_non_destructive(
            source_dependencies=["mirror-alpha-handler", "other-dep"],
        )
        self.assertFalse(is_safe)

    def test_generate_breakaway_plan_not_feasible(self) -> None:
        plan = self.evaluator.generate_breakaway_plan()
        self.assertFalse(plan["feasible"])
        self.assertGreater(len(plan["blocking_conditions"]), 0)

    def test_generate_breakaway_plan_feasible(self) -> None:
        for cond in self.evaluator.conditions:
            if cond.required:
                cond.met = True
        plan = self.evaluator.generate_breakaway_plan()
        self.assertTrue(plan["feasible"])
        self.assertEqual(len(plan["blocking_conditions"]), 0)

    def test_evaluate_breakaway_denied_conditions_unmet(self) -> None:
        record = self.evaluator.evaluate_breakaway()
        self.assertEqual(record.verdict, BreakawayVerdict.DENIED)
        self.assertIn("denied", record.notes.lower())

    def test_evaluate_breakaway_denied_destructive(self) -> None:
        for cond in self.evaluator.conditions:
            cond.met = True
        record = self.evaluator.evaluate_breakaway(
            mirror_writes_to_source=True,
        )
        self.assertEqual(record.verdict, BreakawayVerdict.DENIED)
        self.assertFalse(record.non_destructive)

    def test_evaluate_breakaway_conditional(self) -> None:
        for cond in self.evaluator.conditions:
            if cond.required:
                cond.met = True
        # Leave optional conditions unmet
        record = self.evaluator.evaluate_breakaway()
        self.assertEqual(record.verdict, BreakawayVerdict.CONDITIONAL)

    def test_evaluate_breakaway_approved(self) -> None:
        for cond in self.evaluator.conditions:
            cond.met = True
        record = self.evaluator.evaluate_breakaway()
        self.assertEqual(record.verdict, BreakawayVerdict.APPROVED)
        self.assertTrue(record.non_destructive)

    def test_records_accumulated(self) -> None:
        self.evaluator.evaluate_breakaway()
        self.evaluator.evaluate_breakaway()
        self.assertEqual(len(self.evaluator.records), 2)


if __name__ == "__main__":
    unittest.main()
