"""
Lineage Engine — Wave 17A Construction Reference Graph.

Traces and validates lineage chains through the reference graph.
Required lineage classes:
  canonical_to_variant, variant_to_manifest, manifest_to_render,
  render_to_artifact, artifact_to_markup, artifact_or_project_to_observation.
"""

from typing import Any

from runtime.reference_graph.node_registry import NodeRegistry
from runtime.reference_graph.edge_registry import EdgeRegistry, LINEAGE_RELATION_TYPES


# Required lineage chain classes
REQUIRED_LINEAGE_CLASSES = {
    "canonical_to_variant": {
        "from_type": "DETAIL",
        "to_type": "VARIANT",
        "relation": "derived_from",
        "direction": "reverse",  # VARIANT derived_from DETAIL
    },
    "variant_to_manifest": {
        "from_type": "VARIANT",
        "to_type": "MANIFEST",
        "relation": "produced_by",
        "direction": "reverse",  # MANIFEST produced_by VARIANT (implicit through instruction set)
    },
    "manifest_to_render": {
        "from_type": "MANIFEST",
        "to_type": "RENDER_JOB",
        "relation": "produced_by",
        "direction": "reverse",
    },
    "render_to_artifact": {
        "from_type": "RENDER_JOB",
        "to_type": "DRAWING",
        "relation": "rendered_from",
        "direction": "reverse",  # DRAWING rendered_from RENDER_JOB
    },
    "artifact_to_markup": {
        "from_type": "DRAWING",
        "to_type": "MARKUP",
        "relation": "annotates",
        "direction": "reverse",  # MARKUP annotates DRAWING
    },
    "artifact_or_project_to_observation": {
        "from_type": "PROJECT",
        "to_type": "OBSERVATION",
        "relation": "observed_in",
        "direction": "reverse",  # OBSERVATION observed_in PROJECT
    },
}


class LineageError(Exception):
    """Raised when lineage validation fails."""


class LineageEngine:
    """Traces and validates lineage in the reference graph."""

    def __init__(
        self,
        node_registry: NodeRegistry,
        edge_registry: EdgeRegistry,
    ) -> None:
        self._nodes = node_registry
        self._edges = edge_registry

    def trace_lineage(self, graph_id: str) -> list[dict[str, Any]]:
        """Trace the full lineage chain for a node (upstream ancestors).

        Returns list of nodes in lineage order (root first).
        """
        node = self._nodes.get(graph_id)
        if not node:
            return []

        chain: list[dict[str, Any]] = []
        visited: set[str] = set()
        self._trace_upstream(graph_id, chain, visited)
        chain.reverse()
        return chain

    def trace_downstream(self, graph_id: str) -> list[dict[str, Any]]:
        """Trace all downstream derived objects from a node."""
        node = self._nodes.get(graph_id)
        if not node:
            return []

        descendants: list[dict[str, Any]] = []
        visited: set[str] = set()
        self._trace_downstream(graph_id, descendants, visited)
        return descendants

    def validate_lineage(self, graph_id: str) -> dict[str, Any]:
        """Validate lineage completeness for a node.

        Returns validation result with any broken links.
        """
        node = self._nodes.get(graph_id)
        if not node:
            return {
                "valid": False,
                "graph_id": graph_id,
                "errors": ["Node not found"],
            }

        chain = self.trace_lineage(graph_id)
        errors: list[str] = []

        # Check for broken lineage (unresolved references)
        for link in chain:
            if link.get("authority_type") == "external_unverified":
                errors.append(
                    f"Unverified external lineage at {link['graph_id']}"
                )

        return {
            "valid": len(errors) == 0,
            "graph_id": graph_id,
            "chain_length": len(chain),
            "chain": [n["graph_id"] for n in chain],
            "errors": errors,
        }

    def get_lineage_class(
        self, from_id: str, to_id: str,
    ) -> str | None:
        """Determine the lineage class for an edge between two nodes."""
        from_node = self._nodes.get(from_id)
        to_node = self._nodes.get(to_id)
        if not from_node or not to_node:
            return None

        for class_name, spec in REQUIRED_LINEAGE_CLASSES.items():
            if spec["direction"] == "reverse":
                if (
                    to_node["object_type"] == spec["from_type"]
                    and from_node["object_type"] == spec["to_type"]
                ):
                    return class_name
            else:
                if (
                    from_node["object_type"] == spec["from_type"]
                    and to_node["object_type"] == spec["to_type"]
                ):
                    return class_name
        return None

    def _trace_upstream(
        self,
        graph_id: str,
        chain: list[dict[str, Any]],
        visited: set[str],
    ) -> None:
        """Recursively trace upstream lineage."""
        if graph_id in visited:
            return
        visited.add(graph_id)

        node = self._nodes.get(graph_id)
        if not node:
            return

        chain.append(node)

        # Find lineage edges pointing from this node
        outgoing = self._edges.get_edges_from(graph_id)
        for edge in outgoing:
            if edge["relation_type"] in LINEAGE_RELATION_TYPES:
                self._trace_upstream(edge["to_id"], chain, visited)

    def _trace_downstream(
        self,
        graph_id: str,
        descendants: list[dict[str, Any]],
        visited: set[str],
    ) -> None:
        """Recursively trace downstream lineage."""
        if graph_id in visited:
            return
        visited.add(graph_id)

        # Find lineage edges pointing to this node
        incoming = self._edges.get_edges_to(graph_id)
        for edge in incoming:
            if edge["relation_type"] in LINEAGE_RELATION_TYPES:
                child = self._nodes.get(edge["from_id"])
                if child and edge["from_id"] not in visited:
                    descendants.append(child)
                    self._trace_downstream(edge["from_id"], descendants, visited)
