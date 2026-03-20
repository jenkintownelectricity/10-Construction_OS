"""
Detail Navigation Contract — Wave 15.

Defines the contract surface for the detail navigation subsystem.
"""

from typing import Any

CONTRACT_VERSION = "15.1.0"
WAVE = "15"
SUBSYSTEM = "detail_navigation"

UPSTREAM_RELATIONSHIP_TYPES = frozenset(["depends_on", "requires_continuity_with"])
DOWNSTREAM_RELATIONSHIP_TYPES = frozenset(["blocks", "follows"])
TRANSITION_RELATIONSHIP_TYPES = frozenset(["terminates_into", "precedes", "follows"])
ADJACENCY_RELATIONSHIP_TYPES = frozenset(["adjacent_to", "overlaps_with"])


class DetailNavigationContract:
    """Contract definition for detail navigation operations."""

    @staticmethod
    def operations() -> dict[str, dict[str, Any]]:
        return {
            "find_related_details": {
                "input": "detail_id: str",
                "output": "list[dict] — related details with relationship metadata",
                "failure": "Unknown detail_id returns empty list",
                "deterministic": True,
            },
            "resolve_neighbors": {
                "input": "detail_id: str",
                "output": "list[dict] — immediate neighbor details",
                "failure": "Unknown detail_id returns empty list",
                "deterministic": True,
            },
            "resolve_upstream_dependencies": {
                "input": "detail_id: str",
                "output": "list[dict] — upstream dependency details",
                "failure": "Unknown detail_id returns empty list",
                "deterministic": True,
            },
            "resolve_downstream_paths": {
                "input": "detail_id: str",
                "output": "list[dict] — downstream detail paths",
                "failure": "Unknown detail_id returns empty list",
                "deterministic": True,
            },
            "resolve_installation_transitions": {
                "input": "detail_id: str",
                "output": "list[dict] — installation transition details",
                "failure": "Unknown detail_id returns empty list",
                "deterministic": True,
            },
            "resolve_navigation_path": {
                "input": "detail_a: str, detail_b: str",
                "output": "dict — path with steps and relationship chain",
                "failure": "No path returns path_exists=False",
                "deterministic": True,
            },
        }
