"""
Detail Pathfinder — Wave 14 Subsystem 4.

Computes paths between detail-relevant conditions in the frozen route graph.
BFS-based pathfinding with relationship type preservation.
"""

from collections import deque
from typing import Any

from runtime.detail_map.detail_route_query import FROZEN_ROUTES, get_all_detail_ids


def _build_adjacency() -> dict[str, list[tuple[str, str, str]]]:
    """Build adjacency list from frozen routes, respecting directionality."""
    adj: dict[str, list[tuple[str, str, str]]] = {did: [] for did in get_all_detail_ids()}
    for route in FROZEN_ROUTES:
        adj[route["source"]].append((route["target"], route["type"], route["crit"]))
        if route["dir"] == "bidirectional":
            adj[route["target"]].append((route["source"], route["type"], route["crit"]))
    return adj


def find_path(
    source_detail_id: str,
    target_detail_id: str,
) -> list[dict[str, Any]] | None:
    """
    Find shortest path between two detail IDs in the route graph.
    Returns list of path steps or None if no path exists.
    """
    all_ids = set(get_all_detail_ids())
    if source_detail_id not in all_ids or target_detail_id not in all_ids:
        return None

    if source_detail_id == target_detail_id:
        return [{"detail_id": source_detail_id, "relationship": "self", "criticality": ""}]

    adj = _build_adjacency()
    visited: set[str] = {source_detail_id}
    queue: deque[list[dict[str, Any]]] = deque()

    # Initialize with neighbors of source
    for neighbor, rel_type, crit in sorted(adj.get(source_detail_id, [])):
        if neighbor not in visited:
            path = [
                {"detail_id": source_detail_id, "relationship": "origin", "criticality": ""},
                {"detail_id": neighbor, "relationship": rel_type, "criticality": crit},
            ]
            if neighbor == target_detail_id:
                return path
            queue.append(path)
            visited.add(neighbor)

    while queue:
        current_path = queue.popleft()
        current_id = current_path[-1]["detail_id"]

        for neighbor, rel_type, crit in sorted(adj.get(current_id, [])):
            if neighbor not in visited:
                new_path = current_path + [
                    {"detail_id": neighbor, "relationship": rel_type, "criticality": crit}
                ]
                if neighbor == target_detail_id:
                    return new_path
                queue.append(new_path)
                visited.add(neighbor)

    return None


def find_all_paths(
    source_detail_id: str,
    target_detail_id: str,
    max_depth: int = 5,
) -> list[list[dict[str, Any]]]:
    """
    Find all paths (up to max_depth) between two detail IDs.
    Returns list of paths, sorted by length then lexicographically.
    """
    all_ids = set(get_all_detail_ids())
    if source_detail_id not in all_ids or target_detail_id not in all_ids:
        return []

    adj = _build_adjacency()
    results: list[list[dict[str, Any]]] = []

    def dfs(current: str, path: list[dict[str, Any]], visited: set[str]) -> None:
        if len(path) > max_depth:
            return
        if current == target_detail_id and len(path) > 1:
            results.append(list(path))
            return
        for neighbor, rel_type, crit in sorted(adj.get(current, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append({"detail_id": neighbor, "relationship": rel_type, "criticality": crit})
                dfs(neighbor, path, visited)
                path.pop()
                visited.discard(neighbor)

    start_path = [{"detail_id": source_detail_id, "relationship": "origin", "criticality": ""}]
    dfs(source_detail_id, start_path, {source_detail_id})

    return sorted(results, key=lambda p: (len(p), str(p)))
