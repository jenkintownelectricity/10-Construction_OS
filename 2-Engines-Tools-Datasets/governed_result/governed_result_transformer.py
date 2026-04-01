"""Governed Result Transformer.

Converts internal engine and constraint outputs into application-safe
GovernedResult objects.

Input: RuntimeAdapterResult (Wave 3) + ConstraintPortResult (Wave 4)
Output: GovernedResult (Wave 5)

Boundary rules:
- No engine or constraint internals leak to application consumers
- Fail-closed: any upstream failure produces a FAILED GovernedResult
- Deterministic: same inputs always produce same output
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from governed_result.governed_result_types import (
    GovernedResult,
    GovernedResolutionSummary,
    GovernedConstraintSummary,
    GOVERNED_STATUSES,
)


def transform(
    adapter_result: Any,
    constraint_result: Any | None = None,
) -> GovernedResult:
    """Transform internal results into a GovernedResult.

    Args:
        adapter_result: RuntimeAdapterResult from Wave 3 adapter
        constraint_result: ConstraintPortResult from Wave 4 port (optional)

    Returns:
        GovernedResult for application consumers

    Fail-closed: any error in transformation produces a FAILED result.
    """
    governed_id = f"GOV-{uuid.uuid4().hex[:16]}"
    timestamp = datetime.now(timezone.utc).isoformat()

    # Stage 1: Check adapter result
    if not _is_valid_adapter_result(adapter_result):
        return GovernedResult(
            governed_result_id=governed_id,
            timestamp_utc=timestamp,
            status="FAILED",
            errors=[{"code": "INVALID_ADAPTER_RESULT", "message": "Adapter result is invalid or missing"}],
        )

    if not adapter_result.success:
        error_list = [
            {"code": e.code, "message": e.message, "stage": e.stage}
            for e in adapter_result.adapter_errors
        ]
        return GovernedResult(
            governed_result_id=governed_id,
            timestamp_utc=timestamp,
            status="FAILED",
            errors=error_list,
        )

    # Stage 2: Extract resolution summary
    rr = adapter_result.resolution_result
    resolution_summary = GovernedResolutionSummary(
        condition_id=rr.get("condition_id", "unknown"),
        condition_type=rr.get("condition_type", "unknown"),
        resolution_status=rr.get("status", "UNRESOLVED"),
        pattern_family_id=rr.get("pattern_family_id"),
        pattern_id=rr.get("pattern_id"),
        variant_id=rr.get("variant_id"),
    )

    # Stage 3: If no constraint result, determine status from resolution alone
    if constraint_result is None:
        if rr.get("status") == "RESOLVED":
            status = "APPROVED"
        else:
            status = "FAILED"

        return GovernedResult(
            governed_result_id=governed_id,
            timestamp_utc=timestamp,
            status=status,
            resolution_summary=resolution_summary,
            constraint_summary=None,
            errors=[],
        )

    # Stage 4: Extract constraint summary
    if not _is_valid_constraint_result(constraint_result):
        return GovernedResult(
            governed_result_id=governed_id,
            timestamp_utc=timestamp,
            status="FAILED",
            resolution_summary=resolution_summary,
            errors=[{"code": "INVALID_CONSTRAINT_RESULT", "message": "Constraint result is invalid"}],
        )

    blocking_rules = [
        d.rule_id for d in constraint_result.decisions
        if d.action in ("BLOCK", "REQUIRE_HUMAN_STAMP")
    ]
    warning_rules = [
        d.rule_id for d in constraint_result.decisions
        if d.action == "WARN"
    ]

    constraint_summary = GovernedConstraintSummary(
        aggregate_action=constraint_result.aggregate_action,
        aggregate_severity=constraint_result.aggregate_severity,
        halted=constraint_result.halted,
        decision_count=len(constraint_result.decisions),
        blocking_rules=blocking_rules,
        warning_rules=warning_rules,
    )

    # Stage 5: Determine governed status
    if constraint_result.halted:
        if constraint_result.aggregate_action == "REQUIRE_HUMAN_STAMP":
            status = "HALTED"
        else:
            status = "BLOCKED"
    elif warning_rules:
        status = "WARNED"
    elif rr.get("status") == "RESOLVED":
        status = "APPROVED"
    else:
        status = "FAILED"

    return GovernedResult(
        governed_result_id=governed_id,
        timestamp_utc=timestamp,
        status=status,
        resolution_summary=resolution_summary,
        constraint_summary=constraint_summary,
        errors=[],
    )


def _is_valid_adapter_result(result: Any) -> bool:
    """Check if result looks like a RuntimeAdapterResult."""
    return (
        hasattr(result, "success")
        and hasattr(result, "resolution_result")
        and hasattr(result, "adapter_errors")
    )


def _is_valid_constraint_result(result: Any) -> bool:
    """Check if result looks like a ConstraintPortResult."""
    return (
        hasattr(result, "decisions")
        and hasattr(result, "aggregate_action")
        and hasattr(result, "aggregate_severity")
        and hasattr(result, "halted")
    )
