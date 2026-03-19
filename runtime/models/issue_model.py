"""Issue and blocker models for tracking construction problems."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IssueRecord:
    """Represents a detected issue in the construction model.

    Issues may be QA failures, missing details, incompatible materials,
    unresolved interfaces, or other problems requiring attention.
    """

    issue_id: str = ""
    issue_type: str = ""  # missing_detail | incompatible_material | unresolved_interface | scope_conflict | parameter_gap | missing_ownership | readiness_blocker
    severity: str = "warning"  # info | warning | error | critical
    description: str = ""
    affected_assembly_ids: list[str] = field(default_factory=list)
    affected_interface_ids: list[str] = field(default_factory=list)
    affected_detail_ids: list[str] = field(default_factory=list)
    detected_by: str = ""
    detected_at: str = ""
    state: str = "open"  # open | resolved | deferred | dismissed
    resolution_note: str = ""
    evidence_refs: list[str] = field(default_factory=list)


@dataclass
class BlockerRecord:
    """Represents a blocker preventing readiness or release.

    Blockers are hard dependencies that must be resolved before
    the affected element can proceed.
    """

    blocker_id: str = ""
    blocker_type: str = ""  # dependency | approval | material | design | external
    description: str = ""
    blocking_element_id: str = ""
    blocked_element_ids: list[str] = field(default_factory=list)
    state: str = "active"  # active | resolved | waived
    resolution_note: str = ""
    created_at: str = ""
    resolved_at: Optional[str] = None
