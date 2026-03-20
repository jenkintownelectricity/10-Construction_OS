"""
drift_recorder.py — Records and tracks drift between source and mirror.

Drift is the silent divergence between a mirror and its source.
Left unchecked, drift erodes trust. The DriftRecorder makes drift visible,
measurable, and actionable.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class DriftSeverity(Enum):
    """Severity classification for drift events."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DriftRecord:
    """
    A single recorded drift event between source and mirror.

    Attributes:
        record_id: Unique identifier for this drift record.
        mirror_id: Identifier of the mirror exhibiting drift.
        source_id: Identifier of the source system.
        severity: Drift severity classification.
        category: Drift category (e.g., 'schema', 'behavior', 'output', 'timing').
        description: Human-readable description of the drift.
        deviation: Numeric deviation score.
        source_value: The expected value from the source.
        mirror_value: The observed value from the mirror.
        fixture_id: Optional associated parity fixture.
        recorded_at: ISO timestamp of when the drift was recorded.
        resolved: Whether this drift has been resolved.
        resolved_at: ISO timestamp of resolution, if applicable.
    """
    record_id: str
    mirror_id: str
    source_id: str
    severity: DriftSeverity
    category: str
    description: str
    deviation: float = 0.0
    source_value: Any = None
    mirror_value: Any = None
    fixture_id: Optional[str] = None
    recorded_at: str = ""
    resolved: bool = False
    resolved_at: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.recorded_at:
            self.recorded_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self) -> dict[str, Any]:
        """Serialize drift record to dictionary."""
        return {
            "record_id": self.record_id,
            "mirror_id": self.mirror_id,
            "source_id": self.source_id,
            "severity": self.severity.value,
            "category": self.category,
            "description": self.description,
            "deviation": self.deviation,
            "source_value": self.source_value,
            "mirror_value": self.mirror_value,
            "fixture_id": self.fixture_id,
            "recorded_at": self.recorded_at,
            "resolved": self.resolved,
            "resolved_at": self.resolved_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DriftRecord:
        """Deserialize drift record from dictionary."""
        return cls(
            record_id=data["record_id"],
            mirror_id=data["mirror_id"],
            source_id=data["source_id"],
            severity=DriftSeverity(data["severity"]),
            category=data["category"],
            description=data["description"],
            deviation=data.get("deviation", 0.0),
            source_value=data.get("source_value"),
            mirror_value=data.get("mirror_value"),
            fixture_id=data.get("fixture_id"),
            recorded_at=data.get("recorded_at", ""),
            resolved=data.get("resolved", False),
            resolved_at=data.get("resolved_at"),
        )


class DriftRecorder:
    """
    Records and tracks drift between source and mirror systems.

    Maintains a history of drift events, supports severity assessment,
    and enforces drift thresholds that can trigger alerts or block activation.

    Args:
        mirror_id: Identifier of the mirror being tracked.
        drift_threshold: Maximum number of unresolved HIGH/CRITICAL drift
                         records before the threshold is considered breached.
        max_deviation_threshold: Maximum acceptable deviation score for any
                                 single drift event.
    """

    def __init__(
        self,
        mirror_id: str,
        drift_threshold: int = 5,
        max_deviation_threshold: float = 0.8,
    ) -> None:
        self._mirror_id = mirror_id
        self._drift_threshold = drift_threshold
        self._max_deviation_threshold = max_deviation_threshold
        self._records: list[DriftRecord] = []

    @property
    def mirror_id(self) -> str:
        """Return the mirror ID being tracked."""
        return self._mirror_id

    @property
    def records(self) -> list[DriftRecord]:
        """Return a copy of all drift records."""
        return list(self._records)

    def record_drift(
        self,
        source_id: str,
        category: str,
        description: str,
        severity: Optional[DriftSeverity] = None,
        deviation: float = 0.0,
        source_value: Any = None,
        mirror_value: Any = None,
        fixture_id: Optional[str] = None,
    ) -> DriftRecord:
        """
        Record a new drift event.

        If severity is not provided, it will be auto-assessed from the deviation.

        Args:
            source_id: Identifier of the source system.
            category: Drift category (schema, behavior, output, timing).
            description: Human-readable description.
            severity: Optional explicit severity. Auto-assessed if omitted.
            deviation: Numeric deviation score.
            source_value: Expected value from source.
            mirror_value: Observed value from mirror.
            fixture_id: Optional associated parity fixture ID.

        Returns:
            The created DriftRecord.
        """
        if severity is None:
            severity = self.assess_severity(deviation)

        record = DriftRecord(
            record_id=f"drift-{uuid.uuid4().hex[:12]}",
            mirror_id=self._mirror_id,
            source_id=source_id,
            severity=severity,
            category=category,
            description=description,
            deviation=deviation,
            source_value=source_value,
            mirror_value=mirror_value,
            fixture_id=fixture_id,
        )

        self._records.append(record)
        return record

    def get_drift_history(
        self,
        category: Optional[str] = None,
        severity: Optional[DriftSeverity] = None,
        unresolved_only: bool = False,
        limit: Optional[int] = None,
    ) -> list[DriftRecord]:
        """
        Query drift history with optional filters.

        Args:
            category: Filter by drift category.
            severity: Filter by severity level.
            unresolved_only: If True, only return unresolved drift records.
            limit: Maximum number of records to return (most recent first).

        Returns:
            Filtered list of DriftRecords.
        """
        results = self._records

        if category is not None:
            results = [r for r in results if r.category == category]

        if severity is not None:
            results = [r for r in results if r.severity == severity]

        if unresolved_only:
            results = [r for r in results if not r.resolved]

        # Most recent first
        results = sorted(results, key=lambda r: r.recorded_at, reverse=True)

        if limit is not None:
            results = results[:limit]

        return results

    def assess_severity(self, deviation: float) -> DriftSeverity:
        """
        Assess drift severity based on deviation score.

        Thresholds:
            - deviation <= 0.1  -> LOW
            - deviation <= 0.3  -> MEDIUM
            - deviation <= 0.6  -> HIGH
            - deviation > 0.6   -> CRITICAL

        Args:
            deviation: Numeric deviation score (0.0 = no drift).

        Returns:
            Assessed DriftSeverity.
        """
        if deviation <= 0.1:
            return DriftSeverity.LOW
        elif deviation <= 0.3:
            return DriftSeverity.MEDIUM
        elif deviation <= 0.6:
            return DriftSeverity.HIGH
        else:
            return DriftSeverity.CRITICAL

    def check_drift_threshold(self) -> tuple[bool, str]:
        """
        Check whether drift thresholds have been breached.

        A threshold is breached if:
        1. The number of unresolved HIGH or CRITICAL drift records exceeds
           the configured drift_threshold, OR
        2. Any single drift record has a deviation exceeding the
           max_deviation_threshold.

        Returns:
            Tuple of (within_threshold: bool, explanation: str).
            True means drift is acceptable; False means threshold breached.
        """
        unresolved_severe = [
            r for r in self._records
            if not r.resolved and r.severity in (DriftSeverity.HIGH, DriftSeverity.CRITICAL)
        ]

        if len(unresolved_severe) > self._drift_threshold:
            return False, (
                f"Drift threshold breached: {len(unresolved_severe)} unresolved "
                f"HIGH/CRITICAL records (threshold: {self._drift_threshold})"
            )

        extreme = [
            r for r in self._records
            if not r.resolved and r.deviation > self._max_deviation_threshold
        ]
        if extreme:
            worst = max(extreme, key=lambda r: r.deviation)
            return False, (
                f"Maximum deviation threshold breached: record {worst.record_id} "
                f"has deviation {worst.deviation:.4f} "
                f"(threshold: {self._max_deviation_threshold})"
            )

        return True, (
            f"Drift within acceptable limits: {len(unresolved_severe)} unresolved "
            f"severe records (threshold: {self._drift_threshold})"
        )

    def resolve_drift(self, record_id: str) -> bool:
        """
        Mark a drift record as resolved.

        Args:
            record_id: The record ID to resolve.

        Returns:
            True if the record was found and resolved, False otherwise.
        """
        for record in self._records:
            if record.record_id == record_id:
                record.resolved = True
                record.resolved_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                return True
        return False

    def get_summary(self) -> dict[str, Any]:
        """
        Return a summary of all drift records.

        Returns:
            Dictionary with drift summary statistics.
        """
        total = len(self._records)
        unresolved = sum(1 for r in self._records if not r.resolved)
        by_severity = {}
        for sev in DriftSeverity:
            by_severity[sev.value] = sum(
                1 for r in self._records if r.severity == sev and not r.resolved
            )

        within_threshold, explanation = self.check_drift_threshold()

        return {
            "mirror_id": self._mirror_id,
            "total_records": total,
            "unresolved": unresolved,
            "resolved": total - unresolved,
            "by_severity": by_severity,
            "within_threshold": within_threshold,
            "threshold_explanation": explanation,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    def clear(self) -> None:
        """Clear all drift records."""
        self._records.clear()
