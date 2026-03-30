"""Assembly runtime model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AssemblyModel:
    """Runtime representation of a construction assembly.

    This is an execution-oriented model, not an ontology definition.
    Assembly truth is defined in Construction_Kernel; this model holds
    runtime data for processing.
    """

    name: str = ""
    components: list[dict[str, str]] = field(default_factory=list)
    constraints: list[dict[str, str]] = field(default_factory=list)
    source_text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
