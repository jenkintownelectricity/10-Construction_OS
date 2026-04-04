"""
Constraint Evaluator — Wave 8
Construction OS — Guaranteed Detail Engine

Evaluates constraints before guaranteed detail admission.

Flow:
  1. Import from Constraint-Port/core/
  2. Create manufacturer system lock constraint rules for Barrett RamProof GC
  3. Evaluate: are required system components present in the evidence?
  4. Use build_decision() and aggregate_action() from constraint_decision.py
  5. Map constraint port PASS/WARN/BLOCK to pipeline PASS/PARTIAL/HALT

Fail-closed: unknown states → HALT / BLOCK.
"""

from __future__ import annotations

import os
import sys
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Import from Constraint Port
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_CONSTRAINT_PORT_DIR = os.path.join(
    _REPO_ROOT, "2-Engines-Tools-Datasets", "Constraint-Port"
)

if _CONSTRAINT_PORT_DIR not in sys.path:
    sys.path.insert(0, _CONSTRAINT_PORT_DIR)

from core.constraint_types import (  # noqa: E402
    ConstraintObject,
    ConstraintEvidence,
    ConstraintDecision,
    AppliesTo,
    Trigger,
    DependencyMap,
    EvidenceItem,
)
from core.constraint_decision import (  # noqa: E402
    build_decision,
    aggregate_action,
    aggregate_severity,
    any_halting,
)


# ---------------------------------------------------------------------------
# Barrett RamProof GC constraint rules
# ---------------------------------------------------------------------------

def _barrett_system_lock_constraint() -> ConstraintObject:
    """Create the Barrett RamProof GC manufacturer system lock constraint.

    This ensures that required system components are present in the
    assembly evidence before a detail can be guaranteed.
    """
    return ConstraintObject(
        rule_id="RULE-BARRETT-SYS-LOCK-001",
        rule_label="Barrett RamProof GC System Component Lock",
        rule_family="manufacturer_system_lock",
        constraint_type="WARRANTY_VOID",
        source_authority="Barrett_Company_Technical",
        source_ref="ramproof_gc_systems.json",
        applies_to=AppliesTo(
            entity_type="system",
            entity_ids=["FAM-BARRETT-RAMPROOF-GC"],
        ),
        trigger=Trigger(
            condition="system_components_present",
            context_requirements=["manufacturer_id", "system_id", "condition_type"],
        ),
        dependency_map=DependencyMap(
            kernels=["ownership_classifier", "condition_bridge", "assembly_resolver"],
            external_refs=["ramproof_gc_systems.json"],
        ),
        logic_operator="BLOCK",
        required_evidence=[
            "manufacturer_match",
            "system_match",
            "condition_supported",
            "detail_resolved",
        ],
        decision_on_fail="BLOCK",
        notes="Blocks detail admission if Barrett system components are not verified in evidence.",
    )


def _barrett_condition_support_constraint() -> ConstraintObject:
    """Ensure the detected condition is in Barrett's supported condition list."""
    return ConstraintObject(
        rule_id="RULE-BARRETT-COND-SUPPORT-001",
        rule_label="Barrett Condition Support Verification",
        rule_family="condition_support_check",
        constraint_type="SPEC_CONFLICT",
        source_authority="Barrett_Company_Technical",
        source_ref="assembly_condition_recipes.barrett.json",
        applies_to=AppliesTo(
            entity_type="assembly",
            entity_ids=[],
        ),
        trigger=Trigger(
            condition="condition_in_supported_set",
            context_requirements=["condition_type"],
        ),
        dependency_map=DependencyMap(
            kernels=["condition_bridge"],
            external_refs=["assembly_condition_recipes.barrett.json"],
        ),
        logic_operator="WARN",
        required_evidence=[
            "condition_supported",
        ],
        decision_on_fail="WARN",
        notes="Warns if the detected condition has no matching Barrett recipe.",
    )


# ---------------------------------------------------------------------------
# Evidence builder
# ---------------------------------------------------------------------------

def _build_evidence(
    rule_id: str,
    resolution_result: dict,
    candidate: dict | None = None,
) -> ConstraintEvidence:
    """Build constraint evidence from pipeline upstream results."""
    now_utc = datetime.now(timezone.utc).isoformat()
    items: list[EvidenceItem] = []
    missing: list[str] = []

    resolution_status = resolution_result.get("resolution_status", "")
    manufacturer_id = resolution_result.get("manufacturer_id", "")
    system_id = resolution_result.get("system_id", "")
    condition_type = resolution_result.get("condition_type", "")
    detail_id = resolution_result.get("resolved_detail_id", "")

    # manufacturer_match
    mfr_match = "BARRETT" in (manufacturer_id or "").upper()
    items.append(EvidenceItem(
        key="manufacturer_match",
        value=mfr_match,
        source="assembly_resolver",
        verified=mfr_match,
    ))
    if not mfr_match:
        missing.append("manufacturer_match")

    # system_match
    sys_match = bool(system_id and "RAMPROOF" in system_id.upper())
    items.append(EvidenceItem(
        key="system_match",
        value=sys_match,
        source="assembly_resolver",
        verified=sys_match,
    ))
    if not sys_match:
        missing.append("system_match")

    # condition_supported
    from workers.condition_bridge import SUPPORTED_CONDITIONS  # local import to avoid circular
    cond_supported = condition_type in SUPPORTED_CONDITIONS
    items.append(EvidenceItem(
        key="condition_supported",
        value=cond_supported,
        source="condition_bridge",
        verified=cond_supported,
    ))
    if not cond_supported:
        missing.append("condition_supported")

    # detail_resolved
    detail_ok = resolution_status == "RESOLVED" and bool(detail_id)
    items.append(EvidenceItem(
        key="detail_resolved",
        value=detail_ok,
        source="assembly_resolver",
        verified=detail_ok,
    ))
    if not detail_ok:
        missing.append("detail_resolved")

    completeness = "COMPLETE" if not missing else "PARTIAL"

    return ConstraintEvidence(
        evidence_id=f"EV-{uuid.uuid4().hex[:12].upper()}",
        rule_id=rule_id,
        timestamp=now_utc,
        evidence_items=items,
        completeness=completeness,
        missing_items=missing,
    )


