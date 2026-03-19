"""Tests for ExplanationPanelBuilder — structured explanation panels."""

import pytest

from runtime.navigation_panels.explanation_panels import ExplanationPanelBuilder


@pytest.fixture()
def epb():
    return ExplanationPanelBuilder()


class TestWhyBlocked:
    def test_why_blocked_includes_blockers(self, epb, sample_graph):
        # cond-1 has a blocker
        cond1_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition" and n.source_object_id == "cond-1"
        ]
        assert len(cond1_ids) == 1
        result = epb.build_why_blocked(sample_graph, cond1_ids[0])
        assert "immediate_blockers" in result
        assert "upstream_blockers" in result
        assert "owner_route" in result
        assert "remediation_path" in result
        assert len(result["immediate_blockers"]) > 0

    def test_why_blocked_unblocked_node(self, epb, sample_graph):
        # cond-3 has no blockers
        cond3_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition" and n.source_object_id == "cond-3"
        ]
        assert len(cond3_ids) == 1
        result = epb.build_why_blocked(sample_graph, cond3_ids[0])
        assert result["immediate_blockers"] == []


class TestWhatDepends:
    def test_what_depends_includes_downstream(self, epb, sample_graph):
        # cond-2 is depended on by cond-1
        cond2_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition" and n.source_object_id == "cond-2"
        ]
        assert len(cond2_ids) == 1
        result = epb.build_what_depends(sample_graph, cond2_ids[0])
        assert "downstream_conditions" in result
        assert "downstream_artifacts" in result
        assert "package_implications" in result


class TestEvidenceSupport:
    def test_evidence_support_includes_refs(self, epb, sample_graph):
        # cond-1 has evidence refs
        cond1_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition" and n.source_object_id == "cond-1"
        ]
        assert len(cond1_ids) == 1
        result = epb.build_evidence_support(sample_graph, cond1_ids[0])
        assert "evidence_refs" in result
        assert "source_provenance" in result
        # cond-1 has a supported_by edge to ev-1
        assert len(result["evidence_refs"]) > 0

    def test_evidence_support_no_evidence(self, epb, sample_graph):
        # cond-3 has no evidence
        cond3_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition" and n.source_object_id == "cond-3"
        ]
        assert len(cond3_ids) == 1
        result = epb.build_evidence_support(sample_graph, cond3_ids[0])
        assert result["evidence_refs"] == []
