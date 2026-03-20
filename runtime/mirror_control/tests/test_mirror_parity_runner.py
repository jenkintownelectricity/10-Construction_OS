"""
Tests for parity_runner.py — ParityFixture, ParityResult, and ParityRunner.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from typing import Any

from runtime.mirror_control.parity_runner import (
    ParityFixture,
    ParityOutcome,
    ParityResult,
    ParityRunner,
)


class TestParityFixture(unittest.TestCase):
    """Tests for the ParityFixture dataclass."""

    def test_fixture_creation_with_defaults(self) -> None:
        fixture = ParityFixture(
            fixture_id="f-001",
            name="Basic fixture",
            source_input={"x": 1},
            expected_output={"y": 2},
        )
        self.assertEqual(fixture.fixture_id, "f-001")
        self.assertEqual(fixture.tolerance, 0.0)
        self.assertEqual(fixture.tags, [])
        self.assertNotEqual(fixture.created_at, "")

    def test_fixture_fingerprint_deterministic(self) -> None:
        fixture = ParityFixture(
            fixture_id="f-002",
            name="Fingerprint test",
            source_input={"a": 1, "b": 2},
            expected_output={"c": 3},
        )
        fp1 = fixture.fingerprint()
        fp2 = fixture.fingerprint()
        self.assertEqual(fp1, fp2)
        self.assertEqual(len(fp1), 16)

    def test_fixture_fingerprint_differs_on_content_change(self) -> None:
        f1 = ParityFixture(
            fixture_id="f-003",
            name="A",
            source_input={"x": 1},
            expected_output={"y": 2},
        )
        f2 = ParityFixture(
            fixture_id="f-003",
            name="A",
            source_input={"x": 999},
            expected_output={"y": 2},
        )
        self.assertNotEqual(f1.fingerprint(), f2.fingerprint())

    def test_fixture_to_dict_roundtrip(self) -> None:
        fixture = ParityFixture(
            fixture_id="f-004",
            name="Roundtrip",
            source_input={"data": [1, 2, 3]},
            expected_output={"result": "ok"},
            tolerance=0.05,
            tags=["smoke"],
        )
        d = fixture.to_dict()
        restored = ParityFixture.from_dict(d)
        self.assertEqual(restored.fixture_id, fixture.fixture_id)
        self.assertEqual(restored.source_input, fixture.source_input)
        self.assertEqual(restored.expected_output, fixture.expected_output)
        self.assertEqual(restored.tolerance, fixture.tolerance)
        self.assertEqual(restored.tags, fixture.tags)


class TestParityResult(unittest.TestCase):
    """Tests for the ParityResult dataclass."""

    def test_result_creation(self) -> None:
        result = ParityResult(
            fixture_id="f-001",
            outcome=ParityOutcome.PASS,
            source_output={"y": 2},
            mirror_output={"y": 2},
        )
        self.assertTrue(result.checked_at)
        self.assertEqual(result.deviation, 0.0)

    def test_result_to_dict(self) -> None:
        result = ParityResult(
            fixture_id="f-001",
            outcome=ParityOutcome.FAIL,
            source_output={"y": 2},
            mirror_output={"y": 99},
            deviation=0.75,
            details="Major divergence",
        )
        d = result.to_dict()
        self.assertEqual(d["outcome"], "fail")
        self.assertEqual(d["deviation"], 0.75)


class TestParityRunner(unittest.TestCase):
    """Tests for the ParityRunner class."""

    def setUp(self) -> None:
        self.runner = ParityRunner()
        self.fixture = ParityFixture(
            fixture_id="f-010",
            name="Add test",
            source_input={"a": 5, "b": 3},
            expected_output={"sum": 8},
        )
        self.runner.add_fixture(self.fixture)

    def test_add_fixture(self) -> None:
        self.assertIn("f-010", self.runner.fixtures)
        self.assertTrue(self.runner.has_fixtures())

    def test_run_parity_check_exact_match(self) -> None:
        def mirror_fn(inp: dict[str, Any]) -> dict[str, Any]:
            return {"sum": inp["a"] + inp["b"]}

        results = self.runner.run_parity_check(mirror_fn)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].outcome, ParityOutcome.PASS)
        self.assertEqual(results[0].deviation, 0.0)

    def test_run_parity_check_fail(self) -> None:
        def bad_mirror(inp: dict[str, Any]) -> dict[str, Any]:
            return {"sum": 999, "extra": "garbage"}

        results = self.runner.run_parity_check(bad_mirror)
        self.assertEqual(len(results), 1)
        self.assertIn(results[0].outcome, (ParityOutcome.FAIL, ParityOutcome.DRIFT))
        self.assertGreater(results[0].deviation, 0.0)

    def test_run_parity_check_mirror_exception(self) -> None:
        def exploding_mirror(inp: dict[str, Any]) -> dict[str, Any]:
            raise RuntimeError("mirror exploded")

        results = self.runner.run_parity_check(exploding_mirror)
        self.assertEqual(results[0].outcome, ParityOutcome.ERROR)
        self.assertIn("RuntimeError", results[0].details)

    def test_run_parity_check_missing_fixture_id(self) -> None:
        def mirror_fn(inp: dict[str, Any]) -> dict[str, Any]:
            return {}

        results = self.runner.run_parity_check(mirror_fn, fixture_ids=["nonexistent"])
        self.assertEqual(results[0].outcome, ParityOutcome.ERROR)
        self.assertIn("not found", results[0].details)

    def test_no_fixtures_raises(self) -> None:
        empty_runner = ParityRunner()
        with self.assertRaises(ValueError):
            empty_runner.run_parity_check(lambda x: x)

    def test_generate_parity_report(self) -> None:
        def mirror_fn(inp: dict[str, Any]) -> dict[str, Any]:
            return {"sum": inp["a"] + inp["b"]}

        self.runner.run_parity_check(mirror_fn)
        report = self.runner.generate_parity_report()
        self.assertEqual(report["total"], 1)
        self.assertEqual(report["pass"], 1)
        self.assertEqual(report["pass_rate"], 1.0)

    def test_generate_empty_report(self) -> None:
        report = self.runner.generate_parity_report()
        self.assertEqual(report["total"], 0)

    def test_clear_results(self) -> None:
        def mirror_fn(inp: dict[str, Any]) -> dict[str, Any]:
            return {"sum": inp["a"] + inp["b"]}

        self.runner.run_parity_check(mirror_fn)
        self.assertTrue(len(self.runner.results) > 0)
        self.runner.clear_results()
        self.assertEqual(len(self.runner.results), 0)

    def test_compare_outputs_exact_match(self) -> None:
        dev, detail = self.runner.compare_outputs({"a": 1}, {"a": 1})
        self.assertEqual(dev, 0.0)
        self.assertEqual(detail, "Exact match")

    def test_compare_outputs_missing_keys(self) -> None:
        dev, detail = self.runner.compare_outputs({"a": 1, "b": 2}, {"a": 1})
        self.assertGreater(dev, 0.0)
        self.assertIn("Missing keys", detail)

    def test_load_fixtures_from_list(self) -> None:
        runner = ParityRunner()
        count = runner.load_fixtures_from_list([
            {
                "fixture_id": "fl-1",
                "name": "List fixture",
                "source_input": {"x": 1},
                "expected_output": {"y": 1},
            }
        ])
        self.assertEqual(count, 1)
        self.assertIn("fl-1", runner.fixtures)

    def test_load_fixtures_from_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_data = {
                "fixture_id": "dir-1",
                "name": "Dir fixture",
                "source_input": {"x": 10},
                "expected_output": {"y": 20},
            }
            filepath = os.path.join(tmpdir, "test_fixture.json")
            with open(filepath, "w") as f:
                json.dump(fixture_data, f)

            runner = ParityRunner()
            count = runner.load_fixtures(tmpdir)
            self.assertEqual(count, 1)
            self.assertIn("dir-1", runner.fixtures)

    def test_load_fixtures_missing_directory(self) -> None:
        runner = ParityRunner()
        with self.assertRaises(FileNotFoundError):
            runner.load_fixtures("/nonexistent/path")

    def test_parity_within_tolerance(self) -> None:
        fixture = ParityFixture(
            fixture_id="f-tol",
            name="Tolerance test",
            source_input={"v": 100},
            expected_output={"v": 100.0},
            tolerance=0.5,
        )
        runner = ParityRunner()
        runner.add_fixture(fixture)

        def mirror_fn(inp: dict[str, Any]) -> dict[str, Any]:
            return {"v": 100.04}

        results = runner.run_parity_check(mirror_fn)
        self.assertEqual(results[0].outcome, ParityOutcome.PASS)


if __name__ == "__main__":
    unittest.main()
