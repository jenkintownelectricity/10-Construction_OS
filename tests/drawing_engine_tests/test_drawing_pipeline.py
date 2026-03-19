"""
Deterministic Drawing Pipeline Tests

Proves that:
- Same input produces same output (deterministic)
- Stable IR emission
- Stable renderer output
- Fail-closed on invalid input
- Fail-closed on unresolved applicability
- Fail-closed on parameter conflicts
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.drawing_engine.input_validator import validate_drawing_inputs
from runtime.drawing_engine.detail_resolver import resolve_detail
from runtime.drawing_engine.parameterizer import parameterize_detail
from runtime.drawing_engine.ir_emitter import emit_ir
from runtime.drawing_engine.renderer import render_svg
from runtime.drawing_engine.pipeline import run_drawing_pipeline


# ──────────────────────────────────────────────
# Standard test fixtures
# ──────────────────────────────────────────────

VALID_EPDM_PARAPET_CONDITION = {
    "condition_id": "COND-001",
    "assembly_id": "ASM-001",
    "assembly_type": "roof_assembly",
    "interface_type": "roof_to_parapet",
    "membrane_class": "epdm_membrane",
    "material_references": {
        "membrane": "epdm_membrane",
        "membrane_type": "epdm_membrane",
        "substrate": "concrete_deck",
    },
    "view_intent": {
        "view_intent_type": "detail_view",
        "representation_depth": "component_level",
    },
    "scope_classification": "in_scope",
    "parameters": {
        "membrane_type": "epdm_membrane",
        "parapet_height": "24in",
        "fastener_spacing": "12in",
    },
    "component_ids": ["COMP-001", "COMP-002", "COMP-003"],
}

VALID_TPO_EDGE_CONDITION = {
    "condition_id": "COND-002",
    "assembly_id": "ASM-002",
    "assembly_type": "roof_assembly",
    "interface_type": "roof_edge",
    "membrane_class": "tpo_membrane",
    "material_references": {
        "membrane": "tpo_membrane",
        "membrane_type": "tpo_membrane",
    },
    "view_intent": {
        "view_intent_type": "detail_view",
        "representation_depth": "component_level",
    },
    "scope_classification": "in_scope",
    "parameters": {
        "membrane_type": "tpo_membrane",
    },
}


# ──────────────────────────────────────────────
# Input Validation Tests
# ──────────────────────────────────────────────


class TestInputValidation:
    """Tests for input validation layer."""

    def test_valid_input_passes(self):
        result = validate_drawing_inputs(VALID_EPDM_PARAPET_CONDITION)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_empty_dict_fails(self):
        result = validate_drawing_inputs({})
        assert result.is_valid is False
        assert len(result.errors) > 0

    def test_non_dict_fails(self):
        result = validate_drawing_inputs("not a dict")
        assert result.is_valid is False
        assert result.errors[0]["code"] == "INVALID_INPUT_TYPE"

    def test_missing_condition_id_fails(self):
        condition = dict(VALID_EPDM_PARAPET_CONDITION)
        del condition["condition_id"]
        result = validate_drawing_inputs(condition)
        assert result.is_valid is False
        codes = [e["code"] for e in result.errors]
        assert "MISSING_REQUIRED_INPUT" in codes

    def test_missing_materials_fails(self):
        condition = dict(VALID_EPDM_PARAPET_CONDITION)
        del condition["material_references"]
        result = validate_drawing_inputs(condition)
        assert result.is_valid is False
        codes = [e["code"] for e in result.errors]
        assert "MISSING_REQUIRED_INPUT" in codes

    def test_missing_view_intent_fails(self):
        condition = dict(VALID_EPDM_PARAPET_CONDITION)
        del condition["view_intent"]
        result = validate_drawing_inputs(condition)
        assert result.is_valid is False
        codes = [e["code"] for e in result.errors]
        assert "MISSING_REQUIRED_INPUT" in codes

    def test_missing_scope_warns(self):
        condition = dict(VALID_EPDM_PARAPET_CONDITION)
        del condition["scope_classification"]
        result = validate_drawing_inputs(condition)
        assert result.is_valid is True  # warning, not error
        assert len(result.warnings) > 0


# ──────────────────────────────────────────────
# Detail Resolution Tests
# ──────────────────────────────────────────────


class TestDetailResolution:
    """Tests for detail resolution layer."""

    def test_epdm_parapet_resolves(self):
        result = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        assert result.resolved is True
        assert result.detail_id == "EPDM_PARAPET_FLASHING_STANDARD"
        assert result.detail_family == "parapet_flashing"
        assert len(result.components) > 0

    def test_tpo_edge_resolves(self):
        result = resolve_detail(VALID_TPO_EDGE_CONDITION)
        assert result.resolved is True
        assert result.detail_id == "TPO_ROOF_EDGE_STANDARD"

    def test_unknown_interface_fails_closed(self):
        condition = dict(VALID_EPDM_PARAPET_CONDITION)
        condition["interface_type"] = "unknown_condition"
        condition["membrane_class"] = "unknown_membrane"
        result = resolve_detail(condition)
        assert result.resolved is False
        assert len(result.errors) > 0
        assert result.errors[0]["code"] == "UNRESOLVED_DETAIL_APPLICABILITY"

    def test_resolution_returns_components_and_relationships(self):
        result = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        assert result.resolved is True
        assert len(result.components) >= 4
        assert len(result.relationships) >= 4


# ──────────────────────────────────────────────
# Parameterization Tests
# ──────────────────────────────────────────────


class TestParameterization:
    """Tests for parameterization layer."""

    def test_valid_parameterization(self):
        resolution = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        result = parameterize_detail(
            resolution.components,
            VALID_EPDM_PARAPET_CONDITION["material_references"],
            VALID_EPDM_PARAPET_CONDITION["parameters"],
        )
        assert result.resolved is True
        assert len(result.resolved_components) > 0
        # Verify material_param was resolved to concrete material
        for comp in result.resolved_components:
            assert "material_param" not in comp or comp.get("material")

    def test_missing_material_param_fails(self):
        resolution = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        result = parameterize_detail(
            resolution.components,
            {},  # no material references
            {},  # no parameters
        )
        assert result.resolved is False
        assert len(result.errors) > 0


# ──────────────────────────────────────────────
# IR Emission Tests
# ──────────────────────────────────────────────


class TestIREmission:
    """Tests for IR emission layer."""

    def test_ir_emission_produces_instructions(self):
        resolution = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        param_result = parameterize_detail(
            resolution.components,
            VALID_EPDM_PARAPET_CONDITION["material_references"],
            VALID_EPDM_PARAPET_CONDITION["parameters"],
        )
        ir_result = emit_ir(
            resolution.detail_id,
            param_result.resolved_components,
            resolution.relationships,
            param_result.resolved_parameters,
            VALID_EPDM_PARAPET_CONDITION["view_intent"],
        )
        assert ir_result.emitted is True
        assert len(ir_result.instructions) > 0

    def test_ir_emission_deterministic(self):
        """Same input produces same IR output."""
        resolution = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        param_result = parameterize_detail(
            resolution.components,
            VALID_EPDM_PARAPET_CONDITION["material_references"],
            VALID_EPDM_PARAPET_CONDITION["parameters"],
        )
        ir_1 = emit_ir(
            resolution.detail_id,
            param_result.resolved_components,
            resolution.relationships,
            param_result.resolved_parameters,
            VALID_EPDM_PARAPET_CONDITION["view_intent"],
        )
        ir_2 = emit_ir(
            resolution.detail_id,
            param_result.resolved_components,
            resolution.relationships,
            param_result.resolved_parameters,
            VALID_EPDM_PARAPET_CONDITION["view_intent"],
        )
        assert len(ir_1.instructions) == len(ir_2.instructions)
        for i1, i2 in zip(ir_1.instructions, ir_2.instructions):
            assert i1.instruction_type == i2.instruction_type
            assert i1.target_reference == i2.target_reference
            assert i1.material_reference == i2.material_reference

    def test_empty_components_fails(self):
        ir_result = emit_ir("TEST", [], [], {}, {})
        assert ir_result.emitted is False
        assert len(ir_result.errors) > 0

    def test_ir_instructions_are_construction_semantic(self):
        """Verify IR uses construction-semantic types, not CAD commands."""
        resolution = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        param_result = parameterize_detail(
            resolution.components,
            VALID_EPDM_PARAPET_CONDITION["material_references"],
            VALID_EPDM_PARAPET_CONDITION["parameters"],
        )
        ir_result = emit_ir(
            resolution.detail_id,
            param_result.resolved_components,
            resolution.relationships,
            param_result.resolved_parameters,
            VALID_EPDM_PARAPET_CONDITION["view_intent"],
        )
        allowed_types = {
            "define_view_boundary", "set_representation_depth",
            "draw_component", "draw_profile", "draw_relationship",
            "place_symbol", "place_annotation", "place_dimension",
            "place_material_tag",
        }
        for inst in ir_result.instructions:
            assert inst.instruction_type in allowed_types, (
                f"Non-semantic IR type: {inst.instruction_type}"
            )


# ──────────────────────────────────────────────
# Renderer Tests
# ──────────────────────────────────────────────


class TestRenderer:
    """Tests for renderer layer."""

    def test_svg_rendering(self):
        resolution = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        param_result = parameterize_detail(
            resolution.components,
            VALID_EPDM_PARAPET_CONDITION["material_references"],
            VALID_EPDM_PARAPET_CONDITION["parameters"],
        )
        ir_result = emit_ir(
            resolution.detail_id,
            param_result.resolved_components,
            resolution.relationships,
            param_result.resolved_parameters,
            VALID_EPDM_PARAPET_CONDITION["view_intent"],
        )
        svg_result = render_svg(resolution.detail_id, ir_result.instructions)
        assert svg_result["render_status"] == "success"
        assert svg_result["format"] == "svg"
        assert "<svg" in svg_result["svg_content"]

    def test_svg_deterministic(self):
        """Same IR produces same SVG."""
        resolution = resolve_detail(VALID_EPDM_PARAPET_CONDITION)
        param_result = parameterize_detail(
            resolution.components,
            VALID_EPDM_PARAPET_CONDITION["material_references"],
            VALID_EPDM_PARAPET_CONDITION["parameters"],
        )
        ir_result = emit_ir(
            resolution.detail_id,
            param_result.resolved_components,
            resolution.relationships,
            param_result.resolved_parameters,
            VALID_EPDM_PARAPET_CONDITION["view_intent"],
        )
        svg_1 = render_svg(resolution.detail_id, ir_result.instructions)
        svg_2 = render_svg(resolution.detail_id, ir_result.instructions)
        assert svg_1["svg_content"] == svg_2["svg_content"]


# ──────────────────────────────────────────────
# Full Pipeline Tests
# ──────────────────────────────────────────────


class TestDrawingPipeline:
    """Tests for the full drawing pipeline."""

    def test_full_pipeline_success(self):
        result = run_drawing_pipeline(VALID_EPDM_PARAPET_CONDITION)
        assert result.success is True
        assert result.detail_id == "EPDM_PARAPET_FLASHING_STANDARD"
        assert result.ir_instruction_count > 0
        assert result.render_result.get("render_status") == "success"
        assert result.condition_packet is not None
        assert result.condition_packet.readiness_state == "ready"

    def test_pipeline_deterministic(self):
        """Same condition produces same output."""
        r1 = run_drawing_pipeline(VALID_EPDM_PARAPET_CONDITION)
        r2 = run_drawing_pipeline(VALID_EPDM_PARAPET_CONDITION)
        assert r1.detail_id == r2.detail_id
        assert r1.ir_instruction_count == r2.ir_instruction_count
        assert r1.render_result["svg_content"] == r2.render_result["svg_content"]
        assert r1.condition_packet.readiness_state == r2.condition_packet.readiness_state

    def test_pipeline_fails_closed_invalid_input(self):
        result = run_drawing_pipeline({})
        assert result.success is False
        assert len(result.errors) > 0
        assert result.condition_packet is not None  # packet still built

    def test_pipeline_fails_closed_unresolved_detail(self):
        condition = dict(VALID_EPDM_PARAPET_CONDITION)
        condition["interface_type"] = "totally_unknown"
        condition["membrane_class"] = "unknown_membrane"
        result = run_drawing_pipeline(condition)
        assert result.success is False
        assert any(e["code"] == "UNRESOLVED_DETAIL_APPLICABILITY" for e in result.errors)

    def test_pipeline_audit_log_populated(self):
        result = run_drawing_pipeline(VALID_EPDM_PARAPET_CONDITION)
        assert result.audit_log["final_status"] == "success"
        assert len(result.audit_log["entries"]) > 0

    def test_pipeline_condition_packet_on_failure(self):
        result = run_drawing_pipeline({})
        assert result.condition_packet is not None
        assert result.condition_packet.readiness_state in ("incomplete", "blocked")
        assert len(result.condition_packet.gaps) > 0

    def test_tpo_edge_pipeline(self):
        result = run_drawing_pipeline(VALID_TPO_EDGE_CONDITION)
        assert result.success is True
        assert result.detail_id == "TPO_ROOF_EDGE_STANDARD"


# ──────────────────────────────────────────────
# Run tests
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
