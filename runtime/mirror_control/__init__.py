"""
runtime.mirror_control — Command D: Parity / Drift / Breakaway Machinery

MASTER DOCTRINE:
    Connected by mirrors, never hard-wired.
    Sold by capability, detachable by design.
    Cooperate without entanglement.

This package provides the runtime control system for the Mirror Architecture:
    - Parity checking between source and mirror behavior
    - Drift recording and threshold enforcement
    - Reflection status lifecycle management
    - Compatibility reporting between mirror and core
    - Breakaway evaluation for safe detachment
    - Slice dependency graph validation
    - Mirror activation gating with fail-closed semantics
"""

from runtime.mirror_control.parity_runner import (
    ParityFixture,
    ParityResult,
    ParityRunner,
)
from runtime.mirror_control.drift_recorder import (
    DriftRecord,
    DriftRecorder,
    DriftSeverity,
)
from runtime.mirror_control.reflection_status_manager import (
    ReflectionStatus,
    ReflectionStatusManager,
)
from runtime.mirror_control.compatibility_reporter import (
    CompatibilityReport,
    CompatibilityReporter,
)
from runtime.mirror_control.breakaway_evaluator import (
    BreakawayCondition,
    BreakawayEvaluator,
    BreakawayRecord,
)
from runtime.mirror_control.slice_dependency_validator import (
    DependencyGraph,
    SliceDependencyValidator,
)
from runtime.mirror_control.mirror_activation_gate import (
    ActivationCheck,
    ActivationResult,
    MirrorActivationGate,
)

__all__ = [
    "ParityFixture",
    "ParityResult",
    "ParityRunner",
    "DriftRecord",
    "DriftRecorder",
    "DriftSeverity",
    "ReflectionStatus",
    "ReflectionStatusManager",
    "CompatibilityReport",
    "CompatibilityReporter",
    "BreakawayCondition",
    "BreakawayEvaluator",
    "BreakawayRecord",
    "DependencyGraph",
    "SliceDependencyValidator",
    "ActivationCheck",
    "ActivationResult",
    "MirrorActivationGate",
]
