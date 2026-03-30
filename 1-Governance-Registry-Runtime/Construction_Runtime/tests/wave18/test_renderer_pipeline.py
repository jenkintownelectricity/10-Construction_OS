"""Tests for renderer pipeline module."""

import pytest
from runtime.artifact_renderer.renderer_pipeline import render_artifacts
from runtime.artifact_renderer.artifact_contract import RenderManifest, RenderResult
from runtime.artifact_renderer.renderer_registry import RendererRegistry
from runtime.artifact_renderer.dxf_renderer import DxfRenderer
from runtime.artifact_renderer.svg_renderer import SvgRenderer
from runtime.artifact_renderer.pdf_renderer import PdfRenderer


class TestRenderArtifacts:
    def test_full_pipeline(self, sample_detail_dna, sample_manifest, full_registry):
        result = render_artifacts(
            manifest=sample_manifest,
            detail_dna=sample_detail_dna,
            registry=full_registry,
        )
        assert result.success
        assert result.artifact_count == 3
        assert result.get_artifact_by_format("DXF") is not None
        assert result.get_artifact_by_format("SVG") is not None
        assert result.get_artifact_by_format("PDF") is not None

    def test_dxf_content_valid(self, sample_detail_dna, sample_manifest, full_registry):
        sample_manifest.requested_formats = ["DXF"]
        result = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        dxf = result.get_artifact_by_format("DXF")
        assert dxf.content.startswith("0\nSECTION")
        assert dxf.content.endswith("EOF")

    def test_svg_content_valid(self, sample_detail_dna, sample_manifest, full_registry):
        sample_manifest.requested_formats = ["SVG"]
        result = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        svg = result.get_artifact_by_format("SVG")
        assert "<svg" in svg.content
        assert "</svg>" in svg.content

    def test_pdf_content_valid(self, sample_detail_dna, sample_manifest, full_registry):
        sample_manifest.requested_formats = ["PDF"]
        result = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        pdf = result.get_artifact_by_format("PDF")
        assert pdf.content.startswith("%PDF-")

    def test_lineage_generated(self, sample_detail_dna, sample_manifest, full_registry):
        result = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        assert "records" in result.lineage
        assert len(result.lineage["records"]) == 3
        assert "bundle_hash" in result.lineage

    def test_artifact_ids_unique(self, sample_detail_dna, sample_manifest, full_registry):
        result = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        ids = [a.artifact_id for a in result.artifacts]
        assert len(ids) == len(set(ids))

    def test_content_hashes_unique(self, sample_detail_dna, sample_manifest, full_registry):
        result = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        hashes = [a.content_hash for a in result.artifacts]
        assert len(hashes) == len(set(hashes))

    def test_manifest_validation_failure(self, full_registry):
        manifest = RenderManifest()  # Empty manifest
        result = render_artifacts(manifest, registry=full_registry)
        assert not result.success
        assert len(result.errors) > 0

    def test_dict_manifest(self, sample_detail_dna, full_registry):
        result = render_artifacts(
            manifest={
                "manifest_id": "MAN-dict-001",
                "detail_id": "LOW_SLOPE-PARAPET-EPDM-01",
                "instruction_set_id": "IS-dict-001",
                "requested_formats": ["SVG"],
            },
            detail_dna=sample_detail_dna,
            registry=full_registry,
        )
        assert result.success
        assert result.artifact_count == 1

    def test_single_format(self, sample_detail_dna, full_registry):
        manifest = RenderManifest(
            manifest_id="MAN-single",
            detail_id="LOW_SLOPE-PARAPET-EPDM-01",
            instruction_set_id="IS-single",
            requested_formats=["DXF"],
        )
        result = render_artifacts(manifest, sample_detail_dna, registry=full_registry)
        assert result.success
        assert result.artifact_count == 1

    def test_missing_renderer(self, sample_detail_dna):
        registry = RendererRegistry()
        registry.register(DxfRenderer())
        manifest = RenderManifest(
            manifest_id="MAN-missing",
            detail_id="LOW_SLOPE-PARAPET-EPDM-01",
            instruction_set_id="IS-missing",
            requested_formats=["DXF", "SVG"],
        )
        result = render_artifacts(manifest, sample_detail_dna, registry=registry)
        # DXF should succeed, SVG should error
        assert result.artifact_count == 1
        assert len(result.errors) > 0

    def test_deterministic_rendering(self, sample_detail_dna, sample_manifest, full_registry):
        r1 = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        r2 = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        for fmt in ["DXF", "SVG", "PDF"]:
            a1 = r1.get_artifact_by_format(fmt)
            a2 = r2.get_artifact_by_format(fmt)
            assert a1.content == a2.content

    def test_result_to_dict(self, sample_detail_dna, sample_manifest, full_registry):
        result = render_artifacts(sample_manifest, sample_detail_dna, registry=full_registry)
        d = result.to_dict()
        assert d["success"]
        assert d["artifact_count"] == 3
        assert "contract_version" in d

    def test_manifest_from_detail_dna_only(self, full_registry):
        """Pipeline can work with manifest + detail_dna alone."""
        manifest = RenderManifest(
            manifest_id="MAN-dna-only",
            detail_id="SIMPLE-001",
            instruction_set_id="IS-dna",
            requested_formats=["SVG"],
        )
        dna = {
            "detail_id": "SIMPLE-001",
            "entities": [
                {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 0, "y1": 0, "x2": 5, "y2": 5}},
            ],
        }
        result = render_artifacts(manifest, dna, registry=full_registry)
        assert result.success

    def test_empty_entities_still_renders(self, full_registry):
        manifest = RenderManifest(
            manifest_id="MAN-empty",
            detail_id="EMPTY-001",
            instruction_set_id="IS-empty",
            requested_formats=["DXF"],
        )
        dna = {"detail_id": "EMPTY-001", "entities": []}
        result = render_artifacts(manifest, dna, registry=full_registry)
        assert result.success


class TestRendererErrors:
    def test_invalid_format_in_manifest(self, sample_detail_dna, full_registry):
        manifest = RenderManifest(
            manifest_id="MAN-bad",
            detail_id="D1",
            instruction_set_id="IS1",
            requested_formats=["TIFF"],
        )
        result = render_artifacts(manifest, sample_detail_dna, registry=full_registry)
        assert not result.success
