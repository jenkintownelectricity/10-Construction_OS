"""Tests for OverlayEngine — overlay annotations on graph nodes."""

import pytest

from runtime.navigation_overlays.overlay_engine import OverlayEngine


@pytest.fixture()
def oe():
    return OverlayEngine()


class TestReadinessOverlay:
    def test_readiness_overlay_all_nodes_annotated(self, oe, sample_graph):
        result = oe.get_readiness_overlay(sample_graph)
        assert isinstance(result, list)
        assert len(result) == sample_graph.node_count()
        for item in result:
            assert "readiness_state" in item
            assert item["readiness_state"] in (
                "ready", "pending", "blocked", "unknown"
            )


class TestBlockerOverlay:
    def test_blocker_overlay_returns_blockers(self, oe, sample_graph):
        result = oe.get_blocker_overlay(sample_graph)
        assert isinstance(result, list)
        assert len(result) == sample_graph.node_count()
        for item in result:
            assert "has_blockers" in item
            assert "blocker_count" in item
            assert "immediate_blocker_ids" in item
        # At least one node should have blockers (cond-1)
        blocked_nodes = [n for n in result if n["has_blockers"]]
        assert len(blocked_nodes) > 0


class TestOwnershipOverlay:
    def test_ownership_overlay_preserves_unknown(self, oe, sample_graph):
        result = oe.get_ownership_overlay(sample_graph)
        assert isinstance(result, list)
        assert len(result) == sample_graph.node_count()
        for item in result:
            assert "owner_state" in item
            assert item["owner_state"] in ("assigned", "unassigned", "unknown")
            assert "owner_node_id" in item


class TestPatternOverlay:
    def test_pattern_overlay_marks_enrichment(self, oe, sample_graph):
        result = oe.get_pattern_overlay(sample_graph)
        assert isinstance(result, list)
        for item in result:
            assert "has_pattern_classification" in item
            assert "pattern_classifications" in item
            for pc in item["pattern_classifications"]:
                assert pc["is_enrichment_derived"] is True


class TestImpactOverlay:
    def test_impact_overlay_deterministic(self, oe, sample_graph):
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition"
        ]
        assert len(cond_ids) > 0
        r1 = oe.get_impact_overlay(sample_graph, cond_ids[0])
        r2 = oe.get_impact_overlay(sample_graph, cond_ids[0])
        assert r1 == r2
        assert "downstream" in r1
        assert "upstream" in r1
        assert "impacted_artifacts" in r1
        assert "impacted_packages" in r1
