"""
mirror_activation_gate.py — Controls mirror activation with fail-closed semantics.

THE GATE IS FAIL-CLOSED: If ANY check fails, activation is denied.

This is the final authority on whether a mirror may be activated. It enforces
the L0.6 Mirror Invalidity Rules, ensuring that no mirror goes live without
meeting every structural, contractual, and evidential requirement.

L0.6 MIRROR INVALIDITY RULES:
    1.  mirror-manifest.yaml missing or invalid
    2.  enabled slices not declared
    3.  slice dependency graph missing or invalid
    4.  trust boundary undefined
    5.  reflection status missing
    6.  no parity fixtures exist
    7.  drift record schema missing
    8.  breakaway conditions missing
    9.  truth ownership undefined
    10. mirror contains forbidden app-local logic
    11. lifecycle state is inconsistent with evidence
    12. registry entry missing
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ActivationVerdict(Enum):
    """Final verdict of the activation gate."""
    ALLOW = "allow"
    DENY = "deny"


@dataclass
class ActivationCheck:
    """
    A single activation gate check.

    Attributes:
        check_id: Unique identifier for the check.
        rule_number: L0.6 rule number (1-12).
        name: Human-readable check name.
        passed: Whether the check passed.
        required: Whether the check is mandatory (always True for fail-closed).
        details: Explanation of the check result.
    """
    check_id: str
    rule_number: int
    name: str
    passed: bool
    required: bool = True
    details: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "rule_number": self.rule_number,
            "name": self.name,
            "passed": self.passed,
            "required": self.required,
            "details": self.details,
        }


@dataclass
class ActivationResult:
    """
    Complete result of a mirror activation gate evaluation.

    Attributes:
        mirror_id: The mirror that was evaluated.
        verdict: ALLOW or DENY.
        checks: All checks that were performed.
        fail_closed: Always True — this gate is fail-closed by design.
        evaluated_at: ISO timestamp of the evaluation.
        summary: Human-readable summary.
    """
    mirror_id: str
    verdict: ActivationVerdict
    checks: list[ActivationCheck] = field(default_factory=list)
    fail_closed: bool = True
    evaluated_at: str = ""
    summary: str = ""

    def __post_init__(self) -> None:
        if not self.evaluated_at:
            self.evaluated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @property
    def passed(self) -> bool:
        return self.verdict == ActivationVerdict.ALLOW

    @property
    def failed_checks(self) -> list[ActivationCheck]:
        return [c for c in self.checks if not c.passed]

    @property
    def passed_checks(self) -> list[ActivationCheck]:
        return [c for c in self.checks if c.passed]

    def to_dict(self) -> dict[str, Any]:
        return {
            "mirror_id": self.mirror_id,
            "verdict": self.verdict.value,
            "checks": [c.to_dict() for c in self.checks],
            "fail_closed": self.fail_closed,
            "evaluated_at": self.evaluated_at,
            "summary": self.summary,
            "passed_count": len(self.passed_checks),
            "failed_count": len(self.failed_checks),
            "total_checks": len(self.checks),
        }


# Patterns that indicate forbidden app-local logic in a mirror
FORBIDDEN_PATTERNS: list[str] = [
    r"app\.local\.",
    r"from\s+app\s+import",
    r"import\s+app\b",
    r"__main__",
    r"if\s+__name__\s*==\s*['\"]__main__['\"]",
    r"flask\.Flask\(",
    r"django\.setup\(",
    r"uvicorn\.run\(",
    r"\.env\b",
    r"hardcoded_secret",
    r"localhost:\d+",
]


class MirrorActivationGate:
    """
    Controls mirror activation with FAIL-CLOSED semantics.

    If ANY check fails, activation is denied. There are no overrides,
    no soft failures, no grace periods. A mirror must pass every check
    before it is allowed to activate.

    This gate enforces the L0.6 Mirror Invalidity Rules (rules 1-12).
    """

    def __init__(self) -> None:
        self._forbidden_patterns = [re.compile(p) for p in FORBIDDEN_PATTERNS]

    def evaluate_activation(
        self,
        mirror_id: str,
        manifest: Optional[dict[str, Any]] = None,
        enabled_slices: Optional[list[str]] = None,
        declared_slices: Optional[list[str]] = None,
        dependency_graph: Optional[dict[str, Any]] = None,
        trust_boundary: Optional[str] = None,
        reflection_statuses: Optional[dict[str, str]] = None,
        parity_fixtures: Optional[list[dict[str, Any]]] = None,
        drift_record_schema: Optional[dict[str, Any]] = None,
        breakaway_conditions: Optional[list[dict[str, Any]]] = None,
        truth_ownership: Optional[str] = None,
        mirror_source_code: Optional[list[str]] = None,
        lifecycle_state: Optional[str] = None,
        lifecycle_evidence: Optional[dict[str, Any]] = None,
        registry_entry: Optional[dict[str, Any]] = None,
    ) -> ActivationResult:
        """
        Evaluate all activation checks for a mirror.

        FAIL-CLOSED: If ANY check fails, the verdict is DENY.

        Args:
            mirror_id: Identifier of the mirror to evaluate.
            manifest: Parsed mirror-manifest.yaml content.
            enabled_slices: List of slices the mirror has enabled.
            declared_slices: List of slices declared in the manifest.
            dependency_graph: Parsed slice dependency graph.
            trust_boundary: Trust boundary identifier.
            reflection_statuses: Dict of reflection_id -> status string.
            parity_fixtures: List of parity fixture definitions.
            drift_record_schema: Drift record JSON schema.
            breakaway_conditions: List of breakaway condition definitions.
            truth_ownership: Truth ownership declaration.
            mirror_source_code: List of source code strings to scan.
            lifecycle_state: Current lifecycle state string.
            lifecycle_evidence: Evidence supporting the lifecycle state.
            registry_entry: Mirror's registry entry.

        Returns:
            ActivationResult with verdict and all check details.
        """
        checks: list[ActivationCheck] = []

        # Rule 1: mirror-manifest.yaml missing or invalid
        checks.append(self.check_manifest(manifest))

        # Rule 2: enabled slices not declared
        checks.append(self.check_registry_entry_slices(enabled_slices, declared_slices))

        # Rule 3: slice dependency graph missing or invalid
        checks.append(self.check_slice_validity(dependency_graph))

        # Rule 4: trust boundary undefined
        checks.append(self.check_trust_boundary(trust_boundary))

        # Rule 5: reflection status missing
        checks.append(self.check_reflection_statuses(reflection_statuses))

        # Rule 6: no parity fixtures exist
        checks.append(self.check_fixtures(parity_fixtures))

        # Rule 7: drift record schema missing
        checks.append(self.check_parity_baseline(drift_record_schema))

        # Rule 8: breakaway conditions missing
        checks.append(self._check_breakaway_conditions(breakaway_conditions))

        # Rule 9: truth ownership undefined
        checks.append(self._check_truth_ownership(truth_ownership))

        # Rule 10: mirror contains forbidden app-local logic
        checks.append(self.check_forbidden_patterns(mirror_source_code))

        # Rule 11: lifecycle state is inconsistent with evidence
        checks.append(self._check_lifecycle_consistency(lifecycle_state, lifecycle_evidence))

        # Rule 12: registry entry missing
        checks.append(self.check_registry_entry(registry_entry))

        # FAIL-CLOSED: ANY failure means DENY
        all_passed = all(c.passed for c in checks)
        verdict = ActivationVerdict.ALLOW if all_passed else ActivationVerdict.DENY

        failed = [c for c in checks if not c.passed]
        if all_passed:
            summary = f"Mirror '{mirror_id}' passed all {len(checks)} activation checks"
        else:
            summary = (
                f"Mirror '{mirror_id}' DENIED: {len(failed)}/{len(checks)} checks failed "
                f"[{', '.join(c.check_id for c in failed)}]"
            )

        return ActivationResult(
            mirror_id=mirror_id,
            verdict=verdict,
            checks=checks,
            summary=summary,
        )

    def check_manifest(self, manifest: Optional[dict[str, Any]]) -> ActivationCheck:
        """
        Rule 1: Check that mirror-manifest.yaml exists and is valid.

        A valid manifest must have: mirror_id, version, slices, trust_boundary.
        """
        check = ActivationCheck(
            check_id="manifest",
            rule_number=1,
            name="Mirror Manifest Valid",
            passed=False,
        )

        if manifest is None:
            check.details = "mirror-manifest.yaml is missing"
            return check

        required_fields = ["mirror_id", "version", "slices", "trust_boundary"]
        missing = [f for f in required_fields if f not in manifest]

        if missing:
            check.details = f"Manifest missing required fields: {missing}"
            return check

        if not isinstance(manifest.get("slices"), list):
            check.details = "Manifest 'slices' must be a list"
            return check

        check.passed = True
        check.details = "Manifest is valid"
        return check

    def check_registry_entry_slices(
        self,
        enabled_slices: Optional[list[str]],
        declared_slices: Optional[list[str]],
    ) -> ActivationCheck:
        """
        Rule 2: Check that all enabled slices are declared.
        """
        check = ActivationCheck(
            check_id="slices-declared",
            rule_number=2,
            name="Enabled Slices Declared",
            passed=False,
        )

        if enabled_slices is None:
            check.details = "Enabled slices list not provided"
            return check

        if declared_slices is None:
            check.details = "Declared slices list not provided"
            return check

        undeclared = set(enabled_slices) - set(declared_slices)
        if undeclared:
            check.details = f"Enabled but undeclared slices: {sorted(undeclared)}"
            return check

        check.passed = True
        check.details = f"All {len(enabled_slices)} enabled slices are declared"
        return check

    def check_slice_validity(
        self,
        dependency_graph: Optional[dict[str, Any]],
    ) -> ActivationCheck:
        """
        Rule 3: Check that the slice dependency graph exists and is structurally valid.
        """
        check = ActivationCheck(
            check_id="dependency-graph",
            rule_number=3,
            name="Slice Dependency Graph Valid",
            passed=False,
        )

        if dependency_graph is None:
            check.details = "Slice dependency graph is missing"
            return check

        if "nodes" not in dependency_graph or "edges" not in dependency_graph:
            check.details = "Dependency graph missing 'nodes' or 'edges'"
            return check

        nodes = set(dependency_graph["nodes"])
        edges = dependency_graph["edges"]

        # Quick cycle check using iterative DFS
        for start_node in nodes:
            visited: set[str] = set()
            rec_stack: set[str] = set()
            stack: list[tuple[str, int]] = [(start_node, 0)]
            path: list[str] = []

            while stack:
                node, idx = stack.pop()
                if idx == 0:
                    if node in rec_stack:
                        check.details = f"Circular dependency detected involving '{node}'"
                        return check
                    if node in visited:
                        continue
                    visited.add(node)
                    rec_stack.add(node)
                    path.append(node)

                neighbors = edges.get(node, [])
                if idx < len(neighbors):
                    stack.append((node, idx + 1))
                    stack.append((neighbors[idx], 0))
                else:
                    rec_stack.discard(node)
                    if path:
                        path.pop()

        # Check for references to undeclared nodes
        for node, deps in edges.items():
            for dep in deps:
                if dep not in nodes:
                    check.details = f"Edge references undeclared node '{dep}'"
                    return check

        check.passed = True
        check.details = f"Dependency graph valid: {len(nodes)} nodes"
        return check

    def check_trust_boundary(self, trust_boundary: Optional[str]) -> ActivationCheck:
        """
        Rule 4: Check that the trust boundary is defined.
        """
        check = ActivationCheck(
            check_id="trust-boundary",
            rule_number=4,
            name="Trust Boundary Defined",
            passed=False,
        )

        if not trust_boundary:
            check.details = "Trust boundary is undefined"
            return check

        check.passed = True
        check.details = f"Trust boundary defined: '{trust_boundary}'"
        return check

    def check_reflection_statuses(
        self,
        reflection_statuses: Optional[dict[str, str]],
    ) -> ActivationCheck:
        """
        Rule 5: Check that reflection statuses exist for all reflections.
        """
        check = ActivationCheck(
            check_id="reflection-statuses",
            rule_number=5,
            name="Reflection Statuses Present",
            passed=False,
        )

        if reflection_statuses is None:
            check.details = "Reflection statuses not provided"
            return check

        if not reflection_statuses:
            check.details = "No reflection statuses registered"
            return check

        valid_statuses = {"staged", "active", "frozen", "deprecated"}
        invalid = {
            rid: status for rid, status in reflection_statuses.items()
            if status not in valid_statuses
        }

        if invalid:
            check.details = f"Invalid reflection statuses: {invalid}"
            return check

        check.passed = True
        check.details = f"All {len(reflection_statuses)} reflection statuses valid"
        return check

    def check_fixtures(
        self,
        parity_fixtures: Optional[list[dict[str, Any]]],
    ) -> ActivationCheck:
        """
        Rule 6: Check that parity fixtures exist.
        """
        check = ActivationCheck(
            check_id="parity-fixtures",
            rule_number=6,
            name="Parity Fixtures Exist",
            passed=False,
        )

        if parity_fixtures is None:
            check.details = "Parity fixtures not provided"
            return check

        if len(parity_fixtures) == 0:
            check.details = "No parity fixtures defined"
            return check

        check.passed = True
        check.details = f"{len(parity_fixtures)} parity fixture(s) available"
        return check

    def check_parity_baseline(
        self,
        drift_record_schema: Optional[dict[str, Any]],
    ) -> ActivationCheck:
        """
        Rule 7: Check that drift record schema exists.
        """
        check = ActivationCheck(
            check_id="drift-record-schema",
            rule_number=7,
            name="Drift Record Schema Present",
            passed=False,
        )

        if drift_record_schema is None:
            check.details = "Drift record schema is missing"
            return check

        if not drift_record_schema:
            check.details = "Drift record schema is empty"
            return check

        check.passed = True
        check.details = "Drift record schema present"
        return check

    def _check_breakaway_conditions(
        self,
        breakaway_conditions: Optional[list[dict[str, Any]]],
    ) -> ActivationCheck:
        """
        Rule 8: Check that breakaway conditions are defined.
        """
        check = ActivationCheck(
            check_id="breakaway-conditions",
            rule_number=8,
            name="Breakaway Conditions Defined",
            passed=False,
        )

        if breakaway_conditions is None:
            check.details = "Breakaway conditions not provided"
            return check

        if len(breakaway_conditions) == 0:
            check.details = "No breakaway conditions defined"
            return check

        check.passed = True
        check.details = f"{len(breakaway_conditions)} breakaway condition(s) defined"
        return check

    def _check_truth_ownership(
        self,
        truth_ownership: Optional[str],
    ) -> ActivationCheck:
        """
        Rule 9: Check that truth ownership is defined.
        """
        check = ActivationCheck(
            check_id="truth-ownership",
            rule_number=9,
            name="Truth Ownership Defined",
            passed=False,
        )

        if not truth_ownership:
            check.details = "Truth ownership is undefined"
            return check

        check.passed = True
        check.details = f"Truth ownership: '{truth_ownership}'"
        return check

    def check_forbidden_patterns(
        self,
        mirror_source_code: Optional[list[str]],
    ) -> ActivationCheck:
        """
        Rule 10: Check that mirror does not contain forbidden app-local logic.
        """
        check = ActivationCheck(
            check_id="forbidden-patterns",
            rule_number=10,
            name="No Forbidden App-Local Logic",
            passed=False,
        )

        if mirror_source_code is None:
            check.details = "Mirror source code not provided for scanning"
            return check

        violations: list[str] = []
        for i, code in enumerate(mirror_source_code):
            for pattern in self._forbidden_patterns:
                matches = pattern.findall(code)
                if matches:
                    violations.append(
                        f"Source[{i}]: forbidden pattern '{pattern.pattern}' "
                        f"matched: {matches[:3]}"
                    )

        if violations:
            check.details = f"Forbidden patterns found: {violations[:5]}"
            return check

        check.passed = True
        check.details = "No forbidden patterns detected"
        return check

    def _check_lifecycle_consistency(
        self,
        lifecycle_state: Optional[str],
        lifecycle_evidence: Optional[dict[str, Any]],
    ) -> ActivationCheck:
        """
        Rule 11: Check that lifecycle state is consistent with evidence.
        """
        check = ActivationCheck(
            check_id="lifecycle-consistency",
            rule_number=11,
            name="Lifecycle State Consistent",
            passed=False,
        )

        if lifecycle_state is None:
            check.details = "Lifecycle state not provided"
            return check

        if lifecycle_evidence is None:
            check.details = "Lifecycle evidence not provided"
            return check

        valid_states = {"development", "staging", "active", "frozen", "deprecated"}
        if lifecycle_state not in valid_states:
            check.details = f"Invalid lifecycle state: '{lifecycle_state}'"
            return check

        # Check evidence supports the claimed state
        evidence_state = lifecycle_evidence.get("state")
        if evidence_state and evidence_state != lifecycle_state:
            check.details = (
                f"Lifecycle inconsistency: claimed '{lifecycle_state}', "
                f"evidence shows '{evidence_state}'"
            )
            return check

        # Active state requires parity evidence
        if lifecycle_state == "active":
            if not lifecycle_evidence.get("parity_verified"):
                check.details = (
                    "Active state requires parity_verified evidence"
                )
                return check

        check.passed = True
        check.details = f"Lifecycle state '{lifecycle_state}' consistent with evidence"
        return check

    def check_registry_entry(
        self,
        registry_entry: Optional[dict[str, Any]],
    ) -> ActivationCheck:
        """
        Rule 12: Check that the mirror has a registry entry.
        """
        check = ActivationCheck(
            check_id="registry-entry",
            rule_number=12,
            name="Registry Entry Present",
            passed=False,
        )

        if registry_entry is None:
            check.details = "Registry entry is missing"
            return check

        if not registry_entry:
            check.details = "Registry entry is empty"
            return check

        required = ["mirror_id", "registered_at"]
        missing = [f for f in required if f not in registry_entry]
        if missing:
            check.details = f"Registry entry missing fields: {missing}"
            return check

        check.passed = True
        check.details = "Registry entry present and valid"
        return check
