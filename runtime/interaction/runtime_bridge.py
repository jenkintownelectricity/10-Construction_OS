"""
Runtime Bridge — the only public entrypoint for runtime engines.

All external consumers must use this module instead of importing
engine internals directly. This keeps engine implementations free
to change without breaking downstream callers.
"""

from __future__ import annotations

from typing import Any

from runtime.condition_graph.condition_graph_validator import (
    validate_condition_graph as _validate_condition_graph,
)
from runtime.drawing_engine.detail_resolver import (
    DetailResolutionResult,
    resolve_detail as _resolve_detail,
)
from runtime.artifact_renderer.renderer_pipeline import (
    render_artifacts as _render_artifacts,
)
from runtime.artifact_renderer.artifact_contract import (
    RenderManifest,
    RenderResult,
)
from runtime.artifact_renderer.renderer_registry import RendererRegistry
from runtime.drawing_engine.input_validator import (
    ValidationResult,
    validate_drawing_inputs as _validate_drawing_inputs,
)


def evaluate_condition_graph(graph: dict[str, Any]) -> list[str]:
    """Validate a condition graph and return any errors.

    Delegates to the condition-graph validator. Returns an empty list
    when the graph is structurally valid.
    """
    return _validate_condition_graph(graph)


def resolve_detail(condition: dict[str, Any]) -> DetailResolutionResult:
    """Resolve a canonical detail from governed applicability rules.

    Delegates to the drawing-engine detail resolver. Fail-closed: if no
    governed detail applies the result will have ``resolved=False``.
    """
    return _resolve_detail(condition)


def render_artifact(
    manifest: RenderManifest | dict[str, Any],
    detail_dna: dict[str, Any] | None = None,
    variant_params: dict[str, Any] | None = None,
    registry: RendererRegistry | None = None,
) -> RenderResult:
    """Render artifacts from a manifest.

    Delegates to the artifact-renderer pipeline.
    """
    return _render_artifacts(
        manifest,
        detail_dna=detail_dna,
        variant_params=variant_params,
        registry=registry,
    )


def validate_state(condition: dict[str, Any]) -> ValidationResult:
    """Validate governed runtime state before translation or rendering.

    Delegates to the drawing-engine input validator. Fail-closed: any
    missing or ambiguous input produces an invalid result.
    """
    return _validate_drawing_inputs(condition)
