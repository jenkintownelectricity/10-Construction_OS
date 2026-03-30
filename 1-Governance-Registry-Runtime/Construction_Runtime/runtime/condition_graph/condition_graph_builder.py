"""
Condition Graph Builder — Wave 14 Subsystem 1.

Builds a project condition graph from input condition specifications.
Deterministic, fail-closed, contract-first.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

SUPPORTED_NODE_TYPES = frozenset([
    "ROOF_FIELD", "PARAPET", "EDGE", "DRAIN",
    "SCUPPER", "CURB", "PIPE_PENETRATION", "EXPANSION_JOINT",
])

SUPPORTED_EDGE_TYPES = frozenset([
    "adjacent_to", "drains_to", "penetrates",
    "terminates_at", "intersects", "requires_continuity_with",
])

SEQUENCING_CRITICAL_EDGE_TYPES = frozenset(["drains_to", "terminates_at"])

NODE_PAIR_RULES: dict[str, dict[str, list[str]]] = {
    "drains_to": {
        "valid_sources": ["ROOF_FIELD", "PARAPET", "EDGE", "CURB"],
        "valid_targets": ["DRAIN", "SCUPPER"],
    },
    "penetrates": {
        "valid_sources": ["PIPE_PENETRATION", "CURB"],
        "valid_targets": ["ROOF_FIELD"],
    },
    "terminates_at": {
        "valid_sources": ["EDGE", "EXPANSION_JOINT"],
        "valid_targets": ["PARAPET", "EDGE", "SCUPPER"],
    },
}

CONTRACT_VERSION = "14.1.0"


class ConditionGraphBuildError(Exception):
    """Raised when graph construction fails validation."""


class ConditionGraphBuilder:
    """Builds a project condition graph from condition specifications."""

    def __init__(self, graph_id: str, source_refs: list[str] | None = None):
        self._graph_id = graph_id
        self._source_refs = source_refs or []
        self._nodes: dict[str, dict[str, Any]] = {}
        self._edges: list[dict[str, Any]] = []
        self._edge_counter = 0

    def add_node(
        self,
        node_id: str,
        condition_type: str,
        label: str,
        position_ref: str = "",
        material_context: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if condition_type not in SUPPORTED_NODE_TYPES:
            raise ConditionGraphBuildError(
                f"Unsupported condition type '{condition_type}'. "
                f"Supported: {sorted(SUPPORTED_NODE_TYPES)}"
            )
        if node_id in self._nodes:
            raise ConditionGraphBuildError(
                f"Duplicate node ID '{node_id}'."
            )
        node: dict[str, Any] = {
            "node_id": node_id,
            "condition_type": condition_type,
            "label": label,
            "position_ref": position_ref,
            "metadata": metadata or {},
        }
        if material_context is not None:
            node["material_context"] = material_context
        self._nodes[node_id] = node

    def add_edge(
        self,
        source_node_id: str,
        target_node_id: str,
        edge_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        if edge_type not in SUPPORTED_EDGE_TYPES:
            raise ConditionGraphBuildError(
                f"Unsupported edge type '{edge_type}'. "
                f"Supported: {sorted(SUPPORTED_EDGE_TYPES)}"
            )
        if source_node_id not in self._nodes:
            raise ConditionGraphBuildError(
                f"Source node '{source_node_id}' not found in graph."
            )
        if target_node_id not in self._nodes:
            raise ConditionGraphBuildError(
                f"Target node '{target_node_id}' not found in graph."
            )

        # Validate node pair rules
        if edge_type in NODE_PAIR_RULES:
            rules = NODE_PAIR_RULES[edge_type]
            source_type = self._nodes[source_node_id]["condition_type"]
            target_type = self._nodes[target_node_id]["condition_type"]
            if source_type not in rules["valid_sources"]:
                raise ConditionGraphBuildError(
                    f"Edge type '{edge_type}' does not support source "
                    f"condition type '{source_type}'. "
                    f"Valid sources: {rules['valid_sources']}"
                )
            if target_type not in rules["valid_targets"]:
                raise ConditionGraphBuildError(
                    f"Edge type '{edge_type}' does not support target "
                    f"condition type '{target_type}'. "
                    f"Valid targets: {rules['valid_targets']}"
                )

        self._edge_counter += 1
        edge_id = f"CE-{self._edge_counter:06d}"
        sequencing_critical = edge_type in SEQUENCING_CRITICAL_EDGE_TYPES

        edge: dict[str, Any] = {
            "edge_id": edge_id,
            "source_node_id": source_node_id,
            "target_node_id": target_node_id,
            "edge_type": edge_type,
            "sequencing_critical": sequencing_critical,
        }
        if metadata:
            edge["metadata"] = metadata
        self._edges.append(edge)
        return edge_id

    def build(self) -> dict[str, Any]:
        """Build and return the complete condition graph. Fails closed on invalid state."""
        if not self._nodes:
            raise ConditionGraphBuildError("Cannot build empty graph — no nodes added.")

        # Deterministic ordering
        sorted_nodes = sorted(self._nodes.values(), key=lambda n: n["node_id"])
        sorted_edges = sorted(self._edges, key=lambda e: e["edge_id"])

        graph_content = {
            "graph_id": self._graph_id,
            "source_refs": sorted(self._source_refs),
            "build_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "contract_version": CONTRACT_VERSION,
            "nodes": sorted_nodes,
            "edges": sorted_edges,
        }

        content_for_checksum = json.dumps(
            {"nodes": sorted_nodes, "edges": sorted_edges},
            sort_keys=True,
            separators=(",", ":"),
        )
        graph_content["checksum"] = hashlib.sha256(
            content_for_checksum.encode("utf-8")
        ).hexdigest()

        return graph_content
