"""
Runtime Bridge — VKBUS InteractionKernel ↔ Construction Runtime

Exposes runtime engines as a deterministic, fail-closed facade.
The bridge never mutates truth and only returns computed results.

Export contract:
    evaluate_condition_graph(change_set) → ConditionGraphResult
    resolve_detail(context)             → DetailResult
    render_artifact(manifest)           → ArtifactResult
    validate_state(state)               → ValidationStateResult
"""

from __future__ import annotations

from typing import Any

from runtime.interaction.runtime_bridge_types import (
    ArtifactResult,
    ChangeSet,
    ConditionGraphResult,
    DetailResult,
    RenderManifest,
    ResolutionContext,
    StateSnapshot,
    ValidationStateResult,
)

# ── Engine imports ──────────────────────────────────────────────────

from runtime.condition_graph.condition_graph_validator import (
    validate_condition_graph as _validate_graph,
)
from runtime.drawing_engine.detail_resolver import (
    resolve_detail as _resolve_detail,
)
from runtime.drawing_engine.pipeline import run_drawing_pipeline
from runtime.drawing_engine.input_validator import validate_drawing_inputs
from runtime.detail_resolver.detail_resolution_validator import (
    validate_resolution_manifest as _validate_resolution,
)


# ── WHAT IF → condition_graph ───────────────────────────────────────


def evaluate_condition_graph(change_set: ChangeSet) -> ConditionGraphResult:
    """Evaluate a condition graph for structural validity.

    Delegates to condition_graph.evaluate (the graph validator).
    Deterministic: same graph always produces same validation result.
    Fail-closed: any structural issue surfaces as an error.
    """
    graph = change_set.graph

    if not graph:
        return ConditionGraphResult(
            success=False,
            errors=("ChangeSet contains an empty graph.",),
        )

    errors = _validate_graph(graph)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    return ConditionGraphResult(
        success=len(errors) == 0,
        errors=tuple(errors),
        node_count=len(nodes),
        edge_count=len(edges),
    )


# ── DETAIL → detail_resolver ───────────────────────────────────────


def resolve_detail(context: ResolutionContext) -> DetailResult:
    """Resolve canonical detail logic for a condition.

    Delegates to detail_resolver.resolve.
    Deterministic: same condition always selects the same governed detail.
    Fail-closed: unresolved or ambiguous matches return errors.
    """
    condition = context.condition

    if not condition:
        return DetailResult(
            resolved=False,
            errors=({"code": "EMPTY_CONTEXT", "message": "ResolutionContext contains an empty condition.", "path": "condition"},),
        )

    result = _resolve_detail(condition)

    return DetailResult(
        resolved=result.resolved,
        detail_id=result.detail_id,
        detail_family=result.detail_family,
        components=tuple(result.components),
        relationships=tuple(result.relationships),
        parameter_bindings=result.parameter_bindings,
        errors=tuple(result.errors),
    )


# ── DRAWING → artifact_renderer ────────────────────────────────────


def render_artifact(manifest: RenderManifest) -> ArtifactResult:
    """Render a drawing artifact through the full deterministic pipeline.

    Delegates to artifact_renderer.render (the drawing pipeline).
    Deterministic: same governed inputs always produce the same SVG/DXF.
    Fail-closed: missing or ambiguous inputs stop execution with errors.
    """
    condition = manifest.condition

    if not condition:
        return ArtifactResult(
            success=False,
            errors=({"code": "EMPTY_MANIFEST", "message": "RenderManifest contains an empty condition.", "path": "condition"},),
        )

    pipeline_result = run_drawing_pipeline(condition)

    render = pipeline_result.render_result

    return ArtifactResult(
        success=pipeline_result.success,
        condition_id=pipeline_result.condition_id,
        detail_id=pipeline_result.detail_id,
        render_status=render.get("render_status", ""),
        format=render.get("format", ""),
        svg_content=render.get("svg_content", ""),
        instruction_count=pipeline_result.ir_instruction_count,
        element_count=render.get("element_count", 0),
        errors=tuple(pipeline_result.errors),
    )


# ── Validators → validators.run ────────────────────────────────────


def validate_state(state: StateSnapshot) -> ValidationStateResult:
    """Validate a runtime state artifact.

    Dispatches to the appropriate validator based on state.kind.
    Deterministic: same payload always produces the same validation.
    Fail-closed: unknown kinds are rejected.
    """
    if not state.kind:
        return ValidationStateResult(
            valid=False,
            errors=("StateSnapshot.kind is required.",),
        )

    if not state.payload:
        return ValidationStateResult(
            valid=False,
            errors=("StateSnapshot.payload is empty.",),
        )

    if state.kind == "condition_graph":
        errors = _validate_graph(state.payload)
        return ValidationStateResult(
            valid=len(errors) == 0,
            errors=tuple(errors),
        )

    if state.kind == "resolution_manifest":
        errors = _validate_resolution(state.payload)
        return ValidationStateResult(
            valid=len(errors) == 0,
            errors=tuple(errors),
        )

    if state.kind == "drawing_input":
        result = validate_drawing_inputs(state.payload)
        error_msgs = tuple(
            f"{e['code']}: {e['message']}" for e in result.errors
        )
        return ValidationStateResult(
            valid=result.is_valid,
            errors=error_msgs,
        )

    return ValidationStateResult(
        valid=False,
        errors=(f"Unknown state kind: '{state.kind}'. Expected 'condition_graph', 'resolution_manifest', or 'drawing_input'.",),
    )
