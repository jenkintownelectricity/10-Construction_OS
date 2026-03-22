"""Tests for deterministic pipeline emission hooks."""

import pytest

from runtime.events.event_emitter import RuntimeEventEmitter, EventEmissionError
from runtime.events.bus_adapter import CognitiveBusAdapter
from runtime.events.pipeline_hooks import (
    on_pipeline_entry,
    on_resolution_success,
    on_artifact_success,
    on_validation_failure,
    on_unexpected_failure,
)


def _make_emitter(captured_events):
    def capture(event):
        captured_events.append(event)
        return {"admitted": True, "reason": "admitted"}

    adapter = CognitiveBusAdapter(publish_fn=capture)
    return RuntimeEventEmitter(bus_adapter=adapter)


def _make_failing_emitter():
    def reject(event):
        return {"admitted": False, "reason": "test rejection"}

    adapter = CognitiveBusAdapter(publish_fn=reject)
    return RuntimeEventEmitter(bus_adapter=adapter)


class TestPipelineEntryHook:
    def test_emits_condition_detected(self):
        events = []
        emitter = _make_emitter(events)
        on_pipeline_entry(emitter, condition_id="CS-001", node_type="joint")
        assert len(events) == 1
        assert events[0]["event_type"] == "ConditionDetected"
        assert events[0]["pipeline_stage"] == "pipeline_entry"

    def test_fails_closed(self):
        emitter = _make_failing_emitter()
        with pytest.raises(EventEmissionError):
            on_pipeline_entry(emitter, condition_id="CS-001", node_type="joint")


class TestResolutionSuccessHook:
    def test_emits_detail_resolved(self):
        events = []
        emitter = _make_emitter(events)
        on_resolution_success(
            emitter,
            condition_id="CS-001",
            detail_id="DET-050",
            resolution_source="resolver",
        )
        assert events[0]["event_type"] == "DetailResolved"
        assert events[0]["pipeline_stage"] == "detail_resolution"

    def test_fails_closed(self):
        emitter = _make_failing_emitter()
        with pytest.raises(EventEmissionError):
            on_resolution_success(
                emitter, condition_id="CS-001",
                detail_id="DET", resolution_source="res",
            )


class TestArtifactSuccessHook:
    def test_emits_artifact_rendered(self):
        events = []
        emitter = _make_emitter(events)
        on_artifact_success(
            emitter,
            artifact_id="ART-001",
            artifact_type="DXF",
            renderer_name="DxfRenderer",
        )
        assert events[0]["event_type"] == "ArtifactRendered"
        assert events[0]["pipeline_stage"] == "artifact_rendering"

    def test_fails_closed(self):
        emitter = _make_failing_emitter()
        with pytest.raises(EventEmissionError):
            on_artifact_success(
                emitter, artifact_id="ART-001",
                artifact_type="DXF", renderer_name="DxfRenderer",
            )


class TestValidationFailureHook:
    def test_emits_validation_failed(self):
        events = []
        emitter = _make_emitter(events)
        on_validation_failure(
            emitter,
            validation_stage="input_validation",
            error_code="MISSING_FIELD",
            failure_reason="condition_id required",
            pipeline_stage="input_validation",
        )
        assert events[0]["event_type"] == "ValidationFailed"

    def test_fails_closed(self):
        emitter = _make_failing_emitter()
        with pytest.raises(EventEmissionError):
            on_validation_failure(
                emitter, validation_stage="schema",
                error_code="ERR", failure_reason="bad",
                pipeline_stage="test",
            )


class TestUnexpectedFailureHook:
    def test_emits_runtime_error(self):
        events = []
        emitter = _make_emitter(events)
        exc = ValueError("unexpected null pointer")
        on_unexpected_failure(emitter, exception=exc, pipeline_stage="rendering")
        assert events[0]["event_type"] == "RuntimeError"
        assert events[0]["payload"]["exception_type"] == "ValueError"
        assert events[0]["payload"]["failure_reason"] == "unexpected null pointer"

    def test_fails_closed(self):
        emitter = _make_failing_emitter()
        with pytest.raises(EventEmissionError):
            on_unexpected_failure(
                emitter, exception=RuntimeError("boom"),
                pipeline_stage="test",
            )
