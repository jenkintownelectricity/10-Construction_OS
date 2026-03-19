"""Wave 11A graph materializer — projects source models into the condition graph."""

from typing import Optional

from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph.graph_edge import ConditionGraphEdge
from runtime.graph.condition_graph import ConditionGraph
from runtime.models.condition_packet import ConditionPacket
from runtime.models.issue_model import IssueRecord, BlockerRecord
from runtime.models.evidence_model import EvidenceRecord
from runtime.models.revision_model import RevisionLineage
from runtime.models.drawing_package_model import DrawingPackage, ExportArtifact


class GraphMaterializer:
    """Materializes a ConditionGraph from runtime domain objects.

    Pipeline: node projection -> edge projection -> validation -> indexing.
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        self.config = config or {}

    def materialize(
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
        """Full materialization pipeline: nodes -> edges -> validate -> build graph."""
        nodes = self._project_nodes(
            project_id, condition_packets, issues, blockers,
            evidence_records, revision_lineages, packages, artifacts, pattern_refs,
        )

        graph = ConditionGraph(project_id=project_id)
        for node in nodes:
            graph.add_node(node)

        edges = self._project_edges(project_id, graph.nodes, condition_packets, issues, blockers, pattern_refs)
        for edge in edges:
            graph.add_edge(edge)

        errors = self._validate(graph)
        if errors:
            graph.metadata["validation_errors"] = errors

        return graph

    # ------------------------------------------------------------------
    # Node projection
    # ------------------------------------------------------------------

    def _project_nodes(
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
    ) -> list[ConditionGraphNode]:
        """Project all source objects into graph nodes."""
        nodes: list[ConditionGraphNode] = []
        seen_ids: set[str] = set()

        def _add(node: ConditionGraphNode) -> None:
            if node.graph_node_id not in seen_ids:
                seen_ids.add(node.graph_node_id)
                nodes.append(node)

        for cp in condition_packets:
            # Condition node
            _add(self._make_node(
                project_id, "condition", "condition", cp.condition_id,
                label=f"condition:{cp.condition_id}",
                state_summary={
                    "issue_state": cp.issue_state,
                    "readiness_state": cp.readiness_state,
                    "owner_state": cp.owner_state,
                },
                refs={
                    "blocker_refs": list(cp.blocker_refs),
                    "dependency_refs": list(cp.dependency_refs),
                    "evidence_refs": list(cp.evidence_refs),
                    "artifact_refs": list(cp.artifact_refs),
                    "remediation_candidate_refs": list(cp.remediation_candidate_refs),
                    "pattern_candidate_refs": list(cp.pattern_candidate_refs),
                },
            ))

            # Assembly node
            if cp.assembly_id:
                _add(self._make_node(
                    project_id, "assembly", "assembly", cp.assembly_id,
                    label=f"assembly:{cp.assembly_id}",
                ))

            # Interface node
            if cp.interface_id:
                _add(self._make_node(
                    project_id, "interface", "interface", cp.interface_id,
                    label=f"interface:{cp.interface_id}",
                ))

            # Detail node
            if cp.detail_id:
                _add(self._make_node(
                    project_id, "detail", "detail", cp.detail_id,
                    label=f"detail:{cp.detail_id}",
                ))

            # Owner node — explicit unknown, never omit
            owner_id = cp.condition_id  # owner keyed by condition
            _add(self._make_node(
                project_id, "owner", "owner", f"owner:{owner_id}",
                label=f"owner:{owner_id}",
                state_summary={"owner_state": cp.owner_state},
            ))

        for issue in issues:
            _add(self._make_node(
                project_id, "issue", "issue", issue.issue_id,
                label=f"issue:{issue.issue_id}",
                state_summary={"state": issue.state, "severity": issue.severity},
            ))

        for blocker in blockers:
            _add(self._make_node(
                project_id, "blocker", "blocker", blocker.blocker_id,
                label=f"blocker:{blocker.blocker_id}",
                state_summary={"state": blocker.state, "blocker_type": blocker.blocker_type},
            ))

        for ev in evidence_records:
            _add(self._make_node(
                project_id, "evidence", "evidence", ev.evidence_id,
                label=f"evidence:{ev.evidence_id}",
                state_summary={"confidence": ev.confidence, "source_document": ev.source_document},
            ))

        for rl in revision_lineages:
            _add(self._make_node(
                project_id, "revision", "revision", rl.lineage_id,
                label=f"revision:{rl.lineage_id}",
                state_summary={"head": rl.head_revision_id, "branch": rl.branch_name},
            ))

        for pkg in packages:
            _add(self._make_node(
                project_id, "package", "package", pkg.package_id,
                label=f"package:{pkg.package_id}",
                state_summary={"revision_id": pkg.revision_id, "export_format": pkg.export_format},
            ))

        for art in artifacts:
            _add(self._make_node(
                project_id, "artifact", "artifact", art.artifact_id,
                label=f"artifact:{art.artifact_id}",
                state_summary={"artifact_type": art.artifact_type, "file_format": art.file_format},
            ))

        if pattern_refs:
            for pref in pattern_refs:
                pattern_id = pref.get("pattern_id", "")
                if pattern_id:
                    _add(self._make_node(
                        project_id, "pattern", "pattern", pattern_id,
                        label=f"pattern:{pattern_id}",
                        state_summary=pref.get("state_summary", {}),
                        metadata=pref.get("metadata", {}),
                    ))

        return nodes

    # ------------------------------------------------------------------
    # Edge projection
    # ------------------------------------------------------------------

    def _project_edges(
        self,
        project_id: str,
        nodes: dict[str, ConditionGraphNode],
        condition_packets: list[ConditionPacket],
        issues: list[IssueRecord],
        blockers: list[BlockerRecord],
        pattern_refs: Optional[list[dict]] = None,
    ) -> list[ConditionGraphEdge]:
        """Project all edges from source relationships."""
        edges: list[ConditionGraphEdge] = []
        seen_ids: set[str] = set()

        # Build a source lookup: "source_object_type:source_object_id" -> graph_node_id
        source_lookup: dict[str, str] = {}
        for node in nodes.values():
            key = f"{node.source_object_type}:{node.source_object_id}"
            source_lookup[key] = node.graph_node_id

        def _resolve(obj_type: str, obj_id: str) -> Optional[str]:
            return source_lookup.get(f"{obj_type}:{obj_id}")

        def _add_edge(edge_type: str, from_id: str, to_id: str,
                       source_basis: str = "", is_enrichment: bool = False) -> None:
            eid = ConditionGraphEdge.compute_edge_id(edge_type, from_id, to_id, project_id)
            if eid not in seen_ids:
                seen_ids.add(eid)
                edges.append(ConditionGraphEdge(
                    graph_edge_id=eid,
                    edge_type=edge_type,
                    from_node_id=from_id,
                    to_node_id=to_id,
                    project_id=project_id,
                    source_basis=source_basis,
                    is_enrichment_derived=is_enrichment,
                ))

        for cp in condition_packets:
            cond_nid = _resolve("condition", cp.condition_id)
            if not cond_nid:
                continue

            # blocker_refs -> blocked_by
            for bref in cp.blocker_refs:
                target = _resolve("blocker", bref)
                if target:
                    _add_edge("blocked_by", cond_nid, target, source_basis="condition.blocker_refs")

            # dependency_refs -> depends_on
            for dref in cp.dependency_refs:
                target = _resolve("condition", dref)
                if target:
                    _add_edge("depends_on", cond_nid, target, source_basis="condition.dependency_refs")

            # evidence_refs -> supported_by
            for eref in cp.evidence_refs:
                target = _resolve("evidence", eref)
                if target:
                    _add_edge("supported_by", cond_nid, target, source_basis="condition.evidence_refs")

            # artifact_refs -> derived_from
            for aref in cp.artifact_refs:
                target = _resolve("artifact", aref)
                if target:
                    _add_edge("derived_from", cond_nid, target, source_basis="condition.artifact_refs")

            # remediation_candidate_refs -> resolved_by
            for rref in cp.remediation_candidate_refs:
                target = _resolve("condition", rref)
                if target:
                    _add_edge("resolved_by", cond_nid, target, source_basis="condition.remediation_candidate_refs")

            # pattern_candidate_refs -> classified_as (enrichment-derived)
            for pref in cp.pattern_candidate_refs:
                target = _resolve("pattern", pref)
                if target:
                    _add_edge("classified_as", cond_nid, target,
                              source_basis="condition.pattern_candidate_refs", is_enrichment=True)

            # Owner edge
            owner_nid = _resolve("owner", f"owner:{cp.condition_id}")
            if owner_nid:
                _add_edge("owned_by", cond_nid, owner_nid, source_basis="condition.owner_state")

            # Assembly/interface/detail links from condition
            if cp.assembly_id:
                asm_nid = _resolve("assembly", cp.assembly_id)
                if asm_nid:
                    _add_edge("included_in", cond_nid, asm_nid, source_basis="condition.assembly_id")

            if cp.interface_id:
                ifc_nid = _resolve("interface", cp.interface_id)
                if ifc_nid:
                    _add_edge("interfaces_with", cond_nid, ifc_nid, source_basis="condition.interface_id")

            if cp.detail_id:
                det_nid = _resolve("detail", cp.detail_id)
                if det_nid:
                    _add_edge("implemented_by", cond_nid, det_nid, source_basis="condition.detail_id")

        # Issue edges — link to affected assemblies/interfaces/details
        for issue in issues:
            issue_nid = _resolve("issue", issue.issue_id)
            if not issue_nid:
                continue
            for aid in issue.affected_assembly_ids:
                target = _resolve("assembly", aid)
                if target:
                    _add_edge("blocked_by", target, issue_nid, source_basis="issue.affected_assembly_ids")
            for iid in issue.affected_interface_ids:
                target = _resolve("interface", iid)
                if target:
                    _add_edge("blocked_by", target, issue_nid, source_basis="issue.affected_interface_ids")
            for did in issue.affected_detail_ids:
                target = _resolve("detail", did)
                if target:
                    _add_edge("blocked_by", target, did, source_basis="issue.affected_detail_ids")

        # Blocker edges — blocking_element -> blocked_elements
        for blocker in blockers:
            blocker_nid = _resolve("blocker", blocker.blocker_id)
            if not blocker_nid:
                continue
            # Try to find blocking element node (could be any type)
            blocking_nid = None
            for obj_type in ("assembly", "interface", "detail", "condition"):
                blocking_nid = _resolve(obj_type, blocker.blocking_element_id)
                if blocking_nid:
                    break
            if blocking_nid:
                for blocked_id in blocker.blocked_element_ids:
                    for obj_type in ("assembly", "interface", "detail", "condition"):
                        blocked_nid = _resolve(obj_type, blocked_id)
                        if blocked_nid:
                            _add_edge("blocked_by", blocked_nid, blocker_nid,
                                      source_basis="blocker.blocking_element->blocked_elements")
                            break

        return edges

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate(self, graph: ConditionGraph) -> list[str]:
        """Return a list of validation errors (empty = valid)."""
        errors: list[str] = []

        # Check for orphan edges
        for eid, edge in graph.edges.items():
            if edge.from_node_id not in graph.nodes:
                errors.append(f"Orphan edge {eid}: from_node_id {edge.from_node_id} not in graph")
            if edge.to_node_id not in graph.nodes:
                errors.append(f"Orphan edge {eid}: to_node_id {edge.to_node_id} not in graph")

        # Check node identity determinism
        for nid, node in graph.nodes.items():
            expected = ConditionGraphNode.compute_node_id(
                node.source_object_type, node.source_object_id, node.project_id
            )
            if nid != expected:
                errors.append(f"Node {nid} identity mismatch: expected {expected}")

        return errors

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _make_node(
        project_id: str,
        node_type: str,
        source_object_type: str,
        source_object_id: str,
        label: str = "",
        state_summary: Optional[dict] = None,
        refs: Optional[dict] = None,
        metadata: Optional[dict] = None,
    ) -> ConditionGraphNode:
        """Create a ConditionGraphNode with deterministic id."""
        nid = ConditionGraphNode.compute_node_id(source_object_type, source_object_id, project_id)
        return ConditionGraphNode(
            graph_node_id=nid,
            node_type=node_type,
            source_object_type=source_object_type,
            source_object_id=source_object_id,
            project_id=project_id,
            label=label,
            state_summary=state_summary or {},
            refs=refs or {},
            metadata=metadata or {},
        )
