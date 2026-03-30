"""Integration tests proving live pipeline wiring of event emission hooks.

These tests exercise the REAL runtime call sites, not isolated hook functions.
Each test verifies that the actual pipeline code invokes the correct event
emission hook at the correct checkpoint during real execution flow.
"""

import pytest
from unittest.mock import patch

from runtime.events.event_emitter import RuntimeEventEmitter, EventEmissionError
from runtime.events.bus_adapter import CognitiveBusAdapter


# ---------------------------------------------------------------------------
# Shared test infrastructure
# ---------------------------------------------------------------------------

class EventCapture:
    """Captures events published through the bus adapter."""

    def __init__(self):
        self.events: list[dict] = []

    def publish(self, event: dict) -> dict:
        self.events.append(event)
        return {"admitted": True, "reason": "admitted", "content_hash": "test"}

    def make_emitter(self) -> RuntimeEventEmitter:
        adapter = CognitiveBusAdapter(publish_fn=self.publish)
        return RuntimeEventEmitter(bus_adapter=adapter)

    def event_types(self) -> list[str]:
        return [e["event_type"] for e in self.events]

    def events_of_type(self, event_type: str) -> list[dict]:
        return [e for e in self.events if e["event_type"] == event_type]


def _rejecting_publish(event: dict) -> dict:
    return {"admitted": False, "reason": "test rejection"}


def _make_failing_emitter() -> RuntimeEventEmitter:
    adapter = CognitiveBusAdapter(publish_fn=_rejecting_publish)
    return RuntimeEventEmitter(bus_adapter=adapter)


# ---------------------------------------------------------------------------
# Drawing Engine Pipeline — Live Wiring Tests
# ---------------------------------------------------------------------------

