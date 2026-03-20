"""
Serializer — Wave 17A Construction Reference Graph.

Serializes and deserializes reference graph state to/from JSON.
"""

import hashlib
import json
from typing import Any

from runtime.reference_graph.graph_builder import CONTRACT_VERSION, WAVE


class SerializationError(Exception):
    """Raised when serialization fails."""


class ReferenceGraphSerializer:
    """Serializes reference graph state."""

    @staticmethod
    def serialize(graph_state: dict[str, Any]) -> str:
        """Serialize graph state to JSON string.

        Args:
            graph_state: The graph state dict from builder.build().

        Returns:
            Deterministic JSON string.
        """
        return json.dumps(
            graph_state,
            sort_keys=True,
            indent=2,
            separators=(",", ": "),
            default=str,
        )

    @staticmethod
    def deserialize(json_str: str) -> dict[str, Any]:
        """Deserialize JSON string to graph state dict.

        Validates basic structure.

        Raises:
            SerializationError on invalid input.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise SerializationError(f"Invalid JSON: {e}") from e

        if not isinstance(data, dict):
            raise SerializationError("Expected top-level dict.")

        required = ["version", "wave", "nodes", "edges", "checksum"]
        for field in required:
            if field not in data:
                raise SerializationError(f"Missing required field '{field}'.")

        return data

    @staticmethod
    def compute_checksum(nodes: list, edges: list) -> str:
        """Compute deterministic checksum for nodes and edges."""
        content = json.dumps(
            {"nodes": nodes, "edges": edges},
            sort_keys=True, separators=(",", ":"),
            default=str,
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def to_summary(graph_state: dict[str, Any]) -> dict[str, Any]:
        """Create a compact summary of the graph state."""
        nodes = graph_state.get("nodes", [])
        type_counts: dict[str, int] = {}
        for node in nodes:
            t = node.get("object_type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

        partition_counts: dict[str, int] = {}
        for node in nodes:
            p = node.get("partition", "unknown")
            partition_counts[p] = partition_counts.get(p, 0) + 1

        edges = graph_state.get("edges", [])
        relation_counts: dict[str, int] = {}
        for edge in edges:
            r = edge.get("relation_type", "unknown")
            relation_counts[r] = relation_counts.get(r, 0) + 1

        return {
            "version": graph_state.get("version"),
            "wave": graph_state.get("wave"),
            "node_count": graph_state.get("node_count", len(nodes)),
            "edge_count": graph_state.get("edge_count", len(edges)),
            "type_distribution": type_counts,
            "partition_distribution": partition_counts,
            "relation_distribution": relation_counts,
            "checksum": graph_state.get("checksum"),
        }
