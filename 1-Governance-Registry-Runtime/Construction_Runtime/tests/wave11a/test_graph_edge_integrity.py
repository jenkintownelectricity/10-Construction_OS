"""L17 Graph Edge Integrity tests — duplicate prevention and enrichment tagging."""

import pytest

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph.graph_edge import ConditionGraphEdge

from tests.wave11a.conftest import (
    PROJECT_ID,
    build_standard_graph,
    make_condition_packet,
)


def _make_test_node(project_id, source_type, source_id):
    nid = ConditionGraphNode.compute_node_id(source_type, source_id, project_id)
    return ConditionGraphNode(
        graph_node_id=nid,
        node_type=source_type,
        source_object_type=source_type,
        source_object_id=source_id,
        project_id=project_id,
    )


def _make_test_edge(edge_type, from_id, to_id, project_id, is_enrichment=False):
    eid = ConditionGraphEdge.compute_edge_id(edge_type, from_id, to_id, project_id)
    return ConditionGraphEdge(
        graph_edge_id=eid,
        edge_type=edge_type,
        from_node_id=from_id,
        to_node_id=to_id,
        project_id=project_id,
        is_enrichment_derived=is_enrichment,
    )


class TestGraphEdgeIntegrity:
    """L17: Edge integrity — no duplicates, enrichment clearly tagged."""

    def test_duplicate_edges_prevented(self):
        """Adding the same edge twice to a ConditionGraph must raise ValueError."""
        graph = ConditionGraph(project_id=PROJECT_ID)

        n1 = _make_test_node(PROJECT_ID, "condition", "c1")
        n2 = _make_test_node(PROJECT_ID, "condition", "c2")
        graph.add_node(n1)
        graph.add_node(n2)

        edge = _make_test_edge("depends_on", n1.graph_node_id, n2.graph_node_id, PROJECT_ID)
        graph.add_edge(edge)

        # Second add of the same edge must raise
        with pytest.raises(ValueError, match="Duplicate edge"):
            graph.add_edge(edge)

    def test_enrichment_edges_distinguishable(self):
        """classified_as edges must have is_enrichment_derived=True."""
        cp = make_condition_packet(
            condition_id="cond-e1",
            assembly_id="",
            interface_id="",
            detail_id="",
            pattern_candidate_refs=["pat-e1"],
        )
        pats = [{"pattern_id": "pat-e1", "state_summary": {}, "metadata": {}}]
        graph = build_standard_graph(condition_packets=[cp], pattern_refs=pats)

        classified_edges = graph.get_edges_by_type("classified_as")
        assert len(classified_edges) >= 1, "Expected at least one classified_as edge"

        for edge in classified_edges:
            assert edge.is_enrichment_derived is True, (
                f"classified_as edge {edge.graph_edge_id} must have is_enrichment_derived=True"
            )

    def test_hard_edges_not_enrichment(self):
        """depends_on, blocked_by, owned_by, etc. must have is_enrichment_derived=False."""
        cp1 = make_condition_packet(
            condition_id="cond-h1",
            assembly_id="asm-h1",
            interface_id="",
            detail_id="",
            dependency_refs=["cond-h2"],
        )
        cp2 = make_condition_packet(
            condition_id="cond-h2",
            assembly_id="",
            interface_id="",
            detail_id="",
        )
        graph = build_standard_graph(condition_packets=[cp1, cp2])

        hard_edge_types = {"depends_on", "blocked_by", "owned_by", "included_in",
                           "interfaces_with", "implemented_by", "supported_by", "derived_from"}

        for edge in graph.edges.values():
            if edge.edge_type in hard_edge_types:
                assert edge.is_enrichment_derived is False, (
                    f"Hard edge {edge.edge_type} ({edge.graph_edge_id}) "
                    f"must have is_enrichment_derived=False"
                )
