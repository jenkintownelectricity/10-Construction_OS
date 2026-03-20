"""Tests for Wave 15 Detail Navigation subsystem."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from runtime.detail_graph.graph_builder import build_detail_graph
from runtime.detail_navigation.navigator import DetailNavigator


DETAIL_A = "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"
DETAIL_B = "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01"
DETAIL_C = "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01"
DETAIL_D = "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01"


def _make_index(detail_ids):
    lookup = {}
    for did in detail_ids:
        lookup[did] = {
            "detail_id": did,
            "system": "LOW_SLOPE",
            "class": "TERMINATION",
            "condition": "PARAPET",
            "variant": "COUNTERFLASHING",
            "assembly_family": "EPDM",
            "display_name": f"Test {did}",
        }
    return {"detail_lookup": lookup}


def _build_graph(detail_ids, routes):
    index = _make_index(detail_ids)
    route_index = {"_meta": {}, "routes": routes}
    return build_detail_graph(index, route_index)


class TestFindRelatedDetails:
    def test_finds_related(self):
        graph = _build_graph(
            [DETAIL_A, DETAIL_B],
            [{"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
              "relationship_type": "adjacent_to", "directionality": "bidirectional"}]
        )
        nav = DetailNavigator(graph)
        related = nav.find_related_details(DETAIL_A)
        assert len(related) == 1
        assert related[0]["detail_id"] == DETAIL_B

    def test_unknown_detail_returns_empty(self):
        graph = _build_graph([DETAIL_A], [])
        nav = DetailNavigator(graph)
        assert nav.find_related_details("NONEXISTENT") == []


class TestResolveNeighbors:
    def test_resolves_neighbors(self):
        graph = _build_graph(
            [DETAIL_A, DETAIL_B, DETAIL_C],
            [
                {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
                 "relationship_type": "adjacent_to", "directionality": "bidirectional"},
                {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_C,
                 "relationship_type": "requires_continuity_with", "directionality": "bidirectional"},
            ]
        )
        nav = DetailNavigator(graph)
        neighbors = nav.resolve_neighbors(DETAIL_A)
        neighbor_ids = [n["detail_id"] for n in neighbors]
        assert DETAIL_B in neighbor_ids
        assert DETAIL_C in neighbor_ids


class TestResolveUpstreamDependencies:
    def test_finds_upstream(self):
        graph = _build_graph(
            [DETAIL_A, DETAIL_B],
            [{"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
              "relationship_type": "depends_on", "directionality": "directional"}]
        )
        nav = DetailNavigator(graph)
        upstream = nav.resolve_upstream_dependencies(DETAIL_A)
        assert len(upstream) == 1
        assert upstream[0]["detail_id"] == DETAIL_B


class TestResolveInstallationTransitions:
    def test_finds_transitions(self):
        graph = _build_graph(
            [DETAIL_A, DETAIL_B],
            [{"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
              "relationship_type": "terminates_into", "directionality": "directional"}]
        )
        nav = DetailNavigator(graph)
        transitions = nav.resolve_installation_transitions(DETAIL_A)
        assert len(transitions) == 1
        assert transitions[0]["detail_id"] == DETAIL_B
        assert transitions[0]["relationship_type"] == "terminates_into"


class TestResolveNavigationPath:
    def test_finds_path(self):
        graph = _build_graph(
            [DETAIL_A, DETAIL_B, DETAIL_C],
            [
                {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
                 "relationship_type": "adjacent_to", "directionality": "bidirectional"},
                {"source_detail_id": DETAIL_B, "target_detail_id": DETAIL_C,
                 "relationship_type": "adjacent_to", "directionality": "bidirectional"},
            ]
        )
        nav = DetailNavigator(graph)
        result = nav.resolve_navigation_path(DETAIL_A, DETAIL_C)
        assert result["path_exists"] is True
        assert result["path_length"] == 2
        assert len(result["steps"]) == 3

    def test_no_path(self):
        graph = _build_graph(
            [DETAIL_A, DETAIL_B, DETAIL_C],
            [{"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
              "relationship_type": "adjacent_to", "directionality": "bidirectional"}]
        )
        nav = DetailNavigator(graph)
        result = nav.resolve_navigation_path(DETAIL_A, DETAIL_C)
        assert result["path_exists"] is False

    def test_unknown_detail_no_path(self):
        graph = _build_graph([DETAIL_A], [])
        nav = DetailNavigator(graph)
        result = nav.resolve_navigation_path(DETAIL_A, "NONEXISTENT")
        assert result["path_exists"] is False

    def test_deterministic_path(self):
        graph = _build_graph(
            [DETAIL_A, DETAIL_B, DETAIL_C],
            [
                {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
                 "relationship_type": "adjacent_to", "directionality": "bidirectional"},
                {"source_detail_id": DETAIL_B, "target_detail_id": DETAIL_C,
                 "relationship_type": "adjacent_to", "directionality": "bidirectional"},
            ]
        )
        nav = DetailNavigator(graph)
        r1 = nav.resolve_navigation_path(DETAIL_A, DETAIL_C)
        r2 = nav.resolve_navigation_path(DETAIL_A, DETAIL_C)
        assert r1["steps"] == r2["steps"]
