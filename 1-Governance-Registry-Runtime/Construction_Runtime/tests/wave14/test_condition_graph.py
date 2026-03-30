"""
Wave 14 — Condition Graph Tests.

Tests:
- Graph builds valid structure
- Sequencing-critical edges form DAG
- Invalid nodes fail closed
- Deterministic output
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.condition_graph.condition_graph_builder import (
    ConditionGraphBuilder,
    ConditionGraphBuildError,
)
from runtime.condition_graph.condition_graph_validator import validate_condition_graph
from runtime.condition_graph.condition_graph_serializer import (
    serialize_graph,
    deserialize_graph,
    compute_checksum,
    verify_checksum,
)


def test_graph_builds_valid_structure():
    """Graph builds valid structure with nodes and edges."""
    builder = ConditionGraphBuilder("test-graph-001", ["test"])
    builder.add_node("CN-PARAPET-0001", "PARAPET", "North Parapet", "A1")
    builder.add_node("CN-DRAIN-0001", "DRAIN", "Main Drain", "B2")
    builder.add_node("CN-ROOF_FIELD-0001", "ROOF_FIELD", "Main Field", "C3")
    builder.add_edge("CN-ROOF_FIELD-0001", "CN-DRAIN-0001", "drains_to")
    builder.add_edge("CN-PARAPET-0001", "CN-ROOF_FIELD-0001", "adjacent_to")
    graph = builder.build()

    assert graph["graph_id"] == "test-graph-001"
    assert len(graph["nodes"]) == 3
    assert len(graph["edges"]) == 2
    assert graph["checksum"]
    assert graph["contract_version"]

    errors = validate_condition_graph(graph)
    assert errors == [], f"Validation errors: {errors}"
    print("  PASS: graph_builds_valid_structure")


def test_sequencing_critical_edges_form_dag():
    """Sequencing-critical edges must form a DAG."""
    builder = ConditionGraphBuilder("test-dag-001", ["test"])
    builder.add_node("CN-ROOF_FIELD-0001", "ROOF_FIELD", "Field", "A1")
    builder.add_node("CN-DRAIN-0001", "DRAIN", "Drain", "B1")
    builder.add_node("CN-SCUPPER-0001", "SCUPPER", "Scupper", "C1")
    builder.add_edge("CN-ROOF_FIELD-0001", "CN-DRAIN-0001", "drains_to")
    builder.add_edge("CN-ROOF_FIELD-0001", "CN-SCUPPER-0001", "drains_to")
    graph = builder.build()

    errors = validate_condition_graph(graph)
    assert errors == [], f"DAG validation errors: {errors}"
    print("  PASS: sequencing_critical_edges_form_dag")


def test_invalid_node_type_fails_closed():
    """Unsupported node types must fail closed."""
    builder = ConditionGraphBuilder("test-invalid-001", ["test"])
    try:
        builder.add_node("CN-INVALID-0001", "SKYLIGHT", "Invalid", "A1")
        assert False, "Should have raised ConditionGraphBuildError"
    except ConditionGraphBuildError as e:
        assert "Unsupported condition type" in str(e)
    print("  PASS: invalid_node_type_fails_closed")


def test_invalid_edge_type_fails_closed():
    """Unsupported edge types must fail closed."""
    builder = ConditionGraphBuilder("test-edge-001", ["test"])
    builder.add_node("CN-PARAPET-0001", "PARAPET", "Parapet", "A1")
    builder.add_node("CN-DRAIN-0001", "DRAIN", "Drain", "B1")
    try:
        builder.add_edge("CN-PARAPET-0001", "CN-DRAIN-0001", "invented_relationship")
        assert False, "Should have raised ConditionGraphBuildError"
    except ConditionGraphBuildError as e:
        assert "Unsupported edge type" in str(e)
    print("  PASS: invalid_edge_type_fails_closed")


def test_invalid_node_pair_fails_closed():
    """Invalid node pair for edge type must fail closed."""
    builder = ConditionGraphBuilder("test-pair-001", ["test"])
    builder.add_node("CN-PARAPET-0001", "PARAPET", "Parapet", "A1")
    builder.add_node("CN-DRAIN-0001", "DRAIN", "Drain", "B1")
    try:
        # PARAPET -> DRAIN via "penetrates" is not a valid pair
        builder.add_edge("CN-PARAPET-0001", "CN-DRAIN-0001", "penetrates")
        assert False, "Should have raised ConditionGraphBuildError"
    except ConditionGraphBuildError as e:
        assert "does not support" in str(e)
    print("  PASS: invalid_node_pair_fails_closed")


def test_deterministic_output():
    """Two identical builds must produce identical output (excluding timestamp)."""
    def build():
        b = ConditionGraphBuilder("det-test-001", ["test"])
        b.add_node("CN-PARAPET-0001", "PARAPET", "Parapet", "A1")
        b.add_node("CN-EDGE-0001", "EDGE", "Edge", "B1")
        b.add_node("CN-SCUPPER-0001", "SCUPPER", "Scupper", "C1")
        b.add_edge("CN-PARAPET-0001", "CN-EDGE-0001", "adjacent_to")
        b.add_edge("CN-EDGE-0001", "CN-SCUPPER-0001", "terminates_at")
        g = b.build()
        return g

    g1 = build()
    g2 = build()
    assert g1["checksum"] == g2["checksum"], "Checksums must match for identical builds"
    assert g1["nodes"] == g2["nodes"], "Nodes must match"
    assert g1["edges"] == g2["edges"], "Edges must match"
    print("  PASS: deterministic_output")


def test_serialization_roundtrip():
    """Graph can be serialized and deserialized without data loss."""
    builder = ConditionGraphBuilder("serial-001", ["test"])
    builder.add_node("CN-CURB-0001", "CURB", "HVAC Curb", "D4")
    builder.add_node("CN-PIPE_PENETRATION-0001", "PIPE_PENETRATION", "Pipe", "D5")
    builder.add_edge("CN-CURB-0001", "CN-PIPE_PENETRATION-0001", "adjacent_to")
    graph = builder.build()

    json_str = serialize_graph(graph)
    restored = deserialize_graph(json_str)
    assert restored["graph_id"] == graph["graph_id"]
    assert restored["nodes"] == graph["nodes"]
    assert restored["edges"] == graph["edges"]
    assert verify_checksum(restored)
    print("  PASS: serialization_roundtrip")


def test_empty_graph_fails():
    """Cannot build a graph with no nodes."""
    builder = ConditionGraphBuilder("empty-001", ["test"])
    try:
        builder.build()
        assert False, "Should have raised ConditionGraphBuildError"
    except ConditionGraphBuildError:
        pass
    print("  PASS: empty_graph_fails")


def run_all():
    print("Condition Graph Tests:")
    test_graph_builds_valid_structure()
    test_sequencing_critical_edges_form_dag()
    test_invalid_node_type_fails_closed()
    test_invalid_edge_type_fails_closed()
    test_invalid_node_pair_fails_closed()
    test_deterministic_output()
    test_serialization_roundtrip()
    test_empty_graph_fails()
    print("  All condition graph tests passed.\n")


if __name__ == "__main__":
    run_all()
