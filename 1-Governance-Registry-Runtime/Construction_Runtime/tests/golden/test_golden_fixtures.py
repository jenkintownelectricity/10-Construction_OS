"""Golden fixture tests.

These tests run the full pipeline against known fixture inputs
and verify that output structure and key values are stable.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.pipeline.construction_pipeline import run_assembly_pipeline, run_spec_pipeline

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fixtures")


def _load_fixture(name: str) -> str:
    with open(os.path.join(FIXTURES_DIR, name), "r") as f:
        return f.read()


class TestGoldenAssembly:
    def test_fixture_produces_valid_report(self):
        raw = _load_fixture("sample_assembly.txt")
        report, outputs = run_assembly_pipeline(raw)
        assert report.validation_status == "passed"
        assert report.input_type == "assembly"
        assert "shop_drawing" in report.outputs_generated
        assert "deliverable" in outputs

    def test_fixture_deliverable_has_formats(self):
        raw = _load_fixture("sample_assembly.txt")
        _, outputs = run_assembly_pipeline(raw)
        deliverable = outputs["deliverable"]
        assert deliverable.deliverable_version == "0.2"
        assert "dxf" in deliverable.formats
        assert "svg" in deliverable.formats
        assert "json_preview" in deliverable.formats

    def test_fixture_dxf_generated(self):
        raw = _load_fixture("sample_assembly.txt")
        _, outputs = run_assembly_pipeline(raw)
        dxf_fmt = outputs["deliverable"].formats["dxf"]
        assert dxf_fmt.status == "generated"
        assert "SECTION" in dxf_fmt.content
        assert "EOF" in dxf_fmt.content

    def test_fixture_svg_generated(self):
        raw = _load_fixture("sample_assembly.txt")
        _, outputs = run_assembly_pipeline(raw)
        svg_fmt = outputs["deliverable"].formats["svg"]
        assert svg_fmt.status == "generated"
        assert "<svg" in svg_fmt.content
        assert "</svg>" in svg_fmt.content

    def test_fixture_has_audit_log(self):
        raw = _load_fixture("sample_assembly.txt")
        _, outputs = run_assembly_pipeline(raw)
        assert "audit_log" in outputs
        events = outputs["audit_log"]
        assert len(events) > 0
        # Verify event structure
        event = events[0]
        assert "timestamp" in event
        assert "pipeline_id" in event
        assert "schema_version" in event

    def test_fixture_parsed_components(self):
        raw = _load_fixture("sample_assembly.txt")
        _, outputs = run_assembly_pipeline(raw)
        parsed = outputs["parsed"]
        assert len(parsed["components"]) == 4
        names = [c["name"] for c in parsed["components"]]
        assert "W12x26 Steel Beam" in names

    def test_fixture_parsed_constraints(self):
        raw = _load_fixture("sample_assembly.txt")
        _, outputs = run_assembly_pipeline(raw)
        parsed = outputs["parsed"]
        assert len(parsed["constraints"]) == 4


class TestGoldenSpec:
    def test_fixture_produces_valid_report(self):
        raw = _load_fixture("sample_spec.txt")
        report, outputs = run_spec_pipeline(raw)
        assert report.validation_status == "passed"
        assert report.input_type == "spec"
        assert "spec_intelligence" in report.outputs_generated

    def test_fixture_has_audit_log(self):
        raw = _load_fixture("sample_spec.txt")
        _, outputs = run_spec_pipeline(raw)
        assert "audit_log" in outputs
        events = outputs["audit_log"]
        event_types = [e["event_type"] for e in events]
        assert "PIPELINE_STARTED" in event_types
        assert "PIPELINE_COMPLETED" in event_types

    def test_fixture_detects_requirements(self):
        raw = _load_fixture("sample_spec.txt")
        _, outputs = run_spec_pipeline(raw)
        intel = outputs["intelligence"]
        assert intel["intelligence_status"] == "complete"
        assert len(intel["opportunities"]) > 0

    def test_fixture_detects_manufacturer(self):
        raw = _load_fixture("sample_spec.txt")
        _, outputs = run_spec_pipeline(raw)
        parsed = outputs["parsed"]
        refs = parsed["product_references"]
        manufacturers = [r for r in refs if r["type"] == "manufacturer"]
        assert len(manufacturers) > 0
        assert "Dow Corning" in manufacturers[0]["value"]
