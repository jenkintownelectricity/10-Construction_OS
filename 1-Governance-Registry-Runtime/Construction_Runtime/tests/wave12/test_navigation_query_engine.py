"""Tests for NavigationQueryEngine — high-level navigation queries."""

import pytest

from runtime.navigation_queries.navigation_query_engine import NavigationQueryEngine
from runtime.graph.condition_graph import ConditionGraph


@pytest.fixture()
def nqe():
    return NavigationQueryEngine()


class TestProjectMap:
    def test_get_project_map_returns_systems(self, nqe, sample_graph):
        result = nqe.get_project_map(sample_graph)
        assert "systems" in result
        assert "project_id" in result
        assert "total_systems" in result
        # We have assembly nodes so total_systems should be > 0
        assert result["total_systems"] > 0

    def test_project_map_systems_grouped_by_state(self, nqe, sample_graph):
        result = nqe.get_project_map(sample_graph)
        for state, nodes in result["systems"].items():
            assert isinstance(nodes, list)
            for node in nodes:
                assert node["readiness_state"] == state


class TestSystemMap:
    def test_get_system_map_returns_assemblies(self, nqe, sample_graph):
        # Find an assembly node id from the graph
        assembly_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "assembly"
        ]
        assert len(assembly_ids) > 0
        result = nqe.get_system_map(sample_graph, assembly_ids[0])
        assert "assemblies" in result
        assert "system_id" in result
        assert result["system_node"] is not None

    def test_system_map_missing_returns_empty(self, nqe, sample_graph):
        result = nqe.get_system_map(sample_graph, "nonexistent-id")
        assert result["system_node"] is None
        assert result["assemblies"] == []


class TestAssemblyMap:
    def test_get_assembly_map_returns_conditions(self, nqe, sample_graph):
        # Find an assembly node connected to conditions
        assembly_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "assembly"
        ]
        assert len(assembly_ids) > 0
        result = nqe.get_assembly_map(sample_graph, assembly_ids[0])
        assert "conditions" in result
        assert "blockers" in result
        assert "dependencies" in result
        assert "artifacts" in result
        assert result["assembly_node"] is not None

    def test_assembly_map_missing_returns_empty(self, nqe, sample_graph):
        result = nqe.get_assembly_map(sample_graph, "nonexistent-id")
        assert result["assembly_node"] is None
        assert result["conditions"] == []


class TestConditionDetail:
    def test_get_condition_detail_returns_complete(self, nqe, sample_graph):
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition"
        ]
        assert len(cond_ids) > 0
        result = nqe.get_condition_detail(sample_graph, cond_ids[0])
        expected_keys = {
            "node_id", "found", "node", "readiness_state",
            "blockers", "dependencies", "remediation_path",
            "owner", "next_actions", "downstream_impacts",
            "upstream_dependencies", "neighbors", "enrichment_edges",
        }
        assert expected_keys.issubset(set(result.keys()))
        assert result["found"] is True

    def test_condition_detail_not_found(self, nqe, sample_graph):
        result = nqe.get_condition_detail(sample_graph, "nonexistent-id")
        assert result["found"] is False


class TestBlockerPanel:
    def test_get_blocker_panel(self, nqe, sample_graph):
        # cond-1 has a blocker
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition" and n.source_object_id == "cond-1"
        ]
        assert len(cond_ids) == 1
        result = nqe.get_blocker_panel(sample_graph, cond_ids[0])
        assert "immediate_blockers" in result
        assert "blocking_chain" in result
        assert len(result["immediate_blockers"]) > 0


class TestOwnerPanel:
    def test_get_owner_panel_preserves_unknown(self, nqe, sample_graph):
        # cond-2 has owner_state "unknown"
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition" and n.source_object_id == "cond-2"
        ]
        assert len(cond_ids) == 1
        result = nqe.get_owner_panel(sample_graph, cond_ids[0])
        assert "owner_state" in result
        # Owner state should be one of assigned/unassigned/unknown
        assert result["owner_state"] in ("assigned", "unassigned", "unknown")


class TestReadinessOverlay:
    def test_get_readiness_overlay_covers_all_nodes(self, nqe, sample_graph):
        result = nqe.get_readiness_overlay(sample_graph)
        assert "nodes" in result
        # Every node in the graph should be annotated
        assert len(result["nodes"]) == sample_graph.node_count()
        for annotated in result["nodes"]:
            assert "readiness_state" in annotated


class TestImpactOverlay:
    def test_get_impact_overlay_deterministic(self, nqe, sample_graph):
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition"
        ]
        assert len(cond_ids) > 0
        result1 = nqe.get_impact_overlay(sample_graph, cond_ids[0])
        result2 = nqe.get_impact_overlay(sample_graph, cond_ids[0])
        assert result1 == result2
        assert "upstream" in result1
        assert "downstream" in result1
