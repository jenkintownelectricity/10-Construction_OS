"""Wave 11A graph validator — structural and identity validation for the condition graph."""

from typing import Optional

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph.graph_edge import ConditionGraphEdge


class GraphValidator:
    """Validates a materialized ConditionGraph for structural integrity.

    Checks: orphan edges, duplicate edges, non-empty identifiers,
    deterministic identity recomputation, and cross-build rebuildability.
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        self.config = config or {}

    def validate(self, graph: ConditionGraph) -> list[str]:
        """Validate the graph and return a list of errors (empty = valid).

        Checks performed:
        1. No orphan edges (edges referencing non-existent nodes).
        2. No duplicate edges (enforced by ConditionGraph.add_edge, verified here).
        3. All nodes have non-empty graph_node_id.
        4. All edges have non-empty graph_edge_id.
        5. Node identity is deterministic (recompute and verify).
        """
        errors: list[str] = []

        # Check all nodes have non-empty graph_node_id
        for nid, node in graph.nodes.items():
            if not node.graph_node_id:
                errors.append(
                    f"Node with empty graph_node_id found "
                    f"(source={node.source_object_type}:{node.source_object_id})"
                )

        # Check all edges have non-empty graph_edge_id
        for eid, edge in graph.edges.items():
            if not edge.graph_edge_id:
                errors.append(
                    f"Edge with empty graph_edge_id found "
                    f"(type={edge.edge_type}, {edge.from_node_id} -> {edge.to_node_id})"
                )

        # Check for orphan edges (edges referencing non-existent nodes)
        for eid, edge in graph.edges.items():
            if edge.from_node_id not in graph.nodes:
                errors.append(
                    f"Orphan edge {eid}: from_node_id {edge.from_node_id} not in graph"
                )
            if edge.to_node_id not in graph.nodes:
                errors.append(
                    f"Orphan edge {eid}: to_node_id {edge.to_node_id} not in graph"
                )

        # Check for duplicate edges (should not happen if add_edge is used, but verify)
        seen_edge_ids: set[str] = set()
        for eid in graph.edges:
            if eid in seen_edge_ids:
                errors.append(f"Duplicate edge id detected: {eid}")
            seen_edge_ids.add(eid)

        # Check node identity determinism — recompute and verify
        for nid, node in graph.nodes.items():
            expected = ConditionGraphNode.compute_node_id(
                node.source_object_type, node.source_object_id, node.project_id
            )
            if nid != expected:
                errors.append(
                    f"Node {nid} identity mismatch: expected {expected} "
                    f"(source={node.source_object_type}:{node.source_object_id})"
                )

        return errors

    def validate_rebuildability(
        self, graph1: ConditionGraph, graph2: ConditionGraph
    ) -> list[str]:
        """Validate that two graphs built from identical inputs are equivalent.

        Checks:
        1. Same set of node IDs.
        2. Same set of edge IDs.
        3. Same node and edge counts.
        """
        errors: list[str] = []

        # Check counts
        if graph1.node_count() != graph2.node_count():
            errors.append(
                f"Node count mismatch: {graph1.node_count()} vs {graph2.node_count()}"
            )
        if graph1.edge_count() != graph2.edge_count():
            errors.append(
                f"Edge count mismatch: {graph1.edge_count()} vs {graph2.edge_count()}"
            )

        # Check node ID sets
        nids1 = set(graph1.nodes.keys())
        nids2 = set(graph2.nodes.keys())
        only_in_1 = nids1 - nids2
        only_in_2 = nids2 - nids1
        if only_in_1:
            errors.append(
                f"Nodes only in graph1: {sorted(only_in_1)}"
            )
        if only_in_2:
            errors.append(
                f"Nodes only in graph2: {sorted(only_in_2)}"
            )

        # Check edge ID sets
        eids1 = set(graph1.edges.keys())
        eids2 = set(graph2.edges.keys())
        only_in_1 = eids1 - eids2
        only_in_2 = eids2 - eids1
        if only_in_1:
            errors.append(
                f"Edges only in graph1: {sorted(only_in_1)}"
            )
        if only_in_2:
            errors.append(
                f"Edges only in graph2: {sorted(only_in_2)}"
            )

        return errors
