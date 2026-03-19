"""Tests for ConditionPacket model — Wave 8A structural validation."""

import pytest
from dataclasses import fields

from runtime.models.condition_packet import ConditionPacket


# ---------------------------------------------------------------------------
# Required fields
# ---------------------------------------------------------------------------

REQUIRED_FIELD_NAMES = [
    "condition_id",
    "assembly_id",
    "interface_id",
    "detail_id",
    "parameter_state",
    "issue_state",
    "readiness_state",
    "owner_state",
    "blocker_refs",
    "remediation_candidate_refs",
    "artifact_refs",
    "evidence_refs",
    "graph_ref",
    "dependency_refs",
    "pattern_candidate_refs",
    "pattern_match_basis",
    "pattern_confidence",
]


class TestConditionPacketFields:
    """Verify that ConditionPacket exposes all required fields."""

    def test_all_required_fields_present(self):
        field_names = {f.name for f in fields(ConditionPacket)}
        for name in REQUIRED_FIELD_NAMES:
            assert name in field_names, f"ConditionPacket is missing required field: {name}"

    @pytest.mark.parametrize("field_name", REQUIRED_FIELD_NAMES)
    def test_individual_field_exists(self, field_name):
        field_names = {f.name for f in fields(ConditionPacket)}
        assert field_name in field_names


class TestConditionPacketDefaults:
    """Verify default values for state fields."""

    def test_default_owner_state_is_unknown(self):
        packet = ConditionPacket()
        assert packet.owner_state == "unknown"

    def test_default_readiness_state_is_unknown(self):
        packet = ConditionPacket()
        assert packet.readiness_state == "unknown"

    def test_default_issue_state_is_none(self):
        packet = ConditionPacket()
        assert packet.issue_state == "none"

    def test_default_pattern_confidence_is_zero(self):
        packet = ConditionPacket()
        assert packet.pattern_confidence == 0.0


class TestConditionPacketGraphAddressability:
    """Verify graph_ref field is present (graph-addressable requirement)."""

    def test_graph_ref_field_exists(self):
        packet = ConditionPacket()
        assert hasattr(packet, "graph_ref")

    def test_graph_ref_is_string(self):
        packet = ConditionPacket()
        assert isinstance(packet.graph_ref, str)


class TestConditionPacketReferencePreservation:
    """Verify that reference list fields preserve their contents."""

    def test_blocker_refs_preserved(self):
        refs = ["blocker-1", "blocker-2"]
        packet = ConditionPacket(blocker_refs=refs)
        assert packet.blocker_refs == ["blocker-1", "blocker-2"]

    def test_dependency_refs_preserved(self):
        refs = ["dep-a", "dep-b", "dep-c"]
        packet = ConditionPacket(dependency_refs=refs)
        assert packet.dependency_refs == ["dep-a", "dep-b", "dep-c"]

    def test_artifact_refs_preserved(self):
        refs = ["art-1"]
        packet = ConditionPacket(artifact_refs=refs)
        assert packet.artifact_refs == ["art-1"]

    def test_evidence_refs_preserved(self):
        refs = ["ev-100", "ev-200"]
        packet = ConditionPacket(evidence_refs=refs)
        assert packet.evidence_refs == ["ev-100", "ev-200"]

    def test_remediation_candidate_refs_preserved(self):
        refs = ["rem-1"]
        packet = ConditionPacket(remediation_candidate_refs=refs)
        assert packet.remediation_candidate_refs == ["rem-1"]

    def test_pattern_candidate_refs_preserved(self):
        refs = ["pat-a", "pat-b"]
        packet = ConditionPacket(pattern_candidate_refs=refs)
        assert packet.pattern_candidate_refs == ["pat-a", "pat-b"]

    def test_default_lists_are_empty(self):
        packet = ConditionPacket()
        assert packet.blocker_refs == []
        assert packet.dependency_refs == []
        assert packet.artifact_refs == []
        assert packet.evidence_refs == []
        assert packet.remediation_candidate_refs == []
        assert packet.pattern_candidate_refs == []
