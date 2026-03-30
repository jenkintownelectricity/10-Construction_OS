"""
Construction_Runtime — public API.

Import runtime bridge functions here so external consumers can write:

    from runtime import evaluate_condition_graph

Engine internals must never be imported directly by other repositories.
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
