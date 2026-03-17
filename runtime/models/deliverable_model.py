"""Deliverable runtime model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DeliverableModel:
    """Runtime representation of a generated deliverable.

    Structured output first, render/export second.
    """

    deliverable_type: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    export_targets: list[str] = field(default_factory=list)
