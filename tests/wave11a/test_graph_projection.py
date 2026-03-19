"""L17 Graph Projection tests — deterministic projection from source models."""

import pytest

from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph.materialize_graph import GraphMaterializer
from runtime.models.condition_packet import ConditionPacket

from tests.wave11a.conftest import (
    PROJECT_ID,
    build_standard_graph,
    make_condition_packet,
    make_blocker,
    make_issue,
    make_evidence,
    make_revision,
    make_package,
    make_artifact,
)


def _standard_inputs():
    """Return a complete set of standard inputs for materialization."""
    cp1 = make_condition_packet(
        condition_id="cond-1",
        assembly_id="asm-1",
        interface_id="ifc-1",
        detail_id="dtl-1",
        blocker_refs=["blk-1"],
        dependency_refs=["cond-2"],
        evidence_refs=["ev-1"],
        artifact_refs=["art-1"],
        remediation_candidate_refs=[],
        pattern_candidate_refs=["pat-1"],
        owner_state="unknown",
    )
    cp2 = make_condition_packet(
        condition_id="cond-2",
        assembly_id="asm-2",
        interface_id="",
        detail_id="",
        owner_state="assigned",
    )
    blk = make_blocker(blocker_id="blk-1")
    iss = make_issue(issue_id="iss-1")
    ev = make_evidence(evidence_id="ev-1")
    rev = make_revision(lineage_id="rev-lin-1")
    pkg = make_package(package_id="pkg-1")
    art = make_artifact(artifact_id="art-1")
    pats = [{"pattern_id": "pat-1", "state_summary": {"label": "crack"}, "metadata": {}}]

    return dict(
        project_id=PROJECT_ID,
        condition_packets=[cp1, cp2],
        issues=[iss],
        blockers=[blk],
        evidence_records=[ev],
        revision_lineages=[rev],
        packages=[pkg],
        artifacts=[art],
        pattern_refs=pats,
    )


class TestGraphProjection:
    """L17: Graph projection produces a deterministic, complete graph."""

    def test_identical_inputs_produce_identical_projections(self):
        """Materializing twice from the same inputs must yield the same graph."""
        inputs = _standard_inputs()
        g1 = build_standard_graph(**inputs)
        g2 = build_standard_graph(**inputs)

        assert set(g1.nodes.keys()) == set(g2.nodes.keys()), "Node ID sets differ"
        assert set(g1.edges.keys()) == set(g2.edges.keys()), "Edge ID sets differ"
        assert g1.node_count() == g2.node_count()
        assert g1.edge_count() == g2.edge_count()

    def test_every_condition_packet_produces_node(self):
        """Every ConditionPacket must produce a condition node in the graph."""
        inputs = _standard_inputs()
        graph = build_standard_graph(**inputs)

        condition_nodes = graph.get_nodes_by_type("condition")
        condition_ids = {n.source_object_id for n in condition_nodes}

        for cp in inputs["condition_packets"]:
            assert cp.condition_id in condition_ids, (
                f"ConditionPacket {cp.condition_id} did not produce a condition node"
            )

    def test_blocker_refs_become_blocked_by_edges(self):
        """blocker_refs on a ConditionPacket must produce blocked_by edges."""
        inputs = _standard_inputs()
        graph = build_standard_graph(**inputs)

        blocked_by_edges = graph.get_edges_by_type("blocked_by")
        assert len(blocked_by_edges) > 0, "Expected at least one blocked_by edge"

        # cond-1 has blocker_refs=["blk-1"], so there must be a blocked_by edge
        # from cond-1's node to blk-1's node
        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-1", PROJECT_ID)
        blk1_nid = ConditionGraphNode.compute_node_id("blocker", "blk-1", PROJECT_ID)

        matching = [
            e for e in blocked_by_edges
            if e.from_node_id == cond1_nid and e.to_node_id == blk1_nid
        ]
        assert len(matching) == 1, f"Expected blocked_by edge from cond-1 to blk-1"

    def test_dependency_refs_become_depends_on_edges(self):
        """dependency_refs on a ConditionPacket must produce depends_on edges."""
        inputs = _standard_inputs()
        graph = build_standard_graph(**inputs)

        depends_on_edges = graph.get_edges_by_type("depends_on")
        assert len(depends_on_edges) > 0, "Expected at least one depends_on edge"

        cond1_nid = ConditionGraphNode.compute_node_id("condition", "cond-1", PROJECT_ID)
        cond2_nid = ConditionGraphNode.compute_node_id("condition", "cond-2", PROJECT_ID)

        matching = [
            e for e in depends_on_edges
            if e.from_node_id == cond1_nid and e.to_node_id == cond2_nid
        ]
        assert len(matching) == 1, "Expected depends_on edge from cond-1 to cond-2"

    def test_no_required_node_omissions(self):
        """All source objects must produce nodes — none may be silently omitted."""
        inputs = _standard_inputs()
        graph = build_standard_graph(**inputs)

        # Check each source object type is represented
        assert len(graph.get_nodes_by_type("condition")) == 2
        assert len(graph.get_nodes_by_type("blocker")) == 1
        assert len(graph.get_nodes_by_type("issue")) == 1
        assert len(graph.get_nodes_by_type("evidence")) == 1
        assert len(graph.get_nodes_by_type("revision")) == 1
        assert len(graph.get_nodes_by_type("package")) == 1
        assert len(graph.get_nodes_by_type("artifact")) == 1
        assert len(graph.get_nodes_by_type("pattern")) == 1
        assert len(graph.get_nodes_by_type("owner")) == 2  # one per condition
        # assembly: asm-1 from cond-1, asm-2 from cond-2
        assert len(graph.get_nodes_by_type("assembly")) == 2
        # interface: ifc-1 from cond-1 only (cond-2 has no interface)
        assert len(graph.get_nodes_by_type("interface")) == 1
        # detail: dtl-1 from cond-1 only
        assert len(graph.get_nodes_by_type("detail")) == 1

    def test_node_identity_stable_across_rebuilds(self):
        """Recomputing node IDs must yield the same values as the original graph."""
        inputs = _standard_inputs()
        graph = build_standard_graph(**inputs)

        for nid, node in graph.nodes.items():
            recomputed = ConditionGraphNode.compute_node_id(
                node.source_object_type, node.source_object_id, node.project_id
            )
            assert nid == recomputed, (
                f"Node {nid} identity mismatch on recompute: got {recomputed}"
            )

    def test_owner_unknown_preserved(self):
        """owner_state='unknown' must create an explicit owner node with state_summary."""
        cp = make_condition_packet(
            condition_id="cond-unk",
            assembly_id="",
            interface_id="",
            detail_id="",
            owner_state="unknown",
        )
        graph = build_standard_graph(condition_packets=[cp])

        owner_nodes = graph.get_nodes_by_type("owner")
        assert len(owner_nodes) == 1, "Expected exactly one owner node"

        owner = owner_nodes[0]
        assert owner.state_summary.get("owner_state") == "unknown", (
            "Owner node must preserve owner_state='unknown'"
        )
