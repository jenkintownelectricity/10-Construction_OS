"""
Query Engine — Wave 17A Construction Reference Graph.

Provides graph traversal and query operations over the reference graph.
"""

from collections import deque
from typing import Any

from runtime.reference_graph.node_registry import NodeRegistry
from runtime.reference_graph.edge_registry import EdgeRegistry


class QueryEngine:
    """Query and traversal engine for the reference graph."""

    def __init__(
        self,
        node_registry: NodeRegistry,
        edge_registry: EdgeRegistry,
    ) -> None:
        self._nodes = node_registry
        self._edges = edge_registry

    def bfs(self, start_id: str, max_depth: int | None = None) -> list[str]:
        """Breadth-first traversal from start node. Deterministic ordering."""
        if not self._nodes.get(start_id):
            return []

        visited: list[str] = [start_id]
        visited_set: set[str] = {start_id}
        queue: deque[tuple[str, int]] = deque([(start_id, 0)])

        while queue:
            current, depth = queue.popleft()
            if max_depth is not None and depth >= max_depth:
                continue

            neighbors = self._get_neighbors(current)
            for neighbor in sorted(neighbors):
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    visited.append(neighbor)
                    queue.append((neighbor, depth + 1))

        return visited

    def dfs(self, start_id: str) -> list[str]:
        """Depth-first traversal from start node. Deterministic ordering."""
        if not self._nodes.get(start_id):
            return []

        visited: list[str] = []
        visited_set: set[str] = set()

        def _dfs(node_id: str) -> None:
            visited_set.add(node_id)
            visited.append(node_id)
            for neighbor in sorted(self._get_neighbors(node_id)):
                if neighbor not in visited_set:
                    _dfs(neighbor)

        _dfs(start_id)
        return visited

    def shortest_path(self, source_id: str, target_id: str) -> list[str] | None:
        """Find shortest path via BFS. Returns None if no path."""
        if not self._nodes.get(source_id) or not self._nodes.get(target_id):
            return None
        if source_id == target_id:
            return [source_id]

        visited: set[str] = {source_id}
        queue: deque[list[str]] = deque([[source_id]])

        while queue:
            path = queue.popleft()
            current = path[-1]
            for neighbor in sorted(self._get_neighbors(current)):
                if neighbor == target_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None

    def find_nodes_by_type(self, object_type: str) -> list[dict[str, Any]]:
        """Find all nodes of a given type."""
        return self._nodes.list_nodes(object_type=object_type)

    def find_nodes_by_partition(self, partition: str) -> list[dict[str, Any]]:
        """Find all nodes in a given partition."""
        return self._nodes.list_nodes(partition=partition)

    def get_subgraph(
        self, node_ids: list[str],
    ) -> dict[str, Any]:
        """Extract a subgraph containing only the specified nodes and their edges."""
        nodes = []
        for nid in node_ids:
            node = self._nodes.get(nid)
            if node:
                nodes.append(node)

        id_set = set(node_ids)
        edges = [
            e for e in self._edges.list_edges()
            if e["from_id"] in id_set and e["to_id"] in id_set
        ]

        return {
            "nodes": sorted(nodes, key=lambda n: n["graph_id"]),
            "edges": sorted(edges, key=lambda e: e["edge_id"]),
            "node_count": len(nodes),
            "edge_count": len(edges),
        }

    def get_connected_components(self) -> list[list[str]]:
        """Find all connected components in the graph."""
        all_nodes = {n["graph_id"] for n in self._nodes.list_nodes()}
        visited: set[str] = set()
        components: list[list[str]] = []

        for node_id in sorted(all_nodes):
            if node_id not in visited:
                component = self.bfs(node_id)
                visited.update(component)
                components.append(component)

        return components

    def _get_neighbors(self, node_id: str) -> set[str]:
        """Get all neighbors (both directions) for active edges."""
        neighbors: set[str] = set()
        for edge in self._edges.get_edges_from(node_id):
            if edge["status"] == "active":
                neighbors.add(edge["to_id"])
        for edge in self._edges.get_edges_to(node_id):
            if edge["status"] == "active":
                neighbors.add(edge["from_id"])
        return neighbors
