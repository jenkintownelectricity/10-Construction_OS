"""Geometry runtime model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GeometryModel:
    """Runtime representation of geometric data.

    Holds dimensions, spatial references, and notes for use in
    engine processing and deliverable generation.
    """

    dimensions: dict[str, Any] = field(default_factory=dict)
    spatial_refs: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
