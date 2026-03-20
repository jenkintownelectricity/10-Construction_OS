"""
compatibility_reporter.py — Reports on compatibility between mirror and core.

Compatibility is the contract surface between a mirror and the core system.
A compatible mirror can slot in without friction. An incompatible one
creates coupling, which violates the doctrine.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class CompatibilityLevel(Enum):
    """Compatibility assessment level."""
    FULL = "full"
    PARTIAL = "partial"
    INCOMPATIBLE = "incompatible"
    UNKNOWN = "unknown"


@dataclass
class SchemaCheck:
    """
    Result of a single schema compatibility check.

    Attributes:
        field_name: The field or schema element checked.
        expected_type: Expected type or shape.
        actual_type: Actual type or shape found.
        compatible: Whether this field is compatible.
        details: Explanation of any issues.
    """
    field_name: str
    expected_type: str
    actual_type: str
    compatible: bool
    details: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "field_name": self.field_name,
            "expected_type": self.expected_type,
            "actual_type": self.actual_type,
            "compatible": self.compatible,
            "details": self.details,
        }


@dataclass
class CompatibilityReport:
    """
    Full compatibility report between a mirror and core.

    Attributes:
        mirror_id: Identifier of the mirror.
        core_version: Version of the core being compared against.
        level: Overall compatibility level.
        schema_checks: Results of individual schema checks.
        interface_compatible: Whether the interface contract is met.
        behavior_compatible: Whether behavioral parity is established.
        warnings: Non-blocking issues to be aware of.
        errors: Blocking issues preventing compatibility.
        generated_at: ISO timestamp of report generation.
    """
    mirror_id: str
    core_version: str
    level: CompatibilityLevel = CompatibilityLevel.UNKNOWN
    schema_checks: list[SchemaCheck] = field(default_factory=list)
    interface_compatible: bool = False
    behavior_compatible: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    generated_at: str = ""

    def __post_init__(self) -> None:
        if not self.generated_at:
            self.generated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self) -> dict[str, Any]:
        return {
            "mirror_id": self.mirror_id,
            "core_version": self.core_version,
            "level": self.level.value,
            "schema_checks": [sc.to_dict() for sc in self.schema_checks],
            "interface_compatible": self.interface_compatible,
            "behavior_compatible": self.behavior_compatible,
            "warnings": self.warnings,
            "errors": self.errors,
            "generated_at": self.generated_at,
        }


class CompatibilityReporter:
    """
    Checks and reports on compatibility between a mirror and the core system.

    Evaluates schema compatibility, interface contracts, and behavioral parity
    to produce a comprehensive compatibility report.

    Args:
        core_schema: Dictionary defining the core system's expected schema.
        core_version: Version string for the core system.
    """

    def __init__(
        self,
        core_schema: dict[str, Any],
        core_version: str = "1.0.0",
    ) -> None:
        self._core_schema = core_schema
        self._core_version = core_version
        self._reports: list[CompatibilityReport] = []

    @property
    def core_version(self) -> str:
        return self._core_version

    @property
    def reports(self) -> list[CompatibilityReport]:
        return list(self._reports)

    def check_schema_compatibility(
        self,
        mirror_schema: dict[str, Any],
    ) -> list[SchemaCheck]:
        """
        Check field-by-field schema compatibility between core and mirror.

        The core schema defines required fields with their expected types.
        The mirror schema is checked against these requirements.

        Args:
            mirror_schema: Dictionary defining the mirror's schema.

        Returns:
            List of SchemaCheck results.
        """
        checks: list[SchemaCheck] = []

        # Check all core-required fields exist in mirror
        for field_name, expected_type in self._core_schema.items():
            if field_name not in mirror_schema:
                checks.append(SchemaCheck(
                    field_name=field_name,
                    expected_type=str(expected_type),
                    actual_type="<missing>",
                    compatible=False,
                    details=f"Required field '{field_name}' missing from mirror schema",
                ))
            else:
                actual_type = mirror_schema[field_name]
                is_compatible = self._types_compatible(expected_type, actual_type)
                checks.append(SchemaCheck(
                    field_name=field_name,
                    expected_type=str(expected_type),
                    actual_type=str(actual_type),
                    compatible=is_compatible,
                    details="" if is_compatible else (
                        f"Type mismatch: expected '{expected_type}', got '{actual_type}'"
                    ),
                ))

        # Check for extra fields in mirror (warnings, not errors)
        for field_name in mirror_schema:
            if field_name not in self._core_schema:
                checks.append(SchemaCheck(
                    field_name=field_name,
                    expected_type="<not in core>",
                    actual_type=str(mirror_schema[field_name]),
                    compatible=True,
                    details=f"Extra field '{field_name}' in mirror (not in core schema)",
                ))

        return checks

    def _types_compatible(self, expected: Any, actual: Any) -> bool:
        """Check if two type descriptors are compatible."""
        if expected == actual:
            return True
        # Allow string type names to match
        exp_str = str(expected).lower().strip()
        act_str = str(actual).lower().strip()
        # Common compatible pairs
        compatible_pairs = {
            ("int", "integer"),
            ("str", "string"),
            ("bool", "boolean"),
            ("float", "number"),
            ("dict", "object"),
            ("list", "array"),
        }
        for a, b in compatible_pairs:
            if (exp_str == a and act_str == b) or (exp_str == b and act_str == a):
                return True
        return exp_str == act_str

    def check_compatibility(
        self,
        mirror_id: str,
        mirror_schema: dict[str, Any],
        interface_check: bool = True,
        behavior_check: bool = True,
        parity_pass_rate: float = 1.0,
        required_interfaces: Optional[list[str]] = None,
        mirror_interfaces: Optional[list[str]] = None,
    ) -> CompatibilityReport:
        """
        Perform a full compatibility check between mirror and core.

        Args:
            mirror_id: Identifier of the mirror.
            mirror_schema: The mirror's schema definition.
            interface_check: Whether the mirror implements required interfaces.
            behavior_check: Whether the mirror passes behavioral parity.
            parity_pass_rate: Pass rate from parity checks (0.0 to 1.0).
            required_interfaces: List of interface names the core requires.
            mirror_interfaces: List of interface names the mirror provides.

        Returns:
            A CompatibilityReport with the assessment.
        """
        report = CompatibilityReport(
            mirror_id=mirror_id,
            core_version=self._core_version,
        )

        # Schema checks
        report.schema_checks = self.check_schema_compatibility(mirror_schema)
        schema_failures = [sc for sc in report.schema_checks if not sc.compatible]

        # Interface compatibility
        if required_interfaces and mirror_interfaces is not None:
            missing_interfaces = set(required_interfaces) - set(mirror_interfaces)
            if missing_interfaces:
                report.interface_compatible = False
                report.errors.append(
                    f"Missing required interfaces: {sorted(missing_interfaces)}"
                )
            else:
                report.interface_compatible = True
        else:
            report.interface_compatible = interface_check

        # Behavior compatibility (based on parity)
        if parity_pass_rate >= 1.0:
            report.behavior_compatible = True
        elif parity_pass_rate >= 0.9:
            report.behavior_compatible = True
            report.warnings.append(
                f"Parity pass rate is {parity_pass_rate:.1%} (< 100%)"
            )
        else:
            report.behavior_compatible = False
            report.errors.append(
                f"Parity pass rate too low: {parity_pass_rate:.1%} (minimum 90%)"
            )

        if not behavior_check:
            report.behavior_compatible = False
            report.errors.append("Behavioral parity not established")

        # Schema errors
        if schema_failures:
            for sf in schema_failures:
                if sf.actual_type == "<missing>":
                    report.errors.append(sf.details)
                else:
                    report.errors.append(sf.details)

        # Extra fields are warnings
        extra_fields = [
            sc for sc in report.schema_checks
            if sc.expected_type == "<not in core>"
        ]
        for ef in extra_fields:
            report.warnings.append(ef.details)

        # Determine overall level
        if report.errors:
            if len(schema_failures) > len(report.schema_checks) / 2:
                report.level = CompatibilityLevel.INCOMPATIBLE
            else:
                report.level = CompatibilityLevel.PARTIAL
        elif report.warnings:
            report.level = CompatibilityLevel.PARTIAL
        else:
            report.level = CompatibilityLevel.FULL

        if not report.interface_compatible or not report.behavior_compatible:
            if report.level == CompatibilityLevel.FULL:
                report.level = CompatibilityLevel.PARTIAL

        self._reports.append(report)
        return report

    def generate_report(
        self,
        mirror_id: str,
        mirror_schema: dict[str, Any],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generate a compatibility report as a dictionary.

        This is a convenience wrapper around check_compatibility().

        Args:
            mirror_id: Identifier of the mirror.
            mirror_schema: The mirror's schema definition.
            **kwargs: Additional arguments passed to check_compatibility().

        Returns:
            Dictionary form of the CompatibilityReport.
        """
        report = self.check_compatibility(mirror_id, mirror_schema, **kwargs)
        return report.to_dict()
