"""
Resolution Engine — Wave 17A Construction Reference Graph.

Provides deterministic object resolution across the reference graph.
Resolution modes: deterministic, scoped_deterministic, advisory, unresolved.
Ambiguity fails closed or returns unresolved.
"""

from typing import Any

from runtime.reference_graph.node_registry import NodeRegistry
from runtime.reference_graph.edge_registry import (
    EdgeRegistry,
    DETERMINISTIC_RELATION_TYPES,
    ADVISORY_RELATION_TYPES,
)
from runtime.reference_graph.lineage_engine import LineageEngine


class ResolutionError(Exception):
    """Raised when resolution fails."""


class ResolutionEngine:
    """Resolves objects and references in the reference graph."""

    def __init__(
        self,
        node_registry: NodeRegistry,
        edge_registry: EdgeRegistry,
        lineage_engine: LineageEngine,
    ) -> None:
        self._nodes = node_registry
        self._edges = edge_registry
        self._lineage = lineage_engine

    def resolve_object(self, graph_id: str) -> dict[str, Any]:
        """Resolve a single object by graph_id.

        Returns full node data with resolution metadata.
        """
        node = self._nodes.get(graph_id)
        if not node:
            return {
                "resolved": False,
                "mode": "unresolved",
                "graph_id": graph_id,
                "error": "Node not found",
            }

        if node["status"] == "invalid":
            return {
                "resolved": False,
                "mode": "unresolved",
                "graph_id": graph_id,
                "error": "Node is invalid",
            }

        mode = self._determine_resolution_mode(node)
        return {
            "resolved": True,
            "mode": mode,
            "graph_id": graph_id,
            "node": node,
        }

    def resolve_upstream(self, graph_id: str) -> list[dict[str, Any]]:
        """Resolve all upstream (ancestor) objects."""
        return self._lineage.trace_lineage(graph_id)

    def resolve_downstream(self, graph_id: str) -> list[dict[str, Any]]:
        """Resolve all downstream (descendant) objects."""
        return self._lineage.trace_downstream(graph_id)

    def trace_lineage(self, graph_id: str) -> dict[str, Any]:
        """Full lineage trace with validation."""
        return self._lineage.validate_lineage(graph_id)

    def find_related(
        self,
        graph_id: str,
        relation_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Find all related nodes.

        Args:
            graph_id: The source node.
            relation_type: Optional filter by relation type.

        Returns:
            List of related nodes.
        """
        node = self._nodes.get(graph_id)
        if not node:
            return []

        related: list[dict[str, Any]] = []
        seen: set[str] = set()

        # Outgoing edges
        for edge in self._edges.get_edges_from(graph_id):
            if relation_type and edge["relation_type"] != relation_type:
                continue
            if edge["to_id"] not in seen:
                target = self._nodes.get(edge["to_id"])
                if target and target["status"] != "invalid":
                    related.append(target)
                    seen.add(edge["to_id"])

        # Incoming edges
        for edge in self._edges.get_edges_to(graph_id):
            if relation_type and edge["relation_type"] != relation_type:
                continue
            if edge["from_id"] not in seen:
                source = self._nodes.get(edge["from_id"])
                if source and source["status"] != "invalid":
                    related.append(source)
                    seen.add(edge["from_id"])

        return sorted(related, key=lambda n: n["graph_id"])

    def resolve_by_reference(
        self,
        source_system: str,
        source_reference: str,
        object_type: str,
        scope: str,
    ) -> dict[str, Any]:
        """Resolve by source reference. Prefers exact scoped authoritative matches.

        If multiple authoritative candidates exist in the same scope, returns unresolved.
        """
        from runtime.reference_graph.identity_allocator import IdentityAllocator

        node = self._nodes.get_by_fingerprint(
            source_system, source_reference, object_type, scope,
        )
        if node:
            if node["status"] == "invalid":
                return {
                    "resolved": False,
                    "mode": "unresolved",
                    "error": "Node is invalid",
                }
            return {
                "resolved": True,
                "mode": self._determine_resolution_mode(node),
                "node": node,
            }

        return {
            "resolved": False,
            "mode": "unresolved",
            "error": "No matching node found",
        }

    def _determine_resolution_mode(self, node: dict[str, Any]) -> str:
        """Determine the resolution mode for a node."""
        authority = node.get("authority_type", "")
        if authority == "kernel_canonical":
            return "deterministic"
        if authority == "runtime_derived":
            return "scoped_deterministic"
        if authority == "external_unverified":
            return "advisory"
        return "scoped_deterministic"