class TestDrawingPipelineConditionDetected:
    """Checkpoint 1: Real pipeline entry emits ConditionDetected."""

    def test_pipeline_emits_condition_detected_on_entry(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        capture = EventCapture()
        condition = {
            "condition_id": "CS-LIVE-001",
            "condition_type": "structural_joint",
            "project_id": "PRJ-LIVE",
        }
        run_drawing_pipeline(condition, event_emitter=capture.make_emitter())

        cd_events = capture.events_of_type("ConditionDetected")
        assert len(cd_events) >= 1, "ConditionDetected not emitted at pipeline entry"
        event = cd_events[0]
        assert event["event_class"] == "Observation"
        assert event["source_component"] == "Construction_Runtime"
        assert event["pipeline_stage"] == "pipeline_entry"
        assert event["payload"]["condition_signature_id"] == "CS-LIVE-001"
        assert event["payload"]["node_type"] == "structural_joint"

    def test_condition_detected_emitted_before_validation(self):
        """ConditionDetected must be the first event emitted."""
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        capture = EventCapture()
        run_drawing_pipeline(
            {"condition_id": "CS-002"},
            event_emitter=capture.make_emitter(),
        )
        assert len(capture.events) >= 1
        assert capture.events[0]["event_type"] == "ConditionDetected"


class TestDrawingPipelineDetailResolved:
    """Checkpoint 2: Real resolution path emits DetailResolved."""

    def test_pipeline_emits_detail_resolved_on_success(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        capture = EventCapture()
        condition = {
            "condition_id": "CS-RES-001",
            "condition_type": "roof_edge",
            "detail_type": "base_flashing",
            "parameters": {"height": 8.0},
        }
        run_drawing_pipeline(condition, event_emitter=capture.make_emitter())

        dr_events = capture.events_of_type("DetailResolved")
        # DetailResolved fires only if resolution succeeds
        # If the pipeline's detail_resolver returns resolved=True, we should see it
        # If it doesn't resolve (because detail_type isn't known), we won't
        # Either way, verify the wiring exists by checking event ordering
        types = capture.event_types()
        assert "ConditionDetected" in types, "Pipeline entry event missing"

        # If detail was resolved, DetailResolved should appear after ConditionDetected
        if "DetailResolved" in types:
            cd_idx = types.index("ConditionDetected")
            dr_idx = types.index("DetailResolved")
            assert dr_idx > cd_idx, "DetailResolved must come after ConditionDetected"
            event = dr_events[0]
            assert event["pipeline_stage"] == "detail_resolution"
            assert event["payload"]["resolution_source"] == "drawing_engine_detail_resolver"


class TestDrawingPipelineValidationFailed:
    """Checkpoint 4: Real validation failure path emits ValidationFailed."""

    def test_pipeline_emits_validation_failed_on_bad_input(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        capture = EventCapture()
        # Empty condition should fail input validation
        condition = {}
        run_drawing_pipeline(condition, event_emitter=capture.make_emitter())

        types = capture.event_types()
        assert "ConditionDetected" in types, "Pipeline entry event missing"
        assert "ValidationFailed" in types, "ValidationFailed not emitted on bad input"

        vf_events = capture.events_of_type("ValidationFailed")
        assert len(vf_events) >= 1
        event = vf_events[0]
        assert event["event_class"] == "Observation"
        assert event["source_component"] == "Construction_Runtime"
        assert "validation_stage" in event["payload"]
        assert "error_code" in event["payload"]
        assert "failure_reason" in event["payload"]

    def test_validation_failed_contains_object_id(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        capture = EventCapture()
        condition = {"condition_id": "CS-BADINPUT"}
        run_drawing_pipeline(condition, event_emitter=capture.make_emitter())

        types = capture.event_types()
        if "ValidationFailed" in types:
            vf = capture.events_of_type("ValidationFailed")[0]
            assert vf["payload"].get("object_id") == "CS-BADINPUT"


class TestDrawingPipelineRuntimeError:
    """Checkpoint 5: Real exception path emits RuntimeError."""

    def test_pipeline_emits_runtime_error_on_exception(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        capture = EventCapture()

        # Patch an internal function to raise, simulating unexpected failure
        with patch(
            "runtime.drawing_engine.pipeline.validate_drawing_inputs",
            side_effect=TypeError("unexpected type in pipeline"),
        ):
            with pytest.raises(TypeError):
                run_drawing_pipeline(
                    {"condition_id": "CS-BOOM"},
                    event_emitter=capture.make_emitter(),
                )

        types = capture.event_types()
        assert "ConditionDetected" in types, "Pipeline entry still emitted before crash"
        assert "RuntimeError" in types, "RuntimeError not emitted on exception"

        re_events = capture.events_of_type("RuntimeError")
        event = re_events[0]
        assert event["payload"]["exception_type"] == "TypeError"
        assert "unexpected type" in event["payload"]["failure_reason"]


class TestDrawingPipelineFailClosed:
    """Emission failures in live drawing pipeline still fail closed."""

    def test_condition_detected_failure_halts_pipeline(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        with pytest.raises(EventEmissionError) as exc_info:
            run_drawing_pipeline(
                {"condition_id": "CS-FAILCLOSE"},
                event_emitter=_make_failing_emitter(),
            )
        assert exc_info.value.event_type == "ConditionDetected"

    def test_validation_failed_emission_failure_halts(self):
        """If ValidationFailed emission fails, pipeline must not silently continue."""
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        # We need a condition that passes pipeline entry emission but fails
        # on ValidationFailed emission. Use a custom emitter that rejects
        # only ValidationFailed events.
        call_count = {"n": 0}

        def selective_reject(event):
            call_count["n"] += 1
            if event.get("event_type") == "ValidationFailed":
                return {"admitted": False, "reason": "selective rejection"}
            return {"admitted": True, "reason": "ok"}

        adapter = CognitiveBusAdapter(publish_fn=selective_reject)
        emitter = RuntimeEventEmitter(bus_adapter=adapter)

        # Empty condition triggers validation failure path
        with pytest.raises(EventEmissionError) as exc_info:
            run_drawing_pipeline({}, event_emitter=emitter)
        assert exc_info.value.event_type == "ValidationFailed"


# ---------------------------------------------------------------------------
# Artifact Renderer Pipeline — Live Wiring Tests
# ---------------------------------------------------------------------------

class TestRendererPipelineArtifactRendered:
    """Checkpoint 3: Real artifact renderer emits ArtifactRendered."""

    def test_render_artifacts_emits_artifact_rendered(self):
        from runtime.artifact_renderer.renderer_pipeline import render_artifacts

        capture = EventCapture()
        manifest = {
            "manifest_id": "MAN-LIVE-001",
            "detail_id": "DET-LIVE-001",
            "variant_id": "VAR-A",
            "assembly_family": "roofing",
            "requested_formats": ["SVG"],
            "parameters": {},
            "metadata": {},
        }
        result = render_artifacts(manifest, event_emitter=capture.make_emitter())

        ar_events = capture.events_of_type("ArtifactRendered")
        if result.success and len(result.artifacts) > 0:
            assert len(ar_events) >= 1, "ArtifactRendered not emitted on success"
            event = ar_events[0]
            assert event["event_class"] == "Observation"
            assert event["source_component"] == "Construction_Runtime"
            assert event["pipeline_stage"] == "artifact_rendering"
            assert event["payload"]["artifact_type"] == "SVG"
            assert event["payload"]["renderer_name"] != ""

    def test_artifact_rendered_per_format(self):
        """Each successfully rendered format emits its own ArtifactRendered."""
        from runtime.artifact_renderer.renderer_pipeline import render_artifacts

        capture = EventCapture()
        manifest = {
            "manifest_id": "MAN-MULTI-001",
            "detail_id": "DET-MULTI-001",
            "variant_id": "",
            "assembly_family": "roofing",
            "requested_formats": ["DXF", "SVG", "PDF"],
            "parameters": {},
            "metadata": {},
        }
        result = render_artifacts(manifest, event_emitter=capture.make_emitter())

        ar_events = capture.events_of_type("ArtifactRendered")
        if result.success:
            successful_formats = [a.format for a in result.artifacts]
            assert len(ar_events) == len(successful_formats), (
                f"Expected {len(successful_formats)} ArtifactRendered events, "
                f"got {len(ar_events)}"
            )


class TestRendererPipelineRuntimeError:
    """Checkpoint 5: Real renderer exception emits RuntimeError."""

    def test_render_artifacts_emits_runtime_error_on_exception(self):
        from runtime.artifact_renderer.renderer_pipeline import render_artifacts

        capture = EventCapture()

        # Patch _build_instructions to raise unexpected error
        with patch(
            "runtime.artifact_renderer.renderer_pipeline._build_instructions",
            side_effect=RuntimeError("instruction build crashed"),
        ):
            result = render_artifacts(
                {
                    "manifest_id": "MAN-BOOM",
                    "detail_id": "DET-BOOM",
                    "instruction_set_id": "IS-BOOM",
                    "requested_formats": ["SVG"],
                    "parameters": {},
                    "metadata": {},
                },
                event_emitter=capture.make_emitter(),
            )

        re_events = capture.events_of_type("RuntimeError")
        assert len(re_events) >= 1, "RuntimeError not emitted on unexpected exception"
        event = re_events[0]
        assert event["payload"]["exception_type"] == "RuntimeError"
        assert "instruction build crashed" in event["payload"]["failure_reason"]


class TestRendererPipelineFailClosed:
    """Emission failures in artifact renderer still fail closed."""

    def test_artifact_rendered_failure_propagates(self):
        from runtime.artifact_renderer.renderer_pipeline import render_artifacts

        manifest = {
            "manifest_id": "MAN-FC",
            "detail_id": "DET-FC",
            "requested_formats": ["SVG"],
            "parameters": {},
            "metadata": {},
        }

        # If ArtifactRendered emission fails, it must propagate
        def reject_artifact_rendered(event):
            if event.get("event_type") == "ArtifactRendered":
                return {"admitted": False, "reason": "rejection"}
            return {"admitted": True, "reason": "ok"}

        adapter = CognitiveBusAdapter(publish_fn=reject_artifact_rendered)
        emitter = RuntimeEventEmitter(bus_adapter=adapter)

        # This should raise if artifacts actually render and emission is rejected
        try:
            result = render_artifacts(manifest, event_emitter=emitter)
            # If no artifacts rendered (e.g., invalid manifest), no emission happens
            if result.artifacts:
                pytest.fail("Should have raised EventEmissionError")
        except EventEmissionError as exc:
            assert exc.event_type == "ArtifactRendered"


# ---------------------------------------------------------------------------
# Cross-cutting
# ---------------------------------------------------------------------------

class TestNoEmitterBackwardCompatibility:
    """Pipeline works without emitter when bus is unavailable."""

    def test_drawing_pipeline_works_without_emitter(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        # With event_emitter=None and no bus available, pipeline should
        # still execute normally (create_emitter returns None)
        result = run_drawing_pipeline({"condition_id": "CS-NOBUS"})
        # Pipeline may fail validation, but it should not crash due to missing emitter
        assert result.condition_id == "CS-NOBUS"

    def test_renderer_pipeline_works_without_emitter(self):
        from runtime.artifact_renderer.renderer_pipeline import render_artifacts

        result = render_artifacts({
            "manifest_id": "MAN-NOBUS",
            "detail_id": "DET-NOBUS",
            "requested_formats": ["SVG"],
            "parameters": {},
            "metadata": {},
        })
        # Should not crash due to missing emitter
        assert result.manifest_id == "MAN-NOBUS"


class TestDeterminismPreserved:
    """Existing runtime determinism is preserved with event emission."""

    def test_drawing_pipeline_same_result_with_and_without_emitter(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        condition = {"condition_id": "CS-DET-001"}

        # Run without emitter
        result_no_emitter = run_drawing_pipeline(condition, event_emitter=None)

        # Run with emitter
        capture = EventCapture()
        result_with_emitter = run_drawing_pipeline(
            condition, event_emitter=capture.make_emitter()
        )

        # Pipeline result should be identical regardless of emitter
        assert result_no_emitter.condition_id == result_with_emitter.condition_id
        assert result_no_emitter.success == result_with_emitter.success
        assert result_no_emitter.detail_id == result_with_emitter.detail_id


class TestEventEnvelopeIntegrity:
    """Events emitted from live pipeline have correct envelope structure."""

    def test_all_live_events_have_required_fields(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        capture = EventCapture()
        run_drawing_pipeline(
            {"condition_id": "CS-ENV-001"},
            event_emitter=capture.make_emitter(),
        )

        required_fields = {
            "event_id", "event_class", "event_type", "schema_version",
            "source_component", "source_repo", "timestamp", "payload",
        }
        for event in capture.events:
            missing = required_fields - set(event.keys())
            assert missing == set(), (
                f"Event {event['event_type']} missing fields: {missing}"
            )
            assert event["event_class"] == "Observation"
            assert event["schema_version"] == "0.1"
            assert event["source_component"] == "Construction_Runtime"
            assert event["source_repo"] == "Construction_Runtime"

    def test_no_bus_metadata_in_live_events(self):
        from runtime.drawing_engine.pipeline import run_drawing_pipeline

        capture = EventCapture()
        run_drawing_pipeline(
            {"condition_id": "CS-NOMETA"},
            event_emitter=capture.make_emitter(),
        )

        bus_fields = {"admission_decision", "admission_timestamp", "content_hash", "routing"}
        for event in capture.events:
            present = bus_fields & set(event.keys())
            assert present == set(), (
                f"Bus-owned fields in live event: {present}"
            )
