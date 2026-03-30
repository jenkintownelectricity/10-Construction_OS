"""
Condition Inspector

Browses conditions, inspects parameters, shows readiness state,
and displays blocking issues from condition packets.

This module reads derived condition packets — it does not modify
runtime behavior or redefine construction truth.
All outputs are derived views over derived data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from runtime.drawing_engine.derived_outputs import ConditionPacket


@dataclass
class InspectionView:
    """Derived inspection view over a condition packet."""

    condition_id: str = ""
    detail_id: str = ""
    readiness_state: str = ""
    gaps: list[dict[str, str]] = field(default_factory=list)
    blocking_issues: list[dict[str, str]] = field(default_factory=list)
    parameter_summary: dict[str, Any] = field(default_factory=dict)
    is_ready: bool = False


def inspect_condition(packet: ConditionPacket) -> InspectionView:
    """
    Produce an inspection view from a condition packet.

    Reads the derived packet fields. Does not invoke runtime
    or modify any state. All output is derived.
    """
    view = InspectionView(
        condition_id=packet.condition_id,
        detail_id=packet.detail_id,
        readiness_state=packet.readiness_state,
        gaps=list(packet.gaps),
        is_ready=packet.readiness_state == "ready",
    )

    # Extract blocking issues from gaps (gaps may be strings or dicts)
    for g in packet.gaps:
        if isinstance(g, dict) and g.get("severity") in ("error", "blocking"):
            view.blocking_issues.append(g)
        elif isinstance(g, str):
            view.blocking_issues.append({"message": g, "severity": "error"})

    # Build parameter summary from audit trail
    if hasattr(packet, "audit_summary") and isinstance(packet.audit_summary, dict):
        view.parameter_summary = packet.audit_summary

    return view


def browse_conditions(
    packets: list[ConditionPacket],
) -> list[InspectionView]:
    """
    Browse multiple condition packets and return inspection views.

    Returns views sorted by readiness: blocked first, ready last.
    All output is derived.
    """
    views = [inspect_condition(p) for p in packets]
    # Blocked/incomplete first, ready last
    views.sort(key=lambda v: (v.is_ready, v.condition_id))
    return views
