"""
Detail Route Query — Wave 14 Subsystem 4.

Queries the frozen detail route graph for relationships between detail families.
Read-only access to the kernel route graph.
"""

from typing import Any

# Frozen route graph from Construction_Kernel Wave 13A
FROZEN_ROUTES: list[dict[str, Any]] = [
    {"source": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01", "target": "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01", "type": "adjacent_to", "dir": "bidirectional", "crit": "recommended"},
    {"source": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01", "target": "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01", "type": "adjacent_to", "dir": "bidirectional", "crit": "informational"},
    {"source": "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01", "target": "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01", "type": "requires_continuity_with", "dir": "bidirectional", "crit": "required"},
    {"source": "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01", "target": "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01", "type": "requires_continuity_with", "dir": "bidirectional", "crit": "required"},
    {"source": "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01", "target": "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01", "type": "terminates_into", "dir": "directional", "crit": "required"},
    {"source": "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01", "target": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01", "type": "terminates_into", "dir": "directional", "crit": "required"},
    {"source": "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01", "target": "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01", "type": "terminates_into", "dir": "directional", "crit": "required"},
    {"source": "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01", "target": "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01", "type": "adjacent_to", "dir": "bidirectional", "crit": "recommended"},
    {"source": "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01", "target": "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01", "type": "adjacent_to", "dir": "bidirectional", "crit": "informational"},
    {"source": "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01", "target": "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01", "type": "substitutable_with", "dir": "bidirectional", "crit": "informational"},
    {"source": "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01", "target": "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01", "type": "overlaps_with", "dir": "bidirectional", "crit": "informational"},
]

RELATIONSHIP_SEMANTICS: dict[str, str] = {
    "depends_on": "Source cannot proceed without target being in place.",
    "adjacent_to": "Spatially proximate or sharing boundaries.",
    "blocks": "Source prevents target from proceeding.",
    "requires_continuity_with": "Both require unbroken membrane/barrier continuity.",
    "substitutable_with": "Alternative approaches for the same condition.",
    "terminates_into": "Source ends at or into target.",
    "overlaps_with": "Physical overlap zones between details.",
    "precedes": "Source must be installed before target.",
    "follows": "Source is installed after target.",
}


def get_neighbors(detail_id: str) -> list[dict[str, Any]]:
    """Get all neighbors (direct relationships) for a detail ID."""
    neighbors: list[dict[str, Any]] = []
    for route in FROZEN_ROUTES:
        if route["source"] == detail_id:
            neighbors.append({
                "detail_id": route["target"],
                "relationship_type": route["type"],
                "direction": "outgoing",
                "criticality": route["crit"],
            })
        elif route["target"] == detail_id and route["dir"] == "bidirectional":
            neighbors.append({
                "detail_id": route["source"],
                "relationship_type": route["type"],
                "direction": "incoming_bidirectional",
                "criticality": route["crit"],
            })
    return sorted(neighbors, key=lambda n: (n["detail_id"], n["relationship_type"]))


def get_routes_by_type(relationship_type: str) -> list[dict[str, Any]]:
    """Get all routes of a specific relationship type."""
    return sorted(
        [r for r in FROZEN_ROUTES if r["type"] == relationship_type],
        key=lambda r: (r["source"], r["target"]),
    )


def get_required_relationships(detail_id: str) -> list[dict[str, Any]]:
    """Get all 'required' criticality relationships for a detail."""
    return [
        n for n in get_neighbors(detail_id)
        if n["criticality"] == "required"
    ]


def get_all_detail_ids() -> list[str]:
    """Get all unique detail IDs referenced in the route graph."""
    ids: set[str] = set()
    for route in FROZEN_ROUTES:
        ids.add(route["source"])
        ids.add(route["target"])
    return sorted(ids)
