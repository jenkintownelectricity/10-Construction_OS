"""Shared fixtures for Wave 12 integration tests.

Reuses helpers from wave11a conftest and builds a richer graph with ~15 nodes
and multiple edge types (depends_on, blocked_by, owned_by, resolved_by,
classified_as with is_enrichment_derived=True, supported_by, included_in).
"""

import pytest

from tests.wave11a.conftest import (
    make_condition_packet,
    make_blocker,
    make_issue,
    make_evidence,
    make_revision,
    make_package,
    make_artifact,
    build_standard_graph,
    PROJECT_ID,
)
from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_index import GraphIndex
from runtime.graph_queries.query_engine import QueryEngine
from runtime.readiness_routing.router import ReadinessRouter
from runtime.impact_analysis.analyzer import ImpactAnalyzer


@pytest.fixture()
def sample_graph() -> ConditionGraph:
    """Build a ConditionGraph with ~15 nodes and varied edge types.

    Graph topology:
      cond-1 (asm-1) -- blocked_by --> blk-1
      cond-1 -- depends_on --> cond-2
      cond-1 -- owned_by --> owner:cond-1
      cond-1 -- supported_by --> ev-1
      cond-1 -- classified_as (enrichment) --> pattern pat-1
      cond-2 (asm-1) -- resolved_by --> cond-3 (remediation target)
      cond-3 (asm-2)
      blocker blk-1 blocks cond-1
      evidence ev-1
      revision rev-lin-1
      package pkg-1
      artifact art-1
      pattern pat-1
    """
    packets = [
        make_condition_packet(
            condition_id="cond-1",
            assembly_id="asm-1",
            interface_id="ifc-1",
            detail_id="dtl-1",
            readiness_state="blocked",
            owner_state="assigned",
            blocker_refs=["blk-1"],
            dependency_refs=["cond-2"],
            evidence_refs=["ev-1"],
            artifact_refs=["art-1"],
            pattern_candidate_refs=["pat-1"],
        ),
        make_condition_packet(
            condition_id="cond-2",
            assembly_id="asm-1",
            interface_id="ifc-1",
            detail_id="dtl-1",
            readiness_state="pending",
            owner_state="unknown",
            remediation_candidate_refs=["cond-3"],
        ),
        make_condition_packet(
            condition_id="cond-3",
            assembly_id="asm-2",
            interface_id="ifc-2",
            detail_id="dtl-2",
            readiness_state="ready",
            owner_state="assigned",
        ),
    ]
    blockers = [
        make_blocker(
            blocker_id="blk-1",
            blocker_type="dependency",
            blocking_element_id="asm-1",
            blocked_element_ids=["cond-1"],
            state="active",
        ),
    ]
    issues = [
        make_issue(issue_id="iss-1", state="open"),
    ]
    evidence = [
        make_evidence(evidence_id="ev-1"),
    ]
    revisions = [
        make_revision(lineage_id="rev-lin-1"),
    ]
    packages = [
        make_package(package_id="pkg-1"),
    ]
    artifacts = [
        make_artifact(artifact_id="art-1"),
    ]
    pattern_refs = [
        {"pattern_id": "pat-1", "state_summary": {"classification": "recurring"}, "metadata": {"is_enrichment_derived": True}},
    ]

    graph = build_standard_graph(
        project_id=PROJECT_ID,
        condition_packets=packets,
        issues=issues,
        blockers=blockers,
        evidence_records=evidence,
        revision_lineages=revisions,
        packages=packages,
        artifacts=artifacts,
        pattern_refs=pattern_refs,
    )
    return graph


@pytest.fixture()
def graph_index(sample_graph: ConditionGraph) -> GraphIndex:
    return GraphIndex(sample_graph)


@pytest.fixture()
def query_engine(sample_graph: ConditionGraph) -> QueryEngine:
    return QueryEngine(sample_graph)


@pytest.fixture()
def readiness_router(sample_graph: ConditionGraph) -> ReadinessRouter:
    return ReadinessRouter(sample_graph)


@pytest.fixture()
def impact_analyzer(sample_graph: ConditionGraph) -> ImpactAnalyzer:
    return ImpactAnalyzer(sample_graph)
