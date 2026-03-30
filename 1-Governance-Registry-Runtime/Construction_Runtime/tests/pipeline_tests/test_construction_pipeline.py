"""Tests for construction pipeline."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.pipeline.construction_pipeline import run_assembly_pipeline, run_spec_pipeline


class TestAssemblyPipeline:
    def test_happy_path(self):
        raw = """Assembly: Test Assembly
Components:
- Steel Beam
- Bolt Set
Constraint: Clearance = 1 inch
"""
        report, outputs = run_assembly_pipeline(raw)
        assert report.input_type == "assembly"
        assert report.validation_status == "passed"
        assert "shop_drawing" in report.outputs_generated
        assert "deliverable" in outputs
        assert outputs["deliverable"].deliverable_type == "shop_drawing"

    def test_empty_input_fails(self):
        report, outputs = run_assembly_pipeline("")
        assert report.validation_status == "failed"
        assert len(report.errors) > 0


class TestSpecPipeline:
    def test_happy_path(self):
        raw = """1.0 - General
The system shall meet all codes.
Manufacturer: Acme Corp
"""
        report, outputs = run_spec_pipeline(raw)
        assert report.input_type == "spec"
        assert report.validation_status == "passed"
        assert "spec_intelligence" in report.outputs_generated
        assert "intelligence" in outputs

    def test_empty_input_fails(self):
        report, outputs = run_spec_pipeline("")
        assert report.validation_status == "failed"
        assert len(report.errors) > 0
