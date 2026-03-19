"""Tests for MapProjection — hierarchical map structure from a ConditionGraph."""

import pytest

from runtime.navigation_map.map_projection import MapProjection


@pytest.fixture()
def mp():
    return MapProjection()


class TestHierarchy:
    def test_hierarchy_has_project_level(self, mp, sample_graph):
        result = mp.project_hierarchy(sample_graph)
        assert "project_id" in result
        assert result["project_id"] == sample_graph.project_id
        assert "node_count" in result
        assert result["node_count"] == sample_graph.node_count()
        assert "readiness_summary" in result
        assert "systems" in result

    def test_hierarchy_includes_systems_and_assemblies(self, mp, sample_graph):
        result = mp.project_hierarchy(sample_graph)
        # The graph has assembly nodes, so systems should be non-empty
        # (top-level assemblies become systems in the hierarchy)
        assert isinstance(result["systems"], list)
        for system in result["systems"]:
            assert "node" in system
            assert "readiness_state" in system
            assert "readiness_summary" in system
            assert "node_count" in system
            assert "assemblies" in system

    def test_hierarchy_deterministic(self, mp, sample_graph):
        r1 = mp.project_hierarchy(sample_graph)
        r2 = mp.project_hierarchy(sample_graph)
        assert r1 == r2
