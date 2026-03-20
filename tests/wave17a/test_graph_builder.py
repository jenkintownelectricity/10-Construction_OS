"""
Tests for ReferenceGraphBuilder — Wave 17A.

Tests: atomic bundles, full rebuild, incremental append, idempotent replay.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.graph_builder import (
    ReferenceGraphBuilder,
    GraphBuildError,
    CONTRACT_VERSION,
    WAVE,
)


def _make_nodes():
    return [
        {
            "object_type": "DETAIL", "scope": "global",
            "partition": "global_kernel_partition",
            "source_system": "CK", "source_reference": "D-001",
            "authority_type": "kernel_canonical",
        },
        {
            "object_type": "VARIANT", "scope": "p1",
            "partition": "global_runtime_partition",
            "source_system": "CR", "source_reference": "V-001",
            "authority_type": "runtime_derived",
        },
    ]


class TestAtomicBundles:
    """Bundle registration must be atomic."""

    def test_successful_bundle(self):
        builder = ReferenceGraphBuilder()
        result = builder.register_bundle(_make_nodes(), [])
        assert result["nodes_registered"] == 2
        assert result["edges_registered"] == 0

    def test_bundle_with_invalid_node_fails_whole_bundle(self):
        builder = ReferenceGraphBuilder()
        nodes = _make_nodes() + [{
            "object_type": "INVALID", "scope": "global",
            "partition": "global_kernel_partition",
            "source_system": "CK", "source_reference": "X-001",
            "authority_type": "kernel_canonical",
        }]
        try:
            builder.register_bundle(nodes, [])
            assert False, "Should have raised GraphBuildError"
        except GraphBuildError:
            pass
        # No nodes should have been registered
        assert builder.node_registry.node_count == 0

    def test_bundle_with_edges(self):
        builder = ReferenceGraphBuilder()
        nodes = _make_nodes()
        result = builder.register_bundle(nodes, [])
        node_ids = [n["graph_id"] for n in result["nodes"]]

        edges = [{
            "relation_type": "derived_from",
            "from_id": node_ids[1],  # VARIANT
            "to_id": node_ids[0],    # DETAIL
        }]
        result2 = builder.register_bundle([], edges)
        assert result2["edges_registered"] == 1

    def test_invalid_write_mode_fails(self):
        builder = ReferenceGraphBuilder()
        try:
            builder.register_bundle([], [], mode="invalid_mode")
            assert False, "Should have raised GraphBuildError"
        except GraphBuildError:
            pass


class TestFullRebuild:
    """Full rebuild must clear and rebuild state."""

    def test_full_rebuild_clears_existing(self):
        builder = ReferenceGraphBuilder()
        builder.register_bundle(_make_nodes(), [])
        assert builder.node_registry.node_count == 2

        new_nodes = [{
            "object_type": "DETAIL", "scope": "global",
            "partition": "global_kernel_partition",
            "source_system": "CK", "source_reference": "D-NEW",
            "authority_type": "kernel_canonical",
        }]
        builder.register_bundle(new_nodes, [], mode="full_rebuild")
        assert builder.node_registry.node_count == 1

    def test_full_rebuild_correctness(self):
        builder = ReferenceGraphBuilder()
        nodes = _make_nodes()
        builder.register_bundle(nodes, [], mode="full_rebuild")
        graph = builder.build()
        assert graph["node_count"] == 2
        assert graph["version"] == CONTRACT_VERSION
        assert graph["wave"] == WAVE
        assert "checksum" in graph


class TestIncrementalAppend:
    """Incremental append adds without mutation."""

    def test_incremental_preserves_existing(self):
        builder = ReferenceGraphBuilder()
        builder.register_bundle([_make_nodes()[0]], [])
        assert builder.node_registry.node_count == 1

        builder.register_bundle([_make_nodes()[1]], [], mode="incremental_append")
        assert builder.node_registry.node_count == 2

    def test_incremental_append_correctness(self):
        builder = ReferenceGraphBuilder()
        builder.register_bundle(_make_nodes(), [], mode="incremental_append")
        graph = builder.build()
        assert graph["node_count"] == 2


class TestIdempotentReplay:
    """Idempotent replay must not duplicate."""

    def test_replay_returns_same_nodes(self):
        builder = ReferenceGraphBuilder()
        r1 = builder.register_bundle(_make_nodes(), [], mode="idempotent_replay")
        r2 = builder.register_bundle(_make_nodes(), [], mode="idempotent_replay")
        assert builder.node_registry.node_count == 2  # not 4

    def test_replay_returns_existing_ids(self):
        builder = ReferenceGraphBuilder()
        r1 = builder.register_bundle(_make_nodes(), [], mode="idempotent_replay")
        r2 = builder.register_bundle(_make_nodes(), [], mode="idempotent_replay")
        ids1 = {n["graph_id"] for n in r1["nodes"]}
        ids2 = {n["graph_id"] for n in r2["nodes"]}
        assert ids1 == ids2


class TestGraphBuild:
    """Graph build produces correct output."""

    def test_build_produces_checksum(self):
        builder = ReferenceGraphBuilder()
        builder.register_bundle(_make_nodes(), [])
        graph = builder.build()
        assert len(graph["checksum"]) == 64  # SHA-256

    def test_build_is_deterministic(self):
        b1 = ReferenceGraphBuilder()
        b1.register_bundle(_make_nodes(), [])
        g1 = b1.build()

        b2 = ReferenceGraphBuilder()
        b2.register_bundle(_make_nodes(), [])
        g2 = b2.build()

        assert g1["node_count"] == g2["node_count"]
        assert g1["edge_count"] == g2["edge_count"]

    def test_build_includes_all_nodes(self):
        builder = ReferenceGraphBuilder()
        builder.register_bundle(_make_nodes(), [])
        graph = builder.build()
        types = {n["object_type"] for n in graph["nodes"]}
        assert "DETAIL" in types
        assert "VARIANT" in types
