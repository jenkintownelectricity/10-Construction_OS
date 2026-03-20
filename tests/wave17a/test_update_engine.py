"""
Tests for UpdateEngine — Wave 17A.

Tests: atomic updates, validation enforcement, update log.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.graph_builder import ReferenceGraphBuilder
from runtime.reference_graph.update_engine import UpdateEngine, UpdateError


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


class TestAtomicUpdates:
    """Updates must be atomic."""

    def test_successful_update(self):
        engine = UpdateEngine(ReferenceGraphBuilder())
        result = engine.apply_update(_make_nodes(), [])
        assert result["nodes_registered"] == 2
        assert result["validation"]["valid"] is True

    def test_failed_update_raises(self):
        engine = UpdateEngine(ReferenceGraphBuilder())
        bad_nodes = [{"object_type": "INVALID"}]
        try:
            engine.apply_update(bad_nodes, [])
            assert False, "Should have raised UpdateError"
        except UpdateError:
            pass

    def test_full_rebuild(self):
        engine = UpdateEngine(ReferenceGraphBuilder())
        engine.apply_update(_make_nodes(), [])
        new_nodes = [{
            "object_type": "DETAIL", "scope": "global",
            "partition": "global_kernel_partition",
            "source_system": "CK", "source_reference": "D-NEW",
            "authority_type": "kernel_canonical",
        }]
        result = engine.full_rebuild(new_nodes, [])
        assert result["nodes_registered"] == 1

    def test_incremental_append(self):
        engine = UpdateEngine(ReferenceGraphBuilder())
        engine.apply_update([_make_nodes()[0]], [])
        result = engine.incremental_append([_make_nodes()[1]], [])
        assert result["nodes_registered"] == 1

    def test_idempotent_replay(self):
        engine = UpdateEngine(ReferenceGraphBuilder())
        engine.apply_update(_make_nodes(), [], mode="idempotent_replay")
        result = engine.idempotent_replay(_make_nodes(), [])
        assert result["nodes_registered"] == 2


class TestUpdateLog:
    """Update log tracks history."""

    def test_log_records_updates(self):
        engine = UpdateEngine(ReferenceGraphBuilder())
        engine.apply_update(_make_nodes(), [])
        log = engine.get_update_log()
        assert len(log) == 1
        assert log[0]["update_id"] == 1

    def test_log_grows_with_updates(self):
        engine = UpdateEngine(ReferenceGraphBuilder())
        engine.apply_update([_make_nodes()[0]], [])
        engine.apply_update([_make_nodes()[1]], [])
        assert len(engine.get_update_log()) == 2
