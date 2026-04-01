"""Governed Result Types.

Defines the GovernedResult output contract — the final application-safe
object that downstream consumers (Atlas, Application_OS) receive.

This is the ONLY object application consumers should depend on.
It encapsulates the full resolution + constraint chain without
exposing engine or constraint port internals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# GovernedResult statuses
GOVERNED_STATUSES = frozenset([
    "APPROVED",       # Resolution passed all constraints
    "WARNED",         # Resolution passed with warnings
    "BLOCKED",        # Resolution blocked by constraints
    "HALTED",         # Resolution halted — requires human intervention
    "FAILED",         # Upstream failure (adapter or engine error)
])


@dataclass(frozen=True)
class GovernedResolutionSummary:
    """Summary of the resolution outcome for application consumers.

    Provides only what applications need to know —
    not the full internal resolution pipeline detail.
    """
    condition_id: str
    condition_type: str
    resolution_status: str  # From ResolutionResult: RESOLVED/UNRESOLVED/BLOCKED/CONFLICT
    pattern_family_id: str | None = None
    pattern_id: str | None = None
    variant_id: str | None = None


@dataclass(frozen=True)
class GovernedConstraintSummary:
    """Summary of constraint evaluation for application consumers."""
    aggregate_action: str   # PASS/WARN/BLOCK/REQUIRE_HUMAN_STAMP/DEFER
    aggregate_severity: str  # INFO/LOW/MEDIUM/HIGH/CRITICAL
    halted: bool
    decision_count: int
    blocking_rules: list[str] = field(default_factory=list)
    warning_rules: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class GovernedResult:
    """The final governed output for application-facing consumers.

    This is the terminal seam object in the chain:
    ConditionSignature → ResolutionResult → ConstraintDecision → GovernedResult

    Application consumers ONLY interact with this object.
    """
    governed_result_id: str
    timestamp_utc: str
    status: str  # One of GOVERNED_STATUSES
    resolution_summary: GovernedResolutionSummary | None = None
    constraint_summary: GovernedConstraintSummary | None = None
    errors: list[dict[str, Any]] = field(default_factory=list)
    source_chain: list[str] = field(default_factory=lambda: [
        "Construction_ALEXANDER_Engine",
        "Constraint_Port",
        "Governed_Result_Surface",
    ])
