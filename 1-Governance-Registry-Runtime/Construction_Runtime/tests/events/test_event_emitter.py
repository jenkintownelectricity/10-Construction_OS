"""Tests for RuntimeEventEmitter — deterministic emission at checkpoints."""

import pytest

from runtime.events.event_emitter import RuntimeEventEmitter, EventEmissionError
from runtime.events.bus_adapter import CognitiveBusAdapter, BusPublicationError


def _admitted_bus(event):
    return {"admitted": True, "reason": "admitted", "content_hash": "test"}


def _rejecting_bus(event):
    return {"admitted": False, "reason": "test rejection"}


def _exploding_bus(event):
    raise ConnectionError("bus down")


def _make_emitter(publish_fn=None):
    adapter = CognitiveBusAdapter(publish_fn=publish_fn or _admitted_bus)
    return RuntimeEventEmitter(bus_adapter=adapter)


class TestConditionDetectedEmission:
    """Checkpoint 1: Pipeline entry emits ConditionDetected."""

    def test_emits_successfully(self):
        emitter = _make_emitter()
        result = emitter.emit_condition_detected(
            condition_signature_id="CS-001",
            node_type="structural_joint",
        )
        assert result["admitted"] is True

    def test_event_sent_to_bus(self):
        captured = []

        def capture(event):
            captured.append(event)
            return {"admitted": True, "reason": "ok"}

        emitter = _make_emitter(capture)
        emitter.emit_condition_detected(
            condition_signature_id="CS-001",
            node_type="joint",
            project_id="PRJ-1",
        )
        assert len(captured) == 1
        event = captured[0]
        assert event["event_type"] == "ConditionDetected"
        assert event["event_class"] == "Observation"
        assert event["payload"]["condition_signature_id"] == "CS-001"
        assert event["condition_signature_id"] == "CS-001"


class TestDetailResolvedEmission:
    """Checkpoint 2: Resolution success emits DetailResolved."""

    def test_emits_successfully(self):
        emitter = _make_emitter()
        result = emitter.emit_detail_resolved(
            condition_signature_id="CS-001",
            resolved_detail_id="DET-050",
            resolution_source="detail_resolver",
        )
        assert result["admitted"] is True

    def test_payload_structure(self):
        captured = []

        def capture(event):
            captured.append(event)
            return {"admitted": True, "reason": "ok"}

        emitter = _make_emitter(capture)
        emitter.emit_detail_resolved(
            condition_signature_id="CS-001",
            resolved_detail_id="DET-050",
            resolution_source="resolver",
            pattern_id="PAT-01",
            variant_id="VAR-A",
        )
        payload = captured[0]["payload"]
        assert payload["resolved_detail_id"] == "DET-050"
        assert payload["pattern_id"] == "PAT-01"
        assert payload["variant_id"] == "VAR-A"


class TestArtifactRenderedEmission:
    """Checkpoint 3: Artifact success emits ArtifactRendered."""

    def test_emits_successfully(self):
        emitter = _make_emitter()
        result = emitter.emit_artifact_rendered(
            artifact_id="ART-001",
            artifact_type="DXF",
            renderer_name="DxfRenderer",
        )
        assert result["admitted"] is True

    def test_includes_artifact_id_in_envelope(self):
        captured = []

        def capture(event):
            captured.append(event)
            return {"admitted": True, "reason": "ok"}

        emitter = _make_emitter(capture)
        emitter.emit_artifact_rendered(
            artifact_id="ART-001",
            artifact_type="SVG",
            renderer_name="SvgRenderer",
            instruction_set_id="IS-42",
            lineage_hash="hash123",
        )
        assert captured[0]["artifact_id"] == "ART-001"
        assert captured[0]["payload"]["lineage_hash"] == "hash123"


