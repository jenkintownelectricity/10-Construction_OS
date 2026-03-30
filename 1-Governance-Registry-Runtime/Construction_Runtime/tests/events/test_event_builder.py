"""Tests for governed runtime event envelope builder."""

import pytest
from datetime import datetime

from runtime.events.event_builder import (
    build_event_envelope,
    EventBuildError,
    SCHEMA_VERSION,
    SOURCE_COMPONENT,
    SOURCE_REPO,
    EVENT_CLASS,
)


class TestEnvelopeStructure:
    """Verify event envelope structure is deterministic and complete."""

    def test_minimal_envelope_has_all_required_fields(self):
        env = build_event_envelope(
            event_type="ConditionDetected",
            pipeline_stage="pipeline_entry",
            payload={"condition_signature_id": "CS-001", "node_type": "joint"},
        )
        assert "event_id" in env
        assert env["event_class"] == "Observation"
        assert env["event_type"] == "ConditionDetected"
        assert env["schema_version"] == "0.1"
        assert env["source_component"] == "Construction_Runtime"
        assert env["source_repo"] == "Construction_Runtime"
        assert "timestamp" in env
        assert env["pipeline_stage"] == "pipeline_entry"
        assert isinstance(env["payload"], dict)

    def test_event_id_format(self):
        env = build_event_envelope(
            event_type="ConditionDetected",
            pipeline_stage="pipeline_entry",
            payload={},
        )
        assert env["event_id"].startswith("rt-")
        assert len(env["event_id"]) > 10

    def test_event_ids_are_unique(self):
        ids = set()
        for _ in range(100):
            env = build_event_envelope(
                event_type="ConditionDetected",
                pipeline_stage="pipeline_entry",
                payload={},
            )
            ids.add(env["event_id"])
        assert len(ids) == 100

    def test_timestamp_is_iso8601(self):
        env = build_event_envelope(
            event_type="ConditionDetected",
            pipeline_stage="pipeline_entry",
            payload={},
        )
        # Must parse as ISO 8601
        datetime.fromisoformat(env["timestamp"])

    def test_event_class_is_observation(self):
        env = build_event_envelope(
            event_type="DetailResolved",
            pipeline_stage="detail_resolution",
            payload={},
        )
        assert env["event_class"] == "Observation"

    def test_schema_version_matches_bus(self):
        assert SCHEMA_VERSION == "0.1"

    def test_source_constants(self):
        assert SOURCE_COMPONENT == "Construction_Runtime"
        assert SOURCE_REPO == "Construction_Runtime"
        assert EVENT_CLASS == "Observation"

    def test_optional_condition_signature_id(self):
        env = build_event_envelope(
            event_type="ConditionDetected",
            pipeline_stage="pipeline_entry",
            payload={},
            condition_signature_id="CS-001",
        )
        assert env["condition_signature_id"] == "CS-001"

    def test_optional_artifact_id(self):
        env = build_event_envelope(
            event_type="ArtifactRendered",
            pipeline_stage="artifact_rendering",
            payload={},
            artifact_id="ART-001",
        )
        assert env["artifact_id"] == "ART-001"

    def test_no_bus_metadata_emitted(self):
        """Runtime must NOT emit bus-owned metadata."""
        env = build_event_envelope(
            event_type="ConditionDetected",
            pipeline_stage="pipeline_entry",
            payload={},
        )
        assert "admission_decision" not in env
        assert "admission_timestamp" not in env
        assert "content_hash" not in env
        assert "routing" not in env


class TestEnvelopeBuildFailures:
    """Verify invalid envelope construction fails closed."""

    def test_invalid_event_type_fails(self):
        with pytest.raises(EventBuildError, match="Invalid event_type"):
            build_event_envelope(
                event_type="FakeEvent",
                pipeline_stage="pipeline_entry",
                payload={},
            )

    def test_empty_event_type_fails(self):
        with pytest.raises(EventBuildError):
            build_event_envelope(
                event_type="",
                pipeline_stage="pipeline_entry",
                payload={},
            )

    def test_empty_pipeline_stage_fails(self):
        with pytest.raises(EventBuildError, match="pipeline_stage"):
            build_event_envelope(
                event_type="ConditionDetected",
                pipeline_stage="",
                payload={},
            )

    def test_non_dict_payload_fails(self):
        with pytest.raises(EventBuildError, match="payload must be a dict"):
            build_event_envelope(
                event_type="ConditionDetected",
                pipeline_stage="pipeline_entry",
                payload="not a dict",  # type: ignore[arg-type]
            )

    def test_list_payload_fails(self):
        with pytest.raises(EventBuildError, match="payload must be a dict"):
            build_event_envelope(
                event_type="ConditionDetected",
                pipeline_stage="pipeline_entry",
                payload=[1, 2, 3],  # type: ignore[arg-type]
            )

    def test_none_pipeline_stage_fails(self):
        with pytest.raises(EventBuildError):
            build_event_envelope(
                event_type="ConditionDetected",
                pipeline_stage=None,  # type: ignore[arg-type]
                payload={},
            )


class TestAllFiveEventTypes:
    """Verify all five required event types can be built."""

    @pytest.mark.parametrize("event_type", [
        "ConditionDetected",
        "DetailResolved",
        "ArtifactRendered",
        "ValidationFailed",
        "RuntimeError",
    ])
    def test_all_event_types_accepted(self, event_type):
        env = build_event_envelope(
            event_type=event_type,
            pipeline_stage="test_stage",
            payload={"test": True},
        )
        assert env["event_type"] == event_type
        assert env["event_class"] == "Observation"
