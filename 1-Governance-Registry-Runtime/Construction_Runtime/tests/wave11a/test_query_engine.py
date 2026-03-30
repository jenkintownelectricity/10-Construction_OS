"""L17 Query Engine tests — deterministic, read-only queries over a ConditionGraph."""

import pytest

from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph_queries.query_engine import QueryEngine

from tests.wave11a.conftest import (
    PROJECT_ID,
    build_standard_graph,
    make_condition_packet,
    make_blocker,
    make_evidence,
    make_artifact,
)


def _query_graph_with_blockers():
    """Build a graph where cond-1 is blocked by blk-1."""
    cp1 = make_condition_packet(
        condition_id="cond-q1",
        assembly_id="asm-q1",
        interface_id="",
        detail_id="",
        blocker_refs=["blk-q1"],
        dependency_refs=["cond-q2"],
        evidence_refs=["ev-q1"],
        artifact_refs=["art-q1"],
        remediation_candidate_refs=["cond-q2"],
        pattern_candidate_refs=[],
        owner_state="unknown",
    )
    cp2 = make_condition_packet(
        condition_id="cond-q2",
        assembly_id="",
        interface_id="",
        detail_id="",
        owner_state="assigned",
    )
    blk = make_blocker(blocker_id="blk-q1")
    ev = make_evidence(evidence_id="ev-q1")
    art = make_artifact(artifact_id="art-q1")

    graph = build_standard_graph(
        condition_packets=[cp1, cp2],
        blockers=[blk],
        evidence_records=[ev],
        artifacts=[art],
    )
    return graph, cp1, cp2


class TestQueryEngine:
    """L17: Query engine returns deterministic, correct results."""

    def test_neighborhood_query_deterministic(self):
        """Same graph produces the same neighborhood on repeated queries."""
        graph, cp1, _ = _query_graph_with_blockers()
        engine = QueryEngine(graph)

        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-q1", PROJECT_ID)
        n1 = engine.get_condition_neighborhood(cond1_nid, depth=1)
        n2 = engine.get_condition_neighborhood(cond1_nid, depth=1)

        assert n1["center"].graph_node_id == n2["center"].graph_node_id
        assert {n.graph_node_id for n in n1["neighbors"]} == {n.graph_node_id for n in n2["neighbors"]}
        assert {e.graph_edge_id for e in n1["edges"]} == {e.graph_edge_id for e in n2["edges"]}

    def test_get_blockers_returns_expected(self):
        """get_blockers must return blocker nodes connected via blocked_by edges."""
        graph, _, _ = _query_graph_with_blockers()
        engine = QueryEngine(graph)

        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-q1", PROJECT_ID)
        blockers = engine.get_blockers(cond1_nid)

        blocker_source_ids = {b.source_object_id for b in blockers}
        assert "blk-q1" in blocker_source_ids, "Expected blk-q1 in blockers"

    def test_get_dependencies_returns_expected(self):
        """get_dependencies must return dependency nodes connected via depends_on edges."""
        graph, _, _ = _query_graph_with_blockers()
        engine = QueryEngine(graph)

        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-q1", PROJECT_ID)
        deps = engine.get_dependencies(cond1_nid)

        dep_source_ids = {d.source_object_id for d in deps}
        assert "cond-q2" in dep_source_ids, "Expected cond-q2 in dependencies"

    def test_get_remediation_path_returns_expected(self):
        """get_remediation_path must return nodes connected via resolved_by edges."""
        graph, _, _ = _query_graph_with_blockers()
        engine = QueryEngine(graph)

        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-q1", PROJECT_ID)
        remediations = engine.get_remediation_path(cond1_nid)

        rem_source_ids = {r.source_object_id for r in remediations}
        assert "cond-q2" in rem_source_ids, "Expected cond-q2 in remediation path"

    def test_owner_route_preserves_unknown(self):
        """get_owner_route must return owner_state='unknown' when the owner is unknown."""
        graph, _, _ = _query_graph_with_blockers()
        engine = QueryEngine(graph)

        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-q1", PROJECT_ID)
        route = engine.get_owner_route(cond1_nid)

        assert route["owner_state"] == "unknown", (
            f"Expected owner_state='unknown', got '{route['owner_state']}'"
        )
        assert route["owner_node"] is not None, "Owner node must be present even when unknown"
