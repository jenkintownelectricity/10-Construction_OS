"""Constraint Port — Main Evaluation Flow.

Accepts a ResolutionResult and evaluates it against a set of constraints
with collected evidence, returning ConstraintDecision objects.

Flow:
  accept ResolutionResult + constraints + evidence
  → validate all inputs
  → check evidence completeness
  → evaluate trigger conditions
  → return ConstraintDecision(s)

Boundary rules:
- Deterministic: same inputs always produce same decisions
- Fail-closed at every stage
- No truth mutation
- No UI ownership
- No probabilistic authority
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.constraint_types import (
    ConstraintObject,
    ConstraintEvidence,
    ConstraintDecision,
    TriggeredBy,
    DECISION_ACTIONS,
)
from core.constraint_validator import (
    validate_constraint_object,
    validate_constraint_evidence,
)
from core.constraint_decision import (
    build_decision,
    decide_on_missing_evidence,
    decide_on_unknown_constraint,
    aggregate_action,
    aggregate_severity,
    any_halting,
)


@dataclass(frozen=True)
class ConstraintPortResult:
    """Result from the Constraint Port evaluation.

    Fields:
        decisions: All individual constraint decisions
        aggregate_action: The most severe action across all decisions
        aggregate_severity: The highest severity across all decisions
        halted: Whether any decision requires halting
        validation_errors: Any input validation errors encountered
    """
    decisions: list[ConstraintDecision] = field(default_factory=list)
    aggregate_action: str = "BLOCK"
    aggregate_severity: str = "CRITICAL"
    halted: bool = True
    validation_errors: list[dict[str, str]] = field(default_factory=list)


class ConstraintPort:
    """Deterministic constraint evaluation port.

    Sits between resolution output and execution. Evaluates constraints
    and halts invalid outcomes before runtime proceeds.
    """

    def evaluate(
        self,
        resolution_result: dict[str, Any],
        constraints: list[ConstraintObject],
        evidence_map: dict[str, ConstraintEvidence],
    ) -> ConstraintPortResult:
        """Evaluate a ResolutionResult against a set of constraints.

        Args:
            resolution_result: The ResolutionResult dict from ALEXANDER engine
            constraints: Ordered list of ConstraintObject rules to evaluate
            evidence_map: Map of rule_id -> ConstraintEvidence

        Returns:
            ConstraintPortResult with all decisions and aggregate status

        Constraints are evaluated in rule_id sort order for deterministic sequencing.
        """
        # Validate resolution_result is present
        if not isinstance(resolution_result, dict):
            return ConstraintPortResult(
                validation_errors=[{"code": "INVALID_INPUT", "message": "resolution_result must be a dict"}],
            )

        # Sort constraints by rule_id for deterministic order
        sorted_constraints = sorted(constraints, key=lambda c: c.rule_id)

        decisions: list[ConstraintDecision] = []
        validation_errors: list[dict[str, str]] = []
        decision_counter = 0

        for constraint in sorted_constraints:
            decision_counter += 1
            decision_id = f"CD-EVAL-{decision_counter:04d}"

            # Validate constraint object
            obj_errors = validate_constraint_object(_constraint_to_dict(constraint))
            if obj_errors:
                validation_errors.extend(obj_errors)
                decisions.append(decide_on_unknown_constraint(
                    decision_id=decision_id,
                    rule_id=constraint.rule_id,
                    evidence_id="NONE",
                ))
                continue

            # Look up evidence for this constraint
            evidence = evidence_map.get(constraint.rule_id)
            if evidence is None:
                # No evidence at all — fail-closed
                decisions.append(decide_on_unknown_constraint(
                    decision_id=decision_id,
                    rule_id=constraint.rule_id,
                    evidence_id="NONE",
                ))
                continue

            # Validate evidence
            ev_errors = validate_constraint_evidence(_evidence_to_dict(evidence))
            if ev_errors:
                validation_errors.extend(ev_errors)
                decisions.append(decide_on_unknown_constraint(
                    decision_id=decision_id,
                    rule_id=constraint.rule_id,
                    evidence_id=evidence.evidence_id,
                ))
                continue

            # Check evidence completeness
            if evidence.completeness != "COMPLETE":
                decisions.append(decide_on_missing_evidence(
                    decision_id=decision_id,
                    constraint=constraint,
                    evidence=evidence,
                ))
                continue

            # Evidence is complete — evaluate trigger
            trigger_result = self._evaluate_trigger(
                constraint=constraint,
                evidence=evidence,
                resolution_result=resolution_result,
            )

            if trigger_result["triggered"]:
                # Constraint was triggered — apply logic_operator as action
                action = constraint.logic_operator
                if action not in DECISION_ACTIONS:
                    action = "BLOCK"  # fail-closed

                severity = "HIGH" if action == "BLOCK" else "MEDIUM" if action == "WARN" else "HIGH"

                decisions.append(build_decision(
                    decision_id=decision_id,
                    constraint=constraint,
                    evidence=evidence,
                    action=action,
                    severity=severity,
                    rationale=trigger_result["rationale"],
                    triggered_by=trigger_result.get("triggered_by"),
                    dependency_chain=list(constraint.dependency_map.kernels),
                ))
            else:
                # Constraint not triggered — PASS
                decisions.append(build_decision(
                    decision_id=decision_id,
                    constraint=constraint,
                    evidence=evidence,
                    action="PASS",
                    severity="INFO",
                    rationale=f"Constraint {constraint.rule_id} evaluated: condition not triggered.",
                    dependency_chain=list(constraint.dependency_map.kernels),
                ))

        # Compute aggregates
        if decisions:
            agg_action = aggregate_action(decisions)
            agg_severity = aggregate_severity(decisions)
            halted = any_halting(decisions)
        else:
            # No constraints evaluated — fail-closed
            agg_action = "BLOCK"
            agg_severity = "CRITICAL"
            halted = True

        return ConstraintPortResult(
            decisions=decisions,
            aggregate_action=agg_action,
            aggregate_severity=agg_severity,
            halted=halted,
            validation_errors=validation_errors,
        )

    def _evaluate_trigger(
        self,
        constraint: ConstraintObject,
        evidence: ConstraintEvidence,
        resolution_result: dict[str, Any],
    ) -> dict[str, Any]:
        """Evaluate whether a constraint's trigger condition is met.

        This is a deterministic evaluation based on evidence items
        and the trigger condition string. Currently supports exact-match
        evaluation: checks if required evidence keys match expected values.

        Returns:
            {"triggered": bool, "rationale": str, "triggered_by": TriggeredBy | None}
        """
        # Build evidence lookup
        evidence_lookup: dict[str, Any] = {}
        for item in evidence.evidence_items:
            evidence_lookup[item.key] = item.value

        # Check if all required evidence items are present
        for req_key in constraint.required_evidence:
            if req_key not in evidence_lookup:
                # Required evidence missing despite COMPLETE status —
                # this is a data integrity issue, treat as triggered (fail-closed)
                return {
                    "triggered": True,
                    "rationale": (
                        f"Required evidence key '{req_key}' missing from evidence "
                        f"despite COMPLETE status. Fail-closed: treating as triggered."
                    ),
                    "triggered_by": TriggeredBy(
                        evidence_key=req_key,
                        evidence_value=None,
                        comparison="missing_despite_complete",
                    ),
                }

        # Deterministic trigger evaluation:
        # The trigger.condition is a declarative expression.
        # For the core port, we evaluate it as a simple presence check:
        # if all required evidence is present and complete, the constraint
        # is considered "evaluated" but not necessarily "triggered".
        #
        # Triggering occurs when the evidence reveals a violation.
        # The trigger condition string defines what constitutes a violation.
        # For now, we check if any evidence item has a value that indicates
        # a violation (value is False for boolean checks, or value matches
        # a violation pattern).
        #
        # This can be extended with rulepack-specific evaluators.

        trigger_condition = constraint.trigger.condition

        # Simple deterministic evaluation: check for boolean violation flags
        for item in evidence.evidence_items:
            if item.key in constraint.required_evidence:
                if isinstance(item.value, bool) and item.value is False:
                    return {
                        "triggered": True,
                        "rationale": (
                            f"Constraint {constraint.rule_id} triggered: "
                            f"evidence '{item.key}' = {item.value} indicates violation. "
                            f"Condition: {trigger_condition}"
                        ),
                        "triggered_by": TriggeredBy(
                            evidence_key=item.key,
                            evidence_value=item.value,
                            comparison="boolean_false_violation",
                        ),
                    }

        # No violation detected
        return {
            "triggered": False,
            "rationale": f"Constraint {constraint.rule_id}: all evidence passes. Condition: {trigger_condition}",
            "triggered_by": None,
        }


def _constraint_to_dict(c: ConstraintObject) -> dict[str, Any]:
    """Convert a ConstraintObject dataclass to a dict for validation."""
    return {
        "rule_id": c.rule_id,
        "rule_label": c.rule_label,
        "rule_family": c.rule_family,
        "constraint_type": c.constraint_type,
        "source_authority": c.source_authority,
        "source_ref": c.source_ref,
        "applies_to": {
            "entity_type": c.applies_to.entity_type,
            "entity_ids": c.applies_to.entity_ids,
        },
        "trigger": {
            "condition": c.trigger.condition,
            "context_requirements": c.trigger.context_requirements,
        },
        "dependency_map": {
            "kernels": c.dependency_map.kernels,
            "external_refs": c.dependency_map.external_refs,
        },
        "logic_operator": c.logic_operator,
        "required_evidence": c.required_evidence,
        "decision_on_fail": c.decision_on_fail,
        "notes": c.notes,
    }


def _evidence_to_dict(e: ConstraintEvidence) -> dict[str, Any]:
    """Convert a ConstraintEvidence dataclass to a dict for validation."""
    return {
        "evidence_id": e.evidence_id,
        "rule_id": e.rule_id,
        "timestamp": e.timestamp,
        "evidence_items": [
            {"key": item.key, "value": item.value, "source": item.source, "verified": item.verified}
            for item in e.evidence_items
        ],
        "completeness": e.completeness,
        "missing_items": e.missing_items,
    }
