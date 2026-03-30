"""Tests for ViewBuilder — map, list, and detail view transformations."""

import pytest

from runtime.navigation_views.view_builder import ViewBuilder
from runtime.navigation_queries.navigation_query_engine import NavigationQueryEngine


@pytest.fixture()
def vb():
    return ViewBuilder()


@pytest.fixture()
def nqe():
    return NavigationQueryEngine()


class TestBuildMapView:
    def test_build_map_view_structure(self, vb, nqe, sample_graph):
        project_map = nqe.get_project_map(sample_graph)
        result = vb.build_map_view(project_map)
        assert result["view_type"] == "map"
        assert "project_id" in result
        assert "total_systems" in result
        assert "state_groups" in result
        assert "summary" in result
        assert isinstance(result["state_groups"], list)

    def test_build_map_view_empty(self, vb):
        result = vb.build_map_view({"systems": {}, "project_id": "x", "total_systems": 0})
        assert result["view_type"] == "map"
        assert result["state_groups"] == []
        assert result["total_systems"] == 0


class TestBuildListView:
    def test_build_list_view_sorted(self, vb):
        nodes = [
            {"node_id": "c", "label": "c"},
            {"node_id": "a", "label": "a"},
            {"node_id": "b", "label": "b"},
        ]
        result = vb.build_list_view(nodes, sort_key="node_id")
        assert result["view_type"] == "list"
        assert result["total"] == 3
        assert result["sort_key"] == "node_id"
        ids = [item["node_id"] for item in result["items"]]
        assert ids == ["a", "b", "c"]

    def test_build_list_view_default_sort(self, vb):
        nodes = [{"node_id": "z"}, {"node_id": "a"}]
        result = vb.build_list_view(nodes)
        assert result["items"][0]["node_id"] == "a"


class TestBuildDetailView:
    def test_build_detail_view_complete(self, vb, nqe, sample_graph):
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition"
        ]
        detail = nqe.get_condition_detail(sample_graph, cond_ids[0])
        result = vb.build_detail_view(detail)
        assert result["view_type"] == "detail"
        assert result["found"] is True
        assert "header" in result
        assert "panels" in result
        assert "blockers" in result["panels"]
        assert "dependencies" in result["panels"]
        assert "owner" in result["panels"]

    def test_build_detail_view_not_found(self, vb):
        result = vb.build_detail_view({"node_id": "x", "found": False})
        assert result["view_type"] == "detail"
        assert result["found"] is False
        assert result["header"] == {}
        assert result["panels"] == {}