# ---------------------------------------------------------------------------
# Action mapping: Constraint Port → Pipeline
# ---------------------------------------------------------------------------

_ACTION_TO_PIPELINE: dict[str, str] = {
    "PASS": "PASS",
    "WARN": "PARTIAL",
    "BLOCK": "HALT",
    "REQUIRE_HUMAN_STAMP": "HALT",
    "DEFER_FOR_MISSING_EVIDENCE": "HALT",
}


# ---------------------------------------------------------------------------
# Main evaluator
# ---------------------------------------------------------------------------

def evaluate_constraints(
    resolution_result: dict,
    candidate: dict | None = None,
) -> dict:
    """Evaluate constraints for guaranteed detail admission.

    Args:
        resolution_result: dict matching assembly_resolution_result.schema.json
        candidate: Optional assembly_candidate dict for extra context

    Returns:
        dict with:
            decision: PASS | PARTIAL | HALT
            constraint_action: raw action from constraint port
            severity: INFO | LOW | MEDIUM | HIGH | CRITICAL
            reason_codes: list of reason strings
            halt_reasons: list of halt-causing reasons
            partial_reasons: list of partial/warn reasons
            decisions_raw: list of raw ConstraintDecision dicts
    """
    constraints = [
        _barrett_system_lock_constraint(),
        _barrett_condition_support_constraint(),
    ]

    decisions: list[ConstraintDecision] = []
    counter = 0

    for constraint in constraints:
        counter += 1
        decision_id = f"CD-GDE-{counter:04d}"

        evidence = _build_evidence(
            rule_id=constraint.rule_id,
            resolution_result=resolution_result,
            candidate=candidate,
        )

        # Check evidence completeness
        if evidence.completeness != "COMPLETE":
            # Missing evidence — use decision_on_fail
            action = constraint.decision_on_fail
            if action not in ("PASS", "WARN", "BLOCK", "REQUIRE_HUMAN_STAMP", "DEFER_FOR_MISSING_EVIDENCE"):
                action = "BLOCK"

            severity = "HIGH" if action == "BLOCK" else "MEDIUM"
            missing_str = ", ".join(evidence.missing_items) if evidence.missing_items else "unknown"

            decision = build_decision(
                decision_id=decision_id,
                constraint=constraint,
                evidence=evidence,
                action=action,
                severity=severity,
                rationale=(
                    f"Evidence incomplete for {constraint.rule_id}. "
                    f"Missing: [{missing_str}]. Applying decision_on_fail={action}."
                ),
            )
        else:
            # Evidence complete — check for violations (boolean False values)
            violation_found = False
            violation_key = None
            for item in evidence.evidence_items:
                if item.key in constraint.required_evidence:
                    if isinstance(item.value, bool) and item.value is False:
                        violation_found = True
                        violation_key = item.key
                        break

            if violation_found:
                action = constraint.logic_operator
                if action not in ("PASS", "WARN", "BLOCK", "REQUIRE_HUMAN_STAMP", "DEFER_FOR_MISSING_EVIDENCE"):
                    action = "BLOCK"
                severity = "HIGH" if action == "BLOCK" else "MEDIUM"

                decision = build_decision(
                    decision_id=decision_id,
                    constraint=constraint,
                    evidence=evidence,
                    action=action,
                    severity=severity,
                    rationale=(
                        f"Constraint {constraint.rule_id} triggered: "
                        f"evidence '{violation_key}' = False indicates violation."
                    ),
                )
            else:
                # All good — PASS
                decision = build_decision(
                    decision_id=decision_id,
                    constraint=constraint,
                    evidence=evidence,
                    action="PASS",
                    severity="INFO",
                    rationale=f"Constraint {constraint.rule_id}: all evidence passes.",
                )

        decisions.append(decision)

    # Aggregate
    agg_action = aggregate_action(decisions)
    agg_severity = aggregate_severity(decisions)

    # Map to pipeline decision
    pipeline_decision = _ACTION_TO_PIPELINE.get(agg_action, "HALT")

    # Collect reasons
    reason_codes: list[str] = []
    halt_reasons: list[str] = []
    partial_reasons: list[str] = []

    for d in decisions:
        reason_codes.append(f"{d.rule_id}:{d.action}")
        mapped = _ACTION_TO_PIPELINE.get(d.action, "HALT")
        if mapped == "HALT":
            halt_reasons.append(d.rationale)
        elif mapped == "PARTIAL":
            partial_reasons.append(d.rationale)

    return {
        "decision": pipeline_decision,
        "constraint_action": agg_action,
        "severity": agg_severity,
        "reason_codes": reason_codes,
        "halt_reasons": halt_reasons,
        "partial_reasons": partial_reasons,
        "decisions_raw": [asdict(d) for d in decisions],
    }
