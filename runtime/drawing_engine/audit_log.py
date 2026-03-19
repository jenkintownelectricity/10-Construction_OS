"""
Audit Log Layer

Records runtime decisions and failures for traceability and governance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AuditEntry:
    """A single audit log entry."""

    timestamp: str = ""
    stage: str = ""
    status: str = ""
    detail_id: str = ""
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditLog:
    """Accumulated audit log for a pipeline run."""

    condition_id: str = ""
    entries: list[AuditEntry] = field(default_factory=list)
    final_status: str = "pending"

    def record(
        self,
        stage: str,
        status: str,
        message: str,
        detail_id: str = "",
        data: dict[str, Any] | None = None,
    ) -> None:
        """Record an audit entry."""
        self.entries.append(AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            stage=stage,
            status=status,
            detail_id=detail_id,
            message=message,
            data=data or {},
        ))

    def to_dict(self) -> dict[str, Any]:
        """Serialize audit log to dict."""
        return {
            "condition_id": self.condition_id,
            "final_status": self.final_status,
            "entry_count": len(self.entries),
            "entries": [
                {
                    "timestamp": e.timestamp,
                    "stage": e.stage,
                    "status": e.status,
                    "detail_id": e.detail_id,
                    "message": e.message,
                    "data": e.data,
                }
                for e in self.entries
            ],
        }
