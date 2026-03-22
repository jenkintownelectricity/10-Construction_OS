"""Runtime event emitter — deterministic emission at pipeline checkpoints.

Provides the governed interface for emitting runtime observer events.
All emissions are mandatory and fail-closed.
"""

from __future__ import annotations

from typing import Any

from runtime.events.event_types import (
    ConditionDetected,
    DetailResolved,
    ArtifactRendered,
    ValidationFailed,
    RuntimeError as RuntimeErrorType,
)
from runtime.events.event_models import (
    ConditionDetectedPayload,
    DetailResolvedPayload,
    ArtifactRenderedPayload,
    ValidationFailedPayload,
    RuntimeErrorPayload,
)
from runtime.events.event_builder import build_event_envelope, EventBuildError
from runtime.events.bus_adapter import CognitiveBusAdapter, BusPublicationError


class EventEmissionError(Exception):
    """Raised when a required event emission fails.

    This is a fail-closed error. The runtime pipeline must halt.
    """

    def __init__(self, event_type: str, stage: str, reason: str):
        self.event_type = event_type
        self.stage = stage
        self.reason = reason
        super().__init__(
            f"Required event emission failed at {stage}: "
            f"{event_type} — {reason}"
        )


class RuntimeEventEmitter:
    """Deterministic runtime event emitter.

    Emits governed observer facts at mandatory pipeline checkpoints.
    All emissions fail closed — if any required emission fails,
    the pipeline must halt with a deterministic error state.
    """

    def __init__(self, bus_adapter: CognitiveBusAdapter | None = None):
        self._adapter = bus_adapter or CognitiveBusAdapter()

    def emit_condition_detected(
        self,
        condition_signature_id: str,
        node_type: str,
        pipeline_stage: str = "pipeline_entry",
        project_id: str = "",
    ) -> dict[str, Any]:
        """Emit ConditionDetected at pipeline entry.

        Mandatory checkpoint: a valid ConditionSignature has entered
        runtime processing.

        Raises:
            EventEmissionError: On any failure — fail closed.
        """
        payload = ConditionDetectedPayload(
            condition_signature_id=condition_signature_id,
            node_type=node_type,
            pipeline_stage=pipeline_stage,
            project_id=project_id,
        )
        return self._emit(
            event_type=ConditionDetected,
            pipeline_stage=pipeline_stage,
            payload=payload.to_dict(),
            condition_signature_id=condition_signature_id,
        )

    def emit_detail_resolved(
        self,
        condition_signature_id: str,
        resolved_detail_id: str,
        resolution_source: str,
        pipeline_stage: str = "detail_resolution",
        pattern_id: str = "",
        variant_id: str = "",
    ) -> dict[str, Any]:
        """Emit DetailResolved at resolution success.

        Mandatory checkpoint: the governed runtime resolution path has
        resolved the detail/pattern/variant result.

        Raises:
            EventEmissionError: On any failure — fail closed.
        """
        payload = DetailResolvedPayload(
            condition_signature_id=condition_signature_id,
            resolved_detail_id=resolved_detail_id,
            resolution_source=resolution_source,
            pipeline_stage=pipeline_stage,
            pattern_id=pattern_id,
            variant_id=variant_id,
        )
        return self._emit(
            event_type=DetailResolved,
            pipeline_stage=pipeline_stage,
            payload=payload.to_dict(),
            condition_signature_id=condition_signature_id,
        )

    def emit_artifact_rendered(
        self,
        artifact_id: str,
        artifact_type: str,
        renderer_name: str,
        pipeline_stage: str = "artifact_rendering",
        instruction_set_id: str = "",
        lineage_hash: str = "",
    ) -> dict[str, Any]:
        """Emit ArtifactRendered at artifact success.

        Mandatory checkpoint: a renderer has successfully produced
        a valid artifact output.

        Raises:
            EventEmissionError: On any failure — fail closed.
        """
        payload = ArtifactRenderedPayload(
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            renderer_name=renderer_name,
            pipeline_stage=pipeline_stage,
            instruction_set_id=instruction_set_id,
            lineage_hash=lineage_hash,
        )
        return self._emit(
            event_type=ArtifactRendered,
            pipeline_stage=pipeline_stage,
            payload=payload.to_dict(),
            artifact_id=artifact_id,
        )

    def emit_validation_failed(
        self,
        validation_stage: str,
        error_code: str,
        failure_reason: str,
        pipeline_stage: str,
        object_id: str = "",
    ) -> dict[str, Any]:
        """Emit ValidationFailed at any validation failure.

        Mandatory checkpoint: any schema, pipeline, instruction-set,
        artifact, or render validation failure.

        Raises:
            EventEmissionError: On any failure — fail closed.
        """
        payload = ValidationFailedPayload(
            validation_stage=validation_stage,
            error_code=error_code,
            failure_reason=failure_reason,
            pipeline_stage=pipeline_stage,
            object_id=object_id,
        )
        return self._emit(
            event_type=ValidationFailed,
            pipeline_stage=pipeline_stage,
            payload=payload.to_dict(),
        )

    def emit_runtime_error(
        self,
        exception_type: str,
        failure_reason: str,
        pipeline_stage: str,
        error_code: str = "",
    ) -> dict[str, Any]:
        """Emit RuntimeError at unexpected runtime failure.

        Mandatory checkpoint: any unhandled or classified runtime exception.

        Raises:
            EventEmissionError: On any failure — fail closed.
        """
        payload = RuntimeErrorPayload(
            exception_type=exception_type,
            failure_reason=failure_reason,
            pipeline_stage=pipeline_stage,
            error_code=error_code,
        )
        return self._emit(
            event_type=RuntimeErrorType,
            pipeline_stage=pipeline_stage,
            payload=payload.to_dict(),
        )

    def _emit(
        self,
        event_type: str,
        pipeline_stage: str,
        payload: dict[str, Any],
        condition_signature_id: str = "",
        artifact_id: str = "",
    ) -> dict[str, Any]:
        """Build and publish an event — fail closed on any error.

        Returns:
            The bus admission result.

        Raises:
            EventEmissionError: On build or publication failure.
        """
        try:
            envelope = build_event_envelope(
                event_type=event_type,
                pipeline_stage=pipeline_stage,
                payload=payload,
                condition_signature_id=condition_signature_id,
                artifact_id=artifact_id,
            )
        except EventBuildError as exc:
            raise EventEmissionError(
                event_type=event_type,
                stage=pipeline_stage,
                reason=f"Envelope build failed: {exc}",
            ) from exc

        try:
            return self._adapter.publish(envelope)
        except BusPublicationError as exc:
            raise EventEmissionError(
                event_type=event_type,
                stage=pipeline_stage,
                reason=f"Bus publication failed: {exc}",
            ) from exc
