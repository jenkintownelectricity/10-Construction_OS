"""
Construction Cognitive Bus v0.1 — Emitter policy.

Validates that the source_component of an event is an allowed emitter.
Unknown and explicitly denied emitters are rejected.
"""

from bus.config import ALLOWED_EMITTERS, DENIED_EMITTERS


def validate_emitter(source_component: str) -> tuple[bool, str]:
    """Check whether the emitter is allowed.

    Returns (allowed: bool, reason: str).
    """
    if not source_component:
        return False, "source_component is empty"

    if source_component in DENIED_EMITTERS:
        return False, f"emitter explicitly denied: {source_component}"

    if source_component not in ALLOWED_EMITTERS:
        return False, f"emitter not in allowed set: {source_component}"

    return True, "emitter allowed"
