"""Tests for artifact contract module."""

import pytest
from runtime.artifact_renderer.artifact_contract import (
    RenderManifest,
    ArtifactOutput,
    RenderResult,
    RendererCapability,
    SUPPORTED_OUTPUT_FORMATS,
    ARTIFACT_CONTRACT_VERSION,
)


class TestRenderManifest:
    def test_valid_manifest(self, sample_manifest):
        errors = sample_manifest.validate()
        assert len(errors) == 0

    def test_missing_manifest_id(self):
        m = RenderManifest(detail_id="D1", instruction_set_id="IS1")
        errors = m.validate()
        assert any("manifest_id" in e for e in errors)

    def test_missing_detail_id(self):
        m = RenderManifest(manifest_id="M1", instruction_set_id="IS1")
        errors = m.validate()
        assert any("detail_id" in e for e in errors)

    def test_missing_instruction_set_id(self):
        m = RenderManifest(manifest_id="M1", detail_id="D1")
        errors = m.validate()
        assert any("instruction_set_id" in e for e in errors)

    def test_unsupported_format(self):
        m = RenderManifest(
            manifest_id="M1",
            detail_id="D1",
            instruction_set_id="IS1",
            requested_formats=["DXF", "TIFF"],
        )
        errors = m.validate()
        assert any("TIFF" in e for e in errors)

    def test_default_formats(self):
        m = RenderManifest(manifest_id="M1", detail_id="D1", instruction_set_id="IS1")
        assert m.requested_formats == ["DXF", "SVG", "PDF"]


class TestArtifactOutput:
    def test_to_dict(self):
        a = ArtifactOutput(
            artifact_id="ART-001",
            format="DXF",
            content="test",
            content_hash="abc123",
            source_manifest_id="MAN-001",
            renderer_id="dxf_v18",
        )
        d = a.to_dict()
        assert d["artifact_id"] == "ART-001"
        assert d["format"] == "DXF"
        assert "content" not in d  # Content excluded from dict


class TestRenderResult:
    def test_empty_result(self):
        r = RenderResult(manifest_id="MAN-001")
        assert r.artifact_count == 0
        assert not r.success

    def test_get_artifact_by_format(self):
        r = RenderResult(manifest_id="MAN-001")
        r.artifacts.append(ArtifactOutput(artifact_id="A1", format="DXF"))
        r.artifacts.append(ArtifactOutput(artifact_id="A2", format="SVG"))
        assert r.get_artifact_by_format("DXF").artifact_id == "A1"
        assert r.get_artifact_by_format("SVG").artifact_id == "A2"
        assert r.get_artifact_by_format("PDF") is None

    def test_to_dict_includes_contract_version(self):
        r = RenderResult(manifest_id="MAN-001", success=True)
        d = r.to_dict()
        assert d["contract_version"] == ARTIFACT_CONTRACT_VERSION


class TestRendererCapability:
    def test_supports_primitive(self):
        cap = RendererCapability(
            renderer_id="test",
            output_format="DXF",
            supported_primitives=["LINE", "ARC"],
        )
        assert cap.supports_primitive("LINE")
        assert not cap.supports_primitive("HATCH")


class TestSupportedFormats:
    def test_three_formats(self):
        assert SUPPORTED_OUTPUT_FORMATS == {"DXF", "SVG", "PDF"}
