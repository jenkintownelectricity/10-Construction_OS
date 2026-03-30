"""Deterministic emission hooks at required pipeline checkpoints.

These hooks are wired into the runtime pipelines to emit governed
observer events at the five mandatory checkpoint classes:

1. PIPELINE ENTRY       → ConditionDetected
2. RESOLUTION SUCCESS   → DetailResolved
3. ARTIFACT SUCCESS     → ArtifactRendered
4. VALIDATION FAILURE   → ValidationFailed
5. UNEXPECTED FAILURE   → RuntimeError

All hooks fail closed — emission failure is runtime execution failure.
"""

from __future__ import annotations

from typing import Any

from runtime.events.event_emitter import RuntimeEventEmitter, EventEmissionError


def on_pipeline_entry(
    emitter: RuntimeEventEmitter,
    condition_id: str,
    node_type: str,
    project_id: str = "",
) -> dict[str, Any]:
    """Checkpoint 1: PIPELINE ENTRY — emit ConditionDetected.

    Trigger: a valid ConditionSignature has entered runtime processing.

    Raises:
        EventEmissionError: Fail closed on emission failure.
    """
    return emitter.emit_condition_detected(
        condition_signature_id=condition_id,
        node_type=node_type,
        pipeline_stage="pipeline_entry",
        project_id=project_id,
    )


def on_resolution_success(
    emitter: RuntimeEventEmitter,
    condition_id: str,
    detail_id: str,
    resolution_source: str,
    pattern_id: str = "",
    variant_id: str = "",
) -> dict[str, Any]:
    """Checkpoint 2: RESOLUTION SUCCESS — emit DetailResolved.

    Trigger: the governed runtime resolution path has resolved the
    detail/pattern/variant result used by runtime.

    Raises:
        EventEmissionError: Fail closed on emission failure.
    """
    return emitter.emit_detail_resolved(
        condition_signature_id=condition_id,
        resolved_detail_id=detail_id,
        resolution_source=resolution_source,
        pipeline_stage="detail_resolution",
        pattern_id=pattern_id,
        variant_id=variant_id,
    )


def on_artifact_success(
    emitter: RuntimeEventEmitter,
    artifact_id: str,
    artifact_type: str,
    renderer_name: str,
    instruction_set_id: str = "",
    lineage_hash: str = "",
) -> dict[str, Any]:
    """Checkpoint 3: ARTIFACT SUCCESS — emit ArtifactRendered.

    Trigger: a renderer has successfully produced a valid artifact output.

    Raises:
        EventEmissionError: Fail closed on emission failure.
    """
    return emitter.emit_artifact_rendered(
        artifact_id=artifact_id,
        artifact_type=artifact_type,
        renderer_name=renderer_name,
        pipeline_stage="artifact_rendering",
        instruction_set_id=instruction_set_id,
        lineage_hash=lineage_hash,
    )


def on_validation_failure(
    emitter: RuntimeEventEmitter,
    validation_stage: str,
    error_code: str,
    failure_reason: str,
    pipeline_stage: str,
    object_id: str = "",
) -> dict[str, Any]:
    """Checkpoint 4: VALIDATION FAILURE — emit ValidationFailed.

    Trigger: any schema, pipeline, instruction-set, artifact,
    or render validation failure.

    Raises:
        EventEmissionError: Fail closed on emission failure.
    """
    return emitter.emit_validation_failed(
        validation_stage=validation_stage,
        error_code=error_code,
        failure_reason=failure_reason,
        pipeline_stage=pipeline_stage,
        object_id=object_id,
    )


def on_unexpected_failure(
    emitter: RuntimeEventEmitter,
    exception: Exception,
    pipeline_stage: str,
    error_code: str = "",
) -> dict[str, Any]:
    """Checkpoint 5: UNEXPECTED RUNTIME FAILURE — emit RuntimeError.

    Trigger: any unhandled or classified runtime exception.

    Raises:
        EventEmissionError: Fail closed on emission failure.
    """
    return emitter.emit_runtime_error(
        exception_type=type(exception).__name__,
        failure_reason=str(exception),
        pipeline_stage=pipeline_stage,
        error_code=error_code,
    )
