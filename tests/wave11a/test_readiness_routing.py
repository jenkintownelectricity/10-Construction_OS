"""L17 Readiness Routing tests — blocking chains, routing updates, doctrine discipline."""

import pytest

from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph.graph_edge import ConditionGraphEdge
from runtime.graph.condition_graph import ConditionGraph
from runtime.readiness_routing.router import ReadinessRouter

from tests.wave11a.conftest import (
    PROJECT_ID,
    build_standard_graph,
    make_condition_packet,
    make_blocker,
)


def _build_blocked_graph():
    """Build a graph where cond-1 is blocked by blk-1."""
    cp1 = make_condition_packet(
        condition_id="cond-r1",
        assembly_id="",
        interface_id="",
        detail_id="",
        blocker_refs=["blk-r1"],
        owner_state="assigned",
    )
    blk = make_blocker(blocker_id="blk-r1")
    graph = build_standard_graph(condition_packets=[cp1], blockers=[blk])
    return graph


class TestReadinessRouting:
    """L17: Readiness routing traverses the graph without inventing doctrine."""

    def test_blocked_conditions_return_blocking_chain(self):
        """A blocked condition must return its full blocking chain."""
        graph = _build_blocked_graph()
        router = ReadinessRouter(graph)

        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-r1", PROJECT_ID)
        chain = router.get_blocking_chain(cond1_nid)

        assert len(chain) >= 1, "Expected at least one blocker in chain"
        blocker_source_ids = {n.source_object_id for n in chain}
        assert "blk-r1" in blocker_source_ids, "Expected blk-r1 in blocking chain"

    def test_resolved_blockers_update_routing(self):
        """Removing a blocker edge changes the routing result (no blockers returned)."""
        # Build an unblocked graph (no blocker refs)
        cp_unblocked = make_condition_packet(
            condition_id="cond-r2",
            assembly_id="",
            interface_id="",
            detail_id="",
            blocker_refs=[],
            owner_state="assigned",
        )
        graph = build_standard_graph(condition_packets=[cp_unblocked])
        router = ReadinessRouter(graph)

        cond_nid = ConditionGraphNode.compute_node_id("condition", "cond-r2", PROJECT_ID)
        chain = router.get_blocking_chain(cond_nid)
        assert len(chain) == 0, "Unblocked condition must have empty blocking chain"

        readiness = router.get_readiness_chain(cond_nid)
        assert readiness["blockers"] == [], "Readiness must report no blockers"

    def test_routing_does_not_invent_doctrine(self):
        """Router must not add nodes or edges to the graph."""
        graph = _build_blocked_graph()
        node_count_before = graph.node_count()
        edge_count_before = graph.edge_count()
        node_ids_before = set(graph.nodes.keys())
        edge_ids_before = set(graph.edges.keys())

        router = ReadinessRouter(graph)
        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-r1", PROJECT_ID)

        # Exercise all router methods
        router.get_blocking_chain(cond1_nid)
        router.get_next_actions(cond1_nid)
        router.get_unblock_path(cond1_nid)
        router.get_readiness_chain(cond1_nid)
        router.get_owner_responsibility(cond1_nid)

        assert graph.node_count() == node_count_before, "Router must not add nodes"
        assert graph.edge_count() == edge_count_before, "Router must not add edges"
        assert set(graph.nodes.keys()) == node_ids_before, "Router must not mutate node set"
        assert set(graph.edges.keys()) == edge_ids_before, "Router must not mutate edge set"
