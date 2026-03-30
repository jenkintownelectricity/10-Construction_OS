"""
Tests for ReferenceGraphSerializer — Wave 17A.

Tests: serialization, deserialization, checksum, summary.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.graph_builder import ReferenceGraphBuilder
from runtime.reference_graph.serializer import (
    ReferenceGraphSerializer,
    SerializationError,
)


class TestSerialization:
    """Serialization round-trips."""

    def test_serialize_and_deserialize(self):
        builder = ReferenceGraphBuilder()
        builder.register_bundle([{
            "object_type": "DETAIL", "scope": "global",
            "partition": "global_kernel_partition",
            "source_system": "CK", "source_reference": "D-001",
            "authority_type": "kernel_canonical",
        }], [])
        graph = builder.build()

        json_str = ReferenceGraphSerializer.serialize(graph)
        assert isinstance(json_str, str)
        assert "CRG-DETAIL-" in json_str

        deserialized = ReferenceGraphSerializer.deserialize(json_str)
        assert deserialized["node_count"] == graph["node_count"]

    def test_deserialize_invalid_json(self):
        try:
            ReferenceGraphSerializer.deserialize("not json")
            assert False, "Should have raised SerializationError"
        except SerializationError:
            pass

    def test_deserialize_missing_fields(self):
        try:
            ReferenceGraphSerializer.deserialize('{"foo": "bar"}')
            assert False, "Should have raised SerializationError"
        except SerializationError:
            pass

    def test_checksum_computation(self):
        cs = ReferenceGraphSerializer.compute_checksum(
            [{"id": "1"}], [{"id": "2"}],
        )
        assert len(cs) == 64

    def test_summary(self):
        builder = ReferenceGraphBuilder()
        builder.register_bundle([{
            "object_type": "DETAIL", "scope": "global",
            "partition": "global_kernel_partition",
            "source_system": "CK", "source_reference": "D-001",
            "authority_type": "kernel_canonical",
        }], [])
        graph = builder.build()

        summary = ReferenceGraphSerializer.to_summary(graph)
        assert summary["node_count"] == 1
        assert "DETAIL" in summary["type_distribution"]
        assert "global_kernel_partition" in summary["partition_distribution"]
