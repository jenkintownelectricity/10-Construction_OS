"""Tests for artifact lineage module."""

import pytest
from runtime.artifact_renderer.artifact_lineage import (
    compute_sha256,
    compute_content_hash,
    create_lineage_record,
    verify_determinism,
    build_lineage_chain,
    LineageRecord,
    LineageBundle,
    LINEAGE_VERSION,
)


class TestSha256:
    def test_deterministic(self):
        h1 = compute_sha256("hello world")
        h2 = compute_sha256("hello world")
        assert h1 == h2

    def test_different_inputs(self):
        h1 = compute_sha256("hello")
        h2 = compute_sha256("world")
        assert h1 != h2

    def test_hex_format(self):
        h = compute_sha256("test")
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)


class TestContentHash:
    def test_format_tagged(self):
        h_dxf = compute_content_hash("content", "DXF")
        h_svg = compute_content_hash("content", "SVG")
        assert h_dxf != h_svg

    def test_deterministic(self):
        h1 = compute_content_hash("test", "DXF")
        h2 = compute_content_hash("test", "DXF")
        assert h1 == h2


class TestLineageRecord:
    def test_creation(self):
        record = create_lineage_record(
            artifact_id="ART-001",
            content="dxf content here",
            output_format="DXF",
            source_detail_id="D-001",
            source_instruction_set_id="IS-001",
            source_manifest_id="MAN-001",
            renderer_id="dxf_v18",
        )
        assert record.artifact_id == "ART-001"
        assert record.output_format == "DXF"
        assert len(record.content_hash) == 64

    def test_immutable(self):
        record = create_lineage_record("A1", "c", "DXF", "D1", "IS1", "M1", "R1")
        with pytest.raises(AttributeError):
            record.artifact_id = "changed"

    def test_to_dict(self):
        record = create_lineage_record("A1", "c", "DXF", "D1", "IS1", "M1", "R1")
        d = record.to_dict()
        assert d["artifact_id"] == "A1"
        assert d["lineage_version"] == LINEAGE_VERSION


class TestLineageBundle:
    def test_add_record(self):
        bundle = LineageBundle(manifest_id="MAN-001")
        record = create_lineage_record("A1", "c", "DXF", "D1", "IS1", "M1", "R1")
        bundle.add_record(record)
        assert len(bundle.records) == 1
        assert bundle.bundle_hash != ""

    def test_bundle_hash_changes_on_add(self):
        bundle = LineageBundle(manifest_id="MAN-001")
        r1 = create_lineage_record("A1", "c1", "DXF", "D1", "IS1", "M1", "R1")
        bundle.add_record(r1)
        h1 = bundle.bundle_hash

        r2 = create_lineage_record("A2", "c2", "SVG", "D1", "IS1", "M1", "R2")
        bundle.add_record(r2)
        assert bundle.bundle_hash != h1

    def test_to_dict(self):
        bundle = LineageBundle(manifest_id="MAN-001")
        r = create_lineage_record("A1", "c", "DXF", "D1", "IS1", "M1", "R1")
        bundle.add_record(r)
        d = bundle.to_dict()
        assert d["manifest_id"] == "MAN-001"
        assert d["record_count"] == 1


class TestVerifyDeterminism:
    def test_identical_content(self):
        assert verify_determinism("same", "same", "DXF")

    def test_different_content(self):
        assert not verify_determinism("content_a", "content_b", "DXF")


class TestBuildLineageChain:
    def test_chain_from_artifacts(self):
        artifacts = [
            {"artifact_id": "A1", "content": "dxf", "format": "DXF", "renderer_id": "R1"},
            {"artifact_id": "A2", "content": "svg", "format": "SVG", "renderer_id": "R2"},
            {"artifact_id": "A3", "content": "pdf", "format": "PDF", "renderer_id": "R3"},
        ]
        bundle = build_lineage_chain("D1", "IS1", "MAN-001", artifacts)
        assert len(bundle.records) == 3
        assert bundle.manifest_id == "MAN-001"
        assert bundle.bundle_hash != ""

    def test_empty_artifacts(self):
        bundle = build_lineage_chain("D1", "IS1", "MAN-001", [])
        assert len(bundle.records) == 0
