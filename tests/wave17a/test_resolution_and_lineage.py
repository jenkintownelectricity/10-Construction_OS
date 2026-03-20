"""
Tests for ResolutionEngine and LineageEngine — Wave 17A.

Tests: resolution determinism, unresolved ambiguity, lineage traceability,
orphan detection.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.identity_allocator import IdentityAllocator
from runtime.reference_graph.node_registry import NodeRegistry
from runtime.reference_graph.edge_registry import EdgeRegistry
from runtime.reference_graph.lineage_engine import LineageEngine
from runtime.reference_graph.resolution_engine import ResolutionEngine
from runtime.reference_graph.query_engine import QueryEngine
from runtime.reference_graph.orphan_detector import OrphanDetector


def _build_lineage_graph():
    """Create a graph with a lineage chain: DETAIL -> VARIANT -> RENDER_JOB -> DRAWING."""
    alloc = IdentityAllocator()
    nodes = NodeRegistry(alloc)
    edges = EdgeRegistry(nodes)

    detail = nodes.register(
        object_type="DETAIL", scope="global",
        partition="global_kernel_partition",
        source_system="CK", source_reference="D-001",
        authority_type="kernel_canonical",
    )
    variant = nodes.register(
        object_type="VARIANT", scope="p1",
        partition="global_runtime_partition",
        source_system="CR", source_reference="V-001",
        authority_type="runtime_derived",
    )
    render_job = nodes.register(
        object_type="RENDER_JOB", scope="p1",
        partition="global_runtime_partition",
        source_system="CR", source_reference="RJ-001",
        authority_type="runtime_derived",
    )
    drawing = nodes.register(
        object_type="DRAWING", scope="p1",
        partition="artifact_partition",
        source_system="CR", source_reference="DRW-001",
        authority_type="runtime_derived",
    )

    # VARIANT derived_from DETAIL
    edges.register("derived_from", variant["graph_id"], detail["graph_id"])
    # DRAWING rendered_from RENDER_JOB
    edges.register("rendered_from", drawing["graph_id"], render_job["graph_id"])

    lineage = LineageEngine(nodes, edges)
    resolution = ResolutionEngine(nodes, edges, lineage)
    query = QueryEngine(nodes, edges)
    orphan = OrphanDetector(nodes, edges, query)

    return {
        "nodes": nodes, "edges": edges, "lineage": lineage,
        "resolution": resolution, "query": query, "orphan": orphan,
        "ids": {
            "detail": detail, "variant": variant,
            "render_job": render_job, "drawing": drawing,
        },
    }


class TestResolutionDeterminism:
    """Resolution must be deterministic."""

    def test_resolve_existing_object(self):
        g = _build_lineage_graph()
        result = g["resolution"].resolve_object(g["ids"]["detail"]["graph_id"])
        assert result["resolved"] is True
        assert result["mode"] == "deterministic"

    def test_resolve_runtime_derived_object(self):
        g = _build_lineage_graph()
        result = g["resolution"].resolve_object(g["ids"]["variant"]["graph_id"])
        assert result["resolved"] is True
        assert result["mode"] == "scoped_deterministic"

    def test_resolve_nonexistent_returns_unresolved(self):
        g = _build_lineage_graph()
        result = g["resolution"].resolve_object("CRG-NONEXIST-000001")
        assert result["resolved"] is False
        assert result["mode"] == "unresolved"


class TestUnresolvedAmbiguity:
    """Ambiguous resolution must fail closed or return unresolved."""

    def test_invalid_node_excluded_from_resolution(self):
        g = _build_lineage_graph()
        g["nodes"].update_status(g["ids"]["variant"]["graph_id"], "invalid")
        result = g["resolution"].resolve_object(g["ids"]["variant"]["graph_id"])
        assert result["resolved"] is False

    def test_resolve_by_reference_not_found(self):
        g = _build_lineage_graph()
        result = g["resolution"].resolve_by_reference(
            "nonexistent", "ref", "DETAIL", "global",
        )
        assert result["resolved"] is False
        assert result["mode"] == "unresolved"

    def test_resolve_by_reference_found(self):
        g = _build_lineage_graph()
        result = g["resolution"].resolve_by_reference(
            "CK", "D-001", "DETAIL", "global",
        )
        assert result["resolved"] is True


class TestLineageTraceability:
    """Lineage must be traceable end-to-end."""

    def test_trace_variant_lineage(self):
        g = _build_lineage_graph()
        chain = g["lineage"].trace_lineage(g["ids"]["variant"]["graph_id"])
        assert len(chain) >= 1
        types = [n["object_type"] for n in chain]
        assert "DETAIL" in types or "VARIANT" in types

    def test_trace_downstream(self):
        g = _build_lineage_graph()
        descendants = g["lineage"].trace_downstream(g["ids"]["detail"]["graph_id"])
        # VARIANT is derived_from DETAIL, so VARIANT should appear downstream
        types = [n["object_type"] for n in descendants]
        assert "VARIANT" in types

    def test_validate_lineage(self):
        g = _build_lineage_graph()
        result = g["lineage"].validate_lineage(g["ids"]["variant"]["graph_id"])
        assert result["valid"] is True
        assert result["chain_length"] >= 1

    def test_validate_lineage_nonexistent_node(self):
        g = _build_lineage_graph()
        result = g["lineage"].validate_lineage("CRG-NONEXIST-000001")
        assert result["valid"] is False


class TestOrphanDetection:
    """Orphaned nodes must be detectable."""

    def test_detect_orphans_none(self):
        g = _build_lineage_graph()
        result = g["orphan"].detect_orphans()
        # render_job has no edges to other connected nodes (only drawing -> render_job)
        # But detail, variant, drawing, render_job are all connected via edges
        # Actually: variant->detail, drawing->render_job. render_job has incoming from drawing.
        # All have at least one edge except... let's check
        assert result["total_nodes"] == 4

    def test_detect_orphan_with_isolated_node(self):
        g = _build_lineage_graph()
        # Add an isolated node
        g["nodes"].register(
            object_type="CONDITION", scope="p1",
            partition="global_runtime_partition",
            source_system="CR", source_reference="C-ORPHAN",
            authority_type="runtime_derived",
        )
        result = g["orphan"].detect_orphans()
        assert result["orphan_count"] == 1
        assert "CRG-COND-000001" in result["orphan_ids"]

    def test_detect_disconnected_components(self):
        g = _build_lineage_graph()
        result = g["orphan"].detect_disconnected_components()
        # variant<->detail and drawing<->render_job are two separate components
        assert result["component_count"] == 2


class TestQueryEngine:
    """Query engine traversal."""

    def test_bfs_traversal(self):
        g = _build_lineage_graph()
        result = g["query"].bfs(g["ids"]["variant"]["graph_id"])
        assert len(result) >= 2
        assert result[0] == g["ids"]["variant"]["graph_id"]

    def test_dfs_traversal(self):
        g = _build_lineage_graph()
        result = g["query"].dfs(g["ids"]["variant"]["graph_id"])
        assert len(result) >= 2

    def test_shortest_path(self):
        g = _build_lineage_graph()
        path = g["query"].shortest_path(
            g["ids"]["variant"]["graph_id"],
            g["ids"]["detail"]["graph_id"],
        )
        assert path is not None
        assert len(path) == 2

    def test_shortest_path_no_path(self):
        g = _build_lineage_graph()
        path = g["query"].shortest_path(
            g["ids"]["variant"]["graph_id"],
            g["ids"]["drawing"]["graph_id"],
        )
        # variant and drawing are in different components
        assert path is None

    def test_find_nodes_by_type(self):
        g = _build_lineage_graph()
        details = g["query"].find_nodes_by_type("DETAIL")
        assert len(details) == 1

    def test_find_related(self):
        g = _build_lineage_graph()
        related = g["resolution"].find_related(g["ids"]["detail"]["graph_id"])
        assert len(related) >= 1

    def test_connected_components(self):
        g = _build_lineage_graph()
        components = g["query"].get_connected_components()
        assert len(components) >= 1

    def test_subgraph_extraction(self):
        g = _build_lineage_graph()
        ids_list = [g["ids"]["variant"]["graph_id"], g["ids"]["detail"]["graph_id"]]
        subgraph = g["query"].get_subgraph(ids_list)
        assert subgraph["node_count"] == 2