class TestValidationFailedEmission:
    """Checkpoint 4: Validation failures emit ValidationFailed."""

    def test_emits_successfully(self):
        emitter = _make_emitter()
        result = emitter.emit_validation_failed(
            validation_stage="input_validation",
            error_code="MISSING_FIELD",
            failure_reason="condition_id required",
            pipeline_stage="input_validation",
        )
        assert result["admitted"] is True

    def test_payload_structure(self):
        captured = []

        def capture(event):
            captured.append(event)
            return {"admitted": True, "reason": "ok"}

        emitter = _make_emitter(capture)
        emitter.emit_validation_failed(
            validation_stage="schema",
            error_code="SCHEMA_ERR",
            failure_reason="invalid",
            pipeline_stage="input_validation",
            object_id="OBJ-1",
        )
        payload = captured[0]["payload"]
        assert payload["error_code"] == "SCHEMA_ERR"
        assert payload["object_id"] == "OBJ-1"


class TestRuntimeErrorEmission:
    """Checkpoint 5: Unexpected exceptions emit RuntimeError."""

    def test_emits_successfully(self):
        emitter = _make_emitter()
        result = emitter.emit_runtime_error(
            exception_type="ValueError",
            failure_reason="unexpected None",
            pipeline_stage="rendering",
        )
        assert result["admitted"] is True

    def test_payload_structure(self):
        captured = []

        def capture(event):
            captured.append(event)
            return {"admitted": True, "reason": "ok"}

        emitter = _make_emitter(capture)
        emitter.emit_runtime_error(
            exception_type="IOError",
            failure_reason="disk full",
            pipeline_stage="rendering",
            error_code="IO_001",
        )
        payload = captured[0]["payload"]
        assert payload["exception_type"] == "IOError"
        assert payload["error_code"] == "IO_001"


class TestFailClosedEmission:
    """All emission failures must fail closed."""

    def test_bus_rejection_fails_closed(self):
        emitter = _make_emitter(_rejecting_bus)
        with pytest.raises(EventEmissionError, match="Bus publication failed"):
            emitter.emit_condition_detected(
                condition_signature_id="CS-001",
                node_type="joint",
            )

    def test_bus_exception_fails_closed(self):
        emitter = _make_emitter(_exploding_bus)
        with pytest.raises(EventEmissionError):
            emitter.emit_detail_resolved(
                condition_signature_id="CS-001",
                resolved_detail_id="DET-050",
                resolution_source="resolver",
            )

    def test_emission_error_has_event_type(self):
        emitter = _make_emitter(_rejecting_bus)
        with pytest.raises(EventEmissionError) as exc_info:
            emitter.emit_artifact_rendered(
                artifact_id="ART-001",
                artifact_type="DXF",
                renderer_name="DxfRenderer",
            )
        assert exc_info.value.event_type == "ArtifactRendered"

    def test_emission_error_has_stage(self):
        emitter = _make_emitter(_rejecting_bus)
        with pytest.raises(EventEmissionError) as exc_info:
            emitter.emit_validation_failed(
                validation_stage="schema",
                error_code="ERR",
                failure_reason="bad",
                pipeline_stage="input_validation",
            )
        assert exc_info.value.stage == "input_validation"

    def test_no_silent_continuation(self):
        """Verify emission failure never returns silently."""
        emitter = _make_emitter(_rejecting_bus)
        for method, kwargs in [
            ("emit_condition_detected", {
                "condition_signature_id": "CS-001", "node_type": "joint",
            }),
            ("emit_detail_resolved", {
                "condition_signature_id": "CS-001",
                "resolved_detail_id": "DET-050",
                "resolution_source": "resolver",
            }),
            ("emit_artifact_rendered", {
                "artifact_id": "ART-001",
                "artifact_type": "DXF",
                "renderer_name": "DxfRenderer",
            }),
            ("emit_validation_failed", {
                "validation_stage": "schema",
                "error_code": "ERR",
                "failure_reason": "bad",
                "pipeline_stage": "test",
            }),
            ("emit_runtime_error", {
                "exception_type": "Error",
                "failure_reason": "boom",
                "pipeline_stage": "test",
            }),
        ]:
            with pytest.raises(EventEmissionError):
                getattr(emitter, method)(**kwargs)
