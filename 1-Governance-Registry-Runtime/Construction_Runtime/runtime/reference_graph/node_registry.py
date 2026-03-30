"""
Node Registry — Wave 17A Construction Reference Graph.

Registers and manages all nodes in the reference graph.
Every node must include identity, type, scope, partition, source info,
authority type, timestamp, and status.
"""

from datetime import datetime, timezone
from typing import Any

from runtime.reference_graph.identity_allocator import (
    VALID_OBJECT_TYPES,
    IdentityAllocator,
    IdentityAllocationError,
)

# Valid partitions
VALID_PARTITIONS = frozenset([
    "global_kernel_partition",
    "global_runtime_partition",
    "project_partition",
    "artifact_partition",
    "observation_partition",
])

# Valid authority types
VALID_AUTHORITY_TYPES = frozenset([
    "kernel_canonical",
    "runtime_derived",
    "project_instance",
    "external_unverified",
])

# Valid lifecycle states
VALID_STATUSES = frozenset([
    "active",
    "superseded",
    "archived",
    "invalid",
])

# Kernel object types that must stay in global_kernel_partition
KERNEL_OBJECT_TYPES = frozenset(["DETAIL"])

# Object types that must stay in specific partitions
PARTITION_RULES: dict[str, set[str]] = {
    "global_kernel_partition": {"DETAIL"},
    "observation_partition": {"OBSERVATION"},
    "artifact_partition": {"DRAWING", "PDF", "DXF", "SVG", "ARTIFACT", "ARTIFACT_REGION", "PAGE_REFERENCE"},
}


class NodeRegistrationError(Exception):
    """Raised when node registration fails. Fail closed."""


class NodeRegistry:
    """Registry for all reference graph nodes."""

    def __init__(self, allocator: IdentityAllocator) -> None:
        self._allocator = allocator
        self._nodes: dict[str, dict[str, Any]] = {}
        self._fingerprint_to_id: dict[str, str] = {}

    def register(
        self,
        object_type: str,
        scope: str,
        partition: str,
        source_system: str,
        source_reference: str,
        authority_type: str,
        status: str = "active",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Register a new node in the reference graph.

        Returns:
            The registered node dict.

        Raises:
            NodeRegistrationError on validation failures.
        """
        if object_type not in VALID_OBJECT_TYPES:
            raise NodeRegistrationError(
                f"Invalid object_type '{object_type}'."
            )
        if partition not in VALID_PARTITIONS:
            raise NodeRegistrationError(
                f"Invalid partition '{partition}'. Valid: {sorted(VALID_PARTITIONS)}"
            )
        if authority_type not in VALID_AUTHORITY_TYPES:
            raise NodeRegistrationError(
                f"Invalid authority_type '{authority_type}'."
            )
        if status not in VALID_STATUSES:
            raise NodeRegistrationError(
                f"Invalid status '{status}'. Valid: {sorted(VALID_STATUSES)}"
            )

        self._validate_partition_compliance(object_type, partition)

        payload = metadata or {}

        try:
            graph_id = self._allocator.allocate(
                source_system=source_system,
                source_reference=source_reference,
                object_type=object_type,
                scope=scope,
                payload=payload,
            )
        except IdentityAllocationError as e:
            fingerprint = IdentityAllocator.compute_fingerprint(
                source_system, source_reference, object_type, scope,
            )
            existing_id = self._allocator.lookup(fingerprint)
            if existing_id and existing_id in self._nodes:
                return self._nodes[existing_id]
            raise NodeRegistrationError(str(e)) from e

        node: dict[str, Any] = {
            "graph_id": graph_id,
            "object_type": object_type,
            "scope": scope,
            "partition": partition,
            "source_system": source_system,
            "source_reference": source_reference,
            "authority_type": authority_type,
            "created_timestamp": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "status": status,
            "metadata": payload,
        }

        if graph_id in self._nodes:
            return self._nodes[graph_id]

        self._nodes[graph_id] = node
        fingerprint = IdentityAllocator.compute_fingerprint(
            source_system, source_reference, object_type, scope,
        )
        self._fingerprint_to_id[fingerprint] = graph_id
        return node

    def get(self, graph_id: str) -> dict[str, Any] | None:
        """Retrieve a node by graph_id."""
        return self._nodes.get(graph_id)

    def get_by_fingerprint(
        self,
        source_system: str,
        source_reference: str,
        object_type: str,
        scope: str,
    ) -> dict[str, Any] | None:
        """Retrieve a node by its source fingerprint."""
        fingerprint = IdentityAllocator.compute_fingerprint(
            source_system, source_reference, object_type, scope,
        )
        graph_id = self._fingerprint_to_id.get(fingerprint)
        if graph_id:
            return self._nodes.get(graph_id)
        return None

    def list_nodes(
        self,
        object_type: str | None = None,
        partition: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        """List nodes with optional filters."""
        results = list(self._nodes.values())
        if object_type:
            results = [n for n in results if n["object_type"] == object_type]
        if partition:
            results = [n for n in results if n["partition"] == partition]
        if status:
            results = [n for n in results if n["status"] == status]
        return sorted(results, key=lambda n: n["graph_id"])

    def update_status(self, graph_id: str, new_status: str) -> dict[str, Any]:
        """Update a node's lifecycle status.

        Raises:
            NodeRegistrationError if node not found or invalid status.
        """
        if new_status not in VALID_STATUSES:
            raise NodeRegistrationError(f"Invalid status '{new_status}'.")
        node = self._nodes.get(graph_id)
        if not node:
            raise NodeRegistrationError(f"Node '{graph_id}' not found.")
        if node["status"] == "archived":
            raise NodeRegistrationError(
                f"Cannot change status of archived node '{graph_id}'."
            )
        node["status"] = new_status
        return node

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    def _validate_partition_compliance(
        self, object_type: str, partition: str,
    ) -> None:
        """Validate that object type is allowed in the given partition."""
        for part, allowed_types in PARTITION_RULES.items():
            if object_type in allowed_types and partition != part:
                raise NodeRegistrationError(
                    f"Object type '{object_type}' must be in "
                    f"'{part}', not '{partition}'."
                )
