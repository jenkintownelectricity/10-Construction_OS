"""Tests for app surface modules — verify delegation to runtime."""

import pytest

from runtime.graph.condition_graph import ConditionGraph
from apps.navigation.navigation_app import NavigationApp
from apps.navigation.view_switcher import ViewSwitcherSurface, SUPPORTED_VIEWS
from apps.navigation.filter_bar import FilterBarSurface, AVAILABLE_FILTERS
from apps.navigation.path_trace import PathTraceSurface


class TestNavigationAppDelegatesToRuntime:
    def test_navigation_app_delegates_to_runtime(self, sample_graph):
        app = NavigationApp(sample_graph)
        # get_project_overview should return a dict (delegating to runtime)
        result = app.get_project_overview()
        assert isinstance(result, dict)

    def test_navigation_app_condition_detail(self, sample_graph):
        app = NavigationApp(sample_graph)
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition"
        ]
        result = app.get_condition_detail(cond_ids[0])
        assert isinstance(result, dict)

    def test_navigation_app_switch_view(self, sample_graph):
        app = NavigationApp(sample_graph)
        result = app.switch_view("map")
        assert isinstance(result, dict)
        assert result["view_type"] == "map"


class TestViewSwitcherValidatesViewTypes:
    def test_view_switcher_validates_view_types(self):
        vs = ViewSwitcherSurface()
        assert vs.validate_view_type("map") is True
        assert vs.validate_view_type("list") is True
        assert vs.validate_view_type("detail") is True
        assert vs.validate_view_type("invalid") is False

    def test_view_switcher_rejects_invalid(self):
        vs = ViewSwitcherSurface()
        with pytest.raises(ValueError, match="Unsupported view type"):
            vs.switch("invalid_type")

    def test_view_switcher_supported_views_complete(self):
        assert set(SUPPORTED_VIEWS) == {"map", "list", "detail"}


class TestFilterBarAvailableFilters:
    def test_filter_bar_available_filters(self):
        fb = FilterBarSurface()
        filters = fb.get_available_filters()
        assert isinstance(filters, list)
        assert len(filters) > 0
        # Must include key dimensions
        assert "system" in filters
        assert "owner" in filters
        assert "readiness_state" in filters

    def test_filter_bar_apply_returns_metadata(self, sample_graph):
        fb = FilterBarSurface()
        result = fb.apply(sample_graph, {"system": "sys-A"})
        assert isinstance(result, dict)
        assert result["view_type"] == "filtered"
        assert result["filters_are_derived_views"] is True

    def test_filter_bar_rejects_invalid_filters(self, sample_graph):
        fb = FilterBarSurface()
        result = fb.apply(sample_graph, {"nonexistent": "value", "system": "x"})
        assert "nonexistent" in result["invalid_filters"]
        assert "system" in result["active_filters"]


class TestPathTraceDelegatesToRuntime:
    def test_path_trace_delegates_to_runtime(self, sample_graph):
        pt = PathTraceSurface()
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition"
        ]
        assert len(cond_ids) > 0

        result = pt.render_unblock_path(sample_graph, cond_ids[0])
        assert isinstance(result, dict)
        assert result["trace_type"] == "unblock_path"
        assert "path" in result

    def test_path_trace_owner_route(self, sample_graph):
        pt = PathTraceSurface()
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition"
        ]
        result = pt.render_owner_route(sample_graph, cond_ids[0])
        assert result["trace_type"] == "owner_route"
        assert "owner_state" in result

    def test_path_trace_impact_path(self, sample_graph):
        pt = PathTraceSurface()
        cond_ids = [
            nid for nid, n in sample_graph.nodes.items()
            if n.node_type == "condition"
        ]
        result = pt.render_impact_path(sample_graph, cond_ids[0])
        assert result["trace_type"] == "impact_path"
        assert "downstream_impacts" in result
