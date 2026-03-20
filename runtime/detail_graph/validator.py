"""
Detail Graph Validator — Wave 15.

Validates a built detail graph for structural integrity.
"""

from typing import Any

from runtime.detail_graph.graph_builder import DetailGraph
from runtime.detail_graph.contract import VALID_RELATIONSHIP_TYPES


class DetailGraphValidationError(Exception):
    """Raised when graph validation fails."""


def validate_detail_graph(graph: DetailGraph) -> dict[str, Any]:
    """
    Validate a detail graph instance.

    Returns:
        Validation report dict.

    Raises:
        DetailGraphValidationError on critical failures.
    """
    checks: list[dict[str, Any]] = []

    # Check 1: Non-empty
    checks.append({
        "check": "non_empty_nodes",
        "passed": len(graph.nodes) > 0,
        "detail": f"{len(graph.nodes)} nodes present.",
    })

    # Check 2: All edges reference valid nodes
    invalid_refs = []
    for edge in graph.edges:
        if edge["source_detail_id"] not in graph.nodes:
            invalid_refs.append(edge["source_detail_id"])
        if edge["target_detail_id"] not in graph.nodes:
            invalid_refs.append(edge["target_detail_id"])
    checks.append({
        "check": "edge_node_references",
        "passed": len(invalid_refs) == 0,
        "detail": f"Invalid refs: {invalid_refs}" if invalid_refs else "All edges reference valid nodes.",
    })

    # Check 3: All edge types valid
    invalid_types = [
        e["relationship_type"] for e in graph.edges
        if e["relationship_type"] not in VALID_RELATIONSHIP_TYPES
    ]
    checks.append({
        "check": "edge_type_validity",
        "passed": len(invalid_types) == 0,
        "detail": f"Invalid types: {invalid_types}" if invalid_types else "All edge types valid.",
    })

    # Check 4: Deterministic edge ordering
    sorted_edges = sorted(graph.edges, key=lambda e: (
        e["source_detail_id"], e["target_detail_id"], e["relationship_type"]
    ))
    edges_ordered = graph.edges == sorted_edges
    checks.append({
        "check": "deterministic_edge_ordering",
        "passed": edges_ordered,
        "detail": "Edges in deterministic order." if edges_ordered else "Edge ordering violation.",
    })

    # Check 5: Adjacency consistency
    for detail_id in graph.nodes:
        out_neighbors = set(graph.adjacency_out.get(detail_id, []))
        in_neighbors = set(graph.adjacency_in.get(detail_id, []))
        all_adj = out_neighbors | in_neighbors
        for n in all_adj:
            if n not in graph.nodes:
                checks.append({
                    "check": "adjacency_consistency",
                    "passed": False,
                    "detail": f"Adjacency references unknown node: {n}",
                })
                raise DetailGraphValidationError(f"Adjacency references unknown node: {n}")

    checks.append({
        "check": "adjacency_consistency",
        "passed": True,
        "detail": "All adjacency references valid.",
    })

    # Check 6: Checksum present
    checks.append({
        "check": "checksum_present",
        "passed": bool(graph.checksum),
        "detail": "Checksum present." if graph.checksum else "No checksum.",
    })

    all_passed = all(c["passed"] for c in checks)
    if not all_passed:
        failed = [c for c in checks if not c["passed"]]
        raise DetailGraphValidationError(
            f"Graph validation failed: {[c['check'] for c in failed]}"
        )

    return {
        "subsystem": "detail_graph",
        "wave": "15",
        "status": "PASS",
        "checks": checks,
        "summary": {
            "total_checks": len(checks),
            "passed": sum(1 for c in checks if c["passed"]),
            "failed": sum(1 for c in checks if not c["passed"]),
        },
    }
