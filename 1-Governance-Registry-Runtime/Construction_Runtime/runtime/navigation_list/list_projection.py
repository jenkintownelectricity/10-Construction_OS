"""ListProjection — projects a ConditionGraph into flat/sorted node lists.

Read-only. Consumes graph nodes directly. No traversal logic duplication.
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph


def _node_summary(node) -> dict:
    return {
        "node_id": node.graph_node_id,
        "node_type": node.node_type,
        "label": node.label,
        "state_summary": dict(node.state_summary),
        "is_enrichment_derived": node.metadata.get("is_enrichment_derived", False),
    }


class ListProjection:
    """Projects graph nodes into flat lists with optional type filtering and sorting."""

    def __init__(self) -> None:
        pass

    def project_flat_list(
        self, graph: ConditionGraph, node_type: str | None = None
    ) -> list[dict]:
        """Project all nodes (or filtered by node_type) into a flat list of summaries.

        Parameters
        ----------
        graph:
            The ConditionGraph to project.
        node_type:
            Optional node type filter. If None, all nodes are included.

        Returns
        -------
        list[dict]
            List of node summary dicts sorted by node_id for determinism.
        """
        nodes = graph.nodes.values()
        if node_type is not None:
            nodes = [n for n in nodes if n.node_type == node_type]
        else:
            nodes = list(nodes)

        summaries = [_node_summary(n) for n in nodes]
        return sorted(summaries, key=lambda s: s["node_id"])

    def project_sorted_list(
        self,
        graph: ConditionGraph,
        sort_key: str,
        ascending: bool = True,
    ) -> list[dict]:
        """Project all nodes into a list sorted by a given key.

        Parameters
        ----------
        graph:
            The ConditionGraph to project.
        sort_key:
            Key to sort by. Supports top-level keys ("node_id", "node_type",
            "label") and state_summary sub-keys via "state_summary.<key>".
        ascending:
            Sort direction. True for ascending, False for descending.

        Returns
        -------
        list[dict]
            Sorted list of node summary dicts.
        """
        summaries = [_node_summary(n) for n in graph.nodes.values()]

        if sort_key.startswith("state_summary."):
            sub_key = sort_key[len("state_summary."):]
            key_fn = lambda s: str(s.get("state_summary", {}).get(sub_key, ""))
        else:
            key_fn = lambda s: str(s.get(sort_key, ""))

        return sorted(summaries, key=key_fn, reverse=not ascending)
