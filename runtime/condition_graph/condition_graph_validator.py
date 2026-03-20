"""
Condition Graph Validator — Wave 14 Subsystem 1.

Validates a built condition graph for structural integrity,
acyclicity on sequencing-critical edges, and schema compliance.
"""

from typing import Any

from runtime.condition_graph.condition_graph_builder import (
    SUPPORTED_EDGE_TYPES,
    SUPPORTED_NODE_TYPES,
    SEQUENCING_CRITICAL_EDGE_TYPES,
    NODE_PAIR_RULES,
)


class ConditionGraphValidationError(Exception):
    """Raised when graph validation fails."""


def validate_condition_graph(graph: dict[str, Any]) -> list[str]:
    """
    Validate a condition graph. Returns list of validation errors.
    Empty list means valid.
    Fails closed: any structural issue is an error.
    """
    errors: list[str] = []

    # Required metadata
    for field in ("graph_id", "source_refs", "build_timestamp", "contract_version", "checksum"):
        if field not in graph:
            errors.append(f"Missing required metadata field: {field}")

    if "nodes" not in graph:
        errors.append("Missing 'nodes' array.")
        return errors
    if "edges" not in graph:
        errors.append("Missing 'edges' array.")
        return errors

    # Validate nodes
    node_ids: set[str] = set()
    node_types: dict[str, str] = {}
    for node in graph["nodes"]:
        nid = node.get("node_id", "")
        if not nid:
            errors.append("Node missing 'node_id'.")
            continue
        if nid in node_ids:
            errors.append(f"Duplicate node_id: {nid}")
        node_ids.add(nid)

        ctype = node.get("condition_type", "")
        if ctype not in SUPPORTED_NODE_TYPES:
            errors.append(f"Node {nid}: unsupported condition_type '{ctype}'.")
        node_types[nid] = ctype

    # Validate edges
    edge_ids: set[str] = set()
    for edge in graph["edges"]:
        eid = edge.get("edge_id", "")
        if eid in edge_ids:
            errors.append(f"Duplicate edge_id: {eid}")
        edge_ids.add(eid)

        etype = edge.get("edge_type", "")
        if etype not in SUPPORTED_EDGE_TYPES:
            errors.append(f"Edge {eid}: unsupported edge_type '{etype}'.")

        src = edge.get("source_node_id", "")
        tgt = edge.get("target_node_id", "")
        if src not in node_ids:
            errors.append(f"Edge {eid}: source_node_id '{src}' not in graph.")
        if tgt not in node_ids:
            errors.append(f"Edge {eid}: target_node_id '{tgt}' not in graph.")

        # Validate node pair rules
        if etype in NODE_PAIR_RULES and src in node_types and tgt in node_types:
            rules = NODE_PAIR_RULES[etype]
            if node_types[src] not in rules["valid_sources"]:
                errors.append(
                    f"Edge {eid}: source type '{node_types[src]}' "
                    f"invalid for edge type '{etype}'."
                )
            if node_types[tgt] not in rules["valid_targets"]:
                errors.append(
                    f"Edge {eid}: target type '{node_types[tgt]}' "
                    f"invalid for edge type '{etype}'."
                )

    # DAG check on sequencing-critical edges
    seq_edges = [
        e for e in graph["edges"]
        if e.get("sequencing_critical", False)
        or e.get("edge_type", "") in SEQUENCING_CRITICAL_EDGE_TYPES
    ]
    if seq_edges:
        cycle_error = _check_acyclic(seq_edges, node_ids)
        if cycle_error:
            errors.append(cycle_error)

    # Deterministic ordering check
    node_id_list = [n["node_id"] for n in graph["nodes"]]
    if node_id_list != sorted(node_id_list):
        errors.append("Nodes are not in deterministic sorted order.")

    edge_id_list = [e["edge_id"] for e in graph["edges"]]
    if edge_id_list != sorted(edge_id_list):
        errors.append("Edges are not in deterministic sorted order.")

    return errors


def _check_acyclic(edges: list[dict[str, Any]], node_ids: set[str]) -> str | None:
    """Check that sequencing-critical edges form a DAG. Returns error string or None."""
    adjacency: dict[str, list[str]] = {nid: [] for nid in node_ids}
    for edge in edges:
        src = edge["source_node_id"]
        tgt = edge["target_node_id"]
        if src in adjacency:
            adjacency[src].append(tgt)

    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {nid: WHITE for nid in node_ids}

    def dfs(node: str) -> bool:
        color[node] = GRAY
        for neighbor in adjacency.get(node, []):
            if color.get(neighbor) == GRAY:
                return True  # cycle
            if color.get(neighbor) == WHITE:
                if dfs(neighbor):
                    return True
        color[node] = BLACK
        return False

    for nid in sorted(node_ids):
        if color[nid] == WHITE:
            if dfs(nid):
                return "Cycle detected in sequencing-critical edges. Graph must be a DAG."
    return None
