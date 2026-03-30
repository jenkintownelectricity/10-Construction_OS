"""
Tests for EdgeRegistry — Wave 17A.

Tests: edge registration, duplicate rejection, invalid edge rejection,
relation type validation, advisory/deterministic rules.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.identity_allocator import IdentityAllocator
from runtime.reference_graph.node_registry import NodeRegistry
from runtime.reference_graph.edge_registry import (
    EdgeRegistry,
    EdgeRegistrationError,
    ALL_RELATION_TYPES,
)


def _make_graph_with_nodes():
    """Create a registry with some pre-registered nodes."""
    alloc = IdentityAllocator()
    nodes = NodeRegistry(alloc)
    detail = nodes.register(
        object_type="DETAIL", scope="global",
        partition="global_kernel_partition",
        source_system="CK", source_reference="D-001",
        authority_type="kernel_canonical",
    )
    variant = nodes.register(
        object_type="VARIANT", scope="p1",
        partition="global_runtime_partition",
        source_system="CR", source_reference="V-001",
        authority_type="runtime_derived",
    )
    project = nodes.register(
        object_type="PROJECT", scope="p1",
        partition="global_runtime_partition",
        source_system="CR", source_reference="P-001",
        authority_type="project_instance",
    )
    drawing = nodes.register(
        object_type="DRAWING", scope="p1",
        partition="artifact_partition",
        source_system="CR", source_reference="DRW-001",
        authority_type="runtime_derived",
    )
    render_job = nodes.register(
        object_type="RENDER_JOB", scope="p1",
        partition="global_runtime_partition",
        source_system="CR", source_reference="RJ-001",
        authority_type="runtime_derived",
    )
    observation = nodes.register(
        object_type="OBSERVATION", scope="p1",
        partition="observation_partition",
        source_system="COR", source_reference="OBS-001",
        authority_type="project_instance",
    )
    markup = nodes.register(
        object_type="MARKUP", scope="p1",
        partition="artifact_partition",
        source_system="CR", source_reference="MK-001",
        authority_type="runtime_derived",
    )
    edges = EdgeRegistry(nodes)
    return nodes, edges, {
        "detail": detail, "variant": variant, "project": project,
        "drawing": drawing, "render_job": render_job,
        "observation": observation, "markup": markup,
    }


class TestEdgeRegistration:
    """Basic edge registration."""

    def test_register_derived_from_edge(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edge = edges.register(
            relation_type="derived_from",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
        )
        assert edge["relation_type"] == "derived_from"
        assert edge["status"] == "active"

    def test_register_rendered_from_edge(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edge = edges.register(
            relation_type="rendered_from",
            from_id=ids["drawing"]["graph_id"],
            to_id=ids["render_job"]["graph_id"],
        )
        assert edge["from_type"] == "DRAWING"
        assert edge["to_type"] == "RENDER_JOB"

    def test_edge_has_timestamp(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edge = edges.register(
            relation_type="derived_from",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
        )
        assert "T" in edge["created_timestamp"]


class TestDuplicateEdgeRejection:
    """Duplicate edges must fail closed or return existing."""

    def test_duplicate_edge_returns_existing(self):
        nodes, edges, ids = _make_graph_with_nodes()
        e1 = edges.register(
            relation_type="derived_from",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
        )
        e2 = edges.register(
            relation_type="derived_from",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
        )
        assert e1["edge_id"] == e2["edge_id"]

    def test_edge_count_no_duplicates(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edges.register(
            relation_type="derived_from",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
        )
        edges.register(
            relation_type="derived_from",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
        )
        assert edges.edge_count == 1


class TestInvalidEdgeRejection:
    """Invalid edges must fail closed."""

    def test_invalid_relation_type_fails(self):
        nodes, edges, ids = _make_graph_with_nodes()
        try:
            edges.register(
                relation_type="invalid_type",
                from_id=ids["variant"]["graph_id"],
                to_id=ids["detail"]["graph_id"],
            )
            assert False, "Should have raised EdgeRegistrationError"
        except EdgeRegistrationError:
            pass

    def test_missing_source_node_fails(self):
        nodes, edges, ids = _make_graph_with_nodes()
        try:
            edges.register(
                relation_type="derived_from",
                from_id="CRG-NONEXIST-000001",
                to_id=ids["detail"]["graph_id"],
            )
            assert False, "Should have raised EdgeRegistrationError"
        except EdgeRegistrationError:
            pass

    def test_missing_target_node_fails(self):
        nodes, edges, ids = _make_graph_with_nodes()
        try:
            edges.register(
                relation_type="derived_from",
                from_id=ids["variant"]["graph_id"],
                to_id="CRG-NONEXIST-000001",
            )
            assert False, "Should have raised EdgeRegistrationError"
        except EdgeRegistrationError:
            pass

    def test_invalid_from_type_for_relation_fails(self):
        """derived_from requires VARIANT as from_type."""
        nodes, edges, ids = _make_graph_with_nodes()
        try:
            edges.register(
                relation_type="derived_from",
                from_id=ids["detail"]["graph_id"],  # DETAIL, not VARIANT
                to_id=ids["detail"]["graph_id"],
            )
            assert False, "Should have raised EdgeRegistrationError"
        except EdgeRegistrationError:
            pass


class TestAdvisoryDeterministicRules:
    """Advisory edges cannot overwrite deterministic edges."""

    def test_advisory_cannot_be_deterministic_type(self):
        nodes, edges, ids = _make_graph_with_nodes()
        try:
            edges.register(
                relation_type="derived_from",
                from_id=ids["variant"]["graph_id"],
                to_id=ids["detail"]["graph_id"],
                is_advisory=True,
            )
            assert False, "Should have raised EdgeRegistrationError"
        except EdgeRegistrationError:
            pass

    def test_advisory_navigation_edge_allowed(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edge = edges.register(
            relation_type="related_to",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
            is_advisory=True,
        )
        assert edge["is_advisory"] is True

    def test_observation_edge_registration(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edge = edges.register(
            relation_type="observed_in",
            from_id=ids["observation"]["graph_id"],
            to_id=ids["project"]["graph_id"],
        )
        assert edge["relation_type"] == "observed_in"


class TestEdgeQueries:
    """Edge listing and lookup."""

    def test_get_edges_from_node(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edges.register(
            relation_type="derived_from",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
        )
        outgoing = edges.get_edges_from(ids["variant"]["graph_id"])
        assert len(outgoing) == 1

    def test_get_edges_to_node(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edges.register(
            relation_type="derived_from",
            from_id=ids["variant"]["graph_id"],
            to_id=ids["detail"]["graph_id"],
        )
        incoming = edges.get_edges_to(ids["detail"]["graph_id"])
        assert len(incoming) == 1

    def test_annotates_edge(self):
        nodes, edges, ids = _make_graph_with_nodes()
        edge = edges.register(
            relation_type="annotates",
            from_id=ids["markup"]["graph_id"],
            to_id=ids["drawing"]["graph_id"],
        )
        assert edge["relation_type"] == "annotates"
