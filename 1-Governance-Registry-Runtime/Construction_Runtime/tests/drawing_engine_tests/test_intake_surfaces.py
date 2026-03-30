"""
Wave 7 — Intake & Review Application Surface Tests

Proves:
- Project intake works
- Evidence ingestion accepted
- Assemblies resolved from evidence
- Runtime generates condition packets via trigger
- Condition inspector reads packets
- All outputs remain derived, recomputable, non-canonical
- Intake layer does not modify kernel truth or pipeline behavior
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from apps.intake.project_intake import ingest_project, ProjectRecord
from apps.intake.evidence_ingestion import ingest_evidence, IngestionResult
from apps.intake.assembly_identity_resolver import resolve_assemblies, IdentityResolutionResult
from apps.intake.runtime_trigger import trigger_runtime, TriggerResult
from apps.intake.condition_inspector import inspect_condition, browse_conditions


# ──────────────────────────────────────────────
# Test Fixtures
# ──────────────────────────────────────────────

VALID_PROJECT = {
    "project_id": "PROJ-001",
    "building_systems": [
        {"system_id": "SYS-001", "system_type": "roofing"},
    ],
    "assemblies": [
        {
            "assembly_id": "ASM-001",
            "assembly_type": "roof_assembly",
            "interfaces": [
                {"interface_type": "roof_to_parapet"},
            ],
            "material_classes": ["epdm_membrane"],
        },
    ],
    "materials": ["epdm_membrane", "galvanized_steel"],
    "scope_assignments": [
        {"assembly_id": "ASM-001", "scope": "in_scope"},
    ],
}

VALID_EVIDENCE = [
    {
        "evidence_id": "EV-001",
        "evidence_type": "drawing",
        "source_reference": "A-501",
        "assembly_references": ["ASM-001"],
    },
    {
        "evidence_id": "EV-002",
        "evidence_type": "specification",
        "source_reference": "07 54 00",
        "assembly_references": ["ASM-001"],
    },
]

VALID_RUNTIME_CONDITION = {
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
    "component_ids": ["COMP-001", "COMP-002"],
}


# ──────────────────────────────────────────────
# Project Intake Tests
# ──────────────────────────────────────────────


class TestProjectIntake:
    """Tests for project intake."""

    def test_valid_project_intake(self):
        result = ingest_project(VALID_PROJECT)
        assert result.project_id == "PROJ-001"
        assert len(result.building_systems) == 1
        assert len(result.errors) == 0

    def test_empty_project_fails(self):
        result = ingest_project({})
        assert len(result.errors) > 0

    def test_non_dict_project_fails(self):
        result = ingest_project("not a dict")
        assert len(result.errors) > 0
        assert result.errors[0]["code"] == "INVALID_PROJECT_DATA"

    def test_missing_systems_fails(self):
        result = ingest_project({"project_id": "P1"})
        assert len(result.errors) > 0
        assert result.errors[0]["code"] == "MISSING_BUILDING_SYSTEMS"


# ──────────────────────────────────────────────
# Evidence Ingestion Tests
# ──────────────────────────────────────────────


class TestEvidenceIngestion:
    """Tests for evidence ingestion."""

    def test_valid_evidence_ingestion(self):
        result = ingest_evidence(VALID_EVIDENCE)
        assert result.accepted is True
        assert len(result.evidence_items) == 2

    def test_empty_batch_fails(self):
        result = ingest_evidence([])
        assert result.accepted is False
        assert result.errors[0]["code"] == "EMPTY_EVIDENCE_BATCH"

    def test_unknown_type_rejected(self):
        result = ingest_evidence([{
            "evidence_id": "EV-BAD",
            "evidence_type": "unknown_thing",
        }])
        assert result.accepted is False
        assert any(e["code"] == "UNKNOWN_EVIDENCE_TYPE" for e in result.errors)

    def test_missing_id_rejected(self):
        result = ingest_evidence([{
            "evidence_type": "drawing",
        }])
        assert result.accepted is False


# ──────────────────────────────────────────────
# Assembly Identity Resolution Tests
# ──────────────────────────────────────────────


class TestAssemblyIdentityResolver:
    """Tests for assembly identity resolution."""

    def test_valid_resolution(self):
        result = resolve_assemblies(
            VALID_PROJECT["assemblies"],
            VALID_EVIDENCE,
        )
        assert result.resolved is True
        assert len(result.assemblies) == 1
        assert result.assemblies[0].assembly_type == "roof_assembly"

    def test_unknown_type_unresolved(self):
        result = resolve_assemblies(
            [{"assembly_id": "ASM-X", "assembly_type": "unknown_type"}],
            [],
        )
        assert "ASM-X" in result.unresolved_references

    def test_evidence_linked(self):
        result = resolve_assemblies(
            VALID_PROJECT["assemblies"],
            VALID_EVIDENCE,
        )
        assert len(result.assemblies[0].evidence_sources) == 2

    def test_interfaces_resolved(self):
        result = resolve_assemblies(
            VALID_PROJECT["assemblies"],
            [],
        )
        assert "roof_to_parapet" in result.assemblies[0].interface_types


# ──────────────────────────────────────────────
# Runtime Trigger Tests
# ──────────────────────────────────────────────


class TestRuntimeTrigger:
    """Tests for runtime triggering."""

    def test_trigger_produces_condition_packets(self):
        result = trigger_runtime([VALID_RUNTIME_CONDITION])
        assert result.triggered_count == 1
        assert result.success_count == 1
        assert result.pipeline_results[0].condition_packet is not None

    def test_empty_conditions_fails(self):
        result = trigger_runtime([])
        assert result.errors[0]["code"] == "EMPTY_CONDITIONS"

    def test_invalid_condition_fails_closed(self):
        result = trigger_runtime([{}])
        assert result.triggered_count == 1
        assert result.failure_count == 1

    def test_multiple_conditions(self):
        result = trigger_runtime([VALID_RUNTIME_CONDITION, VALID_RUNTIME_CONDITION])
        assert result.triggered_count == 2
        assert result.success_count == 2


# ──────────────────────────────────────────────
# Condition Inspector Tests
# ──────────────────────────────────────────────


class TestConditionInspector:
    """Tests for condition inspection."""

    def test_inspect_ready_packet(self):
        trigger_result = trigger_runtime([VALID_RUNTIME_CONDITION])
        packet = trigger_result.pipeline_results[0].condition_packet
        view = inspect_condition(packet)
        assert view.condition_id == "COND-001"
        assert view.readiness_state == "ready"
        assert view.is_ready is True

    def test_inspect_failed_packet(self):
        trigger_result = trigger_runtime([{}])
        packet = trigger_result.pipeline_results[0].condition_packet
        view = inspect_condition(packet)
        assert view.is_ready is False
        assert len(view.gaps) > 0

    def test_browse_sorts_blocked_first(self):
        r1 = trigger_runtime([VALID_RUNTIME_CONDITION])
        r2 = trigger_runtime([{}])
        packets = [
            r1.pipeline_results[0].condition_packet,
            r2.pipeline_results[0].condition_packet,
        ]
        views = browse_conditions(packets)
        # Blocked/incomplete should come before ready
        assert views[0].is_ready is False
        assert views[-1].is_ready is True


# ──────────────────────────────────────────────
# Boundary Enforcement Tests
# ──────────────────────────────────────────────


class TestIntakeBoundaryEnforcement:
    """Prove intake layer does not exceed its authority."""

    def test_intake_outputs_are_derived(self):
        """All intake results are derived dataclasses, not canonical truth."""
        record = ingest_project(VALID_PROJECT)
        assert isinstance(record, ProjectRecord)
        # ProjectRecord is a derived representation
        assert hasattr(record, "project_id")

    def test_trigger_does_not_modify_pipeline(self):
        """Triggering twice with same input produces same output."""
        r1 = trigger_runtime([VALID_RUNTIME_CONDITION])
        r2 = trigger_runtime([VALID_RUNTIME_CONDITION])
        assert r1.pipeline_results[0].detail_id == r2.pipeline_results[0].detail_id
        assert (r1.pipeline_results[0].render_result["svg_content"]
                == r2.pipeline_results[0].render_result["svg_content"])

    def test_intake_modules_do_not_import_kernel_contracts(self):
        """Intake modules must not directly import contract_loader."""
        import inspect
        from apps.intake import project_intake, evidence_ingestion
        from apps.intake import assembly_identity_resolver, condition_inspector
        for mod in [project_intake, evidence_ingestion,
                    assembly_identity_resolver, condition_inspector]:
            source = inspect.getsource(mod)
            assert "contract_loader" not in source, (
                f"{mod.__name__} must not import contract_loader directly"
            )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
