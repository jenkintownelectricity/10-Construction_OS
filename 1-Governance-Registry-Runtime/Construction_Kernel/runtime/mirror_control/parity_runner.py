"""
parity_runner.py — Runs parity checks comparing source system behavior
vs mirror behavior using fixtures.

Parity is the proof that a mirror faithfully reproduces the behavior of its
source. Without parity, a mirror is just a copy with opinions.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional


class ParityOutcome(Enum):
    """Outcome of a single parity check."""
    PASS = "pass"
    FAIL = "fail"
    DRIFT = "drift"
    ERROR = "error"


@dataclass
class ParityFixture:
    """
    A fixture that defines expected source behavior for parity comparison.

    Attributes:
        fixture_id: Unique identifier for this fixture.
        name: Human-readable name.
        source_input: The input fed to both source and mirror.
        expected_output: The canonical output from the source system.
        tolerance: Acceptable deviation threshold (0.0 = exact match).
        tags: Optional classification tags.
        created_at: ISO timestamp of fixture creation.
    """
    fixture_id: str
    name: str
    source_input: dict[str, Any]
    expected_output: dict[str, Any]
    tolerance: float = 0.0
    tags: list[str] = field(default_factory=list)
    created_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def fingerprint(self) -> str:
        """Return a content-based fingerprint of the fixture."""
        content = json.dumps(
            {"input": self.source_input, "output": self.expected_output},
            sort_keys=True,
        )
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        """Serialize fixture to dictionary."""
        return {
            "fixture_id": self.fixture_id,
            "name": self.name,
            "source_input": self.source_input,
            "expected_output": self.expected_output,
            "tolerance": self.tolerance,
            "tags": self.tags,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ParityFixture:
        """Deserialize fixture from dictionary."""
        return cls(
            fixture_id=data["fixture_id"],
            name=data["name"],
            source_input=data["source_input"],
            expected_output=data["expected_output"],
            tolerance=data.get("tolerance", 0.0),
            tags=data.get("tags", []),
            created_at=data.get("created_at", ""),
        )


@dataclass
class ParityResult:
    """
    Result of a parity check for one fixture.

    Attributes:
        fixture_id: The fixture that was checked.
        outcome: Pass, fail, drift, or error.
        source_output: What the source produced (or expected output from fixture).
        mirror_output: What the mirror produced.
        deviation: Numeric measure of divergence (0.0 = identical).
        details: Explanatory text about the result.
        checked_at: ISO timestamp of the check.
    """
    fixture_id: str
    outcome: ParityOutcome
    source_output: dict[str, Any]
    mirror_output: dict[str, Any]
    deviation: float = 0.0
    details: str = ""
    checked_at: str = ""

    def __post_init__(self) -> None:
        if not self.checked_at:
            self.checked_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self) -> dict[str, Any]:
        """Serialize result to dictionary."""
        return {
            "fixture_id": self.fixture_id,
            "outcome": self.outcome.value,
            "source_output": self.source_output,
            "mirror_output": self.mirror_output,
            "deviation": self.deviation,
            "details": self.details,
            "checked_at": self.checked_at,
        }


class ParityRunner:
    """
    Runs parity checks comparing source system behavior vs mirror behavior.

    The runner loads fixtures, invokes a mirror function against each fixture's
    input, and compares the mirror output to the fixture's expected output.

    Args:
        fixtures_dir: Optional path to a directory containing fixture JSON files.
    """

    def __init__(self, fixtures_dir: Optional[str | Path] = None) -> None:
        self._fixtures: dict[str, ParityFixture] = {}
        self._results: list[ParityResult] = []
        self._fixtures_dir = Path(fixtures_dir) if fixtures_dir else None

        if self._fixtures_dir and self._fixtures_dir.is_dir():
            self.load_fixtures(self._fixtures_dir)

    @property
    def fixtures(self) -> dict[str, ParityFixture]:
        """Return all loaded fixtures keyed by fixture_id."""
        return dict(self._fixtures)

    @property
    def results(self) -> list[ParityResult]:
        """Return all recorded parity results."""
        return list(self._results)

    def add_fixture(self, fixture: ParityFixture) -> None:
        """Register a fixture for parity checking."""
        self._fixtures[fixture.fixture_id] = fixture

    def load_fixtures(self, directory: str | Path) -> int:
        """
        Load fixture JSON files from a directory.

        Each JSON file must contain a single fixture object or a list of fixtures.

        Args:
            directory: Path to directory containing fixture JSON files.

        Returns:
            Number of fixtures loaded.

        Raises:
            FileNotFoundError: If the directory does not exist.
            ValueError: If a fixture file is malformed.
        """
        directory = Path(directory)
        if not directory.is_dir():
            raise FileNotFoundError(f"Fixtures directory not found: {directory}")

        count = 0
        for filepath in sorted(directory.glob("*.json")):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                for item in data:
                    fixture = ParityFixture.from_dict(item)
                    self._fixtures[fixture.fixture_id] = fixture
                    count += 1
            elif isinstance(data, dict):
                fixture = ParityFixture.from_dict(data)
                self._fixtures[fixture.fixture_id] = fixture
                count += 1
            else:
                raise ValueError(f"Unexpected fixture format in {filepath}")

        return count

    def load_fixtures_from_list(self, fixture_dicts: list[dict[str, Any]]) -> int:
        """
        Load fixtures from a list of dictionaries.

        Args:
            fixture_dicts: List of fixture data dicts.

        Returns:
            Number of fixtures loaded.
        """
        count = 0
        for item in fixture_dicts:
            fixture = ParityFixture.from_dict(item)
            self._fixtures[fixture.fixture_id] = fixture
            count += 1
        return count

    def compare_outputs(
        self,
        expected: dict[str, Any],
        actual: dict[str, Any],
        tolerance: float = 0.0,
    ) -> tuple[float, str]:
        """
        Compare expected source output against actual mirror output.

        Returns a tuple of (deviation_score, detail_message).
        Deviation of 0.0 means exact match. Values > 0.0 indicate divergence.

        Args:
            expected: The canonical expected output.
            actual: The mirror's actual output.
            tolerance: Acceptable deviation before flagging drift.

        Returns:
            Tuple of (deviation, details).
        """
        if expected == actual:
            return 0.0, "Exact match"

        # Compute structural differences
        missing_keys = set(expected.keys()) - set(actual.keys())
        extra_keys = set(actual.keys()) - set(expected.keys())
        common_keys = set(expected.keys()) & set(actual.keys())

        diff_details: list[str] = []
        value_diffs = 0

        if missing_keys:
            diff_details.append(f"Missing keys in mirror: {sorted(missing_keys)}")
            value_diffs += len(missing_keys)

        if extra_keys:
            diff_details.append(f"Extra keys in mirror: {sorted(extra_keys)}")
            value_diffs += len(extra_keys)

        for key in sorted(common_keys):
            if expected[key] != actual[key]:
                exp_val = expected[key]
                act_val = actual[key]
                # Numeric tolerance check
                if isinstance(exp_val, (int, float)) and isinstance(act_val, (int, float)):
                    numeric_diff = abs(exp_val - act_val)
                    if numeric_diff > tolerance:
                        diff_details.append(
                            f"Key '{key}': expected {exp_val}, got {act_val} "
                            f"(diff={numeric_diff:.6f})"
                        )
                        value_diffs += 1
                else:
                    diff_details.append(
                        f"Key '{key}': expected {exp_val!r}, got {act_val!r}"
                    )
                    value_diffs += 1

        total_keys = len(set(expected.keys()) | set(actual.keys()))
        deviation = value_diffs / max(total_keys, 1)
        detail = "; ".join(diff_details) if diff_details else "Minor differences within tolerance"
        return deviation, detail

    def run_parity_check(
        self,
        mirror_fn: Callable[[dict[str, Any]], dict[str, Any]],
        fixture_ids: Optional[list[str]] = None,
    ) -> list[ParityResult]:
        """
        Run parity checks by invoking mirror_fn against fixtures.

        Args:
            mirror_fn: A callable that takes source_input and returns mirror output.
            fixture_ids: Optional list of specific fixture IDs to check.
                         If None, all loaded fixtures are checked.

        Returns:
            List of ParityResult objects.

        Raises:
            ValueError: If no fixtures are loaded.
        """
        if not self._fixtures:
            raise ValueError("No fixtures loaded. Load fixtures before running parity checks.")

        targets = fixture_ids or list(self._fixtures.keys())
        results: list[ParityResult] = []

        for fid in targets:
            if fid not in self._fixtures:
                results.append(ParityResult(
                    fixture_id=fid,
                    outcome=ParityOutcome.ERROR,
                    source_output={},
                    mirror_output={},
                    details=f"Fixture '{fid}' not found",
                ))
                continue

            fixture = self._fixtures[fid]

            try:
                mirror_output = mirror_fn(fixture.source_input)
            except Exception as exc:
                results.append(ParityResult(
                    fixture_id=fid,
                    outcome=ParityOutcome.ERROR,
                    source_output=fixture.expected_output,
                    mirror_output={},
                    details=f"Mirror function raised {type(exc).__name__}: {exc}",
                ))
                continue

            deviation, details = self.compare_outputs(
                fixture.expected_output,
                mirror_output,
                fixture.tolerance,
            )

            if deviation == 0.0:
                outcome = ParityOutcome.PASS
            elif deviation <= fixture.tolerance:
                outcome = ParityOutcome.PASS
                details = f"Within tolerance ({deviation:.4f} <= {fixture.tolerance}): {details}"
            elif deviation < 0.5:
                outcome = ParityOutcome.DRIFT
            else:
                outcome = ParityOutcome.FAIL

            result = ParityResult(
                fixture_id=fid,
                outcome=outcome,
                source_output=fixture.expected_output,
                mirror_output=mirror_output,
                deviation=deviation,
                details=details,
            )
            results.append(result)

        self._results.extend(results)
        return results

    def generate_parity_report(
        self,
        results: Optional[list[ParityResult]] = None,
    ) -> dict[str, Any]:
        """
        Generate a summary report from parity results.

        Args:
            results: Optional list of results to report on.
                     If None, uses all accumulated results.

        Returns:
            Dictionary containing the parity report.
        """
        target_results = results or self._results
        if not target_results:
            return {
                "summary": "No parity results available",
                "total": 0,
                "pass": 0,
                "fail": 0,
                "drift": 0,
                "error": 0,
                "pass_rate": 0.0,
                "results": [],
            }

        counts: dict[str, int] = {"pass": 0, "fail": 0, "drift": 0, "error": 0}
        for r in target_results:
            counts[r.outcome.value] += 1

        total = len(target_results)
        pass_rate = counts["pass"] / total if total > 0 else 0.0

        return {
            "summary": f"Parity check: {counts['pass']}/{total} passed",
            "total": total,
            "pass": counts["pass"],
            "fail": counts["fail"],
            "drift": counts["drift"],
            "error": counts["error"],
            "pass_rate": round(pass_rate, 4),
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "results": [r.to_dict() for r in target_results],
        }

    def clear_results(self) -> None:
        """Clear all accumulated parity results."""
        self._results.clear()

    def has_fixtures(self) -> bool:
        """Return True if any fixtures are loaded."""
        return bool(self._fixtures)
