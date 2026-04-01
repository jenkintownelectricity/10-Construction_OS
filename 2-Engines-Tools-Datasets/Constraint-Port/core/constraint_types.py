"""Constraint Types.

Python dataclass mirrors of the authoritative JSON schemas:
- constraint_object.schema.json
- constraint_evidence.schema.json
- constraint_decision.schema.json

These types do NOT define new contract shapes — they mirror the schemas exactly.
All enum values match the authoritative schemas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ============================================================
# constraint_object.schema.json mirrors
# ============================================================

CONSTRAINT_TYPES = frozenset([
    "PHYSICAL_INCOMPATIBILITY",
    "CODE_VIOLATION",
    "WARRANTY_VOID",
    "SPEC_CONFLICT",
    "INSTALL_SEQUENCE_VIOLATION",
    "RESPONSIBILITY_CONFLICT",
])

LOGIC_OPERATORS = frozenset(["BLOCK", "WARN", "REQUIRE_HUMAN_STAMP"])

DECISION_ACTIONS = frozenset([
    "PASS",
    "WARN",
    "BLOCK",
    "REQUIRE_HUMAN_STAMP",
    "DEFER_FOR_MISSING_EVIDENCE",
])

SEVERITIES = frozenset(["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"])

EVIDENCE_COMPLETENESS_VALUES = frozenset(["COMPLETE", "PARTIAL", "MISSING"])

ENTITY_TYPES = frozenset([
    "material",
    "assembly",
    "system",
    "method",
    "sequence",
    "scope_boundary",
])

DECISION_ON_FAIL_VALUES = frozenset([
    "BLOCK",
    "WARN",
    "REQUIRE_HUMAN_STAMP",
    "DEFER_FOR_MISSING_EVIDENCE",
])

# Severity ordering for aggregate severity computation
SEVERITY_ORDER = {
    "INFO": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}

# Action ordering for aggregate action computation
ACTION_ORDER = {
    "PASS": 0,
    "WARN": 1,
    "DEFER_FOR_MISSING_EVIDENCE": 2,
    "REQUIRE_HUMAN_STAMP": 3,
    "BLOCK": 4,
}


# ============================================================
# constraint_object.schema.json — ConstraintObject
# ============================================================

@dataclass(frozen=True)
class AppliesTo:
    """Target scope a constraint applies to."""
    entity_type: str
    entity_ids: list[str] = field(default_factory=list)
    entity_filter: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Trigger:
    """Conditions that activate constraint evaluation."""
    condition: str
    context_requirements: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DependencyMap:
    """External data dependencies for evaluation."""
    kernels: list[str] = field(default_factory=list)
    external_refs: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConstraintObject:
    """A single constraint rule. Mirrors constraint_object.schema.json."""
    rule_id: str
    rule_label: str
    rule_family: str
    constraint_type: str
    source_authority: str
    source_ref: str
    applies_to: AppliesTo
    trigger: Trigger
    dependency_map: DependencyMap
    logic_operator: str
    required_evidence: list[str]
    decision_on_fail: str
    notes: str | None = None


# ============================================================
# constraint_evidence.schema.json — ConstraintEvidence
# ============================================================

@dataclass(frozen=True)
class EvidenceItem:
    """A single evidence data point."""
    key: str
    value: Any
    source: str
    verified: bool = False


@dataclass(frozen=True)
class ConstraintEvidence:
    """Evidence collected for constraint evaluation. Mirrors constraint_evidence.schema.json."""
    evidence_id: str
    rule_id: str
    timestamp: str
    evidence_items: list[EvidenceItem]
    completeness: str
    missing_items: list[str] = field(default_factory=list)


# ============================================================
# constraint_decision.schema.json — ConstraintDecision
# ============================================================

@dataclass(frozen=True)
class TriggeredBy:
    """The specific evidence that caused the trigger."""
    evidence_key: str
    evidence_value: Any
    threshold: Any = None
    comparison: str | None = None


@dataclass(frozen=True)
class HumanOverride:
    """Present only if a human has stamped an override."""
    overridden_by: str
    override_timestamp: str
    override_rationale: str
    original_action: str  # "BLOCK" | "REQUIRE_HUMAN_STAMP"


@dataclass(frozen=True)
class ConstraintDecision:
    """Output decision of a constraint evaluation. Mirrors constraint_decision.schema.json."""
    decision_id: str
    rule_id: str
    evidence_id: str
    timestamp: str
    action: str
    severity: str
    rationale: str
    source_authority: str
    deterministic: bool = True  # Must always be True per schema
    triggered_by: TriggeredBy | None = None
    dependency_chain: list[str] = field(default_factory=list)
    human_override: HumanOverride | None = None


# ============================================================
# Constraint Port required field sets (from schemas)
# ============================================================

CONSTRAINT_OBJECT_REQUIRED_FIELDS = frozenset([
    "rule_id", "rule_label", "rule_family", "constraint_type",
    "source_authority", "source_ref", "applies_to", "trigger",
    "dependency_map", "logic_operator", "required_evidence", "decision_on_fail",
])

CONSTRAINT_EVIDENCE_REQUIRED_FIELDS = frozenset([
    "evidence_id", "rule_id", "timestamp", "evidence_items", "completeness",
])

CONSTRAINT_DECISION_REQUIRED_FIELDS = frozenset([
    "decision_id", "rule_id", "evidence_id", "timestamp",
    "action", "severity", "rationale", "source_authority", "deterministic",
])
