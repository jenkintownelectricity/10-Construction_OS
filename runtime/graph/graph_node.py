"""Wave 11A condition graph node — deterministic identity, typed projection."""

import hashlib
from dataclasses import dataclass, field


@dataclass
class ConditionGraphNode:
    """A node in the Wave 11A condition graph.

    Each node represents a projected construction element (condition, assembly,
    interface, detail, issue, blocker, remediation, artifact, evidence, pattern,
    package, revision, or owner). Identity is deterministic via SHA-256 of the
    source triple (source_object_type, source_object_id, project_id).
    """

    graph_node_id: str = ""
    node_type: str = ""  # condition | assembly | interface | detail | issue | blocker | remediation | artifact | evidence | pattern | package | revision | owner
    source_object_type: str = ""
    source_object_id: str = ""
    project_id: str = ""
    label: str = ""
    state_summary: dict = field(default_factory=dict)
    refs: dict = field(default_factory=dict)  # blocker_refs, dependency_refs, evidence_refs, artifact_refs, pattern_candidate_refs, etc.
    metadata: dict = field(default_factory=dict)
    lineage_ref: str = ""
    node_version: str = ""

    @staticmethod
    def compute_node_id(source_object_type: str, source_object_id: str, project_id: str) -> str:
        """Return a deterministic SHA-256 hex digest (first 16 chars) of the source triple."""
        raw = f"{source_object_type}:{source_object_id}:{project_id}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
