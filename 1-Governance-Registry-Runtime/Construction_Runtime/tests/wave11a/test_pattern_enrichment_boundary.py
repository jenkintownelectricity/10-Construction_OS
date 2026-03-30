"""L17 Pattern Enrichment Boundary tests — enrichment edges and mutation discipline."""

import copy

import pytest

from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph_queries.query_engine import QueryEngine

from tests.wave11a.conftest import (
    PROJECT_ID,
    build_standard_graph,
    make_condition_packet,
)


def _build_pattern_graph():
    """Build a graph with pattern candidate refs creating classified_as edges."""
    cp = make_condition_packet(
        condition_id="cond-p1",
        assembly_id="asm-p1",
        interface_id="",
        detail_id="",
        pattern_candidate_refs=["pat-p1", "pat-p2"],
        owner_state="assigned",
    )
    pats = [
        {"pattern_id": "pat-p1", "state_summary": {"label": "crack"}, "metadata": {}},
        {"pattern_id": "pat-p2", "state_summary": {"label": "spall"}, "metadata": {}},
    ]
    graph = build_standard_graph(condition_packets=[cp], pattern_refs=pats)
    return graph, cp


class TestPatternEnrichmentBoundary:
    """L17: Pattern enrichment edges are clearly tagged and don't mutate protected state."""

    def test_enrichment_edges_distinguishable(self):
        """classified_as edges must have is_enrichment_derived=True."""
        graph, _ = _build_pattern_graph()

        classified_edges = graph.get_edges_by_type("classified_as")
        assert len(classified_edges) >= 2, "Expected at least two classified_as edges"

        for edge in classified_edges:
            assert edge.is_enrichment_derived is True, (
                f"classified_as edge {edge.graph_edge_id} must be enrichment-derived"
            )

    def test_pattern_candidates_dont_mutate_protected_state(self):
        """Materializing a graph with patterns must not alter protected condition fields.

        Protected fields: condition_id, assembly_id, issue_state, readiness_state, owner_state.
        """
        cp = make_condition_packet(
            condition_id="cond-prot",
            assembly_id="asm-prot",
            interface_id="ifc-prot",
            detail_id="dtl-prot",
            issue_state="open",
            readiness_state="blocked",
            owner_state="assigned",
            pattern_candidate_refs=["pat-prot"],
        )
        pats = [{"pattern_id": "pat-prot", "state_summary": {"label": "rust"}, "metadata": {}}]

        # Take a deep copy of the condition packet before materialization
        cp_before = copy.deepcopy(cp)

        graph = build_standard_graph(condition_packets=[cp], pattern_refs=pats)

        # Verify the condition packet was not mutated
        assert cp.condition_id == cp_before.condition_id
        assert cp.assembly_id == cp_before.assembly_id
        assert cp.issue_state == cp_before.issue_state
        assert cp.readiness_state == cp_before.readiness_state
        assert cp.owner_state == cp_before.owner_state

        # Verify the projected condition node preserves state
        cond_nid = ConditionGraphNode.compute_node_id("condition", "cond-prot", PROJECT_ID)
        cond_node = graph.get_node(cond_nid)
        assert cond_node is not None
        assert cond_node.state_summary["issue_state"] == "open"
        assert cond_node.state_summary["readiness_state"] == "blocked"
        assert cond_node.state_summary["owner_state"] == "assigned"
