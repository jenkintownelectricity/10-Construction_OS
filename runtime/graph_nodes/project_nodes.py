"""Wave 11A node projectors — project source domain objects into ConditionGraphNodes."""

from typing import Optional

from runtime.graph.graph_node import ConditionGraphNode
from runtime.models.condition_packet import ConditionPacket
from runtime.models.issue_model import IssueRecord, BlockerRecord
from runtime.models.evidence_model import EvidenceRecord
from runtime.models.revision_model import RevisionLineage
from runtime.models.drawing_package_model import DrawingPackage, ExportArtifact


class NodeProjector:
    """Projects source domain objects into ConditionGraphNode instances.

    Each project_* method takes a source object and project_id, returning
    a fully formed ConditionGraphNode with deterministic identity.
    """

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
        nid = ConditionGraphNode.compute_node_id(
            source_object_type, source_object_id, project_id
        )
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

    def project_condition_node(
        self, condition: ConditionPacket, project_id: str
    ) -> ConditionGraphNode:
        """Project a ConditionPacket into a condition graph node."""
        return self._make_node(
            project_id,
            "condition",
            "condition",
            condition.condition_id,
            label=f"condition:{condition.condition_id}",
            state_summary={
                "issue_state": condition.issue_state,
                "readiness_state": condition.readiness_state,
                "owner_state": condition.owner_state,
            },
            refs={
                "blocker_refs": list(condition.blocker_refs),
                "dependency_refs": list(condition.dependency_refs),
                "evidence_refs": list(condition.evidence_refs),
                "artifact_refs": list(condition.artifact_refs),
                "remediation_candidate_refs": list(condition.remediation_candidate_refs),
                "pattern_candidate_refs": list(condition.pattern_candidate_refs),
            },
        )

    def project_issue_node(
        self, issue: IssueRecord, project_id: str
    ) -> ConditionGraphNode:
        """Project an IssueRecord into an issue graph node."""
        return self._make_node(
            project_id,
            "issue",
            "issue",
            issue.issue_id,
            label=f"issue:{issue.issue_id}",
            state_summary={"state": issue.state, "severity": issue.severity},
        )

    def project_blocker_node(
        self, blocker: BlockerRecord, project_id: str
    ) -> ConditionGraphNode:
        """Project a BlockerRecord into a blocker graph node."""
        return self._make_node(
            project_id,
            "blocker",
            "blocker",
            blocker.blocker_id,
            label=f"blocker:{blocker.blocker_id}",
            state_summary={"state": blocker.state, "blocker_type": blocker.blocker_type},
        )

    def project_evidence_node(
        self, evidence: EvidenceRecord, project_id: str
    ) -> ConditionGraphNode:
        """Project an EvidenceRecord into an evidence graph node."""
        return self._make_node(
            project_id,
            "evidence",
            "evidence",
            evidence.evidence_id,
            label=f"evidence:{evidence.evidence_id}",
            state_summary={
                "confidence": evidence.confidence,
                "source_document": evidence.source_document,
            },
        )

    def project_revision_node(
        self, lineage: RevisionLineage, project_id: str
    ) -> ConditionGraphNode:
        """Project a RevisionLineage into a revision graph node."""
        return self._make_node(
            project_id,
            "revision",
            "revision",
            lineage.lineage_id,
            label=f"revision:{lineage.lineage_id}",
            state_summary={
                "head": lineage.head_revision_id,
                "branch": lineage.branch_name,
            },
        )

    def project_package_node(
        self, package: DrawingPackage, project_id: str
    ) -> ConditionGraphNode:
        """Project a DrawingPackage into a package graph node."""
        return self._make_node(
            project_id,
            "package",
            "package",
            package.package_id,
            label=f"package:{package.package_id}",
            state_summary={
                "revision_id": package.revision_id,
                "export_format": package.export_format,
            },
        )

    def project_artifact_node(
        self, artifact: ExportArtifact, project_id: str
    ) -> ConditionGraphNode:
        """Project an ExportArtifact into an artifact graph node."""
        return self._make_node(
            project_id,
            "artifact",
            "artifact",
            artifact.artifact_id,
            label=f"artifact:{artifact.artifact_id}",
            state_summary={
                "artifact_type": artifact.artifact_type,
                "file_format": artifact.file_format,
            },
        )

    def project_owner_node(
        self, condition: ConditionPacket, project_id: str
    ) -> ConditionGraphNode:
        """Project an owner node from a ConditionPacket.

        Owner nodes are always created — explicit unknown, never omit.
        """
        owner_id = f"owner:{condition.condition_id}"
        return self._make_node(
            project_id,
            "owner",
            "owner",
            owner_id,
            label=f"owner:{condition.condition_id}",
            state_summary={"owner_state": condition.owner_state},
        )

    def project_pattern_node(
        self, pattern_ref: dict, project_id: str
    ) -> ConditionGraphNode:
        """Project a pattern reference dict into a pattern graph node."""
        pattern_id = pattern_ref.get("pattern_id", "")
        return self._make_node(
            project_id,
            "pattern",
            "pattern",
            pattern_id,
            label=f"pattern:{pattern_id}",
            state_summary=pattern_ref.get("state_summary", {}),
            metadata=pattern_ref.get("metadata", {}),
        )
