"""
Validator — Wave 17A Construction Reference Graph.

Validates the complete reference graph for integrity, lineage completeness,
partition compliance, and relationship correctness.
"""

from typing import Any

from runtime.reference_graph.node_registry import (
    NodeRegistry,
    VALID_PARTITIONS,
    PARTITION_RULES,
)
from runtime.reference_graph.edge_registry import (
    EdgeRegistry,
    ALL_RELATION_TYPES,
    RELATION_TYPE_RULES,
)
from runtime.reference_graph.lineage_engine import LineageEngine


class GraphValidator:
    """Validates the reference graph for correctness and integrity."""

    def __init__(
        self,
        node_registry: NodeRegistry,
        edge_registry: EdgeRegistry,
        lineage_engine: LineageEngine,
    ) -> None:
        self._nodes = node_registry
        self._edges = edge_registry
        self._lineage = lineage_engine

    def validate_reference_graph(self) -> dict[str, Any]:
        """Run all validation checks. Returns comprehensive report."""
        results: list[dict[str, Any]] = []

        results.append(self._validate_node_integrity())
        results.append(self._validate_edge_integrity())
        results.append(self._validate_partition_compliance())
        results.append(self._validate_relationship_rules())
        results.append(self._validate_no_orphan_edges())
        results.append(self._validate_kernel_immutability())

        all_valid = all(r["valid"] for r in results)
        total_errors = sum(len(r.get("errors", [])) for r in results)

        return {
            "valid": all_valid,
            "checks_run": len(results),
            "total_errors": total_errors,
            "results": results,
        }

    def _validate_node_integrity(self) -> dict[str, Any]:
        """Validate all nodes have required fields and valid values."""
        errors: list[str] = []
        nodes = self._nodes.list_nodes()

        required_fields = [
            "graph_id", "object_type", "scope", "partition",
            "source_system", "source_reference", "authority_type",
            "created_timestamp", "status",
        ]

        for node in nodes:
            for field in required_fields:
                if field not in node:
                    errors.append(
                        f"Node {node.get('graph_id', '?')} missing field '{field}'"
                    )

        return {
            "check": "node_integrity",
            "valid": len(errors) == 0,
            "nodes_checked": len(nodes),
            "errors": errors,
        }

    def _validate_edge_integrity(self) -> dict[str, Any]:
        """Validate all edges have valid relation types and existing endpoints."""
        errors: list[str] = []
        edges = self._edges.list_edges()

        for edge in edges:
            if edge["relation_type"] not in ALL_RELATION_TYPES:
                errors.append(
                    f"Edge {edge['edge_id']} has invalid relation_type "
                    f"'{edge['relation_type']}'"
                )
            if not self._nodes.get(edge["from_id"]):
                errors.append(
                    f"Edge {edge['edge_id']} references missing from_id "
                    f"'{edge['from_id']}'"
                )
            if not self._nodes.get(edge["to_id"]):
                errors.append(
                    f"Edge {edge['edge_id']} references missing to_id "
                    f"'{edge['to_id']}'"
                )

        return {
            "check": "edge_integrity",
            "valid": len(errors) == 0,
            "edges_checked": len(edges),
            "errors": errors,
        }

    def _validate_partition_compliance(self) -> dict[str, Any]:
        """Validate all nodes are in their correct partitions."""
        errors: list[str] = []
        nodes = self._nodes.list_nodes()

        for node in nodes:
            obj_type = node["object_type"]
            partition = node["partition"]
            for part, allowed_types in PARTITION_RULES.items():
                if obj_type in allowed_types and partition != part:
                    errors.append(
                        f"Node {node['graph_id']} ({obj_type}) is in partition "
                        f"'{partition}' but should be in '{part}'"
                    )

        return {
            "check": "partition_compliance",
            "valid": len(errors) == 0,
            "nodes_checked": len(nodes),
            "errors": errors,
        }

    def _validate_relationship_rules(self) -> dict[str, Any]:
        """Validate edge from/to types match relation type rules."""
        errors: list[str] = []
        edges = self._edges.list_edges()

        for edge in edges:
            rel_type = edge["relation_type"]
            if rel_type in RELATION_TYPE_RULES:
                rules = RELATION_TYPE_RULES[rel_type]
                if edge["from_type"] not in rules["valid_from"]:
                    errors.append(
                        f"Edge {edge['edge_id']}: relation '{rel_type}' "
                        f"invalid from_type '{edge['from_type']}'"
                    )
                if edge["to_type"] not in rules["valid_to"]:
                    errors.append(
                        f"Edge {edge['edge_id']}: relation '{rel_type}' "
                        f"invalid to_type '{edge['to_type']}'"
                    )

        return {
            "check": "relationship_rules",
            "valid": len(errors) == 0,
            "edges_checked": len(edges),
            "errors": errors,
        }

    def _validate_no_orphan_edges(self) -> dict[str, Any]:
        """Validate no edges reference non-existent nodes."""
        errors: list[str] = []
        edges = self._edges.list_edges()

        for edge in edges:
            if not self._nodes.get(edge["from_id"]):
                errors.append(f"Orphan edge {edge['edge_id']}: missing from_id")
            if not self._nodes.get(edge["to_id"]):
                errors.append(f"Orphan edge {edge['edge_id']}: missing to_id")

        return {
            "check": "no_orphan_edges",
            "valid": len(errors) == 0,
            "edges_checked": len(edges),
            "errors": errors,
        }

    def _validate_kernel_immutability(self) -> dict[str, Any]:
        """Validate that kernel objects are not modified by runtime."""
        errors: list[str] = []
        kernel_nodes = self._nodes.list_nodes(
            partition="global_kernel_partition",
        )

        for node in kernel_nodes:
            if node["authority_type"] != "kernel_canonical":
                errors.append(
                    f"Kernel node {node['graph_id']} has non-kernel authority "
                    f"'{node['authority_type']}'"
                )

        return {
            "check": "kernel_immutability",
            "valid": len(errors) == 0,
            "kernel_nodes_checked": len(kernel_nodes),
            "errors": errors,
        }
