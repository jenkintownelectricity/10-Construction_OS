"""Deliverable runtime model v0.2.

Extended to support DXF, SVG, and JSON preview formats with version metadata.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DeliverableFormat:
    """A single format output within a deliverable."""
    content: str = ""
    status: str = "pending"  # "generated", "failed", "skipped", "pending"


@dataclass
class DeliverableModel:
    """Runtime representation of a generated deliverable.

    v0.2: Extended with deliverable_id, deliverable_version, and multi-format support.
    Backward-compatible: payload and export_targets still work for v0.1 consumers.
    """

    deliverable_type: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    export_targets: list[str] = field(default_factory=list)

    # v0.2 fields
    deliverable_id: str = ""
    deliverable_version: str = "0.2"
    formats: dict[str, DeliverableFormat] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for contract validation."""
        return {
            "deliverable_id": self.deliverable_id,
            "deliverable_version": self.deliverable_version,
            "deliverable_type": self.deliverable_type,
            "formats": {
                name: {"content": fmt.content, "status": fmt.status}
                for name, fmt in self.formats.items()
            },
            "payload": self.payload,
            "export_targets": self.export_targets,
        }
