"""
Detail Graph Visualizer — Wave 14 Subsystem 4.

Produces navigation summary data from the frozen route graph.
No rendering — output is structured data for UI/downstream consumption.
"""

from typing import Any

from runtime.detail_map.detail_route_query import (
    FROZEN_ROUTES,
    RELATIONSHIP_SEMANTICS,
    get_all_detail_ids,
    get_neighbors,
)


def build_navigation_summary() -> dict[str, Any]:
    """
    Build a navigation summary of the entire detail route graph.
    Returns structured data suitable for UI rendering.
    """
    all_ids = get_all_detail_ids()
    nodes = []
    for did in all_ids:
        neighbors = get_neighbors(did)
        nodes.append({
            "detail_id": did,
            "neighbor_count": len(neighbors),
            "required_relationships": sum(1 for n in neighbors if n["criticality"] == "required"),
            "relationship_types": sorted(set(n["relationship_type"] for n in neighbors)),
        })

    edge_summary = []
    for route in sorted(FROZEN_ROUTES, key=lambda r: (r["source"], r["target"])):
        edge_summary.append({
            "source": route["source"],
            "target": route["target"],
            "type": route["type"],
            "directionality": route["dir"],
            "criticality": route["crit"],
            "semantic": RELATIONSHIP_SEMANTICS.get(route["type"], "Unknown"),
        })

    return {
        "total_details": len(all_ids),
        "total_routes": len(FROZEN_ROUTES),
        "nodes": nodes,
        "edges": edge_summary,
        "relationship_type_counts": _count_by_type(),
    }


def _count_by_type() -> dict[str, int]:
    counts: dict[str, int] = {}
    for route in FROZEN_ROUTES:
        t = route["type"]
        counts[t] = counts.get(t, 0) + 1
    return dict(sorted(counts.items()))
