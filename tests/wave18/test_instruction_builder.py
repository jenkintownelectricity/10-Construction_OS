"""Tests for instruction builder module."""

import pytest
from runtime.artifact_renderer.instruction_builder import (
    build_instruction_set,
    primitives_to_drawing_instruction_set,
)
from runtime.artifact_renderer.renderer_errors import InvalidInstructionSetError
from runtime.artifact_renderer.geometry_primitives import (
    LinePrimitive,
    ArcPrimitive,
    RectanglePrimitive,
    TextPrimitive,
    HatchPrimitive,
    DimensionPrimitive,
    CalloutPrimitive,
    PolylinePrimitive,
)


class TestBuildInstructionSet:
    def test_basic_build(self, sample_detail_dna):
        result = build_instruction_set(sample_detail_dna)
        assert result["detail_id"] == "LOW_SLOPE-PARAPET-EPDM-01"
        assert result["builder_version"] == "18.0"
        assert "instruction_set_id" in result
        assert result["instruction_set_id"].startswith("IS-")

    def test_all_primitive_types_extracted(self, sample_detail_dna):
        result = build_instruction_set(sample_detail_dna)
        primitives = result["primitives"]
        types = {p.primitive_type for p in primitives}
        assert types == {"LINE", "RECTANGLE", "ARC", "TEXT", "HATCH", "DIMENSION", "CALLOUT"}

    def test_layers_collected(self, sample_detail_dna):
        result = build_instruction_set(sample_detail_dna)
        assert "A-DETAIL" in result["layers"]
        assert "A-COMP" in result["layers"]
        assert "A-TEXT" in result["layers"]

    def test_sheet_metadata(self, sample_detail_dna):
        result = build_instruction_set(sample_detail_dna)
        assert result["sheet"]["width"] == 36.0
        assert result["sheet"]["height"] == 24.0
        assert result["sheet"]["unit"] == "in"
        assert result["sheet"]["scale"] == "3:1"

    def test_provenance(self, sample_detail_dna):
        result = build_instruction_set(sample_detail_dna)
        assert result["provenance"]["resolved_by"] == "Construction_Runtime"
        assert result["provenance"]["wave"] == "18"

    def test_missing_detail_id_fails(self):
        with pytest.raises(InvalidInstructionSetError):
            build_instruction_set({"entities": []})

    def test_variant_params_override(self, sample_detail_dna):
        # Override a property value via variant params
        result = build_instruction_set(sample_detail_dna, {"x2": 20})
        # Should build without error — variant params applied
        assert len(result["primitives"]) > 0

    def test_empty_entities_produces_empty_primitives(self):
        dna = {"detail_id": "TEST-001", "entities": []}
        result = build_instruction_set(dna)
        assert len(result["primitives"]) == 0

    def test_unsupported_entity_type_skipped(self):
        dna = {
            "detail_id": "TEST-002",
            "entities": [
                {"type": "UNKNOWN_TYPE", "layer": "A-DETAIL", "properties": {}},
                {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 0, "y1": 0, "x2": 1, "y2": 1}},
            ],
        }
        result = build_instruction_set(dna)
        # Only LINE should be extracted, UNKNOWN_TYPE is skipped
        assert len(result["primitives"]) == 1
        assert result["primitives"][0].primitive_type == "LINE"


class TestPrimitivesToDrawingInstructionSet:
    def test_conversion(self, sample_detail_dna):
        inst = build_instruction_set(sample_detail_dna)
        dis = primitives_to_drawing_instruction_set(inst)
        assert dis["instruction_version"] == "0.2"
        assert len(dis["entities"]) > 0
        assert isinstance(dis["layers"], list)
        assert dis["sheet_metadata"]["unit"] == "in"

    def test_line_conversion(self, sample_detail_dna):
        inst = build_instruction_set(sample_detail_dna)
        dis = primitives_to_drawing_instruction_set(inst)
        lines = [e for e in dis["entities"] if e["entity_type"] == "LINE"]
        assert len(lines) >= 1

    def test_dimension_conversion(self, sample_detail_dna):
        inst = build_instruction_set(sample_detail_dna)
        dis = primitives_to_drawing_instruction_set(inst)
        assert len(dis["dimensions"]) >= 1
        assert dis["dimensions"][0]["dim_type"] == "linear"

    def test_text_annotation_conversion(self, sample_detail_dna):
        inst = build_instruction_set(sample_detail_dna)
        dis = primitives_to_drawing_instruction_set(inst)
        assert len(dis["text_annotations"]) >= 1
