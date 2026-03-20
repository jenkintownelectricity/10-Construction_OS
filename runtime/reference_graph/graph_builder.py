"""
Graph Builder — Wave 17A Construction Reference Graph.

Builds a complete reference graph from registration bundles.
Atomic bundle writes: if any node or edge in a bundle fails, the whole bundle fails.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from runtime.reference_graph.identity_allocator import IdentityAllocator
from runtime.reference_graph.node_registry import NodeRegistry, NodeRegistrationError
from runtime.reference_graph.edge_registry import EdgeRegistry, EdgeRegistrationError


CONTRACT_VERSION = "17A.1.0"
WAVE = "17A"


class GraphBuildError(Exception):
    """Raised when graph construction fails. Fail closed."""


class ReferenceGraphBuilder:
    """Builds a Construction Reference Graph from registration bundles.

    Supports three write modes:
    - full_rebuild: rebuild graph from authoritative source set
    - incremental_append: add new valid nodes/edges
    - idempotent_replay: repeated identical writes return existing state
    """

    def __init__(self) -> None:
        self._allocator = IdentityAllocator()
        self._node_registry = NodeRegistry(self._allocator)
        self._edge_registry = EdgeRegistry(self._node_registry)
        self._build_count = 0

    @property
    def node_registry(self) -> NodeRegistry:
        return self._node_registry

    @property
    def edge_registry(self) -> EdgeRegistry:
        return self._edge_registry

    @property
    def allocator(self) -> IdentityAllocator:
        return self._allocator

    def register_bundle(
        self,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
        mode: str = "incremental_append",
    ) -> dict[str, Any]:
        """Register a bundle of nodes and edges atomically.

        Args:
            nodes: List of node registration dicts.
            edges: List of edge registration dicts.
            mode: Write mode (full_rebuild, incremental_append, idempotent_replay).

        Returns:
            Bundle result with registered nodes and edges.

        Raises:
            GraphBuildError if any validation fails (atomic — whole bundle fails).
        """
        if mode not in ("full_rebuild", "incremental_append", "idempotent_replay"):
            raise GraphBuildError(f"Invalid write mode '{mode}'.")

        if mode == "full_rebuild":
            self._allocator.reset()
            self._node_registry = NodeRegistry(self._allocator)
            self._edge_registry = EdgeRegistry(self._node_registry)

        # Pre-validate all nodes before committing any
        validated_nodes: list[dict[str, Any]] = []
        for node_spec in nodes:
            try:
                self._validate_node_spec(node_spec)
                validated_nodes.append(node_spec)
            except (NodeRegistrationError, KeyError) as e:
                raise GraphBuildError(
                    f"Bundle validation failed on node: {e}"
                ) from e

        # Pre-validate edge specs (structural check only — node existence checked after registration)
        for edge_spec in edges:
            try:
                self._validate_edge_spec(edge_spec)
            except (EdgeRegistrationError, KeyError) as e:
                raise GraphBuildError(
                    f"Bundle validation failed on edge: {e}"
                ) from e

        # Register nodes
        registered_nodes: list[dict[str, Any]] = []
        for node_spec in validated_nodes:
            try:
                node = self._node_registry.register(
                    object_type=node_spec["object_type"],
                    scope=node_spec["scope"],
                    partition=node_spec["partition"],
                    source_system=node_spec["source_system"],
                    source_reference=node_spec["source_reference"],
                    authority_type=node_spec["authority_type"],
                    status=node_spec.get("status", "active"),
                    metadata=node_spec.get("metadata"),
                )
                registered_nodes.append(node)
            except NodeRegistrationError as e:
                if mode == "idempotent_replay":
                    existing = self._node_registry.get_by_fingerprint(
                        node_spec["source_system"],
                        node_spec["source_reference"],
                        node_spec["object_type"],
                        node_spec["scope"],
                    )
                    if existing:
                        registered_nodes.append(existing)
                        continue
                raise GraphBuildError(
                    f"Bundle node registration failed: {e}"
                ) from e

        # Register edges
        registered_edges: list[dict[str, Any]] = []
        for edge_spec in edges:
            try:
                edge = self._edge_registry.register(
                    relation_type=edge_spec["relation_type"],
                    from_id=edge_spec["from_id"],
                    to_id=edge_spec["to_id"],
                    source_basis=edge_spec.get("source_basis", ""),
                    is_advisory=edge_spec.get("is_advisory", False),
                    metadata=edge_spec.get("metadata"),
                )
                registered_edges.append(edge)
            except EdgeRegistrationError as e:
                if mode == "idempotent_replay":
                    edge_id = EdgeRegistry.compute_edge_id(
                        edge_spec["relation_type"],
                        edge_spec["from_id"],
                        edge_spec["to_id"],
                    )
                    existing = self._edge_registry.get(edge_id)
                    if existing:
                        registered_edges.append(existing)
                        continue
                raise GraphBuildError(
                    f"Bundle edge registration failed: {e}"
                ) from e

        self._build_count += 1

        return {
            "bundle_id": self._build_count,
            "mode": mode,
            "nodes_registered": len(registered_nodes),
            "edges_registered": len(registered_edges),
            "nodes": registered_nodes,
            "edges": registered_edges,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    def build(self) -> dict[str, Any]:
        """Build and return the complete reference graph state."""
        nodes = self._node_registry.list_nodes()
        edges = self._edge_registry.list_edges()

        content = json.dumps(
            {"nodes": nodes, "edges": edges},
            sort_keys=True, separators=(",", ":"),
            default=str,
        )
        checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()

        return {
            "version": CONTRACT_VERSION,
            "wave": WAVE,
            "build_timestamp": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges,
            "checksum": checksum,
        }

    @staticmethod
    def _validate_node_spec(spec: dict[str, Any]) -> None:
        required = ["object_type", "scope", "partition", "source_system",
                     "source_reference", "authority_type"]
        for field in required:
            if field not in spec:
                raise NodeRegistrationError(
                    f"Missing required field '{field}' in node spec."
                )
        from runtime.reference_graph.identity_allocator import VALID_OBJECT_TYPES
        if spec["object_type"] not in VALID_OBJECT_TYPES:
            raise NodeRegistrationError(
                f"Invalid object_type '{spec['object_type']}' in node spec."
            )
        from runtime.reference_graph.node_registry import VALID_PARTITIONS
        if spec["partition"] not in VALID_PARTITIONS:
            raise NodeRegistrationError(
                f"Invalid partition '{spec['partition']}' in node spec."
            )

    @staticmethod
    def _validate_edge_spec(spec: dict[str, Any]) -> None:
        required = ["relation_type", "from_id", "to_id"]
        for field in required:
            if field not in spec:
                raise EdgeRegistrationError(
                    f"Missing required field '{field}' in edge spec."
                )
