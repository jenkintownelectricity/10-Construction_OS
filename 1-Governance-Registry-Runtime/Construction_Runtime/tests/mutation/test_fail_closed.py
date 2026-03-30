"""Mutation tests for fail-closed behavior.

These tests confirm that the system fails closed when inputs are
mutated, corrupted, or missing critical fields.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from validators.structural_validator import validate_structural
from validators.domain_validator import validate_domain
from validators.generation_validator import validate_generation
from runtime.engines.constraint_engine.engine import run_constraint_engine
from runtime.models.assembly_model import AssemblyModel
from runtime.pipeline.construction_pipeline import run_assembly_pipeline, run_spec_pipeline


class TestStructuralFailClosed:
    def test_none_data_fails(self):
        result = validate_structural(None, "assembly")
        assert result["is_valid"] is False
        assert result["errors"][0]["code"] == "VALIDATION_EMPTY_DATA"

    def test_empty_dict_fails(self):
        result = validate_structural({}, "assembly")
        assert result["is_valid"] is False

    def test_missing_components_fails(self):
        result = validate_structural({"metadata": {"parse_status": "success"}, "source_text": "x"}, "assembly")
        assert result["is_valid"] is False

    def test_empty_components_fails(self):
        data = {"metadata": {"parse_status": "success"}, "components": [], "source_text": "x"}
        result = validate_structural(data, "assembly")
        assert result["is_valid"] is False

    def test_unnamed_component_fails(self):
        data = {
            "metadata": {"parse_status": "success"},
            "components": [{"name": "", "type": "component"}],
            "source_text": "x",
        }
        result = validate_structural(data, "assembly")
        assert result["is_valid"] is False

    def test_invalid_parse_status_fails(self):
        data = {"metadata": {"parse_status": "garbage"}, "components": [{"name": "A", "type": "c"}], "source_text": "x"}
        result = validate_structural(data, "assembly")
        assert result["is_valid"] is False

    def test_unknown_input_type_fails(self):
        data = {"metadata": {"parse_status": "success"}}
        result = validate_structural(data, "unknown_type")
        assert result["is_valid"] is False


class TestDomainFailClosed:
    def test_empty_interface_description_fails(self):
        data = {
            "components": [{"name": "Beam", "type": "component"}],
            "constraints": [{"type": "interface", "description": ""}],
        }
        result = validate_domain(data, "assembly")
        assert result["is_valid"] is False


class TestGenerationFailClosed:
    def test_empty_instruction_set_fails(self):
        result = validate_generation({})
        assert result["is_valid"] is False

    def test_no_entities_fails(self):
        result = validate_generation({"entities": [], "sheet_metadata": {"width": 36, "height": 24}})
        assert result["is_valid"] is False

    def test_unsupported_entity_type_fails(self):
        result = validate_generation({
            "entities": [{"entity_type": "INVALID_TYPE", "layer": "A-WALL"}],
            "sheet_metadata": {"width": 36, "height": 24},
        })
        assert result["is_valid"] is False

    def test_missing_layer_fails(self):
        result = validate_generation({
            "entities": [{"entity_type": "RECT", "layer": ""}],
            "sheet_metadata": {"width": 36, "height": 24},
        })
        assert result["is_valid"] is False


class TestConstraintEngineFailClosed:
    def test_no_components_fails(self):
        assembly = AssemblyModel(name="Empty")
        result = run_constraint_engine(assembly)
        assert result["is_valid"] is False

    def test_unnamed_component_fails(self):
        assembly = AssemblyModel(name="Bad", components=[{"name": "", "type": "c"}])
        result = run_constraint_engine(assembly)
        assert result["is_valid"] is False


class TestPipelineFailClosed:
    def test_empty_assembly_input(self):
        report, _ = run_assembly_pipeline("")
        assert report.validation_status == "failed"
        assert len(report.errors) > 0

    def test_empty_spec_input(self):
        report, _ = run_spec_pipeline("")
        assert report.validation_status == "failed"
        assert len(report.errors) > 0

    def test_assembly_no_components(self):
        report, _ = run_assembly_pipeline("Just a random line of text")
        assert report.validation_status == "failed"
