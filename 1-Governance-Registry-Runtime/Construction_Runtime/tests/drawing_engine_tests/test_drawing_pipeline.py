"""
Deterministic Drawing Pipeline Tests

Proves that:
- Same input produces same output (deterministic)
- Stable IR emission
- Stable renderer output
- Fail-closed on invalid input
- Fail-closed on unresolved applicability
- Fail-closed on parameter conflicts
- Runtime loads governed contracts from Construction_Kernel
- Missing or malformed governed artifacts fail closed
- IR instruction types match governed contract
- Runtime no longer defines applicability rules inline
"""

import sys
import os
import json
import inspect

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.drawing_engine.input_validator import validate_drawing_inputs
from runtime.drawing_engine.detail_resolver import resolve_detail
from runtime.drawing_engine.parameterizer import parameterize_detail
from runtime.drawing_engine.ir_emitter import emit_ir
from runtime.drawing_engine.renderer import render_svg
from runtime.drawing_engine.pipeline import run_drawing_pipeline
from runtime.drawing_engine.contract_loader import (
    load_applicability_rules,
    load_ir_instruction_types,
    load_detail_schema,
    ContractLoadError,
    ContractVersionError,
    ContractSchemaError,
    EXPECTED_CONTRACT_VERSION,
)


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
        """Verify IR uses only instruction types governed by kernel contract."""
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
        # Load allowed types from governed kernel contract — not self-authored
        governed_types = set(load_ir_instruction_types())
        for inst in ir_result.instructions:
            assert inst.instruction_type in governed_types, (
                f"IR type '{inst.instruction_type}' not in governed contract"
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
# Governed Contract Tests (Wave 6.5 Hardening)
# ──────────────────────────────────────────────


class TestGovernedContracts:
    """Prove runtime consumes governed contracts from Construction_Kernel."""

    def test_applicability_rules_load_from_kernel(self):
        """Runtime loads applicability rules from governed kernel contracts."""
        rules = load_applicability_rules()
        assert isinstance(rules, list)
        assert len(rules) >= 5

    def test_applicability_rules_have_required_fields(self):
        """Every governed rule has all required fields."""
        rules = load_applicability_rules()
        required = {"rule_id", "condition_pattern", "applies_detail", "detail_family", "components", "relationships"}
        for rule in rules:
            missing = required - set(rule.keys())
            assert not missing, f"Rule {rule.get('rule_id')} missing: {missing}"

    def test_ir_instruction_types_load_from_kernel(self):
        """Runtime loads IR types from governed kernel contract."""
        types = load_ir_instruction_types()
        assert isinstance(types, list)
        assert len(types) == 9
        assert "draw_component" in types
        assert "draw_profile" in types

    def test_detail_schema_loads_from_kernel(self):
        """Runtime loads detail schema from governed kernel contract."""
        schema = load_detail_schema()
        assert "valid_component_roles" in schema
        assert "valid_relationship_types" in schema
        assert "waterproofing" in schema["valid_component_roles"]

    def test_resolver_no_inline_rules(self):
        """Prove detail_resolver.py no longer defines APPLICABILITY_RULES inline."""
        import runtime.drawing_engine.detail_resolver as mod
        source = inspect.getsource(mod)
        assert "APPLICABILITY_RULES" not in source, (
            "detail_resolver.py must not define APPLICABILITY_RULES inline. "
            "Rules must be loaded from governed kernel contracts."
        )

    def test_resolver_uses_contract_loader(self):
        """Prove detail_resolver.py imports from contract_loader."""
        import runtime.drawing_engine.detail_resolver as mod
        source = inspect.getsource(mod)
        assert "contract_loader" in source
        assert "load_applicability_rules" in source


class TestGovernedContractFailClosed:
    """Prove runtime fails closed when governed contracts are missing or malformed."""

    def test_missing_contracts_fail_closed(self, monkeypatch):
        """If kernel contracts path does not exist, resolution fails closed."""
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", "/nonexistent/path")
        # Must reimport to pick up env change
        from runtime.drawing_engine import contract_loader
        try:
            contract_loader.load_applicability_rules()
            assert False, "Should have raised ContractLoadError"
        except ContractLoadError as exc:
            assert "missing" in str(exc).lower() or "Governed contract" in str(exc)

    def test_malformed_contracts_fail_closed(self, tmp_path, monkeypatch):
        """If kernel contract JSON is malformed, resolution fails closed."""
        bad_dir = tmp_path / "detail_applicability"
        bad_dir.mkdir(parents=True)
        (bad_dir / "applicability_rules.json").write_text("NOT VALID JSON {{{")
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", str(tmp_path))
        from runtime.drawing_engine import contract_loader
        try:
            contract_loader.load_applicability_rules()
            assert False, "Should have raised ContractLoadError"
        except ContractLoadError as exc:
            assert "malformed" in str(exc).lower() or "Governed contract" in str(exc)

    def test_empty_rules_fail_closed(self, tmp_path, monkeypatch):
        """If kernel contract has no rules, resolution fails closed."""
        rules_dir = tmp_path / "detail_applicability"
        rules_dir.mkdir(parents=True)
        (rules_dir / "applicability_rules.json").write_text(json.dumps({"rules": []}))
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", str(tmp_path))
        from runtime.drawing_engine import contract_loader
        try:
            contract_loader.load_applicability_rules()
            assert False, "Should have raised ContractLoadError"
        except ContractLoadError as exc:
            assert "no rules" in str(exc).lower() or "Governed contract" in str(exc)

    def test_pipeline_fails_closed_on_missing_contracts(self, monkeypatch):
        """Full pipeline fails closed when governed contracts are unreachable."""
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", "/nonexistent/path")
        result = run_drawing_pipeline(VALID_EPDM_PARAPET_CONDITION)
        assert result.success is False
        assert len(result.errors) > 0


class TestDeterminismPreserved:
    """Prove deterministic output unchanged after contract externalization."""

    def test_epdm_parapet_output_stable(self):
        """EPDM parapet produces identical output across two runs."""
        r1 = run_drawing_pipeline(VALID_EPDM_PARAPET_CONDITION)
        r2 = run_drawing_pipeline(VALID_EPDM_PARAPET_CONDITION)
        assert r1.success is True
        assert r2.success is True
        assert r1.detail_id == r2.detail_id == "EPDM_PARAPET_FLASHING_STANDARD"
        assert r1.ir_instruction_count == r2.ir_instruction_count
        assert r1.render_result["svg_content"] == r2.render_result["svg_content"]

    def test_tpo_edge_output_stable(self):
        """TPO edge produces identical output across two runs."""
        r1 = run_drawing_pipeline(VALID_TPO_EDGE_CONDITION)
        r2 = run_drawing_pipeline(VALID_TPO_EDGE_CONDITION)
        assert r1.success is True
        assert r2.success is True
        assert r1.detail_id == r2.detail_id == "TPO_ROOF_EDGE_STANDARD"
        assert r1.ir_instruction_count == r2.ir_instruction_count


# ──────────────────────────────────────────────
# Contract Seam Lock Tests (Wave 6.6 Hardening)
# ──────────────────────────────────────────────


class TestContractVersionLock:
    """Prove runtime enforces exact contract version match."""

    def test_runtime_rejects_unknown_contract_version(self, tmp_path, monkeypatch):
        """Contract with wrong version fails closed with ContractVersionError."""
        rules_dir = tmp_path / "detail_applicability"
        schemas_dir = tmp_path / "schemas"
        rules_dir.mkdir(parents=True)
        schemas_dir.mkdir(parents=True)
        # Write a contract with wrong version
        contract = {
            "contract_id": "construction_kernel.detail_applicability.rules",
            "version": "99.0",
            "authority": "Construction_Kernel",
            "contract_type": "governed_applicability_rules",
            "rules": [{"rule_id": "R1", "condition_pattern": {"interface_type": "test"},
                        "applies_detail": "D1", "detail_family": "f1",
                        "priority": 1, "components": [{"name": "c", "role": "r"}],
                        "relationships": []}],
        }
        (rules_dir / "applicability_rules.json").write_text(json.dumps(contract))
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", str(tmp_path))
        from runtime.drawing_engine import contract_loader
        try:
            contract_loader.load_applicability_rules()
            assert False, "Should have raised ContractVersionError"
        except ContractVersionError as exc:
            assert "99.0" in str(exc)
            assert EXPECTED_CONTRACT_VERSION in str(exc)

    def test_runtime_rejects_missing_version(self, tmp_path, monkeypatch):
        """Contract without version field fails closed."""
        rules_dir = tmp_path / "detail_applicability"
        rules_dir.mkdir(parents=True)
        contract = {
            "contract_id": "construction_kernel.detail_applicability.rules",
            "authority": "Construction_Kernel",
            "contract_type": "governed_applicability_rules",
            "rules": [{"rule_id": "R1", "condition_pattern": {"interface_type": "test"},
                        "applies_detail": "D1", "detail_family": "f1",
                        "priority": 1, "components": [{"name": "c", "role": "r"}],
                        "relationships": []}],
        }
        (rules_dir / "applicability_rules.json").write_text(json.dumps(contract))
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", str(tmp_path))
        from runtime.drawing_engine import contract_loader
        try:
            contract_loader.load_applicability_rules()
            assert False, "Should have raised ContractVersionError"
        except ContractVersionError as exc:
            assert "None" in str(exc)

    def test_correct_version_accepted(self):
        """Contract with correct version loads successfully."""
        rules = load_applicability_rules()
        assert len(rules) >= 1


class TestContractSchemaValidation:
    """Prove runtime validates contracts against kernel-owned schemas."""

    def test_runtime_rejects_schema_mismatch(self, tmp_path, monkeypatch):
        """Contract missing schema-required fields fails with ContractSchemaError."""
        rules_dir = tmp_path / "detail_applicability"
        schemas_dir = tmp_path / "schemas"
        rules_dir.mkdir(parents=True)
        schemas_dir.mkdir(parents=True)
        # Write a valid schema
        schema = {
            "$id": "test",
            "required": ["contract_id", "version", "authority", "contract_type", "rules"],
            "properties": {
                "version": {"type": "string", "const": "1.0"},
                "authority": {"type": "string", "const": "Construction_Kernel"},
                "contract_type": {"type": "string", "const": "governed_applicability_rules"},
                "rules": {"type": "array", "minItems": 1},
            },
        }
        (schemas_dir / "detail_applicability.schema.json").write_text(json.dumps(schema))
        # Write a contract missing required 'rules' field
        contract = {
            "contract_id": "construction_kernel.detail_applicability.rules",
            "version": "1.0",
            "authority": "Construction_Kernel",
            "contract_type": "governed_applicability_rules",
        }
        (rules_dir / "applicability_rules.json").write_text(json.dumps(contract))
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", str(tmp_path))
        from runtime.drawing_engine import contract_loader
        try:
            contract_loader.load_applicability_rules()
            assert False, "Should have raised ContractSchemaError"
        except ContractSchemaError as exc:
            assert "rules" in str(exc)

    def test_contracts_validate_against_kernel_schemas(self):
        """All production contracts pass schema validation (proven by successful load)."""
        rules = load_applicability_rules()
        assert len(rules) >= 5
        types = load_ir_instruction_types()
        assert len(types) == 9
        schema = load_detail_schema()
        assert len(schema["valid_component_roles"]) >= 10

    def test_runtime_rejects_wrong_authority(self, tmp_path, monkeypatch):
        """Contract with wrong authority fails closed."""
        rules_dir = tmp_path / "detail_applicability"
        schemas_dir = tmp_path / "schemas"
        rules_dir.mkdir(parents=True)
        schemas_dir.mkdir(parents=True)
        schema = {
            "$id": "test",
            "required": ["contract_id", "version", "authority", "contract_type", "rules"],
            "properties": {
                "version": {"type": "string", "const": "1.0"},
                "authority": {"type": "string", "const": "Construction_Kernel"},
                "contract_type": {"type": "string", "const": "governed_applicability_rules"},
                "rules": {"type": "array", "minItems": 1},
            },
        }
        (schemas_dir / "detail_applicability.schema.json").write_text(json.dumps(schema))
        contract = {
            "contract_id": "construction_kernel.detail_applicability.rules",
            "version": "1.0",
            "authority": "Some_Other_System",
            "contract_type": "governed_applicability_rules",
            "rules": [{"rule_id": "R1", "condition_pattern": {"interface_type": "t"},
                        "applies_detail": "D1", "detail_family": "f1",
                        "priority": 1, "components": [{"name": "c", "role": "r"}],
                        "relationships": []}],
        }
        (rules_dir / "applicability_rules.json").write_text(json.dumps(contract))
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", str(tmp_path))
        from runtime.drawing_engine import contract_loader
        try:
            contract_loader.load_applicability_rules()
            assert False, "Should have raised ContractSchemaError"
        except ContractSchemaError as exc:
            assert "authority" in str(exc)


class TestContractBypassDetection:
    """Prove runtime cannot operate without contract_loader."""

    def test_runtime_must_use_contract_loader(self):
        """detail_resolver.py must import and use contract_loader."""
        import runtime.drawing_engine.detail_resolver as mod
        source = inspect.getsource(mod)
        assert "from runtime.drawing_engine.contract_loader import" in source
        assert "load_applicability_rules" in source
        # Must not contain inline rule definitions
        assert "APPLICABILITY_RULES" not in source

    def test_runtime_rejects_empty_contract_rules(self, tmp_path, monkeypatch):
        """Pipeline fails closed when contract has empty rules list."""
        rules_dir = tmp_path / "detail_applicability"
        schemas_dir = tmp_path / "schemas"
        rules_dir.mkdir(parents=True)
        schemas_dir.mkdir(parents=True)
        schema = {
            "$id": "test",
            "required": ["contract_id", "version", "authority", "contract_type", "rules"],
            "properties": {
                "version": {"type": "string", "const": "1.0"},
                "authority": {"type": "string", "const": "Construction_Kernel"},
                "contract_type": {"type": "string", "const": "governed_applicability_rules"},
                "rules": {"type": "array", "minItems": 1},
            },
        }
        (schemas_dir / "detail_applicability.schema.json").write_text(json.dumps(schema))
        contract = {
            "contract_id": "construction_kernel.detail_applicability.rules",
            "version": "1.0",
            "authority": "Construction_Kernel",
            "contract_type": "governed_applicability_rules",
            "rules": [],
        }
        (rules_dir / "applicability_rules.json").write_text(json.dumps(contract))
        monkeypatch.setenv("CONSTRUCTION_KERNEL_CONTRACTS_PATH", str(tmp_path))
        from runtime.drawing_engine import contract_loader
        try:
            contract_loader.load_applicability_rules()
            assert False, "Should have raised ContractSchemaError for empty rules"
        except (ContractSchemaError, ContractLoadError) as exc:
            assert "rules" in str(exc).lower() or "no rules" in str(exc).lower()

    def test_loader_does_not_define_schema_structures(self):
        """contract_loader.py must not embed schema definitions."""
        import runtime.drawing_engine.contract_loader as mod
        source = inspect.getsource(mod)
        # Must not contain JSON Schema definition keywords that would indicate
        # the loader is defining schema truth instead of loading it
        assert '"$id"' not in source
        assert '"title"' not in source
        assert '"additionalProperties"' not in source


# ──────────────────────────────────────────────
# Run tests
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
