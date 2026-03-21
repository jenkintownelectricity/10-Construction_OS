"""
Interaction layer — public entrypoints for runtime engines.

External consumers import from here, never from engine internals.
"""

from runtime.interaction.runtime_bridge import (
    evaluate_condition_graph,
    resolve_detail,
    render_artifact,
    validate_state,
)

__all__ = [
    "evaluate_condition_graph",
    "resolve_detail",
    "render_artifact",
    "validate_state",
]
