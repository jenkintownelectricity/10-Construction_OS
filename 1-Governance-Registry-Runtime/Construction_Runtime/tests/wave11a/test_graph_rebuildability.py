"""L17 Graph Rebuildability tests — deterministic rebuild from identical inputs."""

import pytest

from runtime.graph.materialize_graph import GraphMaterializer
from runtime.graph_validation.graph_validator import GraphValidator

from tests.wave11a.conftest import (
    PROJECT_ID,
    build_standard_graph,
    make_condition_packet,
    make_blocker,
    make_evidence,
    make_revision,
    make_package,
    make_artifact,
)


def _rebuild_inputs():
    cp = make_condition_packet(
        condition_id="cond-r1",
        assembly_id="asm-r1",
        interface_id="ifc-r1",
        detail_id="dtl-r1",
        blocker_refs=["blk-r1"],
        dependency_refs=[],
        evidence_refs=["ev-r1"],
        artifact_refs=["art-r1"],
        owner_state="assigned",
    )
    blk = make_blocker(blocker_id="blk-r1")
    ev = make_evidence(evidence_id="ev-r1")
    rev = make_revision(lineage_id="rev-r1")
    pkg = make_package(package_id="pkg-r1")
    art = make_artifact(artifact_id="art-r1")

    return dict(
        project_id=PROJECT_ID,
        condition_packets=[cp],
        issues=[],
        blockers=[blk],
        evidence_records=[ev],
        revision_lineages=[rev],
        packages=[pkg],
        artifacts=[art],
    )


class TestGraphRebuildability:
    """L17: Graphs rebuilt from identical inputs must be identical."""

    def test_graph_reconstructed_deterministically(self):
        """Two independent builds from the same inputs produce the same graph."""
        inputs = _rebuild_inputs()
        g1 = build_standard_graph(**inputs)
        g2 = build_standard_graph(**inputs)

        assert set(g1.nodes.keys()) == set(g2.nodes.keys())
        assert set(g1.edges.keys()) == set(g2.edges.keys())

        # Also verify node contents match
        for nid in g1.nodes:
            n1 = g1.nodes[nid]
            n2 = g2.nodes[nid]
            assert n1.node_type == n2.node_type
            assert n1.source_object_type == n2.source_object_type
            assert n1.source_object_id == n2.source_object_id
            assert n1.state_summary == n2.state_summary

    def test_graph_validator_rebuildability_check(self):
        """GraphValidator.validate_rebuildability returns no errors for identical builds."""
        inputs = _rebuild_inputs()
        g1 = build_standard_graph(**inputs)
        g2 = build_standard_graph(**inputs)

        validator = GraphValidator()
        errors = validator.validate_rebuildability(g1, g2)
        assert errors == [], f"Rebuildability errors: {errors}"
