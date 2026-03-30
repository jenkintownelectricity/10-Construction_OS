"""
Orphan Detector — Wave 17A Construction Reference Graph.

Detects orphaned nodes (no edges) and disconnected subgraphs.
"""

from typing import Any

from runtime.reference_graph.node_registry import NodeRegistry
from runtime.reference_graph.edge_registry import EdgeRegistry
from runtime.reference_graph.query_engine import QueryEngine


class OrphanDetector:
    """Detects orphans and disconnected components in the reference graph."""

    def __init__(
        self,
        node_registry: NodeRegistry,
        edge_registry: EdgeRegistry,
        query_engine: QueryEngine,
    ) -> None:
        self._nodes = node_registry
        self._edges = edge_registry
        self._query = query_engine

    def detect_orphans(self) -> dict[str, Any]:
        """Detect all orphaned nodes (nodes with no edges).

        Returns:
            Report with list of orphan node IDs.
        """
        all_nodes = self._nodes.list_nodes(status="active")
        connected_ids: set[str] = set()

        for edge in self._edges.list_edges(status="active"):
            connected_ids.add(edge["from_id"])
            connected_ids.add(edge["to_id"])

        orphans = [
            n for n in all_nodes
            if n["graph_id"] not in connected_ids
        ]

        return {
            "orphan_count": len(orphans),
            "total_nodes": len(all_nodes),
            "orphan_ids": [o["graph_id"] for o in orphans],
            "orphan_types": {
                o["object_type"]: sum(
                    1 for x in orphans if x["object_type"] == o["object_type"]
                )
                for o in orphans
            },
        }

    def detect_disconnected_components(self) -> dict[str, Any]:
        """Detect disconnected subgraphs.

        Returns:
            Report with component counts and sizes.
        """
        components = self._query.get_connected_components()

        return {
            "component_count": len(components),
            "components": [
                {
                    "size": len(comp),
                    "node_ids": comp,
                }
                for comp in components
            ],
            "largest_component_size": max(
                (len(c) for c in components), default=0
            ),
            "singleton_count": sum(1 for c in components if len(c) == 1),
        }
