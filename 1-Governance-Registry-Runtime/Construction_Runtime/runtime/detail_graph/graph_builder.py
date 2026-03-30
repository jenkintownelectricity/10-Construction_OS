"""
Detail Graph Builder — Wave 15.

Constructs a detail relationship graph from kernel-backed route data.
Nodes are detail identities. Edges are valid kernel-backed relationships.
"""

import hashlib
import json
from collections import defaultdict, deque
from typing import Any

from runtime.detail_graph.contract import (
    CONTRACT_VERSION,
    WAVE,
    VALID_RELATIONSHIP_TYPES,
    ACYCLIC_RELATIONSHIP_TYPES,
    BIDIRECTIONAL_TYPES,
)


class DetailGraphBuildError(Exception):
    """Raised when graph construction fails. Fail closed."""


class DetailGraph:
    """In-memory detail relationship graph with traversal operations."""

    def __init__(
        self,
        nodes: dict[str, dict[str, Any]],
        edges: list[dict[str, Any]],
        adjacency_out: dict[str, list[str]],
        adjacency_in: dict[str, list[str]],
        checksum: str,
    ):
        self.nodes = nodes
        self.edges = edges
        self.adjacency_out = adjacency_out
        self.adjacency_in = adjacency_in
        self.checksum = checksum

    def neighbor_lookup(self, detail_id: str) -> list[str]:
        """Return all neighboring detail IDs (both directions)."""
        if detail_id not in self.nodes:
            return []
        neighbors = set()
        for nid in self.adjacency_out.get(detail_id, []):
            neighbors.add(nid)
        for nid in self.adjacency_in.get(detail_id, []):
            neighbors.add(nid)
        return sorted(neighbors)

    def bfs(self, start_id: str) -> list[str]:
        """Breadth-first traversal from start_id. Deterministic ordering."""
        if start_id not in self.nodes:
            return []
        visited = [start_id]
        visited_set = {start_id}
        queue: deque[str] = deque([start_id])
        while queue:
            current = queue.popleft()
            for neighbor in sorted(
                set(self.adjacency_out.get(current, []))
                | set(self.adjacency_in.get(current, []))
            ):
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    visited.append(neighbor)
                    queue.append(neighbor)
        return visited

    def dfs(self, start_id: str) -> list[str]:
        """Depth-first traversal from start_id. Deterministic ordering."""
        if start_id not in self.nodes:
            return []
        visited: list[str] = []
        visited_set: set[str] = set()

        def _dfs(node_id: str) -> None:
            visited_set.add(node_id)
            visited.append(node_id)
            for neighbor in sorted(
                set(self.adjacency_out.get(node_id, []))
                | set(self.adjacency_in.get(node_id, []))
            ):
                if neighbor not in visited_set:
                    _dfs(neighbor)

        _dfs(start_id)
        return visited

    def shortest_path(self, source_id: str, target_id: str) -> list[str] | None:
        """Find shortest path via BFS. Returns None if no path exists."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        if source_id == target_id:
            return [source_id]

        visited = {source_id}
        queue: deque[list[str]] = deque([[source_id]])
        while queue:
            path = queue.popleft()
            current = path[-1]
            for neighbor in sorted(
                set(self.adjacency_out.get(current, []))
                | set(self.adjacency_in.get(current, []))
            ):
                if neighbor == target_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None

    def path_exists(self, source_id: str, target_id: str) -> bool:
        """Check if a path exists between two details."""
        return self.shortest_path(source_id, target_id) is not None

    def get_edges_for(self, detail_id: str) -> list[dict[str, Any]]:
        """Return all edges involving this detail."""
        return [
            e for e in self.edges
            if e["source_detail_id"] == detail_id or e["target_detail_id"] == detail_id
        ]

    def get_edges_by_type(self, relationship_type: str) -> list[dict[str, Any]]:
        """Return all edges of a given relationship type."""
        return [e for e in self.edges if e["relationship_type"] == relationship_type]

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        return {
            "version": CONTRACT_VERSION,
            "wave": WAVE,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes": self.nodes,
            "edges": self.edges,
            "adjacency_out": {k: sorted(v) for k, v in sorted(self.adjacency_out.items())},
            "adjacency_in": {k: sorted(v) for k, v in sorted(self.adjacency_in.items())},
            "checksum": self.checksum,
        }


def build_detail_graph(
    detail_index: dict[str, Any],
    route_index: dict[str, Any],
) -> DetailGraph:
    """
    Build a detail relationship graph from index and route data.

    Args:
        detail_index: Built detail index artifact.
        route_index: Kernel route index with routes list.

    Returns:
        DetailGraph instance.

    Raises:
        DetailGraphBuildError on validation failures.
    """
    detail_lookup = detail_index.get("detail_lookup", {})
    if not detail_lookup:
        raise DetailGraphBuildError("Cannot build graph from empty detail lookup.")

    # Build nodes from detail index
    nodes: dict[str, dict[str, Any]] = {}
    for detail_id, record in sorted(detail_lookup.items()):
        nodes[detail_id] = {
            "detail_id": detail_id,
            "system": record.get("system"),
            "class": record.get("class"),
            "condition": record.get("condition"),
            "variant": record.get("variant"),
            "assembly_family": record.get("assembly_family"),
            "display_name": record.get("display_name"),
        }

    # Build edges from route index
    routes = route_index.get("routes", [])
    edges: list[dict[str, Any]] = []
    adjacency_out: dict[str, list[str]] = defaultdict(list)
    adjacency_in: dict[str, list[str]] = defaultdict(list)

    for route in routes:
        source_id = route["source_detail_id"]
        target_id = route["target_detail_id"]
        rel_type = route["relationship_type"]

        if rel_type not in VALID_RELATIONSHIP_TYPES:
            raise DetailGraphBuildError(
                f"Invalid relationship_type '{rel_type}' in route "
                f"{source_id} -> {target_id}"
            )

        if source_id not in nodes:
            raise DetailGraphBuildError(
                f"Edge references unknown source detail_id: {source_id}"
            )
        if target_id not in nodes:
            raise DetailGraphBuildError(
                f"Edge references unknown target detail_id: {target_id}"
            )

        edge = {
            "source_detail_id": source_id,
            "target_detail_id": target_id,
            "relationship_type": rel_type,
            "directionality": route.get("directionality", "directional"),
            "criticality": route.get("criticality", "required"),
        }
        if "description" in route:
            edge["description"] = route["description"]

        edges.append(edge)
        adjacency_out[source_id].append(target_id)
        adjacency_in[target_id].append(source_id)

        # For bidirectional relationships, add reverse edge to adjacency
        if route.get("directionality") == "bidirectional":
            adjacency_out[target_id].append(source_id)
            adjacency_in[source_id].append(target_id)

    # Sort edges deterministically
    edges.sort(key=lambda e: (e["source_detail_id"], e["target_detail_id"], e["relationship_type"]))

    # Validate DAG constraint on acyclic types
    _validate_acyclic(edges, set(nodes.keys()))

    # Compute checksum
    content = json.dumps(
        {"nodes": dict(sorted(nodes.items())), "edges": edges},
        sort_keys=True, separators=(",", ":"),
    )
    checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()

    return DetailGraph(
        nodes=dict(sorted(nodes.items())),
        edges=edges,
        adjacency_out=dict(adjacency_out),
        adjacency_in=dict(adjacency_in),
        checksum=checksum,
    )


def _validate_acyclic(edges: list[dict[str, Any]], node_ids: set[str]) -> None:
    """Validate that acyclic relationship types form a DAG."""
    acyclic_adj: dict[str, list[str]] = {nid: [] for nid in node_ids}
    for e in edges:
        if e["relationship_type"] in ACYCLIC_RELATIONSHIP_TYPES:
            acyclic_adj[e["source_detail_id"]].append(e["target_detail_id"])

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {nid: WHITE for nid in node_ids}

    def dfs(n: str) -> bool:
        color[n] = GRAY
        for nb in acyclic_adj.get(n, []):
            if color.get(nb) == GRAY:
                return True
            if color.get(nb) == WHITE and dfs(nb):
                return True
        color[n] = BLACK
        return False

    for nid in sorted(node_ids):
        if color[nid] == WHITE and dfs(nid):
            raise DetailGraphBuildError(
                f"Cycle detected in acyclic relationship types (depends_on/precedes). "
                f"Graph must be a DAG for these edge types."
            )
