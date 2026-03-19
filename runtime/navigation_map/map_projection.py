"""MapProjection — projects a ConditionGraph into a hierarchical map structure.

Read-only. Consumes ReadinessRouter for readiness states. Does not duplicate
traversal logic.
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_index import GraphIndex
from runtime.readiness_routing.router import ReadinessRouter


def _node_summary(node) -> dict:
    return {
        "node_id": node.graph_node_id,
        "node_type": node.node_type,
        "label": node.label,
        "state_summary": dict(node.state_summary),
        "is_enrichment_derived": node.metadata.get("is_enrichment_derived", False),
    }


def _readiness_state(rr: ReadinessRouter, node_id: str) -> str:
    """Safely derive readiness state string from ReadinessRouter."""
    try:
        chain = rr.get_readiness_chain(node_id)
        if chain.get("ready"):
            return "ready"
        if chain.get("blockers"):
            return "blocked"
        if not chain.get("dependencies_met"):
            return "pending"
        return "pending"
    except KeyError:
        return "unknown"


def _readiness_summary(states: list[str]) -> dict:
    """Compute a summary of readiness states from a list."""
    summary: dict[str, int] = {}
    for s in states:
        summary[s] = summary.get(s, 0) + 1
    return summary


class MapProjection:
    """Projects a ConditionGraph into a nested hierarchy with readiness summaries.

    Hierarchy: project -> systems -> assemblies -> conditions.
    Each level includes a readiness_summary and node_count.
    """

    def __init__(self) -> None:
        pass

    def project_hierarchy(self, graph: ConditionGraph) -> dict:
        """Project the full graph into a nested hierarchical map.

        Returns::
            {
                "project_id": str,
                "node_count": int,
                "readiness_summary": {"ready": int, ...},
                "systems": [
                    {
                        "node": dict,
                        "readiness_state": str,
                        "readiness_summary": {...},
                        "node_count": int,
                        "assemblies": [
                            {
                                "node": dict,
                                "readiness_state": str,
                                "readiness_summary": {...},
                                "node_count": int,
                                "conditions": [
                                    {"node": dict, "readiness_state": str},
                                    ...
                                ]
                            },
                            ...
                        ]
                    },
                    ...
                ]
            }
        """
        rr = ReadinessRouter(graph)
        index = GraphIndex(graph)

        # Build parent-child relationships from edges.
        # Children are nodes linked FROM a parent via any structural edge.
        children_of: dict[str, list[str]] = {}
        for edge in graph.edges.values():
            children_of.setdefault(edge.from_node_id, []).append(edge.to_node_id)

        # Identify top-level systems: assembly nodes not pointed to by other assemblies
        assembly_ids = set(index.nodes_by_type.get("assembly", []))
        child_assembly_ids: set[str] = set()
        for parent_id in assembly_ids:
            for child_id in children_of.get(parent_id, []):
                if child_id in assembly_ids:
                    child_assembly_ids.add(child_id)

        system_ids = sorted(assembly_ids - child_assembly_ids)

        all_states: list[str] = []

        systems: list[dict] = []
        for sys_id in system_ids:
            sys_node = graph.get_node(sys_id)
            if sys_node is None:
                continue
            sys_state = _readiness_state(rr, sys_id)
            all_states.append(sys_state)

            # Find sub-assemblies under this system
            sub_assembly_ids = [
                cid for cid in children_of.get(sys_id, [])
                if cid in assembly_ids and cid != sys_id
            ]

            assemblies: list[dict] = []
            sys_child_states: list[str] = [sys_state]

            for asm_id in sorted(sub_assembly_ids):
                asm_node = graph.get_node(asm_id)
                if asm_node is None:
                    continue
                asm_state = _readiness_state(rr, asm_id)
                sys_child_states.append(asm_state)
                all_states.append(asm_state)

                # Find conditions under this assembly
                condition_ids = [
                    cid for cid in children_of.get(asm_id, [])
                    if graph.get_node(cid) is not None
                    and graph.get_node(cid).node_type == "condition"
                ]

                conditions: list[dict] = []
                asm_child_states: list[str] = [asm_state]

                for cond_id in sorted(condition_ids):
                    cond_node = graph.get_node(cond_id)
                    if cond_node is None:
                        continue
                    cond_state = _readiness_state(rr, cond_id)
                    asm_child_states.append(cond_state)
                    all_states.append(cond_state)
                    conditions.append({
                        "node": _node_summary(cond_node),
                        "readiness_state": cond_state,
                    })

                assemblies.append({
                    "node": _node_summary(asm_node),
                    "readiness_state": asm_state,
                    "readiness_summary": _readiness_summary(asm_child_states),
                    "node_count": len(conditions),
                    "conditions": conditions,
                })

            systems.append({
                "node": _node_summary(sys_node),
                "readiness_state": sys_state,
                "readiness_summary": _readiness_summary(sys_child_states),
                "node_count": len(assemblies),
                "assemblies": assemblies,
            })

        return {
            "project_id": graph.project_id,
            "node_count": graph.node_count(),
            "readiness_summary": _readiness_summary(all_states),
            "systems": systems,
        }
