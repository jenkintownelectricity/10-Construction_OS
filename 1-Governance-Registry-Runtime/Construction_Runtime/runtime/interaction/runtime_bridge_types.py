"""
Runtime Bridge Types

Typed contracts for the InteractionKernel ↔ Runtime bridge.
All types are frozen dataclasses — the bridge never mutates truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Inputs ──────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ChangeSet:
    """Input to evaluateConditionGraph — describes what changed."""

    graph: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResolutionContext:
    """Input to resolveDetail — a single condition needing detail resolution."""

    condition: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RenderManifest:
    """Input to renderArtifact — resolved detail ready for rendering."""

    condition: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StateSnapshot:
    """Input to validateState — a graph or resolution manifest to validate."""

    kind: str = ""  # "condition_graph" | "resolution_manifest"
    payload: dict[str, Any] = field(default_factory=dict)


# ── Outputs ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ConditionGraphResult:
    """Output of evaluateConditionGraph."""

    success: bool = False
    errors: tuple[str, ...] = ()
    node_count: int = 0
    edge_count: int = 0


@dataclass(frozen=True)
class DetailResult:
    """Output of resolveDetail."""

    resolved: bool = False
    detail_id: str = ""
    detail_family: str = ""
    components: tuple[dict[str, Any], ...] = ()
    relationships: tuple[dict[str, str], ...] = ()
    parameter_bindings: dict[str, Any] = field(default_factory=dict)
    errors: tuple[dict[str, str], ...] = ()


@dataclass(frozen=True)
class ArtifactResult:
    """Output of renderArtifact."""

    success: bool = False
    condition_id: str = ""
    detail_id: str = ""
    render_status: str = ""
    format: str = ""
    svg_content: str = ""
    instruction_count: int = 0
    element_count: int = 0
    errors: tuple[dict[str, str], ...] = ()


@dataclass(frozen=True)
class ValidationStateResult:
    """Output of validateState."""

    valid: bool = False
    errors: tuple[str, ...] = ()
