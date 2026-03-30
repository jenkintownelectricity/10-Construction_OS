"""
Tests for Wave 15 Detail Graph Migration — Wave 17A.

Tests: migration correctness, node preservation, edge mapping, lineage traceability.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.graph_builder import ReferenceGraphBuilder
from runtime.reference_graph.lineage_engine import LineageEngine
from runtime.reference_graph.resolution_engine import ResolutionEngine


# Wave 15 relationship type to Wave 17A relation type mapping
WAVE15_TO_WAVE17A_MAP = {
    "depends_on": "prerequisite_for",
    "adjacent_to": "related_to",
    "blocks": "prerequisite_for",
    "requires_continuity_with": "related_to",
    "substitutable_with": "alternative_to",
    "terminates_into": "related_to",
    "overlaps_with": "related_to",
    "precedes": "installed_before",
    "follows": "installed_after",
}


def _simulate_wave15_migration():
    """Simulate migrating Wave 15 detail graph nodes and edges into CRG."""
    builder = ReferenceGraphBuilder()

    # Simulate Wave 15 detail nodes
    wave15_details = [
        {"detail_id": "LOW_SLOPE-TERMINATION-PARAPET-REGLET-EPDM-01", "system": "LOW_SLOPE"},
        {"detail_id": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-TPO-01", "system": "LOW_SLOPE"},
        {"detail_id": "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01", "system": "LOW_SLOPE"},
    ]

    crg_nodes = []
    for detail in wave15_details:
        crg_nodes.append({
            "object_type": "DETAIL",
            "scope": "global",
            "partition": "global_kernel_partition",
            "source_system": "Construction_Kernel",
            "source_reference": detail["detail_id"],
            "authority_type": "kernel_canonical",
            "metadata": detail,
        })

    result = builder.register_bundle(crg_nodes, [])
    node_map = {n["metadata"]["detail_id"]: n["graph_id"] for n in result["nodes"]}

    # Simulate Wave 15 edges
    wave15_edges = [
        {"source": wave15_details[0]["detail_id"], "target": wave15_details[1]["detail_id"], "type": "adjacent_to"},
        {"source": wave15_details[0]["detail_id"], "target": wave15_details[2]["detail_id"], "type": "depends_on"},
    ]

    crg_edges = []
    for edge in wave15_edges:
        mapped_type = WAVE15_TO_WAVE17A_MAP[edge["type"]]
        crg_edges.append({
            "relation_type": mapped_type,
            "from_id": node_map[edge["source"]],
            "to_id": node_map[edge["target"]],
            "source_basis": f"wave15_migration:{edge['type']}",
            "is_advisory": True,  # navigation types are advisory
        })

    builder.register_bundle([], crg_edges)

    lineage = LineageEngine(builder.node_registry, builder.edge_registry)
    resolution = ResolutionEngine(builder.node_registry, builder.edge_registry, lineage)

    return builder, node_map, resolution


class TestMigrationCorrectness:
    """Wave 15 migration must preserve all nodes and edges."""

    def test_all_wave15_nodes_migrated(self):
        builder, node_map, _ = _simulate_wave15_migration()
        assert len(node_map) == 3
        graph = builder.build()
        assert graph["node_count"] == 3

    def test_migrated_nodes_are_kernel_canonical(self):
        builder, _, _ = _simulate_wave15_migration()
        for node in builder.node_registry.list_nodes():
            assert node["authority_type"] == "kernel_canonical"
            assert node["partition"] == "global_kernel_partition"

    def test_wave15_ids_traceable(self):
        builder, node_map, resolution = _simulate_wave15_migration()
        for detail_id, graph_id in node_map.items():
            result = resolution.resolve_by_reference(
                "Construction_Kernel", detail_id, "DETAIL", "global",
            )
            assert result["resolved"] is True

    def test_wave15_edges_mapped(self):
        builder, _, _ = _simulate_wave15_migration()
        graph = builder.build()
        assert graph["edge_count"] == 2

    def test_wave15_relationship_types_mapped(self):
        builder, _, _ = _simulate_wave15_migration()
        edges = builder.edge_registry.list_edges()
        edge_types = {e["relation_type"] for e in edges}
        assert "related_to" in edge_types
        assert "prerequisite_for" in edge_types

    def test_all_wave15_relationship_types_have_mapping(self):
        """Every Wave 15 relationship type must have a CRG mapping."""
        wave15_types = [
            "depends_on", "adjacent_to", "blocks", "requires_continuity_with",
            "substitutable_with", "terminates_into", "overlaps_with",
            "precedes", "follows",
        ]
        for w15_type in wave15_types:
            assert w15_type in WAVE15_TO_WAVE17A_MAP

    def test_source_basis_preserves_original_type(self):
        builder, _, _ = _simulate_wave15_migration()
        edges = builder.edge_registry.list_edges()
        for edge in edges:
            assert edge["source_basis"].startswith("wave15_migration:")
