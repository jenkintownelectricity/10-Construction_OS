"""
breakaway_evaluator.py — Evaluates breakaway conditions for mirror detachment.

Breakaway is the controlled separation of a mirror from its source.
It must be non-destructive: the source continues unaffected, the mirror
either stands alone or is decommissioned cleanly.

DOCTRINE: Sold by capability, detachable by design.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class BreakawayVerdict(Enum):
    """Outcome of a breakaway evaluation."""
    APPROVED = "approved"
    DENIED = "denied"
    CONDITIONAL = "conditional"


@dataclass
class BreakawayCondition:
    """
    A single condition that must be met for breakaway.

    Attributes:
        condition_id: Unique identifier.
        name: Human-readable condition name.
        description: What this condition checks.
        check_fn_name: Name of the function/method that evaluates this condition.
        required: Whether this condition is mandatory (blocking).
        met: Whether the condition is currently satisfied.
        details: Explanation of the current state.
    """
    condition_id: str
    name: str
    description: str
    check_fn_name: str = ""
    required: bool = True
    met: bool = False
    details: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "condition_id": self.condition_id,
            "name": self.name,
            "description": self.description,
            "check_fn_name": self.check_fn_name,
            "required": self.required,
            "met": self.met,
            "details": self.details,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BreakawayCondition:
        return cls(
            condition_id=data["condition_id"],
            name=data["name"],
            description=data["description"],
            check_fn_name=data.get("check_fn_name", ""),
            required=data.get("required", True),
            met=data.get("met", False),
            details=data.get("details", ""),
        )


@dataclass
class BreakawayRecord:
    """
    Record of a breakaway evaluation.

    Attributes:
        record_id: Unique identifier.
        mirror_id: The mirror being evaluated for breakaway.
        source_id: The source the mirror would detach from.
        verdict: Approved, denied, or conditional.
        conditions: All conditions evaluated.
        non_destructive: Whether breakaway is confirmed non-destructive.
        plan: The breakaway plan if approved.
        evaluated_at: ISO timestamp of the evaluation.
        notes: Additional notes.
    """
    record_id: str
    mirror_id: str
    source_id: str
    verdict: BreakawayVerdict
    conditions: list[BreakawayCondition] = field(default_factory=list)
    non_destructive: bool = False
    plan: dict[str, Any] = field(default_factory=dict)
    evaluated_at: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.evaluated_at:
            self.evaluated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "mirror_id": self.mirror_id,
            "source_id": self.source_id,
            "verdict": self.verdict.value,
            "conditions": [c.to_dict() for c in self.conditions],
            "non_destructive": self.non_destructive,
            "plan": self.plan,
            "evaluated_at": self.evaluated_at,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BreakawayRecord:
        return cls(
            record_id=data["record_id"],
            mirror_id=data["mirror_id"],
            source_id=data["source_id"],
            verdict=BreakawayVerdict(data["verdict"]),
            conditions=[BreakawayCondition.from_dict(c) for c in data.get("conditions", [])],
            non_destructive=data.get("non_destructive", False),
            plan=data.get("plan", {}),
            evaluated_at=data.get("evaluated_at", ""),
            notes=data.get("notes", ""),
        )


class BreakawayEvaluator:
    """
    Evaluates whether a mirror can safely break away from its source.

    Breakaway is approved only when:
    1. All required conditions are met.
    2. The breakaway is verified as non-destructive.
    3. A valid breakaway plan can be generated.

    Args:
        mirror_id: The mirror to evaluate.
        source_id: The source system.
    """

    # Standard breakaway conditions
    STANDARD_CONDITIONS: list[dict[str, Any]] = [
        {
            "condition_id": "no-shared-state",
            "name": "No Shared Mutable State",
            "description": "Mirror does not share mutable state with source",
            "required": True,
        },
        {
            "condition_id": "no-source-callbacks",
            "name": "No Source Callbacks",
            "description": "Mirror does not register callbacks into source",
            "required": True,
        },
        {
            "condition_id": "independent-data",
            "name": "Independent Data Path",
            "description": "Mirror has its own data path, not piped from source",
            "required": True,
        },
        {
            "condition_id": "no-entangled-config",
            "name": "No Entangled Configuration",
            "description": "Mirror configuration is self-contained",
            "required": True,
        },
        {
            "condition_id": "clean-interface-boundary",
            "name": "Clean Interface Boundary",
            "description": "All communication goes through defined interfaces",
            "required": True,
        },
        {
            "condition_id": "drift-acceptable",
            "name": "Drift Within Threshold",
            "description": "Current drift levels are within acceptable range",
            "required": False,
        },
        {
            "condition_id": "parity-baseline-exists",
            "name": "Parity Baseline Exists",
            "description": "A parity baseline exists for post-breakaway validation",
            "required": False,
        },
    ]

    def __init__(self, mirror_id: str, source_id: str) -> None:
        self._mirror_id = mirror_id
        self._source_id = source_id
        self._conditions: list[BreakawayCondition] = []
        self._records: list[BreakawayRecord] = []

        # Load standard conditions
        for cond_data in self.STANDARD_CONDITIONS:
            self._conditions.append(BreakawayCondition(
                condition_id=cond_data["condition_id"],
                name=cond_data["name"],
                description=cond_data["description"],
                required=cond_data["required"],
            ))

    @property
    def mirror_id(self) -> str:
        return self._mirror_id

    @property
    def source_id(self) -> str:
        return self._source_id

    @property
    def conditions(self) -> list[BreakawayCondition]:
        return list(self._conditions)

    @property
    def records(self) -> list[BreakawayRecord]:
        return list(self._records)

    def add_condition(self, condition: BreakawayCondition) -> None:
        """Add a custom breakaway condition."""
        self._conditions.append(condition)

    def set_condition_met(
        self,
        condition_id: str,
        met: bool,
        details: str = "",
    ) -> bool:
        """
        Set the met status of a condition.

        Args:
            condition_id: The condition to update.
            met: Whether the condition is satisfied.
            details: Explanation.

        Returns:
            True if the condition was found and updated, False otherwise.
        """
        for cond in self._conditions:
            if cond.condition_id == condition_id:
                cond.met = met
                cond.details = details
                return True
        return False

    def check_conditions(self) -> tuple[list[BreakawayCondition], list[BreakawayCondition]]:
        """
        Check all conditions and partition into met and unmet.

        Returns:
            Tuple of (met_conditions, unmet_conditions).
        """
        met: list[BreakawayCondition] = []
        unmet: list[BreakawayCondition] = []
        for cond in self._conditions:
            if cond.met:
                met.append(cond)
            else:
                unmet.append(cond)
        return met, unmet

    def verify_non_destructive(
        self,
        source_dependencies: Optional[list[str]] = None,
        mirror_writes_to_source: bool = False,
        shared_resources: Optional[list[str]] = None,
    ) -> tuple[bool, list[str]]:
        """
        Verify that breakaway will not damage the source system.

        A breakaway is non-destructive if:
        1. The mirror does not write to source-owned resources.
        2. No shared resources exist that would be disrupted.
        3. Source has no runtime dependency on the mirror.

        Args:
            source_dependencies: Resources the source depends on.
            mirror_writes_to_source: Whether the mirror writes to source.
            shared_resources: Resources shared between mirror and source.

        Returns:
            Tuple of (is_non_destructive, list_of_issues).
        """
        issues: list[str] = []

        if mirror_writes_to_source:
            issues.append(
                "Mirror writes to source-owned resources; "
                "breakaway would disrupt source data flow"
            )

        if shared_resources:
            issues.append(
                f"Shared resources detected: {shared_resources}; "
                "breakaway could disrupt shared state"
            )

        if source_dependencies:
            # Check if any source dependency points to the mirror
            mirror_refs = [
                dep for dep in source_dependencies
                if self._mirror_id in dep or "mirror" in dep.lower()
            ]
            if mirror_refs:
                issues.append(
                    f"Source has dependencies referencing mirror: {mirror_refs}"
                )

        return len(issues) == 0, issues

    def generate_breakaway_plan(
        self,
        target_state: str = "standalone",
        migration_steps: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """
        Generate a breakaway execution plan.

        Args:
            target_state: Desired state after breakaway (standalone/decommission).
            migration_steps: Optional custom migration steps.

        Returns:
            Dictionary containing the breakaway plan.
        """
        met_conditions, unmet_conditions = self.check_conditions()
        required_unmet = [c for c in unmet_conditions if c.required]

        default_steps = [
            "Snapshot current mirror state",
            "Verify all parity baselines are recorded",
            "Disconnect mirror interface bindings",
            "Remove mirror from source's registry",
            "Update reflection status to DEPRECATED",
            "Run post-breakaway validation against parity baseline",
            "Archive breakaway record",
        ]

        steps = migration_steps or default_steps

        plan = {
            "mirror_id": self._mirror_id,
            "source_id": self._source_id,
            "target_state": target_state,
            "feasible": len(required_unmet) == 0,
            "blocking_conditions": [c.to_dict() for c in required_unmet],
            "met_conditions": [c.to_dict() for c in met_conditions],
            "steps": steps,
            "estimated_risk": "low" if len(required_unmet) == 0 else "high",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

        return plan

    def evaluate_breakaway(
        self,
        source_dependencies: Optional[list[str]] = None,
        mirror_writes_to_source: bool = False,
        shared_resources: Optional[list[str]] = None,
        target_state: str = "standalone",
    ) -> BreakawayRecord:
        """
        Perform a full breakaway evaluation.

        This is the primary entry point. It checks conditions, verifies
        non-destructive behavior, generates a plan, and produces a record.

        Args:
            source_dependencies: Resources the source depends on.
            mirror_writes_to_source: Whether the mirror writes to source.
            shared_resources: Resources shared between mirror and source.
            target_state: Desired state after breakaway.

        Returns:
            A BreakawayRecord with the evaluation results.
        """
        met_conditions, unmet_conditions = self.check_conditions()
        required_unmet = [c for c in unmet_conditions if c.required]

        is_non_destructive, nd_issues = self.verify_non_destructive(
            source_dependencies=source_dependencies,
            mirror_writes_to_source=mirror_writes_to_source,
            shared_resources=shared_resources,
        )

        plan = self.generate_breakaway_plan(target_state=target_state)

        # Determine verdict
        if required_unmet:
            verdict = BreakawayVerdict.DENIED
            notes = (
                f"Breakaway denied: {len(required_unmet)} required condition(s) unmet: "
                f"{[c.name for c in required_unmet]}"
            )
        elif not is_non_destructive:
            verdict = BreakawayVerdict.DENIED
            notes = f"Breakaway denied: non-destructive check failed: {nd_issues}"
        elif unmet_conditions:
            verdict = BreakawayVerdict.CONDITIONAL
            notes = (
                f"Breakaway conditionally approved: {len(unmet_conditions)} "
                f"optional condition(s) unmet: {[c.name for c in unmet_conditions]}"
            )
        else:
            verdict = BreakawayVerdict.APPROVED
            notes = "All conditions met, breakaway approved"

        record = BreakawayRecord(
            record_id=f"breakaway-{uuid.uuid4().hex[:12]}",
            mirror_id=self._mirror_id,
            source_id=self._source_id,
            verdict=verdict,
            conditions=list(self._conditions),
            non_destructive=is_non_destructive,
            plan=plan,
            notes=notes,
        )

        self._records.append(record)
        return record
