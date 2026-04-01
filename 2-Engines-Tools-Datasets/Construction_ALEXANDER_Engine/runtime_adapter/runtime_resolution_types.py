"""Runtime Resolution Types.

Python dataclass mirrors of the authoritative JSON schemas:
- condition_signature.schema.json
- resolution_result.schema.json

These types exist for runtime adapter validation and type safety.
They do NOT define new contract shapes — they mirror the schemas exactly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ============================================================
# condition_signature.schema.json mirrors
# ============================================================

# Authoritative enum values from schema
CONDITION_TYPES = frozenset([
    "roof_edge",
    "parapet",
    "drain",
    "penetration",
    "expansion_joint",
    "interface",
    "transition",
])

INTERFACE_CONDITIONS = frozenset([
    "roof_to_wall",
    "parapet",
    "penetration",
    "fenestration",
    "below_grade",
    "expansion_joint",
    "deck_to_wall",
    "roof_edge",
    "curb",
    "drain",
    "custom",
])

WIND_ZONES = frozenset([1, 2, 3])

MOISTURE_EXPOSURES = frozenset(["low", "moderate", "high", "severe"])

CONDITION_SIGNATURE_REQUIRED_FIELDS = frozenset([
    "condition_id",
    "schema_version",
    "timestamp_utc",
    "condition_type",
    "location_context",
])


# ============================================================
# resolution_result.schema.json mirrors
# ============================================================

RESOLUTION_STATUSES = frozenset(["RESOLVED", "UNRESOLVED", "BLOCKED", "CONFLICT"])

STAGE_STATUSES = frozenset(["PASS", "FAIL", "SKIP"])

RESOLUTION_STAGES_REQUIRED = (
    "intake",
    "normalization",
    "family_classification",
    "pattern_resolution",
    "variant_selection",
    "constraint_enforcement",
    "conflict_detection",
    "scoring",
)

FAIL_REASON_CODES = frozenset([
    "INVALID_CONDITION",
    "MISSING_REQUIRED_FIELD",
    "UNKNOWN_CONDITION_TYPE",
    "NO_FAMILY_MATCH",
    "AMBIGUOUS_FAMILY",
    "NO_PATTERN_MATCH",
    "AMBIGUOUS_PATTERN",
    "NO_VARIANT_MATCH",
    "AMBIGUOUS_VARIANT",
    "CONSTRAINT_VIOLATION",
    "CONFLICT_DETECTED",
    "MISSING_TRUTH",
    "INCOMPATIBLE_CONTEXT",
    "SCORING_FAILURE",
    "INTERNAL_ERROR",
])

FAIL_REASON_STAGES = frozenset([
    "intake",
    "normalization",
    "family_classification",
    "pattern_resolution",
    "variant_selection",
    "constraint_enforcement",
    "conflict_detection",
    "scoring",
    "assembly",
])

RESOLUTION_RESULT_REQUIRED_FIELDS = frozenset([
    "result_id",
    "schema_version",
    "timestamp_utc",
    "condition_id",
    "status",
    "resolution_stages",
])

RESOLUTION_RESULT_SCHEMA_VERSION = "1.0.0"


@dataclass(frozen=True)
class RuntimeAdapterError:
    """Structured error from the runtime adapter."""
    code: str
    message: str
    stage: str = "adapter"
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RuntimeAdapterResult:
    """Wrapper returned by the runtime adapter to runtime consumers.

    Fields:
        success: Whether the adapter call completed without adapter-level errors
        resolution_result: The ResolutionResult dict if engine invocation succeeded
        adapter_errors: List of adapter-level errors (validation failures, etc.)
    """
    success: bool
    resolution_result: dict[str, Any] | None = None
    adapter_errors: list[RuntimeAdapterError] = field(default_factory=list)
