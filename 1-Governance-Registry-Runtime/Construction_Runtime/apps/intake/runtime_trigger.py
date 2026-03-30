"""
Runtime Trigger

Invokes the deterministic drawing runtime for resolved assemblies
and their interface conditions. Produces condition packets for each
triggered condition.

This module invokes the runtime pipeline but does not modify it.
All outputs are derived condition packets — non-canonical, recomputable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from runtime.drawing_engine.pipeline import run_drawing_pipeline, DrawingPipelineResult


@dataclass
class TriggerResult:
    """Derived result of runtime triggering. Non-canonical, recomputable."""

    triggered_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    pipeline_results: list[DrawingPipelineResult] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)


def trigger_runtime(conditions: list[dict[str, Any]]) -> TriggerResult:
    """
    Trigger the deterministic drawing pipeline for a list of conditions.

    Each condition is passed to run_drawing_pipeline. Results are
    collected as derived outputs. The runtime pipeline is not modified.
    Fail-closed: if the condition list is invalid, returns immediately.
    """
    result = TriggerResult()

    if not isinstance(conditions, list) or len(conditions) == 0:
        result.errors.append({
            "code": "EMPTY_CONDITIONS",
            "message": "Must provide at least one condition to trigger.",
        })
        return result

    for condition in conditions:
        result.triggered_count += 1
        pipeline_result = run_drawing_pipeline(condition)
        result.pipeline_results.append(pipeline_result)

        if pipeline_result.success:
            result.success_count += 1
        else:
            result.failure_count += 1

    return result
