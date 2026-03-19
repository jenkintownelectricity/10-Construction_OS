"""Readiness routing — traverse the condition graph to determine readiness state and next actions.

Consumes a ConditionGraph without modifying it. All operations are deterministic
for identical graph input. Does NOT redefine scope truth, ownership truth, or kernel doctrine.
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode


class ReadinessRouter:
    """Traverses a ConditionGraph to determine readiness state and next actions."""

    def __init__(self, graph: ConditionGraph) -> None:
        self._graph = graph

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_node_or_raise(self, node_id: str) -> ConditionGraphNode:
        """Return the node for *node_id* or raise ``KeyError``."""
        node = self._graph.get_node(node_id)
        if node is None:
            raise KeyError(f"Node not found in graph: {node_id}")
        return node

    def _get_blocker_edges(self, node_id: str):
        """Return edges where *node_id* is blocked_by another node.

        Convention: a ``blocked_by`` edge FROM *node_id* TO the blocker means
        "*node_id* is blocked by <to_node_id>".
        """
        return [
            e for e in self._graph.get_edges_from(node_id)
            if e.edge_type == "blocked_by"
        ]

    def _get_dependency_edges(self, node_id: str):
        """Return ``depends_on`` edges originating from *node_id*."""
        return [
            e for e in self._graph.get_edges_from(node_id)
            if e.edge_type == "depends_on"
        ]

    def _get_resolved_by_edges(self, node_id: str):
        """Return ``resolved_by`` edges originating from *node_id*."""
        return [
            e for e in self._graph.get_edges_from(node_id)
            if e.edge_type == "resolved_by"
        ]

    def _get_owned_by_edges(self, node_id: str):
        """Return ``owned_by`` edges originating from *node_id*."""
        return [
            e for e in self._graph.get_edges_from(node_id)
            if e.edge_type == "owned_by"
        ]

    def _get_owns_edges(self, owner_node_id: str):
        """Return all edges where *owner_node_id* is the target of an ``owned_by`` edge."""
        return [
            e for e in self._graph.get_edges_to(owner_node_id)
            if e.edge_type == "owned_by"
        ]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_blocking_chain(self, node_id: str) -> list[ConditionGraphNode]:
        """Traverse ``blocked_by`` edges recursively to find the full blocking chain.

        Returns an ordered list starting from the immediate blockers of *node_id*
        and expanding outward.  Each node appears at most once (cycle-safe).
        """
        self._get_node_or_raise(node_id)

        result: list[ConditionGraphNode] = []
        visited: set[str] = set()
        queue: list[str] = [node_id]

        while queue:
            current = queue.pop(0)
            for edge in self._get_blocker_edges(current):
                blocker_id = edge.to_node_id
                if blocker_id not in visited:
                    visited.add(blocker_id)
                    blocker_node = self._graph.get_node(blocker_id)
                    if blocker_node is not None:
                        result.append(blocker_node)
                        queue.append(blocker_id)

        return result

    def get_next_actions(self, node_id: str) -> list[dict]:
        """Determine what actions would unblock *node_id*.

        Returns a list of ``{"action": str, "target_node_id": str, "reason": str}``
        dicts.  Logic:
        * For each blocker of this node, check if the blocker has a ``resolved_by``
          edge — if so, suggest resolving *that* target.
        * If the blocker has no remediation path, suggest a generic
          ``"resolve_blocker"`` action.
        """
        self._get_node_or_raise(node_id)

        actions: list[dict] = []
        seen_targets: set[str] = set()

        for edge in self._get_blocker_edges(node_id):
            blocker_id = edge.to_node_id
            if blocker_id in seen_targets:
                continue
            seen_targets.add(blocker_id)

            resolved_edges = self._get_resolved_by_edges(blocker_id)
            if resolved_edges:
                for re in resolved_edges:
                    actions.append({
                        "action": "resolve_via_remediation",
                        "target_node_id": re.to_node_id,
                        "reason": (
                            f"Blocker {blocker_id} can be resolved by "
                            f"completing remediation {re.to_node_id}"
                        ),
                    })
            else:
                actions.append({
                    "action": "resolve_blocker",
                    "target_node_id": blocker_id,
                    "reason": (
                        f"Blocker {blocker_id} has no linked remediation; "
                        f"manual resolution required"
                    ),
                })

        return actions

    def get_unblock_path(self, node_id: str) -> list[ConditionGraphNode]:
        """Return an ordered list of nodes that must be resolved to unblock *node_id*.

        Performs a topological sort of the blocking chain so that resolving the
        returned nodes in order will progressively unblock the target.
        """
        chain = self.get_blocking_chain(node_id)
        if not chain:
            return []

        chain_ids = {n.graph_node_id for n in chain}
        chain_map = {n.graph_node_id: n for n in chain}

        # Build in-degree map restricted to chain nodes.
        in_degree: dict[str, int] = {nid: 0 for nid in chain_ids}
        adj: dict[str, list[str]] = {nid: [] for nid in chain_ids}

        for nid in chain_ids:
            for edge in self._get_blocker_edges(nid):
                dep_id = edge.to_node_id
                if dep_id in chain_ids:
                    adj[dep_id].append(nid)
                    in_degree[nid] += 1

        # Kahn's algorithm — deterministic via sorted tie-breaking.
        queue = sorted([nid for nid, deg in in_degree.items() if deg == 0])
        ordered: list[ConditionGraphNode] = []

        while queue:
            current = queue.pop(0)
            ordered.append(chain_map[current])
            for neighbour in sorted(adj[current]):
                in_degree[neighbour] -= 1
                if in_degree[neighbour] == 0:
                    queue.append(neighbour)
            queue.sort()

        return ordered

    def get_readiness_chain(self, node_id: str) -> dict:
        """Return a readiness assessment for *node_id*.

        Returns::

            {
                "node": ConditionGraphNode,
                "ready": bool,
                "blockers": [ConditionGraphNode, ...],
                "dependencies_met": bool,
                "next_actions": [{"action": ..., "target_node_id": ..., "reason": ...}, ...],
            }

        A node is *ready* when it has no active blocker edges AND all
        ``depends_on`` edges lead to nodes whose ``state_summary`` indicates
        readiness (i.e. ``state_summary.get("status") == "ready"``).
        """
        node = self._get_node_or_raise(node_id)

        blockers = self.get_blocking_chain(node_id)
        next_actions = self.get_next_actions(node_id)

        # Check dependency readiness.
        dependencies_met = True
        for dep_edge in self._get_dependency_edges(node_id):
            dep_node = self._graph.get_node(dep_edge.to_node_id)
            if dep_node is None:
                dependencies_met = False
                break
            if dep_node.state_summary.get("status") != "ready":
                dependencies_met = False
                break

        ready = len(blockers) == 0 and dependencies_met

        return {
            "node": node,
            "ready": ready,
            "blockers": blockers,
            "dependencies_met": dependencies_met,
            "next_actions": next_actions,
        }

    def get_owner_responsibility(self, node_id: str) -> dict:
        """Follow ``owned_by`` edges from *node_id* and return ownership info.

        Returns::

            {
                "owner_node": ConditionGraphNode | None,
                "owner_state": "unknown" | "assigned" | "unassigned",
                "owned_conditions": [str, ...],
            }
        """
        self._get_node_or_raise(node_id)

        owned_by_edges = self._get_owned_by_edges(node_id)

        if not owned_by_edges:
            return {
                "owner_node": None,
                "owner_state": "unassigned",
                "owned_conditions": [],
            }

        # Use the first owned_by edge (deterministic — edges are stored in dict order).
        owner_id = owned_by_edges[0].to_node_id
        owner_node = self._graph.get_node(owner_id)

        if owner_node is None:
            return {
                "owner_node": None,
                "owner_state": "unknown",
                "owned_conditions": [],
            }

        # Find all nodes owned by this owner.
        owns_edges = self._get_owns_edges(owner_id)
        owned_conditions = sorted({e.from_node_id for e in owns_edges})

        return {
            "owner_node": owner_node,
            "owner_state": "assigned",
            "owned_conditions": owned_conditions,
        }
