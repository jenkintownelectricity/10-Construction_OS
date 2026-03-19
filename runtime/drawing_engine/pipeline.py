"""
Drawing Engine Pipeline

Orchestrates the deterministic drawing runtime pipeline:
1. Input validation
2. Detail resolution
3. Parameterization
4. IR emission
5. Rendering
6. Audit logging
7. Derived output generation

Given the same governed inputs, produces the same outputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from runtime.drawing_engine.audit_log import AuditLog
from runtime.drawing_engine.input_validator import validate_drawing_inputs
from runtime.drawing_engine.detail_resolver import resolve_detail
from runtime.drawing_engine.parameterizer import parameterize_detail
from runtime.drawing_engine.ir_emitter import emit_ir
from runtime.drawing_engine.renderer import render_svg, render_dxf_stub
from runtime.drawing_engine.derived_outputs import (
    ConditionPacket,
    derive_issues,
    derive_route,
    derive_review_summary,
    build_condition_packet,
)


@dataclass
class DrawingPipelineResult:
    """Complete result of the drawing pipeline."""

    success: bool = False
    condition_id: str = ""
    detail_id: str = ""
    ir_instruction_count: int = 0
    render_result: dict[str, Any] = field(default_factory=dict)
    condition_packet: ConditionPacket | None = None
    audit_log: dict[str, Any] = field(default_factory=dict)
    errors: list[dict[str, str]] = field(default_factory=list)


def run_drawing_pipeline(condition: dict[str, Any]) -> DrawingPipelineResult:
    """
    Run the deterministic drawing pipeline for a single condition.

    Stages:
    1. Input validation — fail-closed on missing/ambiguous inputs
    2. Detail resolution — select governed canonical detail logic
    3. Parameterization — bind parameters to concrete values
    4. IR emission — emit construction-semantic instructions
    5. Rendering — produce SVG/DXF from IR
    6. Audit logging — record all decisions
    7. Derived outputs — issues, routes, reviews, condition packet
    """
    pipeline_result = DrawingPipelineResult(
        condition_id=condition.get("condition_id", "unknown"),
    )
    audit = AuditLog(condition_id=pipeline_result.condition_id)

    # Stage 1: Input Validation
    validation = validate_drawing_inputs(condition)
    audit.record(
        stage="input_validation",
        status="success" if validation.is_valid else "failure",
        message="Input validation " + ("passed" if validation.is_valid else "failed"),
        data={"errors": validation.errors, "warnings": validation.warnings},
    )

    if not validation.is_valid:
        audit.final_status = "failed_validation"
        pipeline_result.errors = validation.errors
        pipeline_result.audit_log = audit.to_dict()
        # Build derived outputs even on failure
        issues = derive_issues(pipeline_result.condition_id, audit)
        route = derive_route(pipeline_result.condition_id, audit)
        pipeline_result.condition_packet = build_condition_packet(
            condition, "", audit, issues, route, None,
        )
        return pipeline_result

    # Stage 2: Detail Resolution
    resolution = resolve_detail(condition)
    audit.record(
        stage="detail_resolution",
        status="success" if resolution.resolved else "failure",
        message=f"Detail resolution: {resolution.detail_id or 'unresolved'}",
        detail_id=resolution.detail_id,
        data={"errors": resolution.errors},
    )

    if not resolution.resolved:
        audit.final_status = "failed_detail_resolution"
        pipeline_result.errors = resolution.errors
        pipeline_result.audit_log = audit.to_dict()
        issues = derive_issues(pipeline_result.condition_id, audit)
        route = derive_route(pipeline_result.condition_id, audit)
        pipeline_result.condition_packet = build_condition_packet(
            condition, "", audit, issues, route, None,
        )
        return pipeline_result

    pipeline_result.detail_id = resolution.detail_id

    # Stage 3: Parameterization
    material_refs = condition.get("material_references", {})
    parameters = condition.get("parameters", {})

    param_result = parameterize_detail(
        resolution.components, material_refs, parameters,
    )
    audit.record(
        stage="parameterization",
        status="success" if param_result.resolved else "failure",
        message="Parameterization " + ("resolved" if param_result.resolved else "failed"),
        detail_id=resolution.detail_id,
        data={"errors": param_result.errors},
    )

    if not param_result.resolved:
        audit.final_status = "failed_parameterization"
        pipeline_result.errors = param_result.errors
        pipeline_result.audit_log = audit.to_dict()
        issues = derive_issues(pipeline_result.condition_id, audit)
        route = derive_route(pipeline_result.condition_id, audit)
        pipeline_result.condition_packet = build_condition_packet(
            condition, resolution.detail_id, audit, issues, route, None,
        )
        return pipeline_result

    # Stage 4: IR Emission
    view_intent = condition.get("view_intent", {})
    ir_result = emit_ir(
        resolution.detail_id,
        param_result.resolved_components,
        resolution.relationships,
        param_result.resolved_parameters,
        view_intent,
    )
    audit.record(
        stage="ir_emission",
        status="success" if ir_result.emitted else "failure",
        message=f"IR emission: {len(ir_result.instructions)} instructions",
        detail_id=resolution.detail_id,
        data={"instruction_count": len(ir_result.instructions), "errors": ir_result.errors},
    )

    if not ir_result.emitted:
        audit.final_status = "failed_ir_emission"
        pipeline_result.errors = ir_result.errors
        pipeline_result.audit_log = audit.to_dict()
        issues = derive_issues(pipeline_result.condition_id, audit)
        route = derive_route(pipeline_result.condition_id, audit)
        pipeline_result.condition_packet = build_condition_packet(
            condition, resolution.detail_id, audit, issues, route, None,
        )
        return pipeline_result

    pipeline_result.ir_instruction_count = len(ir_result.instructions)

    # Stage 5: Rendering
    svg_result = render_svg(resolution.detail_id, ir_result.instructions)
    audit.record(
        stage="rendering",
        status="success" if svg_result.get("render_status") == "success" else "failure",
        message=f"SVG rendering: {svg_result.get('element_count', 0)} elements",
        detail_id=resolution.detail_id,
        data={"format": "svg", "element_count": svg_result.get("element_count", 0)},
    )

    pipeline_result.render_result = svg_result

    # Stage 6: Final audit
    audit.final_status = "success"
    audit.record(
        stage="pipeline_complete",
        status="success",
        message="Drawing pipeline completed successfully",
        detail_id=resolution.detail_id,
    )

    # Stage 7: Derived outputs
    issues = derive_issues(pipeline_result.condition_id, audit)
    route = derive_route(pipeline_result.condition_id, audit)
    pipeline_result.condition_packet = build_condition_packet(
        condition, resolution.detail_id, audit, issues, route, svg_result,
    )

    pipeline_result.success = True
    pipeline_result.audit_log = audit.to_dict()

    return pipeline_result
