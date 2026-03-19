"""Shared fixtures for Wave 11A integration tests."""

import pytest

from runtime.models.condition_packet import ConditionPacket
from runtime.models.issue_model import IssueRecord, BlockerRecord
from runtime.models.evidence_model import EvidenceRecord
from runtime.models.revision_model import RevisionLineage
from runtime.models.drawing_package_model import DrawingPackage, ExportArtifact
from runtime.graph.materialize_graph import GraphMaterializer


PROJECT_ID = "test-project-001"


def make_condition_packet(**overrides) -> ConditionPacket:
    """Create a ConditionPacket with sensible defaults, overridable."""
    defaults = dict(
        condition_id="cond-1",
        assembly_id="asm-1",
        interface_id="ifc-1",
        detail_id="dtl-1",
        issue_state="none",
        readiness_state="unknown",
        owner_state="unknown",
        blocker_refs=[],
        dependency_refs=[],
        evidence_refs=[],
        artifact_refs=[],
        remediation_candidate_refs=[],
        pattern_candidate_refs=[],
    )
    defaults.update(overrides)
    return ConditionPacket(**defaults)


def make_blocker(**overrides) -> BlockerRecord:
    defaults = dict(
        blocker_id="blk-1",
        blocker_type="dependency",
        description="test blocker",
        blocking_element_id="asm-1",
        blocked_element_ids=["cond-1"],
        state="active",
    )
    defaults.update(overrides)
    return BlockerRecord(**defaults)


def make_issue(**overrides) -> IssueRecord:
    defaults = dict(
        issue_id="iss-1",
        issue_type="missing_detail",
        severity="warning",
        description="test issue",
        state="open",
    )
    defaults.update(overrides)
    return IssueRecord(**defaults)


def make_evidence(**overrides) -> EvidenceRecord:
    defaults = dict(
        evidence_id="ev-1",
        source_document="spec-v1.pdf",
        extraction_method="manual",
        confidence=0.95,
    )
    defaults.update(overrides)
    return EvidenceRecord(**defaults)


def make_revision(**overrides) -> RevisionLineage:
    defaults = dict(
        lineage_id="rev-lin-1",
        root_revision_id="rev-0",
        head_revision_id="rev-3",
        branch_name="main",
    )
    defaults.update(overrides)
    return RevisionLineage(**defaults)


def make_package(**overrides) -> DrawingPackage:
    defaults = dict(
        package_id="pkg-1",
        package_name="drawing-pkg-1",
        revision_id="rev-3",
        export_format="pdf",
    )
    defaults.update(overrides)
    return DrawingPackage(**defaults)


def make_artifact(**overrides) -> ExportArtifact:
    defaults = dict(
        artifact_id="art-1",
        artifact_type="drawing",
        file_format="pdf",
        file_path="/out/drawing.pdf",
    )
    defaults.update(overrides)
    return ExportArtifact(**defaults)


def build_standard_graph(
    project_id=PROJECT_ID,
    condition_packets=None,
    issues=None,
    blockers=None,
    evidence_records=None,
    revision_lineages=None,
    packages=None,
    artifacts=None,
    pattern_refs=None,
):
    """Build a graph using the GraphMaterializer with provided or default inputs."""
    m = GraphMaterializer()
    return m.materialize(
        project_id=project_id,
        condition_packets=condition_packets or [],
        issues=issues or [],
        blockers=blockers or [],
        evidence_records=evidence_records or [],
        revision_lineages=revision_lineages or [],
        packages=packages or [],
        artifacts=artifacts or [],
        pattern_refs=pattern_refs,
    )
