"""Snapshot tests for output stability.

These tests verify that key output shapes and structures remain stable
across runtime versions.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.models.drawing_instruction import DrawingInstructionSet, DrawingEntity, SheetMetadata
from geometry.geometry_engine import build_drawing_instructions
from generator.dxf_writer import write_dxf
from generator.svg_writer import write_svg
from runtime.logging.runtime_log import RuntimeLogger
from contracts import validate_contract


class TestDrawingInstructionSnapshot:
    def test_instruction_set_to_dict_shape(self):
        inst = DrawingInstructionSet(
            entities=[DrawingEntity(entity_type="RECT", layer="A-COMP", properties={"x": 0, "y": 0, "width": 10, "height": 5})],
            layers=["A-COMP"],
        )
        d = inst.to_dict()
        assert "instruction_version" in d
        assert "entities" in d
        assert "dimensions" in d
        assert "text_annotations" in d
        assert "layers" in d
        assert "sheet_metadata" in d
        assert "title_block_data" in d
        assert "provenance" in d
        assert d["instruction_version"] == "0.2"

    def test_geometry_engine_output_shape(self):
        engine_result = {
            "assembly_name": "Snapshot Test",
            "components": [{"name": "Beam", "type": "component"}],
            "constraints": [],
            "geometry": {"dimensions": {}, "spatial_refs": []},
            "materials": [],
            "build_status": "ready",
        }
        inst, result = build_drawing_instructions(engine_result)
        assert inst is not None
        assert result["is_valid"] is True
        assert len(inst.entities) > 0
        assert inst.instruction_version == "0.2"


class TestDxfSnapshot:
    def test_dxf_contains_sections(self):
        inst = DrawingInstructionSet(
            entities=[DrawingEntity(entity_type="RECT", layer="A-COMP", properties={"x": 0, "y": 0, "width": 10, "height": 5})],
            layers=["A-COMP"],
        )
        dxf, errors = write_dxf(inst)
        assert len(errors) == 0
        assert "SECTION" in dxf
        assert "HEADER" in dxf
        assert "ENTITIES" in dxf
        assert "EOF" in dxf
        assert "LWPOLYLINE" in dxf


class TestSvgSnapshot:
    def test_svg_contains_structure(self):
        inst = DrawingInstructionSet(
            entities=[DrawingEntity(entity_type="RECT", layer="A-COMP", properties={"x": 0, "y": 0, "width": 10, "height": 5})],
            layers=["A-COMP"],
        )
        svg, errors = write_svg(inst)
        assert len(errors) == 0
        assert "<svg" in svg
        assert 'id="A-COMP"' in svg
        assert "<rect" in svg
        assert "</svg>" in svg

    def test_svg_has_viewbox(self):
        inst = DrawingInstructionSet(
            entities=[DrawingEntity(entity_type="LINE", layer="A-WALL", properties={"x1": 0, "y1": 0, "x2": 10, "y2": 10})],
            layers=["A-WALL"],
        )
        svg, _ = write_svg(inst)
        assert "viewBox" in svg


class TestAuditLogSnapshot:
    def test_event_structure(self):
        logger = RuntimeLogger("snapshot_test")
        logger.log_pipeline_started("assembly")
        logger.log_parse_completed("test_parser")
        logger.log_pipeline_completed()
        events = logger.get_events()
        assert len(events) == 3

        for event in events:
            assert "timestamp" in event
            assert "pipeline_id" in event
            assert "run_id" in event
            assert "stage" in event
            assert "event_type" in event
            assert "severity" in event
            assert "schema_version" in event
            assert event["schema_version"] == "0.2"


class TestContractSnapshot:
    def test_assembly_input_contract(self):
        data = {
            "name": "Test",
            "components": [{"name": "Beam", "type": "component"}],
            "constraints": [],
            "source_text": "test",
            "metadata": {"parse_status": "success"},
        }
        result = validate_contract(data, "assembly_input")
        assert result["is_valid"] is True
        assert result["schema_version"] == "0.2"

    def test_invalid_contract_detected(self):
        result = validate_contract({}, "assembly_input")
        assert result["is_valid"] is False
        assert len(result["errors"]) > 0
