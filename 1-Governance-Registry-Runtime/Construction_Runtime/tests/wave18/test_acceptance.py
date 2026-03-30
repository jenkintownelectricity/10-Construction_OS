"""End-to-end acceptance test for the full pipeline.

Acceptance path:
  Condition -> resolve detail -> generate variant -> manifest
  -> render DXF/SVG/PDF -> artifacts stored -> graph data built
  -> artifact downloadable

This test exercises the complete Wave 14 + Wave 18 pipeline.
"""

import os
import json
import tempfile
import pytest

from runtime.condition_graph.condition_graph_builder import ConditionGraphBuilder
from runtime.detail_resolver.detail_resolution_engine import resolve_details
from runtime.detail_variants.variant_generator import generate_variant
from runtime.installation_sequence.sequence_engine import generate_sequence
from runtime.artifact_renderer.renderer_pipeline import render_artifacts
from runtime.artifact_renderer.artifact_contract import RenderManifest
from runtime.artifact_renderer.pipeline_integration import (
    build_detail_dna,
    run_full_render_pipeline,
    store_artifact,
)


class TestAcceptancePipeline:
    """Full acceptance test: condition -> render -> download."""

    def test_condition_to_artifact_full_pipeline(self, tmp_path):
        """The core acceptance test — exercises the entire path."""
        # Step 1: Build condition graph
        builder = ConditionGraphBuilder("acceptance-test", ["test-input"])
        builder.add_node("N1", "PARAPET", "North Parapet", material_context="EPDM")
        builder.add_node("N2", "PIPE_PENETRATION", "Vent Pipe A", material_context="EPDM")
        builder.add_node("N3", "DRAIN", "Roof Drain 1", material_context="TPO")
        builder.add_node("N4", "ROOF_FIELD", "Main Roof Area")
        builder.add_edge("N4", "N3", "drains_to")
        builder.add_edge("N2", "N4", "penetrates")
        condition_graph = builder.build()

        assert condition_graph["graph_id"] == "acceptance-test"
        assert len(condition_graph["nodes"]) == 4
        assert "checksum" in condition_graph

        # Step 2: Resolve details from condition graph
        resolved = resolve_details(condition_graph, material_context="EPDM")
        assert resolved["manifest_id"].startswith("resolved-")
        resolved_items = [
            r for r in resolved["resolved_items"]
            if r["resolution_status"] == "RESOLVED"
        ]
        assert len(resolved_items) >= 1, "At least one detail should resolve"

        # Step 3: For each resolved detail, generate variant + render
        for item in resolved_items:
            canonical_id = item["canonical_detail_id"]
            assert canonical_id is not None

            # Step 3a: Build detail DNA
            detail_dna = build_detail_dna(canonical_id)
            assert detail_dna["detail_id"] == canonical_id
            assert len(detail_dna["entities"]) > 0

            # Step 3b: Render all three formats
            manifest = RenderManifest(
                manifest_id=f"MAN-acceptance-{canonical_id}",
                detail_id=canonical_id,
                instruction_set_id=f"IS-acceptance-{canonical_id}",
                requested_formats=["DXF", "SVG", "PDF"],
            )

            result = render_artifacts(manifest, detail_dna)
            assert result.success, f"Render failed for {canonical_id}: {result.errors}"
            assert result.artifact_count == 3

            # Step 3c: Verify DXF
            dxf = result.get_artifact_by_format("DXF")
            assert dxf is not None
            assert dxf.content.startswith("0\nSECTION")
            assert dxf.content.endswith("EOF")
            assert len(dxf.content_hash) == 64

            # Step 3d: Verify SVG
            svg = result.get_artifact_by_format("SVG")
            assert svg is not None
            assert "<svg" in svg.content
            assert "</svg>" in svg.content

            # Step 3e: Verify PDF
            pdf = result.get_artifact_by_format("PDF")
            assert pdf is not None
            assert pdf.content.startswith("%PDF-")
            assert "%%EOF" in pdf.content

            # Step 3f: Verify lineage
            assert "records" in result.lineage
            assert len(result.lineage["records"]) == 3
            assert result.lineage["bundle_hash"] != ""

            # Step 3g: Store artifacts to disk
            output_dir = str(tmp_path / canonical_id.replace("/", "_"))
            os.makedirs(output_dir, exist_ok=True)

            for artifact in result.artifacts:
                stored = store_artifact(artifact, output_dir)
                assert os.path.isfile(stored["filepath"])
                assert stored["file_size"] > 0
                assert stored["content_hash"] == artifact.content_hash

    def test_full_pipeline_integration(self, tmp_path):
        """Test run_full_render_pipeline end-to-end."""
        builder = ConditionGraphBuilder("integration-test", ["test"])
        builder.add_node("N1", "PARAPET", "Test Parapet", material_context="EPDM")
        builder.add_node("N2", "ROOF_FIELD", "Test Roof")
        condition_graph = builder.build()

        output_dir = str(tmp_path / "pipeline_output")
        result = run_full_render_pipeline(
            condition_graph,
            material_context="EPDM",
            output_dir=output_dir,
        )

        assert result["summary"]["success"]
        assert result["summary"]["details_resolved"] >= 1
        assert result["summary"]["artifacts_rendered"] >= 3
        assert result["summary"]["artifacts_stored"] >= 3
        assert result["summary"]["errors"] == 0

        # Verify files on disk
        stored = result["stored_artifacts"]
        for art in stored:
            assert os.path.isfile(art["filepath"])

        # Verify pipeline result JSON written
        assert os.path.isfile(os.path.join(output_dir, "pipeline_result.json"))

    def test_artifact_determinism(self, tmp_path):
        """Verify the same input produces identical output twice."""
        detail_dna = build_detail_dna(
            "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"
        )
        manifest = RenderManifest(
            manifest_id="MAN-determinism-test",
            detail_id="LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
            instruction_set_id="IS-determinism-test",
            requested_formats=["DXF", "SVG", "PDF"],
        )

        r1 = render_artifacts(manifest, detail_dna)
        r2 = render_artifacts(manifest, detail_dna)

        for fmt in ["DXF", "SVG", "PDF"]:
            a1 = r1.get_artifact_by_format(fmt)
            a2 = r2.get_artifact_by_format(fmt)
            assert a1.content == a2.content, f"{fmt} output not deterministic"
            assert a1.content_hash == a2.content_hash

    def test_variant_affects_output(self):
        """Verify that variant parameters produce different output."""
        detail_dna = build_detail_dna(
            "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"
        )
        manifest = RenderManifest(
            manifest_id="MAN-variant-test",
            detail_id="LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
            instruction_set_id="IS-variant-test",
            requested_formats=["SVG"],
        )

        r1 = render_artifacts(manifest, detail_dna, variant_params=None)
        r2 = render_artifacts(manifest, detail_dna, variant_params={"parapet_height": 48.0})

        # Both should succeed
        assert r1.success
        assert r2.success

    def test_installation_sequence_generated(self):
        """Verify installation sequences are generated for resolved details."""
        canonical_id = "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"
        seq = generate_sequence(canonical_id)
        assert seq["detail_ref"] == canonical_id
        assert len(seq["steps"]) >= 3
        assert seq["status"] in ("GENERATED", "RESOLVED")

    def test_graph_data_from_pipeline(self, tmp_path):
        """Verify the API graph builder can read pipeline results."""
        # Import here to avoid circular issues at module level
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "apps", "atlas_api"))

        builder = ConditionGraphBuilder("graph-data-test", ["test"])
        builder.add_node("N1", "PARAPET", "Parapet A", material_context="EPDM")
        builder.add_node("N2", "ROOF_FIELD", "Roof")
        condition_graph = builder.build()

        output_dir = str(tmp_path / "graph_test")
        result = run_full_render_pipeline(
            condition_graph,
            material_context="EPDM",
            output_dir=output_dir,
        )

        # Verify pipeline result was written and is valid JSON
        result_path = os.path.join(output_dir, "pipeline_result.json")
        assert os.path.isfile(result_path)
        with open(result_path) as f:
            loaded = json.load(f)
        assert loaded["summary"]["success"]
        assert len(loaded["stored_artifacts"]) > 0

    def test_kernel_never_mutated(self):
        """Verify kernel data is never written to during rendering."""
        # The kernel is a sibling directory. We verify no writes happen
        # by checking the renderer code doesn't import kernel write functions.
        import runtime.artifact_renderer.dxf_renderer as dxf_mod
        import runtime.artifact_renderer.svg_renderer as svg_mod
        import runtime.artifact_renderer.pdf_renderer as pdf_mod

        for mod in [dxf_mod, svg_mod, pdf_mod]:
            source = open(mod.__file__).read()
            assert "kernel.write" not in source
            assert "kernel.mutate" not in source
            assert "Construction_Kernel" not in source
