"""Wave 11A edge projectors — project source relationships into ConditionGraphEdges."""

from typing import Optional

from runtime.graph.graph_edge import ConditionGraphEdge
from runtime.graph.graph_node import ConditionGraphNode
from runtime.models.condition_packet import ConditionPacket
from runtime.models.issue_model import IssueRecord, BlockerRecord


class EdgeProjector:
    """Projects source domain relationships into ConditionGraphEdge instances.

    Each project_* method takes source data and project_id, returning
    a list of ConditionGraphEdge instances with deterministic identity.
    """

    @staticmethod
    def _make_edge(
        edge_type: str,
        from_node_id: str,
        to_node_id: str,
        project_id: str,
        source_basis: str = "",
        is_enrichment_derived: bool = False,
    ) -> ConditionGraphEdge:
        """Create a ConditionGraphEdge with deterministic id."""
        eid = ConditionGraphEdge.compute_edge_id(
            edge_type, from_node_id, to_node_id, project_id
        )
        return ConditionGraphEdge(
            graph_edge_id=eid,
            edge_type=edge_type,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            project_id=project_id,
            source_basis=source_basis,
            is_enrichment_derived=is_enrichment_derived,
        )

    def _resolve(
        self, source_lookup: dict[str, str], obj_type: str, obj_id: str
    ) -> Optional[str]:
        """Resolve a source object to its graph node id."""
        return source_lookup.get(f"{obj_type}:{obj_id}")

    def project_blocker_edges(
        self,
        condition: ConditionPacket,
        cond_node_id: str,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project blocker_refs -> blocked_by edges from a condition packet."""
        edges: list[ConditionGraphEdge] = []
        for bref in condition.blocker_refs:
            target = self._resolve(source_lookup, "blocker", bref)
            if target:
                edges.append(
                    self._make_edge(
                        "blocked_by", cond_node_id, target, project_id,
                        source_basis="condition.blocker_refs",
                    )
                )
        return edges

    def project_dependency_edges(
        self,
        condition: ConditionPacket,
        cond_node_id: str,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project dependency_refs -> depends_on edges from a condition packet."""
        edges: list[ConditionGraphEdge] = []
        for dref in condition.dependency_refs:
            target = self._resolve(source_lookup, "condition", dref)
            if target:
                edges.append(
                    self._make_edge(
                        "depends_on", cond_node_id, target, project_id,
                        source_basis="condition.dependency_refs",
                    )
                )
        return edges

    def project_evidence_edges(
        self,
        condition: ConditionPacket,
        cond_node_id: str,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project evidence_refs -> supported_by edges from a condition packet."""
        edges: list[ConditionGraphEdge] = []
        for eref in condition.evidence_refs:
            target = self._resolve(source_lookup, "evidence", eref)
            if target:
                edges.append(
                    self._make_edge(
                        "supported_by", cond_node_id, target, project_id,
                        source_basis="condition.evidence_refs",
                    )
                )
        return edges

    def project_artifact_edges(
        self,
        condition: ConditionPacket,
        cond_node_id: str,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project artifact_refs -> derived_from edges from a condition packet."""
        edges: list[ConditionGraphEdge] = []
        for aref in condition.artifact_refs:
            target = self._resolve(source_lookup, "artifact", aref)
            if target:
                edges.append(
                    self._make_edge(
                        "derived_from", cond_node_id, target, project_id,
                        source_basis="condition.artifact_refs",
                    )
                )
        return edges

    def project_remediation_edges(
        self,
        condition: ConditionPacket,
        cond_node_id: str,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project remediation_candidate_refs -> resolved_by edges from a condition packet."""
        edges: list[ConditionGraphEdge] = []
        for rref in condition.remediation_candidate_refs:
            target = self._resolve(source_lookup, "condition", rref)
            if target:
                edges.append(
                    self._make_edge(
                        "resolved_by", cond_node_id, target, project_id,
                        source_basis="condition.remediation_candidate_refs",
                    )
                )
        return edges

    def project_classification_edges(
        self,
        condition: ConditionPacket,
        cond_node_id: str,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project pattern_candidate_refs -> classified_as edges (enrichment-derived)."""
        edges: list[ConditionGraphEdge] = []
        for pref in condition.pattern_candidate_refs:
            target = self._resolve(source_lookup, "pattern", pref)
            if target:
                edges.append(
                    self._make_edge(
                        "classified_as", cond_node_id, target, project_id,
                        source_basis="condition.pattern_candidate_refs",
                        is_enrichment_derived=True,
                    )
                )
        return edges

    def project_ownership_edges(
        self,
        condition: ConditionPacket,
        cond_node_id: str,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project owned_by edges from a condition to its owner node."""
        edges: list[ConditionGraphEdge] = []
        owner_nid = self._resolve(source_lookup, "owner", f"owner:{condition.condition_id}")
        if owner_nid:
            edges.append(
                self._make_edge(
                    "owned_by", cond_node_id, owner_nid, project_id,
                    source_basis="condition.owner_state",
                )
            )
        return edges

    def project_issue_edges(
        self,
        issue: IssueRecord,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project issue -> affected assembly/interface/detail edges."""
        edges: list[ConditionGraphEdge] = []
        issue_nid = self._resolve(source_lookup, "issue", issue.issue_id)
        if not issue_nid:
            return edges

        for aid in issue.affected_assembly_ids:
            target = self._resolve(source_lookup, "assembly", aid)
            if target:
                edges.append(
                    self._make_edge(
                        "blocked_by", target, issue_nid, project_id,
                        source_basis="issue.affected_assembly_ids",
                    )
                )
        for iid in issue.affected_interface_ids:
            target = self._resolve(source_lookup, "interface", iid)
            if target:
                edges.append(
                    self._make_edge(
                        "blocked_by", target, issue_nid, project_id,
                        source_basis="issue.affected_interface_ids",
                    )
                )
        for did in issue.affected_detail_ids:
            target = self._resolve(source_lookup, "detail", did)
            if target:
                edges.append(
                    self._make_edge(
                        "blocked_by", target, issue_nid, project_id,
                        source_basis="issue.affected_detail_ids",
                    )
                )
        return edges

    def project_blocker_record_edges(
        self,
        blocker: BlockerRecord,
        source_lookup: dict[str, str],
        project_id: str,
    ) -> list[ConditionGraphEdge]:
        """Project blocker -> blocked_elements edges."""
        edges: list[ConditionGraphEdge] = []
        blocker_nid = self._resolve(source_lookup, "blocker", blocker.blocker_id)
        if not blocker_nid:
            return edges

        # Find blocking element node (could be any type)
        blocking_nid = None
        for obj_type in ("assembly", "interface", "detail", "condition"):
            blocking_nid = self._resolve(source_lookup, obj_type, blocker.blocking_element_id)
            if blocking_nid:
                break

        if blocking_nid:
            for blocked_id in blocker.blocked_element_ids:
                for obj_type in ("assembly", "interface", "detail", "condition"):
                    blocked_nid = self._resolve(source_lookup, obj_type, blocked_id)
                    if blocked_nid:
                        edges.append(
                            self._make_edge(
                                "blocked_by", blocked_nid, blocker_nid, project_id,
                                source_basis="blocker.blocking_element->blocked_elements",
                            )
                        )
                        break

        return edges
