"""
Tests for NodeRegistry — Wave 17A.

Tests: node registration, duplicate rejection, partition compliance,
lifecycle states, kernel immutability.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.identity_allocator import IdentityAllocator
from runtime.reference_graph.node_registry import (
    NodeRegistry,
    NodeRegistrationError,
    VALID_PARTITIONS,
)


def _make_registry():
    return NodeRegistry(IdentityAllocator())


class TestNodeRegistration:
    """Basic node registration."""

    def test_register_detail_node(self):
        reg = _make_registry()
        node = reg.register(
            object_type="DETAIL", scope="global",
            partition="global_kernel_partition",
            source_system="Construction_Kernel", source_reference="D-001",
            authority_type="kernel_canonical",
        )
        assert node["graph_id"].startswith("CRG-DETAIL-")
        assert node["object_type"] == "DETAIL"
        assert node["status"] == "active"

    def test_register_variant_node(self):
        reg = _make_registry()
        node = reg.register(
            object_type="VARIANT", scope="project-1",
            partition="global_runtime_partition",
            source_system="Construction_Runtime", source_reference="V-001",
            authority_type="runtime_derived",
        )
        assert node["graph_id"].startswith("CRG-VARIANT-")

    def test_register_with_metadata(self):
        reg = _make_registry()
        node = reg.register(
            object_type="DETAIL", scope="global",
            partition="global_kernel_partition",
            source_system="CK", source_reference="D-002",
            authority_type="kernel_canonical",
            metadata={"display_name": "Parapet Detail"},
        )
        assert node["metadata"]["display_name"] == "Parapet Detail"

    def test_node_has_timestamp(self):
        reg = _make_registry()
        node = reg.register(
            object_type="DETAIL", scope="global",
            partition="global_kernel_partition",
            source_system="CK", source_reference="D-003",
            authority_type="kernel_canonical",
        )
        assert "created_timestamp" in node
        assert "T" in node["created_timestamp"]


class TestDuplicateNodeRejection:
    """Duplicate nodes must fail closed."""

    def test_duplicate_node_returns_existing(self):
        reg = _make_registry()
        n1 = reg.register(
            object_type="DETAIL", scope="global",
            partition="global_kernel_partition",
            source_system="CK", source_reference="D-001",
            authority_type="kernel_canonical",
        )
        # Idempotent replay with same fingerprint returns existing
        n2 = reg.register(
            object_type="DETAIL", scope="global",
            partition="global_kernel_partition",
            source_system="CK", source_reference="D-001",
            authority_type="kernel_canonical",
        )
        assert n1["graph_id"] == n2["graph_id"]


class TestPartitionCompliance:
    """Object types must be in correct partitions."""

    def test_detail_in_wrong_partition_fails(self):
        reg = _make_registry()
        try:
            reg.register(
                object_type="DETAIL", scope="project-1",
                partition="project_partition",
                source_system="CK", source_reference="D-001",
                authority_type="kernel_canonical",
            )
            assert False, "Should have raised NodeRegistrationError"
        except NodeRegistrationError:
            pass

    def test_observation_in_wrong_partition_fails(self):
        reg = _make_registry()
        try:
            reg.register(
                object_type="OBSERVATION", scope="p1",
                partition="global_runtime_partition",
                source_system="COR", source_reference="O-001",
                authority_type="project_instance",
            )
            assert False, "Should have raised NodeRegistrationError"
        except NodeRegistrationError:
            pass

    def test_observation_in_correct_partition(self):
        reg = _make_registry()
        node = reg.register(
            object_type="OBSERVATION", scope="p1",
            partition="observation_partition",
            source_system="COR", source_reference="O-001",
            authority_type="project_instance",
        )
        assert node["partition"] == "observation_partition"

    def test_drawing_must_be_in_artifact_partition(self):
        reg = _make_registry()
        try:
            reg.register(
                object_type="DRAWING", scope="p1",
                partition="project_partition",
                source_system="CR", source_reference="DRW-001",
                authority_type="runtime_derived",
            )
            assert False, "Should have raised NodeRegistrationError"
        except NodeRegistrationError:
            pass


class TestLifecycleStates:
    """Lifecycle state management."""

    def test_update_status_to_superseded(self):
        reg = _make_registry()
        node = reg.register(
            object_type="VARIANT", scope="p1",
            partition="global_runtime_partition",
            source_system="CR", source_reference="V-001",
            authority_type="runtime_derived",
        )
        updated = reg.update_status(node["graph_id"], "superseded")
        assert updated["status"] == "superseded"

    def test_cannot_change_archived_status(self):
        reg = _make_registry()
        node = reg.register(
            object_type="VARIANT", scope="p1",
            partition="global_runtime_partition",
            source_system="CR", source_reference="V-002",
            authority_type="runtime_derived",
        )
        reg.update_status(node["graph_id"], "archived")
        try:
            reg.update_status(node["graph_id"], "active")
            assert False, "Should have raised NodeRegistrationError"
        except NodeRegistrationError:
            pass

    def test_invalid_status_fails(self):
        reg = _make_registry()
        node = reg.register(
            object_type="VARIANT", scope="p1",
            partition="global_runtime_partition",
            source_system="CR", source_reference="V-003",
            authority_type="runtime_derived",
        )
        try:
            reg.update_status(node["graph_id"], "deleted")
            assert False, "Should have raised NodeRegistrationError"
        except NodeRegistrationError:
            pass


class TestNodeQueries:
    """Node listing and lookup."""

    def test_list_nodes_by_type(self):
        reg = _make_registry()
        reg.register(
            object_type="DETAIL", scope="global",
            partition="global_kernel_partition",
            source_system="CK", source_reference="D-001",
            authority_type="kernel_canonical",
        )
        reg.register(
            object_type="VARIANT", scope="p1",
            partition="global_runtime_partition",
            source_system="CR", source_reference="V-001",
            authority_type="runtime_derived",
        )
        details = reg.list_nodes(object_type="DETAIL")
        assert len(details) == 1
        assert details[0]["object_type"] == "DETAIL"

    def test_get_by_fingerprint(self):
        reg = _make_registry()
        node = reg.register(
            object_type="DETAIL", scope="global",
            partition="global_kernel_partition",
            source_system="CK", source_reference="D-001",
            authority_type="kernel_canonical",
        )
        found = reg.get_by_fingerprint("CK", "D-001", "DETAIL", "global")
        assert found is not None
        assert found["graph_id"] == node["graph_id"]

    def test_node_count(self):
        reg = _make_registry()
        assert reg.node_count == 0
        reg.register(
            object_type="DETAIL", scope="global",
            partition="global_kernel_partition",
            source_system="CK", source_reference="D-001",
            authority_type="kernel_canonical",
        )
        assert reg.node_count == 1
