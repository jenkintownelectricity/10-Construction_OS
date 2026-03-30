"""Revision lineage model for tracking changes across project lifecycle."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RevisionEntry:
    """A single revision entry in the lineage chain.

    Each revision captures the state delta, parent reference, and metadata
    for a specific point in the project timeline.
    """

    revision_id: str = ""
    parent_revision_id: str = ""
    timestamp: str = ""
    author: str = ""
    description: str = ""
    changed_assembly_ids: list[str] = field(default_factory=list)
    changed_interface_ids: list[str] = field(default_factory=list)
    changed_detail_ids: list[str] = field(default_factory=list)
    changed_parameter_keys: list[str] = field(default_factory=list)
    snapshot_hash: str = ""
    tag: str = ""


@dataclass
class RevisionLineage:
    """The full lineage of revisions for a project or sub-element.

    Provides an ordered chain of RevisionEntry objects from initial creation
    through the current state.
    """

    lineage_id: str = ""
    root_revision_id: str = ""
    head_revision_id: str = ""
    entries: list[RevisionEntry] = field(default_factory=list)
    branch_name: str = "main"
