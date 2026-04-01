"""Constraint Decision Model.

PASS / WARN / BLOCK semantics with fail-closed behavior.
Provides deterministic decision construction and aggregation.

Fail-closed rules:
- Missing evidence → BLOCK (unless decision_on_fail overrides)
- Unknown constraint → BLOCK
- Non-deterministic state → BLOCK
- No silent pass-through
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from core.constraint_types import (
    ConstraintObject,
    ConstraintEvidence,
    ConstraintDecision,
    TriggeredBy,
    DECISION_ACTIONS,
    SEVERITIES,
    ACTION_ORDER,
    SEVERITY_ORDER,
)


def build_decision(
    decision_id: str,
    constraint: ConstraintObject,
    evidence: ConstraintEvidence,
    action: str,
    severity: str,
    rationale: str,
    triggered_by: TriggeredBy | None = None,
    dependency_chain: list[str] | None = None,
) -> ConstraintDecision:
    """Build a validated ConstraintDecision.

    Fail-closed: raises ValueError if action or severity is invalid.
    deterministic is always True.
    """
    if action not in DECISION_ACTIONS:
        raise ValueError(f"Invalid action '{action}'. Must be one of {sorted(DECISION_ACTIONS)}")
    if severity not in SEVERITIES:
        raise ValueError(f"Invalid severity '{severity}'. Must be one of {sorted(SEVERITIES)}")

    return ConstraintDecision(
        decision_id=decision_id,
        rule_id=constraint.rule_id,
        evidence_id=evidence.evidence_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        action=action,
        severity=severity,
        rationale=rationale,
        source_authority=constraint.source_authority,
        deterministic=True,
        triggered_by=triggered_by,
        dependency_chain=dependency_chain or [],
    )


def decide_on_missing_evidence(
    decision_id: str,
    constraint: ConstraintObject,
    evidence: ConstraintEvidence,
) -> ConstraintDecision:
    """Produce a decision when evidence is incomplete.

    Uses constraint.decision_on_fail to determine action.
    Fail-closed: defaults to BLOCK if decision_on_fail is invalid.
    """
    action = constraint.decision_on_fail
    if action not in DECISION_ACTIONS:
        action = "BLOCK"  # fail-closed default

    missing_str = ", ".join(evidence.missing_items) if evidence.missing_items else "unknown"
    rationale = (
        f"Evidence incomplete (completeness={evidence.completeness}). "
        f"Missing: [{missing_str}]. "
        f"Applying decision_on_fail={action} per rule {constraint.rule_id}."
    )

    severity = "HIGH" if action == "BLOCK" else "MEDIUM"

    return build_decision(
        decision_id=decision_id,
        constraint=constraint,
        evidence=evidence,
        action=action,
        severity=severity,
        rationale=rationale,
    )


def decide_on_unknown_constraint(
    decision_id: str,
    rule_id: str,
    evidence_id: str,
) -> ConstraintDecision:
    """Produce a BLOCK decision for an unknown/unrecognized constraint.

    Fail-closed: unknown constraints always BLOCK.
    """
    return ConstraintDecision(
        decision_id=decision_id,
        rule_id=rule_id,
        evidence_id=evidence_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        action="BLOCK",
        severity="CRITICAL",
        rationale=f"Unknown constraint rule '{rule_id}'. Fail-closed: BLOCK.",
        source_authority="Constraint_Port_Governance",
        deterministic=True,
        dependency_chain=[],
    )


def aggregate_action(decisions: list[ConstraintDecision]) -> str:
    """Return the most severe action from a list of decisions.

    Severity order: BLOCK > REQUIRE_HUMAN_STAMP > DEFER > WARN > PASS.
    Fail-closed: empty list returns BLOCK.
    """
    if not decisions:
        return "BLOCK"

    return max(
        (d.action for d in decisions),
        key=lambda a: ACTION_ORDER.get(a, ACTION_ORDER["BLOCK"]),
    )


def aggregate_severity(decisions: list[ConstraintDecision]) -> str:
    """Return the highest severity from a list of decisions.

    Severity order: CRITICAL > HIGH > MEDIUM > LOW > INFO.
    Fail-closed: empty list returns CRITICAL.
    """
    if not decisions:
        return "CRITICAL"

    return max(
        (d.severity for d in decisions),
        key=lambda s: SEVERITY_ORDER.get(s, SEVERITY_ORDER["CRITICAL"]),
    )


def is_halting(decision: ConstraintDecision) -> bool:
    """Check whether a decision requires halting execution.

    BLOCK and REQUIRE_HUMAN_STAMP are halting actions.
    """
    return decision.action in ("BLOCK", "REQUIRE_HUMAN_STAMP")


def any_halting(decisions: list[ConstraintDecision]) -> bool:
    """Check whether any decision in the list requires halting."""
    return any(is_halting(d) for d in decisions)
