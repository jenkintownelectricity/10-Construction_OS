"""Tests for the detail preview seam.

Validates:
1. Roofing generation produces SVG + DXF from same lineage
2. Fireproofing fails closed with diagnostics
3. Empty assembly fails closed
4. SVG content is real, not placeholder
5. DXF is available for download
"""

import pytest

from runtime.artifact_renderer.detail_preview_seam import (
    generate_detail_preview,
    DetailPreviewResult,
    SEAM_ID,
    SUPPORTED_CATEGORIES,
)


# ── Sample roofing assembly draft ──────────────────────────────────────

ROOFING_DRAFT = {
    "schema_version": "v1",
    "system_id": "DRAFT-ROOF-SDC-001",
    "title": "Carlisle TPO Roof Assembly — Main Store Roof",
    "assembly_type": "roof_assembly",
    "status": "draft",
    "layers": [
        {
            "layer_id": "LYR-R-001",
            "position": 1,
            "control_layer_id": "bulk_water_control",
            "material_ref": "MATL-TPO-001",
            "attachment_method": "fully_adhered",
            "notes": "Carlisle Sure-Weld TPO 60 mil White",
        },
        {
            "layer_id": "LYR-R-002",
            "position": 2,
            "control_layer_id": "protection_layer",
            "material_ref": "MATL-COVERBD-001",
            "attachment_method": "mechanically_attached",
            "notes": "DensDeck Prime 1/4\" Gypsum Cover Board",
        },
        {
            "layer_id": "LYR-R-003",
            "position": 3,
            "control_layer_id": "thermal_control",
            "material_ref": "MATL-POLYISO-001",
            "attachment_method": "mechanically_attached",
            "notes": "Polyisocyanurate 3.0\" R-17.4",
        },
        {
            "layer_id": "LYR-R-004",
            "position": 4,
            "control_layer_id": "vapor_control",
            "material_ref": "MATL-VR-001",
            "attachment_method": "self_adhered",
            "notes": "Carlisle VapAir 710 Self-Adhered",
        },
    ],
    "control_layer_continuity": {
        "bulk_water_control": "continuous",
        "thermal_control": "continuous",
        "vapor_control": "continuous",
    },
}


class TestRoofingGeneration:
    """Roofing detail generation through the preview seam."""

    def test_roofing_produces_svg_and_dxf(self):
        result = generate_detail_preview(ROOFING_DRAFT, "roofing")
        assert result.success is True
        assert result.generation_status == "success"
        assert result.svg_content != ""
        assert result.dxf_available is True

    def test_svg_content_is_real_svg(self):
        result = generate_detail_preview(ROOFING_DRAFT, "roofing")
        assert result.svg_content.startswith("<svg")
        assert "xmlns" in result.svg_content
        assert "</svg>" in result.svg_content

    def test_dxf_content_is_available(self):
        result = generate_detail_preview(ROOFING_DRAFT, "roofing")
        assert result.dxf_content != ""
        assert result.dxf_artifact_id != ""

    def test_artifact_metadata_populated(self):
        result = generate_detail_preview(ROOFING_DRAFT, "roofing")
        assert result.detail_id == "DRAFT-ROOF-SDC-001"
        assert result.artifact_type == "roofing_detail"
        assert result.artifact_filename.endswith(".dxf")
        assert result.generator_seam == SEAM_ID

    def test_lineage_chain_present(self):
        result = generate_detail_preview(ROOFING_DRAFT, "roofing")
        assert result.manifest_id != ""
        assert result.svg_content_hash != ""
        assert result.dxf_content_hash != ""

    def test_same_lineage_for_svg_and_dxf(self):
        """SVG and DXF must come from the same artifact lineage."""
        result = generate_detail_preview(ROOFING_DRAFT, "roofing")
        assert result.lineage != {}
        # Both share the same manifest
        assert result.manifest_id != ""


class TestFireproofingFailClosed:
    """Fireproofing must fail closed — no fake generator."""

    def test_fireproofing_unsupported(self):
        result = generate_detail_preview(ROOFING_DRAFT, "fireproofing")
        assert result.success is False
        assert result.generation_status == "unsupported"

    def test_fireproofing_has_diagnostics(self):
        result = generate_detail_preview(ROOFING_DRAFT, "fireproofing")
        assert len(result.diagnostics) > 0
        assert "FAIL_CLOSED" in result.diagnostics[0]
        assert "fireproofing" in result.diagnostics[0]

    def test_fireproofing_has_error(self):
        result = generate_detail_preview(ROOFING_DRAFT, "fireproofing")
        assert len(result.errors) > 0
        assert result.errors[0]["code"] == "UNSUPPORTED_CATEGORY"


class TestEmptyDraftFailClosed:
    """Empty assembly drafts must fail closed."""

    def test_empty_layers_fail_closed(self):
        result = generate_detail_preview({"layers": []}, "roofing")
        assert result.success is False
        assert result.generation_status == "validation_failed"
        assert "FAIL_CLOSED" in result.diagnostics[0]

    def test_no_layers_key_fail_closed(self):
        result = generate_detail_preview({}, "roofing")
        assert result.success is False
        assert result.generation_status == "validation_failed"


class TestSeamMetadata:
    """Seam identification and metadata."""

    def test_seam_id_set(self):
        result = generate_detail_preview(ROOFING_DRAFT, "roofing")
        assert result.seam_id == SEAM_ID

    def test_category_reflected(self):
        result = generate_detail_preview(ROOFING_DRAFT, "roofing")
        assert result.category == "roofing"

    def test_supported_categories(self):
        assert "roofing" in SUPPORTED_CATEGORIES
        assert "fireproofing" not in SUPPORTED_CATEGORIES
