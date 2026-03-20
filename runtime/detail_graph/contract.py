"""
Detail Graph Contract — Wave 15.

Defines the contract surface for the detail graph subsystem.
"""

from typing import Any

CONTRACT_VERSION = "15.1.0"
WAVE = "15"
SUBSYSTEM = "detail_graph"

VALID_RELATIONSHIP_TYPES = frozenset([
    "depends_on", "adjacent_to", "blocks", "requires_continuity_with",
    "substitutable_with", "terminates_into", "overlaps_with",
    "precedes", "follows",
])

ACYCLIC_RELATIONSHIP_TYPES = frozenset(["depends_on", "precedes"])
ALLOWED_CYCLIC_TYPES = frozenset(["adjacent_to", "substitutable_with", "overlaps_with"])

BIDIRECTIONAL_TYPES = frozenset([
    "adjacent_to", "substitutable_with", "overlaps_with", "requires_continuity_with",
])


class DetailGraphContract:
    """Contract definition for build_detail_graph()."""

    @staticmethod
    def input_spec() -> dict[str, Any]:
        return {
            "detail_index": "dict — built detail index from detail_index subsystem",
            "route_index": "dict — detail route index from Construction_Kernel",
        }

    @staticmethod
    def output_spec() -> dict[str, Any]:
        return {
            "detail_graph": {
                "version": "str",
                "wave": "str",
                "nodes": "dict[detail_id -> node_data]",
                "edges": "list[edge_data]",
                "adjacency_out": "dict[detail_id -> list[detail_id]]",
                "adjacency_in": "dict[detail_id -> list[detail_id]]",
                "checksum": "str",
            }
        }

    @staticmethod
    def failure_cases() -> list[str]:
        return [
            "Edge references unknown detail_id — fail closed",
            "Invalid relationship_type — fail closed",
            "Cycle in acyclic relationship types — fail closed",
            "Empty node set — fail closed",
        ]

    @staticmethod
    def graph_operations() -> list[str]:
        return [
            "neighbor_lookup(detail_id) -> list[detail_id]",
            "bfs(start_id) -> list[detail_id]",
            "dfs(start_id) -> list[detail_id]",
            "shortest_path(source_id, target_id) -> list[detail_id] | None",
            "path_exists(source_id, target_id) -> bool",
        ]
