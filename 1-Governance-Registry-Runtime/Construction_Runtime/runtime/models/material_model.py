"""Material runtime model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MaterialModel:
    """Runtime representation of a construction material.

    Holds material identity, manufacturer info, and properties
    for use in engine processing.
    """

    material_name: str = ""
    manufacturer: str = ""
    properties: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
