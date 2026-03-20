"""Tests for renderer errors module."""

import pytest
from runtime.artifact_renderer.renderer_errors import (
    RendererError,
    UnsupportedPrimitiveError,
    MissingLayerError,
    InvalidInstructionSetError,
    RendererNotFoundError,
    ManifestError,
    LineageError,
    PipelineError,
    DeterminismError,
)


class TestRendererError:
    def test_base_error(self):
        e = RendererError("CODE", "message")
        assert e.code == "CODE"
        assert e.message == "message"
        assert str(e) == "[CODE] message"

    def test_to_dict(self):
        e = RendererError("CODE", "msg", {"key": "val"})
        d = e.to_dict()
        assert d["code"] == "CODE"
        assert d["context"]["key"] == "val"


class TestSpecificErrors:
    def test_unsupported_primitive(self):
        e = UnsupportedPrimitiveError("SPLINE")
        assert "SPLINE" in str(e)
        assert e.code == "RENDER_UNSUPPORTED_PRIMITIVE"

    def test_missing_layer(self):
        e = MissingLayerError("A-CUSTOM")
        assert "A-CUSTOM" in str(e)

    def test_invalid_instruction_set(self):
        e = InvalidInstructionSetError("bad format", ["err1", "err2"])
        assert len(e.context["errors"]) == 2

    def test_renderer_not_found(self):
        e = RendererNotFoundError("TIFF")
        assert "TIFF" in str(e)

    def test_manifest_error(self):
        e = ManifestError("missing detail_id")
        assert "missing" in str(e)

    def test_lineage_error(self):
        e = LineageError("hash mismatch")
        assert "hash mismatch" in str(e)

    def test_pipeline_error(self):
        e = PipelineError("render_DXF", "timeout")
        assert "render_DXF" in str(e)
        assert e.context["stage"] == "render_DXF"

    def test_determinism_error(self):
        e = DeterminismError("DXF", "abc", "def")
        assert e.context["expected_hash"] == "abc"
        assert e.context["actual_hash"] == "def"


class TestErrorHierarchy:
    def test_all_inherit_renderer_error(self):
        errors = [
            UnsupportedPrimitiveError("X"),
            MissingLayerError("L"),
            InvalidInstructionSetError("R"),
            RendererNotFoundError("F"),
            ManifestError("M"),
            LineageError("L"),
            PipelineError("S", "R"),
            DeterminismError("F", "E", "A"),
        ]
        for e in errors:
            assert isinstance(e, RendererError)
            assert isinstance(e, Exception)
