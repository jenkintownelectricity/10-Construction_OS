"""
Tests for drift_recorder.py — DriftRecord, DriftSeverity, and DriftRecorder.
"""

from __future__ import annotations

import unittest

from runtime.mirror_control.drift_recorder import (
    DriftRecord,
    DriftRecorder,
    DriftSeverity,
)


class TestDriftSeverity(unittest.TestCase):
    """Tests for the DriftSeverity enum."""

    def test_severity_values(self) -> None:
        self.assertEqual(DriftSeverity.LOW.value, "low")
        self.assertEqual(DriftSeverity.MEDIUM.value, "medium")
        self.assertEqual(DriftSeverity.HIGH.value, "high")
        self.assertEqual(DriftSeverity.CRITICAL.value, "critical")


class TestDriftRecord(unittest.TestCase):
    """Tests for the DriftRecord dataclass."""

    def test_record_creation(self) -> None:
        record = DriftRecord(
            record_id="drift-abcdef123456",
            mirror_id="mirror-alpha",
            source_id="source-prime",
            severity=DriftSeverity.LOW,
            category="schema",
            description="Field type changed",
        )
        self.assertEqual(record.mirror_id, "mirror-alpha")
        self.assertFalse(record.resolved)
        self.assertIsNone(record.resolved_at)
        self.assertNotEqual(record.recorded_at, "")

    def test_record_to_dict_roundtrip(self) -> None:
        record = DriftRecord(
            record_id="drift-000000000001",
            mirror_id="m1",
            source_id="s1",
            severity=DriftSeverity.HIGH,
            category="behavior",
            description="Output mismatch",
            deviation=0.45,
            source_value={"x": 1},
            mirror_value={"x": 2},
            fixture_id="f-100",
        )
        d = record.to_dict()
        restored = DriftRecord.from_dict(d)
        self.assertEqual(restored.record_id, record.record_id)
        self.assertEqual(restored.severity, DriftSeverity.HIGH)
        self.assertEqual(restored.deviation, 0.45)
        self.assertEqual(restored.fixture_id, "f-100")


class TestDriftRecorder(unittest.TestCase):
    """Tests for the DriftRecorder class."""

    def setUp(self) -> None:
        self.recorder = DriftRecorder(
            mirror_id="mirror-test",
            drift_threshold=3,
            max_deviation_threshold=0.7,
        )

    def test_mirror_id(self) -> None:
        self.assertEqual(self.recorder.mirror_id, "mirror-test")

    def test_record_drift_auto_severity(self) -> None:
        record = self.recorder.record_drift(
            source_id="src",
            category="output",
            description="Small difference",
            deviation=0.05,
        )
        self.assertEqual(record.severity, DriftSeverity.LOW)

    def test_record_drift_explicit_severity(self) -> None:
        record = self.recorder.record_drift(
            source_id="src",
            category="schema",
            description="Forced critical",
            severity=DriftSeverity.CRITICAL,
            deviation=0.01,
        )
        self.assertEqual(record.severity, DriftSeverity.CRITICAL)

    def test_assess_severity_thresholds(self) -> None:
        self.assertEqual(self.recorder.assess_severity(0.0), DriftSeverity.LOW)
        self.assertEqual(self.recorder.assess_severity(0.1), DriftSeverity.LOW)
        self.assertEqual(self.recorder.assess_severity(0.2), DriftSeverity.MEDIUM)
        self.assertEqual(self.recorder.assess_severity(0.3), DriftSeverity.MEDIUM)
        self.assertEqual(self.recorder.assess_severity(0.5), DriftSeverity.HIGH)
        self.assertEqual(self.recorder.assess_severity(0.6), DriftSeverity.HIGH)
        self.assertEqual(self.recorder.assess_severity(0.9), DriftSeverity.CRITICAL)

    def test_get_drift_history_no_filter(self) -> None:
        self.recorder.record_drift("s1", "output", "d1", deviation=0.1)
        self.recorder.record_drift("s1", "schema", "d2", deviation=0.5)
        history = self.recorder.get_drift_history()
        self.assertEqual(len(history), 2)

    def test_get_drift_history_filter_category(self) -> None:
        self.recorder.record_drift("s1", "output", "d1", deviation=0.1)
        self.recorder.record_drift("s1", "schema", "d2", deviation=0.5)
        history = self.recorder.get_drift_history(category="schema")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].category, "schema")

    def test_get_drift_history_filter_severity(self) -> None:
        self.recorder.record_drift("s1", "output", "low", deviation=0.05)
        self.recorder.record_drift("s1", "output", "high", deviation=0.5)
        history = self.recorder.get_drift_history(severity=DriftSeverity.HIGH)
        self.assertEqual(len(history), 1)

    def test_get_drift_history_unresolved_only(self) -> None:
        r1 = self.recorder.record_drift("s1", "output", "d1", deviation=0.1)
        self.recorder.record_drift("s1", "output", "d2", deviation=0.2)
        self.recorder.resolve_drift(r1.record_id)
        history = self.recorder.get_drift_history(unresolved_only=True)
        self.assertEqual(len(history), 1)

    def test_get_drift_history_limit(self) -> None:
        for i in range(10):
            self.recorder.record_drift("s1", "output", f"d{i}", deviation=0.1)
        history = self.recorder.get_drift_history(limit=3)
        self.assertEqual(len(history), 3)

    def test_check_drift_threshold_within(self) -> None:
        self.recorder.record_drift("s1", "output", "low drift", deviation=0.05)
        within, explanation = self.recorder.check_drift_threshold()
        self.assertTrue(within)

    def test_check_drift_threshold_breached_by_count(self) -> None:
        for i in range(5):
            self.recorder.record_drift(
                "s1", "output", f"high-{i}", deviation=0.5,
            )
        within, explanation = self.recorder.check_drift_threshold()
        self.assertFalse(within)
        self.assertIn("threshold breached", explanation.lower())

    def test_check_drift_threshold_breached_by_deviation(self) -> None:
        self.recorder.record_drift(
            "s1", "output", "extreme", deviation=0.95,
        )
        within, explanation = self.recorder.check_drift_threshold()
        self.assertFalse(within)
        self.assertIn("deviation threshold breached", explanation.lower())

    def test_resolve_drift(self) -> None:
        record = self.recorder.record_drift("s1", "output", "resolve me", deviation=0.1)
        result = self.recorder.resolve_drift(record.record_id)
        self.assertTrue(result)
        self.assertTrue(record.resolved)
        self.assertIsNotNone(record.resolved_at)

    def test_resolve_drift_not_found(self) -> None:
        result = self.recorder.resolve_drift("nonexistent-id")
        self.assertFalse(result)

    def test_get_summary(self) -> None:
        self.recorder.record_drift("s1", "output", "d1", deviation=0.05)
        self.recorder.record_drift("s1", "output", "d2", deviation=0.5)
        summary = self.recorder.get_summary()
        self.assertEqual(summary["mirror_id"], "mirror-test")
        self.assertEqual(summary["total_records"], 2)
        self.assertEqual(summary["unresolved"], 2)
        self.assertIn("by_severity", summary)

    def test_clear(self) -> None:
        self.recorder.record_drift("s1", "output", "d1", deviation=0.1)
        self.recorder.clear()
        self.assertEqual(len(self.recorder.records), 0)


if __name__ == "__main__":
    unittest.main()
