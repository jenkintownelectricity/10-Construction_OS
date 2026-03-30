"""Tests for typed event payload models."""

import pytest

from runtime.events.event_models import (
    ConditionDetectedPayload,
    DetailResolvedPayload,
    ArtifactRenderedPayload,
    ValidationFailedPayload,
    RuntimeErrorPayload,
    PAYLOAD_TYPES,
)


class TestConditionDetectedPayload:
    def test_required_fields(self):
        p = ConditionDetectedPayload(
            condition_signature_id="CS-001",
            node_type="structural_joint",
            pipeline_stage="pipeline_entry",
        )
        d = p.to_dict()
        assert d["condition_signature_id"] == "CS-001"
        assert d["node_type"] == "structural_joint"
        assert d["pipeline_stage"] == "pipeline_entry"

    def test_optional_project_id(self):
        p = ConditionDetectedPayload(
            condition_signature_id="CS-001",
            node_type="joint",
            pipeline_stage="pipeline_entry",
            project_id="PRJ-42",
        )
        assert p.to_dict()["project_id"] == "PRJ-42"

    def test_omits_empty_optional(self):
        p = ConditionDetectedPayload(
            condition_signature_id="CS-001",
            node_type="joint",
            pipeline_stage="pipeline_entry",
        )
        assert "project_id" not in p.to_dict()

    def test_immutable(self):
        p = ConditionDetectedPayload(
            condition_signature_id="CS-001",
            node_type="joint",
            pipeline_stage="pipeline_entry",
        )
        with pytest.raises(AttributeError):
            p.condition_signature_id = "other"  # type: ignore[misc]


class TestDetailResolvedPayload:
    def test_required_fields(self):
        p = DetailResolvedPayload(
            condition_signature_id="CS-001",
            resolved_detail_id="DET-050",
            resolution_source="detail_resolver",
            pipeline_stage="detail_resolution",
        )
        d = p.to_dict()
        assert d["condition_signature_id"] == "CS-001"
        assert d["resolved_detail_id"] == "DET-050"
        assert d["resolution_source"] == "detail_resolver"
        assert d["pipeline_stage"] == "detail_resolution"

    def test_optional_fields(self):
        p = DetailResolvedPayload(
            condition_signature_id="CS-001",
            resolved_detail_id="DET-050",
            resolution_source="resolver",
            pipeline_stage="detail_resolution",
            pattern_id="PAT-01",
            variant_id="VAR-A",
        )
        d = p.to_dict()
        assert d["pattern_id"] == "PAT-01"
        assert d["variant_id"] == "VAR-A"


class TestArtifactRenderedPayload:
    def test_required_fields(self):
        p = ArtifactRenderedPayload(
            artifact_id="ART-001",
            artifact_type="DXF",
            renderer_name="DxfRenderer",
            pipeline_stage="artifact_rendering",
        )
        d = p.to_dict()
        assert d["artifact_id"] == "ART-001"
        assert d["artifact_type"] == "DXF"
        assert d["renderer_name"] == "DxfRenderer"

    def test_optional_lineage(self):
        p = ArtifactRenderedPayload(
            artifact_id="ART-001",
            artifact_type="SVG",
            renderer_name="SvgRenderer",
            pipeline_stage="artifact_rendering",
            lineage_hash="abc123",
        )
        assert p.to_dict()["lineage_hash"] == "abc123"


class TestValidationFailedPayload:
    def test_required_fields(self):
        p = ValidationFailedPayload(
            validation_stage="input_validation",
            error_code="MISSING_FIELD",
            failure_reason="condition_id is required",
            pipeline_stage="input_validation",
        )
        d = p.to_dict()
        assert d["validation_stage"] == "input_validation"
        assert d["error_code"] == "MISSING_FIELD"
        assert d["failure_reason"] == "condition_id is required"

    def test_optional_object_id(self):
        p = ValidationFailedPayload(
            validation_stage="schema",
            error_code="INVALID_SCHEMA",
            failure_reason="bad schema",
            pipeline_stage="input_validation",
            object_id="OBJ-99",
        )
        assert p.to_dict()["object_id"] == "OBJ-99"


class TestRuntimeErrorPayload:
    def test_required_fields(self):
        p = RuntimeErrorPayload(
            exception_type="ValueError",
            failure_reason="unexpected None",
            pipeline_stage="rendering",
        )
        d = p.to_dict()
        assert d["exception_type"] == "ValueError"
        assert d["failure_reason"] == "unexpected None"
        assert d["pipeline_stage"] == "rendering"

    def test_optional_error_code(self):
        p = RuntimeErrorPayload(
            exception_type="IOError",
            failure_reason="disk full",
            pipeline_stage="rendering",
            error_code="IO_001",
        )
        assert p.to_dict()["error_code"] == "IO_001"


class TestPayloadTypeRegistry:
    def test_all_five_types_registered(self):
        assert len(PAYLOAD_TYPES) == 5
        assert set(PAYLOAD_TYPES.keys()) == {
            "ConditionDetected",
            "DetailResolved",
            "ArtifactRendered",
            "ValidationFailed",
            "RuntimeError",
        }
