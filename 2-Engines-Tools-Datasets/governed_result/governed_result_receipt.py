"""Governed Result Receipt Hook.

Provides hook points for emitting governed result receipts
into the 5-State-Receipts-Signals layer.

This module does NOT write directly to the state layer.
It produces receipt dicts that callers can persist as needed.

Boundary rules:
- Receipt generation only — no direct file writes
- No registry modifications
- Compatible with existing JSON receipt format
- Deterministic: same GovernedResult always produces same receipt
"""

from __future__ import annotations

from typing import Any

from governed_result.governed_result_types import GovernedResult


def generate_receipt(governed_result: GovernedResult) -> dict[str, Any]:
    """Generate a receipt dict for a GovernedResult.

    The receipt can be persisted to 5-State-Receipts-Signals/
    by the calling layer. This function only produces the receipt data.

    Returns a dict compatible with the existing absorption receipt format.
    """
    receipt: dict[str, Any] = {
        "receipt_type": "governed_result",
        "receipt_version": "1.0.0",
        "governed_result_id": governed_result.governed_result_id,
        "timestamp_utc": governed_result.timestamp_utc,
        "status": governed_result.status,
        "source_chain": list(governed_result.source_chain),
    }

    if governed_result.resolution_summary is not None:
        receipt["resolution"] = {
            "condition_id": governed_result.resolution_summary.condition_id,
            "condition_type": governed_result.resolution_summary.condition_type,
            "resolution_status": governed_result.resolution_summary.resolution_status,
            "pattern_family_id": governed_result.resolution_summary.pattern_family_id,
            "pattern_id": governed_result.resolution_summary.pattern_id,
            "variant_id": governed_result.resolution_summary.variant_id,
        }

    if governed_result.constraint_summary is not None:
        receipt["constraint"] = {
            "aggregate_action": governed_result.constraint_summary.aggregate_action,
            "aggregate_severity": governed_result.constraint_summary.aggregate_severity,
            "halted": governed_result.constraint_summary.halted,
            "decision_count": governed_result.constraint_summary.decision_count,
            "blocking_rules": list(governed_result.constraint_summary.blocking_rules),
            "warning_rules": list(governed_result.constraint_summary.warning_rules),
        }

    if governed_result.errors:
        receipt["errors"] = governed_result.errors

    return receipt


def generate_signal(governed_result: GovernedResult) -> dict[str, Any]:
    """Generate a signal dict for downstream notification.

    Signals are lightweight notifications that downstream consumers
    can use to trigger actions without needing the full result.

    Returns a dict with minimal governed status information.
    """
    signal: dict[str, Any] = {
        "signal_type": "governed_result_ready",
        "governed_result_id": governed_result.governed_result_id,
        "timestamp_utc": governed_result.timestamp_utc,
        "status": governed_result.status,
        "halted": False,
    }

    if governed_result.constraint_summary is not None:
        signal["halted"] = governed_result.constraint_summary.halted

    if governed_result.resolution_summary is not None:
        signal["condition_id"] = governed_result.resolution_summary.condition_id

    return signal
