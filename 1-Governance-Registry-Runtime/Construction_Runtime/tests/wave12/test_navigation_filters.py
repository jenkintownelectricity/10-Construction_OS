"""Tests for FilterEngine — pure predicate-based filtering."""

import copy

import pytest

from runtime.navigation_filters.filter_engine import FilterEngine


@pytest.fixture()
def fe():
    return FilterEngine()


@pytest.fixture()
def sample_nodes():
    return [
        {
            "node_id": "n1",
            "node_type": "condition",
            "readiness_state": "ready",
            "state_summary": {"system": "sys-A", "owner": "alice"},
            "is_enrichment_derived": False,
        },
        {
            "node_id": "n2",
            "node_type": "condition",
            "readiness_state": "blocked",
            "state_summary": {"system": "sys-B", "owner": "bob"},
            "is_enrichment_derived": False,
        },
        {
            "node_id": "n3",
            "node_type": "blocker",
            "readiness_state": "pending",
            "state_summary": {"system": "sys-A", "owner": "alice"},
            "is_enrichment_derived": True,
        },
    ]


class TestFilterBySystem:
    def test_filter_by_system(self, fe, sample_nodes):
        result = fe.apply_filters(sample_nodes, {"system": "sys-A"})
        assert len(result) == 2
        assert all(
            n["state_summary"]["system"] == "sys-A" for n in result
        )


class TestFilterByReadinessState:
    def test_filter_by_readiness_state(self, fe, sample_nodes):
        result = fe.apply_filters(sample_nodes, {"readiness_state": "blocked"})
        assert len(result) == 1
        assert result[0]["node_id"] == "n2"


class TestFilterByOwner:
    def test_filter_by_owner(self, fe, sample_nodes):
        result = fe.apply_filters(sample_nodes, {"owner": "alice"})
        assert len(result) == 2


class TestFilterDoesNotMutateSource:
    def test_filter_does_not_mutate_source(self, fe, sample_nodes):
        original = copy.deepcopy(sample_nodes)
        fe.apply_filters(sample_nodes, {"system": "sys-A"})
        assert sample_nodes == original


class TestEmptyFilters:
    def test_empty_filters_returns_all(self, fe, sample_nodes):
        result = fe.apply_filters(sample_nodes, {})
        assert len(result) == len(sample_nodes)

    def test_unknown_filter_key_returns_all(self, fe, sample_nodes):
        result = fe.apply_filters(sample_nodes, {"nonexistent_key": "val"})
        assert len(result) == len(sample_nodes)


class TestMultipleFilters:
    def test_conjunction_filters(self, fe, sample_nodes):
        result = fe.apply_filters(
            sample_nodes, {"system": "sys-A", "node_type": "condition"}
        )
        assert len(result) == 1
        assert result[0]["node_id"] == "n1"
