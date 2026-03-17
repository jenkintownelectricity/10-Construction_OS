"""Runtime report model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RuntimeReportModel:
    """Summary report for a runtime pipeline execution."""

    input_type: str = ""
    validation_status: str = ""
    actions_taken: list[str] = field(default_factory=list)
    outputs_generated: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
