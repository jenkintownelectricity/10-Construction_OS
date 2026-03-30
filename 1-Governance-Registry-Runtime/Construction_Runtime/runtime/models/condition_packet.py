"""Condition packet model for tracking assembly/interface/detail state."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConditionPacket:
    """Core condition packet representing the state of a construction element.

    Tracks issue state, readiness, ownership, blockers, remediation candidates,
    evidence references, graph references, dependencies, and pattern candidates.
    """

    condition_id: str = ""
    assembly_id: str = ""
    interface_id: str = ""
    detail_id: str = ""
    parameter_state: dict = field(default_factory=dict)
    issue_state: str = "none"  # none | open | resolved | deferred
    readiness_state: str = "unknown"  # unknown | ready | blocked | incomplete
    owner_state: str = "unknown"  # unknown | assigned | unassigned
    blocker_refs: list[str] = field(default_factory=list)
    remediation_candidate_refs: list[str] = field(default_factory=list)
    artifact_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    graph_ref: str = ""
    dependency_refs: list[str] = field(default_factory=list)
    pattern_candidate_refs: list[str] = field(default_factory=list)
    pattern_match_basis: str = ""
    pattern_confidence: float = 0.0
