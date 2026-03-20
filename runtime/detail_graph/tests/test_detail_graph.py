"""Tests for Wave 15 Detail Graph subsystem."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from runtime.detail_graph.graph_builder import build_detail_graph, DetailGraph, DetailGraphBuildError
from runtime.detail_graph.validator import validate_detail_graph, DetailGraphValidationError


def _make_index(detail_ids):
    lookup = {}
    for did in detail_ids:
        parts = did.split("-")
        lookup[did] = {
            "detail_id": did,
            "system": parts[0] + "_" + parts[1] if len(parts) > 1 else parts[0],
            "class": parts[2] if len(parts) > 2 else "TERMINATION",
            "condition": parts[3] if len(parts) > 3 else "PARAPET",
            "variant": parts[4] if len(parts) > 4 else "COUNTERFLASHING",
            "assembly_family": parts[5] if len(parts) > 5 else "EPDM",
            "display_name": f"Test {did}",
        }
    # Fix system field to be valid
    for did in lookup:
        lookup[did]["system"] = "LOW_SLOPE"
        lookup[did]["class"] = "TERMINATION"
    return {"detail_lookup": lookup}


DETAIL_A = "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"
DETAIL_B = "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01"
DETAIL_C = "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01"


def _make_route_index(routes):
    return {"_meta": {}, "routes": routes}


class TestBuildDetailGraph:
    def test_builds_valid_graph(self):
        index = _make_index([DETAIL_A, DETAIL_B])
        routes = _make_route_index([{
            "source_detail_id": DETAIL_A,
            "target_detail_id": DETAIL_B,
            "relationship_type": "adjacent_to",
            "directionality": "bidirectional",
            "criticality": "recommended",
        }])
        graph = build_detail_graph(index, routes)
        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
        assert DETAIL_A in graph.nodes
        assert DETAIL_B in graph.nodes

    def test_neighbor_lookup(self):
        index = _make_index([DETAIL_A, DETAIL_B, DETAIL_C])
        routes = _make_route_index([
            {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
             "relationship_type": "adjacent_to", "directionality": "bidirectional"},
            {"source_detail_id": DETAIL_B, "target_detail_id": DETAIL_C,
             "relationship_type": "terminates_into", "directionality": "directional"},
        ])
        graph = build_detail_graph(index, routes)
        neighbors_a = graph.neighbor_lookup(DETAIL_A)
        assert DETAIL_B in neighbors_a

    def test_bfs(self):
        index = _make_index([DETAIL_A, DETAIL_B, DETAIL_C])
        routes = _make_route_index([
            {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
             "relationship_type": "adjacent_to", "directionality": "bidirectional"},
            {"source_detail_id": DETAIL_B, "target_detail_id": DETAIL_C,
             "relationship_type": "adjacent_to", "directionality": "bidirectional"},
        ])
        graph = build_detail_graph(index, routes)
        bfs_result = graph.bfs(DETAIL_A)
        assert DETAIL_A in bfs_result
        assert DETAIL_B in bfs_result
        assert DETAIL_C in bfs_result

    def test_dfs(self):
        index = _make_index([DETAIL_A, DETAIL_B, DETAIL_C])
        routes = _make_route_index([
            {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
             "relationship_type": "adjacent_to", "directionality": "bidirectional"},
            {"source_detail_id": DETAIL_B, "target_detail_id": DETAIL_C,
             "relationship_type": "adjacent_to", "directionality": "bidirectional"},
        ])
        graph = build_detail_graph(index, routes)
        dfs_result = graph.dfs(DETAIL_A)
        assert len(dfs_result) == 3

    def test_shortest_path(self):
        index = _make_index([DETAIL_A, DETAIL_B, DETAIL_C])
        routes = _make_route_index([
            {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
             "relationship_type": "adjacent_to", "directionality": "bidirectional"},
            {"source_detail_id": DETAIL_B, "target_detail_id": DETAIL_C,
             "relationship_type": "adjacent_to", "directionality": "bidirectional"},
        ])
        graph = build_detail_graph(index, routes)
        path = graph.shortest_path(DETAIL_A, DETAIL_C)
        assert path is not None
        assert path[0] == DETAIL_A
        assert path[-1] == DETAIL_C

    def test_path_exists(self):
        index = _make_index([DETAIL_A, DETAIL_B, DETAIL_C])
        routes = _make_route_index([
            {"source_detail_id": DETAIL_A, "target_detail_id": DETAIL_B,
             "relationship_type": "adjacent_to", "directionality": "bidirectional"},
        ])
        graph = build_detail_graph(index, routes)
        assert graph.path_exists(DETAIL_A, DETAIL_B)
        assert not graph.path_exists(DETAIL_A, DETAIL_C)

    def test_invalid_edge_type_fail_closed(self):
        index = _make_index([DETAIL_A, DETAIL_B])
        routes = _make_route_index([{
            "source_detail_id": DETAIL_A,
            "target_detail_id": DETAIL_B,
            "relationship_type": "INVALID_TYPE",
        }])
        with pytest.raises(DetailGraphBuildError, match="Invalid relationship_type"):
            build_detail_graph(index, routes)

    def test_unknown_node_fail_closed(self):
        index = _make_index([DETAIL_A])
        routes = _make_route_index([{
            "source_detail_id": DETAIL_A,
            "target_detail_id": "NONEXISTENT-01",
            "relationship_type": "adjacent_to",
        }])
        with pytest.raises(DetailGraphBuildError, match="unknown target"):
            build_detail_graph(index, routes)

    def test_empty_index_fail_closed(self):
        with pytest.raises(DetailGraphBuildError, match="empty"):
            build_detail_graph({"detail_lookup": {}}, {"routes": []})

    def test_deterministic_checksum(self):
        index = _make_index([DETAIL_A, DETAIL_B])
        routes = _make_route_index([{
            "source_detail_id": DETAIL_A,
            "target_detail_id": DETAIL_B,
            "relationship_type": "adjacent_to",
            "directionality": "bidirectional",
        }])
        g1 = build_detail_graph(index, routes)
        g2 = build_detail_graph(index, routes)
        assert g1.checksum == g2.checksum


class TestValidateDetailGraph:
    def test_valid_graph_passes(self):
        index = _make_index([DETAIL_A, DETAIL_B])
        routes = _make_route_index([{
            "source_detail_id": DETAIL_A,
            "target_detail_id": DETAIL_B,
            "relationship_type": "adjacent_to",
            "directionality": "bidirectional",
        }])
        graph = build_detail_graph(index, routes)
        report = validate_detail_graph(graph)
        assert report["status"] == "PASS"
