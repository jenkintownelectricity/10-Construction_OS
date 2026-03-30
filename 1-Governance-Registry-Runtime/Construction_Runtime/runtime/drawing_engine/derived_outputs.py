"""
Derived Output Surfaces

Produces derived, non-canonical, recomputable runtime outputs:
- Issue surface (structured runtime issues)
- Route surface (dependency/blocking paths)
- Review surface (review-ready summaries)
- Condition packet (app-ready structured inspection object)

These outputs do not create new construction truth.
They summarize or route already-governed conditions and runtime outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from runtime.drawing_engine.audit_log import AuditLog


@dataclass
class RuntimeIssue:
    """A structured runtime issue for an unresolved condition."""

    issue_type: str = ""
    severity: str = ""
    condition_id: str = ""
    message: str = ""
    source_stage: str = ""
    blocking: bool = False


@dataclass
class RuntimeRoute:
    """A derived dependency/blocking path for a condition."""

    condition_id: str = ""
    stages: list[dict[str, str]] = field(default_factory=list)
    final_state: str = ""
    blocking_stage: str = ""


@dataclass
class ReviewSummary:
    """A derived review-ready summary."""

    condition_id: str = ""
    blocking_conditions: list[str] = field(default_factory=list)
    coordination_required: list[str] = field(default_factory=list)
    unresolved_materials: list[str] = field(default_factory=list)
    unresolved_scope: list[str] = field(default_factory=list)
    completed_stages: list[str] = field(default_factory=list)


@dataclass
class ConditionPacket:
    """
    A single app-ready structured runtime packet per condition.

    Derived, non-canonical, recomputable from governed truth + runtime state.
    """

    condition_id: str = ""
    assembly_id: str = ""
    component_ids: list[str] = field(default_factory=list)
    detail_id: str = ""
    view_intent_id: str = ""
    parameter_state: str = ""
    issue_state: str = ""
    route_state: str = ""
    render_state: str = ""
    output_artifact_refs: list[str] = field(default_factory=list)
    readiness_state: str = ""
    gaps: list[str] = field(default_factory=list)


def derive_issues(
    condition_id: str,
    audit_log: AuditLog,
) -> list[RuntimeIssue]:
    """Derive structured issues from audit log entries."""
    issues: list[RuntimeIssue] = []

    for entry in audit_log.entries:
        if entry.status == "failure":
            issue_type = _classify_issue(entry.data)
            issues.append(RuntimeIssue(
                issue_type=issue_type,
                severity="blocking" if issue_type != "warning" else "non_blocking",
                condition_id=condition_id,
                message=entry.message,
                source_stage=entry.stage,
                blocking=True,
            ))

    return issues


def derive_route(
    condition_id: str,
    audit_log: AuditLog,
) -> RuntimeRoute:
    """Derive a dependency/blocking path from audit log."""
    route = RuntimeRoute(condition_id=condition_id)
    stages: list[dict[str, str]] = []
    blocking_stage = ""

    for entry in audit_log.entries:
        stages.append({
            "stage": entry.stage,
            "status": entry.status,
        })
        if entry.status == "failure" and not blocking_stage:
            blocking_stage = entry.stage

    route.stages = stages
    route.blocking_stage = blocking_stage
    route.final_state = audit_log.final_status

    return route


def derive_review_summary(
    condition_id: str,
    issues: list[RuntimeIssue],
    audit_log: AuditLog,
) -> ReviewSummary:
    """Derive a review-ready summary from issues and audit log."""
    summary = ReviewSummary(condition_id=condition_id)

    for issue in issues:
        if issue.blocking:
            summary.blocking_conditions.append(issue.message)
        if "material" in issue.issue_type:
            summary.unresolved_materials.append(issue.message)
        if "scope" in issue.issue_type:
            summary.unresolved_scope.append(issue.message)
        if "coordination" in issue.issue_type:
            summary.coordination_required.append(issue.message)

    for entry in audit_log.entries:
        if entry.status == "success":
            summary.completed_stages.append(entry.stage)

    return summary


def build_condition_packet(
    condition: dict[str, Any],
    detail_id: str,
    audit_log: AuditLog,
    issues: list[RuntimeIssue],
    route: RuntimeRoute,
    render_result: dict[str, Any] | None,
) -> ConditionPacket:
    """
    Build a single app-ready structured runtime packet per condition.

    Fail-closed: if the packet cannot be assembled from governed truth
    plus runtime state, surfaces explicit gaps rather than filling by inference.
    """
    packet = ConditionPacket(
        condition_id=condition.get("condition_id", ""),
        assembly_id=condition.get("assembly_id", ""),
        detail_id=detail_id,
        view_intent_id=condition.get("view_intent", {}).get("view_intent_type", ""),
    )

    # Component IDs from condition
    packet.component_ids = condition.get("component_ids", [])

    # Parameter state
    if condition.get("parameters"):
        packet.parameter_state = "resolved"
    else:
        packet.parameter_state = "unresolved"
        packet.gaps.append("parameters_missing")

    # Issue state
    if issues:
        blocking = [i for i in issues if i.blocking]
        packet.issue_state = f"{len(blocking)}_blocking" if blocking else "non_blocking"
    else:
        packet.issue_state = "clear"

    # Route state
    packet.route_state = route.final_state

    # Render state
    if render_result and render_result.get("render_status") == "success":
        packet.render_state = "rendered"
        packet.output_artifact_refs.append(f"svg:{detail_id}")
    else:
        packet.render_state = "not_rendered"
        packet.gaps.append("render_incomplete")

    # Readiness state
    if packet.issue_state == "clear" and packet.render_state == "rendered":
        packet.readiness_state = "ready"
    elif packet.gaps:
        packet.readiness_state = "incomplete"
    else:
        packet.readiness_state = "blocked"

    return packet


def _classify_issue(data: dict[str, Any]) -> str:
    """Classify issue type from audit entry data."""
    errors = data.get("errors", [])
    if not errors:
        return "unknown_failure"

    first_code = ""
    if isinstance(errors, list) and errors:
        first_error = errors[0]
        if isinstance(first_error, dict):
            first_code = first_error.get("code", "")
        elif isinstance(first_error, str):
            first_code = first_error

    code_map = {
        "MISSING_REQUIRED_INPUT": "missing_required_input",
        "UNRESOLVED_DETAIL_APPLICABILITY": "unresolved_detail_applicability",
        "CONFLICTING_DETAIL_APPLICABILITY": "conflicting_detail_applicability",
        "UNSUPPORTED_PARAMETERIZATION": "unsupported_parameterization",
        "INVALID_MATERIAL_REFERENCE": "unknown_material_reference",
        "INCOMPLETE_VIEW_INTENT": "incomplete_view_intent",
        "IR_EMISSION_FAILURE": "ir_emission_failure",
    }

    return code_map.get(first_code, "unknown_failure")
