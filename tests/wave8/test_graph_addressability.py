"""Tests for graph addressability — Wave 8A structural validation.

Validates that condition packets are graph-addressable and that the
GraphReferenceService supports creation and resolution of references.
"""

import pytest

from runtime.models.condition_packet import ConditionPacket
from runtime.graph_refs.graph_service import GraphReferenceService


# ---------------------------------------------------------------------------
# ConditionPacket graph_ref field
# ---------------------------------------------------------------------------

class TestConditionPacketGraphRef:
    """Verify ConditionPacket has the graph_ref field for addressability."""

    def test_graph_ref_field_exists(self):
        packet = ConditionPacket()
        assert hasattr(packet, "graph_ref")

    def test_graph_ref_default_is_empty_string(self):
        packet = ConditionPacket()
        assert packet.graph_ref == ""

    def test_graph_ref_can_be_set(self):
        packet = ConditionPacket(graph_ref="project/assembly-01/detail-03")
        assert packet.graph_ref == "project/assembly-01/detail-03"


# ---------------------------------------------------------------------------
# GraphReferenceService instantiation
# ---------------------------------------------------------------------------

class TestGraphReferenceServiceInstantiation:
    """Verify GraphReferenceService can be created and has expected methods."""

    def test_can_instantiate_without_args(self):
        service = GraphReferenceService()
        assert service is not None

    def test_can_instantiate_with_contract_loader(self):
        service = GraphReferenceService(contract_loader="mock_loader")
        assert service._contract_loader == "mock_loader"

    def test_has_create_ref_method(self):
        service = GraphReferenceService()
        assert callable(getattr(service, "create_ref", None))

    def test_has_resolve_ref_method(self):
        service = GraphReferenceService()
        assert callable(getattr(service, "resolve_ref", None))

    def test_has_attach_ref_method(self):
        service = GraphReferenceService()
        assert callable(getattr(service, "attach_ref", None))

    def test_has_validate_graph_addressability_method(self):
        service = GraphReferenceService()
        assert callable(getattr(service, "validate_graph_addressability", None))


# ---------------------------------------------------------------------------
# Condition packet reference preservation
# ---------------------------------------------------------------------------

class TestConditionPacketRefPreservation:
    """Verify blocker_refs and dependency_refs are preserved on packets."""

    def test_blocker_refs_preserved(self):
        refs = ["blocker-x", "blocker-y"]
        packet = ConditionPacket(blocker_refs=refs)
        assert packet.blocker_refs == ["blocker-x", "blocker-y"]

    def test_dependency_refs_preserved(self):
        refs = ["dep-1", "dep-2", "dep-3"]
        packet = ConditionPacket(dependency_refs=refs)
        assert packet.dependency_refs == ["dep-1", "dep-2", "dep-3"]

    def test_blocker_refs_default_empty(self):
        packet = ConditionPacket()
        assert packet.blocker_refs == []

    def test_dependency_refs_default_empty(self):
        packet = ConditionPacket()
        assert packet.dependency_refs == []

    def test_blocker_refs_are_independent_between_instances(self):
        """Ensure default list factory prevents shared state between instances."""
        p1 = ConditionPacket()
        p2 = ConditionPacket()
        p1.blocker_refs.append("only-on-p1")
        assert p2.blocker_refs == []

    def test_dependency_refs_are_independent_between_instances(self):
        p1 = ConditionPacket()
        p2 = ConditionPacket()
        p1.dependency_refs.append("only-on-p1")
        assert p2.dependency_refs == []
