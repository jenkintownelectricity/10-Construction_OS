"""Wave 11A materialization pipeline — orchestrates NodeProjector, EdgeProjector,
GraphValidator, GraphIndex into a full ConditionGraph build."""

from typing import Optional

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph.graph_index import GraphIndex
from runtime.graph_nodes.project_nodes import NodeProjector
from runtime.graph_edges.project_edges import EdgeProjector
from runtime.graph_validation.graph_validator import GraphValidator
from runtime.models.condition_packet import ConditionPacket
from runtime.models.issue_model import IssueRecord, BlockerRecord
from runtime.models.evidence_model import EvidenceRecord
from runtime.models.revision_model import RevisionLineage
from runtime.models.drawing_package_model import DrawingPackage, ExportArtifact


class MaterializationPipeline:
    """Orchestrates the full graph materialization pipeline.

    Stages: NodeProjector -> EdgeProjector -> GraphValidator -> GraphIndex -> ConditionGraph.
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        self.config = config or {}
        self.node_projector = NodeProjector()
        self.edge_projector = EdgeProjector()
        self.validator = GraphValidator(config=self.config)

    def run(
        self,
        project_id: str,
        condition_packets: list[ConditionPacket],
        issues: list[IssueRecord],
        blockers: list[BlockerRecord],
        evidence_records: list[EvidenceRecord],
        revision_lineages: list[RevisionLineage],
        packages: list[DrawingPackage],
        artifacts: list[ExportArtifact],
        pattern_refs: Optional[list[dict]] = None,
    ) -> ConditionGraph:
        """Run the full materialization pipeline and return a ConditionGraph.

        Pipeline:
        1. Project all source objects into nodes (NodeProjector).
        2. Build the graph container and add nodes.
        3. Build source lookup for edge resolution.
        4. Project all edges (EdgeProjector).
        5. Validate the graph (GraphValidator).
        6. Build indexes (GraphIndex).
        7. Attach index and metadata to graph.
        """
        # --- Stage 1: Node projection ---
        graph = ConditionGraph(project_id=project_id)
        seen_node_ids: set[str] = set()

        def _add_node(node: ConditionGraphNode) -> None:
            if node.graph_node_id not in seen_node_ids:
                seen_node_ids.add(node.graph_node_id)
                graph.add_node(node)

        for cp in condition_packets:
            # Condition node
            _add_node(self.node_projector.project_condition_node(cp, project_id))

            # Assembly node
            if cp.assembly_id:
                _add_node(self.node_projector._make_node(
                    project_id, "assembly", "assembly", cp.assembly_id,
                    label=f"assembly:{cp.assembly_id}",
                ))

            # Interface node
            if cp.interface_id:
                _add_node(self.node_projector._make_node(
                    project_id, "interface", "interface", cp.interface_id,
                    label=f"interface:{cp.interface_id}",
                ))

            # Detail node
            if cp.detail_id:
                _add_node(self.node_projector._make_node(
                    project_id, "detail", "detail", cp.detail_id,
                    label=f"detail:{cp.detail_id}",
                ))

            # Owner node — explicit unknown, never omit
            _add_node(self.node_projector.project_owner_node(cp, project_id))

        for issue in issues:
            _add_node(self.node_projector.project_issue_node(issue, project_id))

        for blocker in blockers:
            _add_node(self.node_projector.project_blocker_node(blocker, project_id))

        for ev in evidence_records:
            _add_node(self.node_projector.project_evidence_node(ev, project_id))

        for rl in revision_lineages:
            _add_node(self.node_projector.project_revision_node(rl, project_id))

        for pkg in packages:
            _add_node(self.node_projector.project_package_node(pkg, project_id))

        for art in artifacts:
            _add_node(self.node_projector.project_artifact_node(art, project_id))

        if pattern_refs:
            for pref in pattern_refs:
                if pref.get("pattern_id"):
                    _add_node(
                        self.node_projector.project_pattern_node(pref, project_id)
                    )

        # --- Stage 2: Build source lookup ---
        source_lookup: dict[str, str] = {}
        for node in graph.nodes.values():
            key = f"{node.source_object_type}:{node.source_object_id}"
            source_lookup[key] = node.graph_node_id

        # --- Stage 3: Edge projection ---
        seen_edge_ids: set[str] = set()

        def _add_edge_safe(edge):
            if edge.graph_edge_id not in seen_edge_ids:
                seen_edge_ids.add(edge.graph_edge_id)
                graph.add_edge(edge)

        for cp in condition_packets:
            cond_nid = source_lookup.get(f"condition:{cp.condition_id}")
            if not cond_nid:
                continue

            for edge in self.edge_projector.project_blocker_edges(
                cp, cond_nid, source_lookup, project_id
            ):
                _add_edge_safe(edge)

            for edge in self.edge_projector.project_dependency_edges(
                cp, cond_nid, source_lookup, project_id
            ):
                _add_edge_safe(edge)

            for edge in self.edge_projector.project_evidence_edges(
                cp, cond_nid, source_lookup, project_id
            ):
                _add_edge_safe(edge)

            for edge in self.edge_projector.project_artifact_edges(
                cp, cond_nid, source_lookup, project_id
            ):
                _add_edge_safe(edge)

            for edge in self.edge_projector.project_remediation_edges(
                cp, cond_nid, source_lookup, project_id
            ):
                _add_edge_safe(edge)

            for edge in self.edge_projector.project_classification_edges(
                cp, cond_nid, source_lookup, project_id
            ):
                _add_edge_safe(edge)

            for edge in self.edge_projector.project_ownership_edges(
                cp, cond_nid, source_lookup, project_id
            ):
                _add_edge_safe(edge)

            # Assembly/interface/detail structural edges from condition
            if cp.assembly_id:
                asm_nid = source_lookup.get(f"assembly:{cp.assembly_id}")
                if asm_nid:
                    edge = self.edge_projector._make_edge(
                        "included_in", cond_nid, asm_nid, project_id,
                        source_basis="condition.assembly_id",
                    )
                    _add_edge_safe(edge)

            if cp.interface_id:
                ifc_nid = source_lookup.get(f"interface:{cp.interface_id}")
                if ifc_nid:
                    edge = self.edge_projector._make_edge(
                        "interfaces_with", cond_nid, ifc_nid, project_id,
                        source_basis="condition.interface_id",
                    )
                    _add_edge_safe(edge)

            if cp.detail_id:
                det_nid = source_lookup.get(f"detail:{cp.detail_id}")
                if det_nid:
                    edge = self.edge_projector._make_edge(
                        "implemented_by", cond_nid, det_nid, project_id,
                        source_basis="condition.detail_id",
                    )
                    _add_edge_safe(edge)

        # Issue edges
        for issue in issues:
            for edge in self.edge_projector.project_issue_edges(
                issue, source_lookup, project_id
            ):
                _add_edge_safe(edge)

        # Blocker record edges
        for blocker in blockers:
            for edge in self.edge_projector.project_blocker_record_edges(
                blocker, source_lookup, project_id
            ):
                _add_edge_safe(edge)

        # --- Stage 4: Validation ---
        errors = self.validator.validate(graph)
        if errors:
            graph.metadata["validation_errors"] = errors

        # --- Stage 5: Indexing ---
        index = GraphIndex(graph)
        graph.metadata["_index"] = index

        return graph
