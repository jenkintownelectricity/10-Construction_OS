"""Impact analysis — traverse the condition graph to determine downstream/upstream impacts.

Consumes a ConditionGraph without modifying it. All operations are deterministic
for identical graph input. Does NOT redefine revision doctrine or package doctrine.
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode


# Node types used for artifact/package/revision filtering.
_ARTIFACT_TYPES = {"artifact"}
_PACKAGE_TYPES = {"package"}
_REVISION_TYPES = {"revision"}


class ImpactAnalyzer:
    """Traverses a ConditionGraph to determine impact of changes at a given node."""

    def __init__(self, graph: ConditionGraph) -> None:
        self._graph = graph

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_node_or_raise(self, node_id: str) -> ConditionGraphNode:
        node = self._graph.get_node(node_id)
        if node is None:
            raise KeyError(f"Node not found in graph: {node_id}")
        return node

    def _bfs_downstream(self, start_id: str, max_depth: int) -> list[ConditionGraphNode]:
        """BFS over *reverse* dependency/blocker relationships.

        "Downstream" means nodes that depend on or are blocked by *start_id*.
        These are edges where ``to_node_id == start_id`` with type ``depends_on``
        or ``blocked_by`` — i.e. some other node X has a ``depends_on`` or
        ``blocked_by`` edge pointing TO *start_id*, making X downstream of
        *start_id*.
        """
        visited: set[str] = set()
        result: list[ConditionGraphNode] = []
        # (node_id, current_depth)
        queue: list[tuple[str, int]] = [(start_id, 0)]
        visited.add(start_id)

        while queue:
            current_id, depth = queue.pop(0)
            if max_depth >= 0 and depth >= max_depth:
                continue

            # Find nodes that point TO current_id via depends_on or blocked_by.
            for edge in self._graph.get_edges_to(current_id):
                if edge.edge_type in ("depends_on", "blocked_by"):
                    downstream_id = edge.from_node_id
                    if downstream_id not in visited:
                        visited.add(downstream_id)
                        node = self._graph.get_node(downstream_id)
                        if node is not None:
                            result.append(node)
                            queue.append((downstream_id, depth + 1))

        return result

    def _bfs_upstream(self, start_id: str, max_depth: int) -> list[ConditionGraphNode]:
        """BFS over forward dependency/blocker relationships.

        "Upstream" means nodes that *start_id* depends on or is blocked by.
        These are edges where ``from_node_id == start_id`` with type
        ``depends_on`` or ``blocked_by``.
        """
        visited: set[str] = set()
        result: list[ConditionGraphNode] = []
        queue: list[tuple[str, int]] = [(start_id, 0)]
        visited.add(start_id)

        while queue:
            current_id, depth = queue.pop(0)
            if max_depth >= 0 and depth >= max_depth:
                continue

            for edge in self._graph.get_edges_from(current_id):
                if edge.edge_type in ("depends_on", "blocked_by"):
                    upstream_id = edge.to_node_id
                    if upstream_id not in visited:
                        visited.add(upstream_id)
                        node = self._graph.get_node(upstream_id)
                        if node is not None:
                            result.append(node)
                            queue.append((upstream_id, depth + 1))

        return result

    def _reachable_subgraph(self, start_id: str) -> set[str]:
        """Return the set of all node ids reachable from *start_id* via any edge direction."""
        visited: set[str] = set()
        queue: list[str] = [start_id]
        visited.add(start_id)

        while queue:
            current = queue.pop(0)
            for edge in self._graph.get_edges_from(current):
                if edge.to_node_id not in visited:
                    visited.add(edge.to_node_id)
                    queue.append(edge.to_node_id)
            for edge in self._graph.get_edges_to(current):
                if edge.from_node_id not in visited:
                    visited.add(edge.from_node_id)
                    queue.append(edge.from_node_id)

        return visited

    def _filter_by_types(self, node_ids: set[str], type_set: set[str]) -> list[ConditionGraphNode]:
        """Return nodes from *node_ids* whose ``node_type`` is in *type_set*, sorted by id."""
        result: list[ConditionGraphNode] = []
        for nid in sorted(node_ids):
            node = self._graph.get_node(nid)
            if node is not None and node.node_type in type_set:
                result.append(node)
        return result

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_downstream_impacts(self, node_id: str, max_depth: int = -1) -> list[ConditionGraphNode]:
        """Return all nodes downstream of *node_id*.

        Follows reversed ``depends_on`` and ``blocked_by`` edges — i.e. finds
        nodes that depend on or are blocked by *node_id*, recursively up to
        *max_depth* (-1 = unlimited).
        """
        self._get_node_or_raise(node_id)
        return self._bfs_downstream(node_id, max_depth)

    def get_upstream_dependencies(self, node_id: str, max_depth: int = -1) -> list[ConditionGraphNode]:
        """Return all nodes upstream of *node_id*.

        Follows ``depends_on`` and ``blocked_by`` edges FROM *node_id*
        recursively up to *max_depth* (-1 = unlimited).
        """
        self._get_node_or_raise(node_id)
        return self._bfs_upstream(node_id, max_depth)

    def get_artifact_impacts(self, node_id: str) -> list[ConditionGraphNode]:
        """Return all artifact nodes in the subgraph reachable from *node_id*."""
        self._get_node_or_raise(node_id)
        reachable = self._reachable_subgraph(node_id)
        return self._filter_by_types(reachable, _ARTIFACT_TYPES)

    def get_package_impacts(self, node_id: str) -> list[ConditionGraphNode]:
        """Return all package nodes in the subgraph reachable from *node_id*."""
        self._get_node_or_raise(node_id)
        reachable = self._reachable_subgraph(node_id)
        return self._filter_by_types(reachable, _PACKAGE_TYPES)

    def get_revision_impacts(self, node_id: str) -> list[ConditionGraphNode]:
        """Return all revision nodes in the subgraph reachable from *node_id*."""
        self._get_node_or_raise(node_id)
        reachable = self._reachable_subgraph(node_id)
        return self._filter_by_types(reachable, _REVISION_TYPES)

    def get_regeneration_targets(self, node_id: str) -> list[dict]:
        """Find artifacts/packages that need regeneration due to changes at *node_id*.

        Returns a list of ``{"target_node_id": str, "target_type": str, "reason": str}``
        dicts.  A target needs regeneration if it is downstream of *node_id* (via
        dependency or blocker edges) or is an artifact/package in the reachable
        subgraph.
        """
        self._get_node_or_raise(node_id)

        targets: list[dict] = []
        seen: set[str] = set()

        # Downstream artifacts/packages via dependency chain.
        downstream = self._bfs_downstream(node_id, max_depth=-1)
        for node in downstream:
            if node.node_type in ("artifact", "package") and node.graph_node_id not in seen:
                seen.add(node.graph_node_id)
                targets.append({
                    "target_node_id": node.graph_node_id,
                    "target_type": node.node_type,
                    "reason": f"Downstream {node.node_type} depends on changed node {node_id}",
                })

        # Also check artifacts/packages reachable via any edge that weren't
        # already captured (e.g. connected via included_in, derived_from, etc.).
        reachable = self._reachable_subgraph(node_id)
        for nid in sorted(reachable):
            if nid in seen:
                continue
            rnode = self._graph.get_node(nid)
            if rnode is not None and rnode.node_type in ("artifact", "package"):
                seen.add(nid)
                targets.append({
                    "target_node_id": nid,
                    "target_type": rnode.node_type,
                    "reason": f"Reachable {rnode.node_type} connected to changed node {node_id}",
                })

        return targets
