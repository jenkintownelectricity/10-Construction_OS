"""
Construction Cognitive Bus v0.1 — Router.

Produces routing decisions only. No network delivery.
Maps event_class to target identifiers for downstream consumers.
"""

from bus.models import make_routing_decision

# Routing table: event_class -> list of target identifiers
ROUTING_TABLE: dict[str, list[str]] = {
    "ExternallyValidatedEvent": ["awareness_cache"],
    "Observation": ["diagnostics"],
    "Proposal": ["awareness_cache", "diagnostics"],
}


def route(event: dict) -> dict:
    """Produce a routing decision for an admitted event.

    Returns a routing decision dict with target list.
    Unknown event classes produce an empty target list.
    """
    event_class = event.get("event_class", "")
    targets = ROUTING_TABLE.get(event_class, [])
    return make_routing_decision(event, targets)
