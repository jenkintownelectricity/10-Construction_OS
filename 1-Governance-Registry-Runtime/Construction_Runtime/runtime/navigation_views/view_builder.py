"""ViewBuilder — transforms navigation query results into view-ready structures.

Read-only transformations. No graph mutation. No traversal logic duplication.
Works on the plain-dict outputs of NavigationQueryEngine.
"""

from __future__ import annotations


class ViewBuilder:
    """Transforms query results into structured view data for map, list, and detail views."""

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Map view
    # ------------------------------------------------------------------

    def build_map_view(self, project_map: dict) -> dict:
        """Transform a project_map (from NavigationQueryEngine.get_project_map)
        into a structured map view.

        Returns::
            {
                "view_type": "map",
                "project_id": str,
                "total_systems": int,
                "state_groups": [
                    {"state": str, "count": int, "systems": [dict, ...]},
                    ...
                ],
                "summary": {"ready": int, "pending": int, "blocked": int, "unknown": int},
            }
        """
        systems = project_map.get("systems", {})
        state_groups: list[dict] = []
        summary: dict[str, int] = {}

        for state in sorted(systems.keys()):
            group_nodes = systems[state]
            state_groups.append({
                "state": state,
                "count": len(group_nodes),
                "systems": group_nodes,
            })
            summary[state] = len(group_nodes)

        return {
            "view_type": "map",
            "project_id": project_map.get("project_id", ""),
            "total_systems": project_map.get("total_systems", 0),
            "state_groups": state_groups,
            "summary": summary,
        }

    # ------------------------------------------------------------------
    # List view
    # ------------------------------------------------------------------

    def build_list_view(self, nodes: list[dict], sort_key: str = "node_id") -> dict:
        """Transform a list of node summaries into a sorted list view.

        Parameters
        ----------
        nodes:
            List of node summary dicts (as returned by NavigationQueryEngine panels).
        sort_key:
            Key to sort by. Must exist in each node dict. Defaults to "node_id".

        Returns::
            {
                "view_type": "list",
                "total": int,
                "sort_key": str,
                "items": [dict, ...],
            }
        """
        sorted_nodes = sorted(
            nodes,
            key=lambda n: n.get(sort_key, ""),
        )

        return {
            "view_type": "list",
            "total": len(sorted_nodes),
            "sort_key": sort_key,
            "items": sorted_nodes,
        }

    # ------------------------------------------------------------------
    # Detail view
    # ------------------------------------------------------------------

    def build_detail_view(self, condition_detail: dict) -> dict:
        """Transform a condition_detail (from NavigationQueryEngine.get_condition_detail)
        into a structured detail view.

        Returns::
            {
                "view_type": "detail",
                "node_id": str,
                "found": bool,
                "header": {"label": ..., "node_type": ..., "readiness_state": ...},
                "panels": {
                    "blockers": [...],
                    "dependencies": [...],
                    "remediation_path": [...],
                    "owner": {...},
                    "next_actions": [...],
                    "downstream_impacts": [...],
                    "upstream_dependencies": [...],
                    "neighbors": [...],
                    "enrichment_edges": [...],
                },
            }
        """
        if not condition_detail.get("found", False):
            return {
                "view_type": "detail",
                "node_id": condition_detail.get("node_id", ""),
                "found": False,
                "header": {},
                "panels": {},
            }

        node = condition_detail.get("node", {})

        header = {
            "label": node.get("label", ""),
            "node_type": node.get("node_type", ""),
            "readiness_state": condition_detail.get("readiness_state", "unknown"),
            "state_summary": node.get("state_summary", {}),
        }

        panels = {
            "blockers": condition_detail.get("blockers", []),
            "dependencies": condition_detail.get("dependencies", []),
            "remediation_path": condition_detail.get("remediation_path", []),
            "owner": condition_detail.get("owner", {"owner_node": None, "owner_state": "unknown"}),
            "next_actions": condition_detail.get("next_actions", []),
            "downstream_impacts": condition_detail.get("downstream_impacts", []),
            "upstream_dependencies": condition_detail.get("upstream_dependencies", []),
            "neighbors": condition_detail.get("neighbors", []),
            "enrichment_edges": condition_detail.get("enrichment_edges", []),
        }

        return {
            "view_type": "detail",
            "node_id": condition_detail.get("node_id", ""),
            "found": True,
            "header": header,
            "panels": panels,
        }
