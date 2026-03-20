"""
Update Engine — Wave 17A Construction Reference Graph.

Enforces transaction bundle validation for all graph writes.
Supported modes: full_rebuild, incremental_append, idempotent_replay.
No partial commits allowed.
"""

from typing import Any

from runtime.reference_graph.graph_builder import ReferenceGraphBuilder, GraphBuildError
from runtime.reference_graph.validator import GraphValidator
from runtime.reference_graph.lineage_engine import LineageEngine


class UpdateError(Exception):
    """Raised when a graph update fails."""


class UpdateEngine:
    """Manages atomic graph updates with validation."""

    def __init__(self, builder: ReferenceGraphBuilder) -> None:
        self._builder = builder
        self._lineage = LineageEngine(
            builder.node_registry,
            builder.edge_registry,
        )
        self._validator = GraphValidator(
            builder.node_registry,
            builder.edge_registry,
            self._lineage,
        )
        self._update_log: list[dict[str, Any]] = []

    @property
    def builder(self) -> ReferenceGraphBuilder:
        return self._builder

    @property
    def lineage_engine(self) -> LineageEngine:
        return self._lineage

    @property
    def validator(self) -> GraphValidator:
        return self._validator

    def apply_update(
        self,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
        mode: str = "incremental_append",
        validate_after: bool = True,
    ) -> dict[str, Any]:
        """Apply an atomic update bundle.

        Args:
            nodes: Node specs to register.
            edges: Edge specs to register.
            mode: Write mode.
            validate_after: Whether to run validation after update.

        Returns:
            Update result with validation report if requested.

        Raises:
            UpdateError if bundle fails validation.
        """
        try:
            result = self._builder.register_bundle(nodes, edges, mode=mode)
        except GraphBuildError as e:
            raise UpdateError(f"Update failed: {e}") from e

        validation_report = None
        if validate_after:
            validation_report = self._validator.validate_reference_graph()
            if not validation_report["valid"]:
                raise UpdateError(
                    f"Post-update validation failed: "
                    f"{validation_report['total_errors']} errors"
                )

        update_entry = {
            "update_id": len(self._update_log) + 1,
            "mode": mode,
            "nodes_registered": result["nodes_registered"],
            "edges_registered": result["edges_registered"],
            "validation": validation_report,
        }
        self._update_log.append(update_entry)

        return update_entry

    def full_rebuild(
        self,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Perform a full graph rebuild from authoritative source set."""
        return self.apply_update(nodes, edges, mode="full_rebuild")

    def incremental_append(
        self,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Append new nodes/edges without mutating history."""
        return self.apply_update(nodes, edges, mode="incremental_append")

    def idempotent_replay(
        self,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Replay identical writes — returns existing state if identical."""
        return self.apply_update(nodes, edges, mode="idempotent_replay")

    def get_update_log(self) -> list[dict[str, Any]]:
        """Return the update history."""
        return list(self._update_log)
