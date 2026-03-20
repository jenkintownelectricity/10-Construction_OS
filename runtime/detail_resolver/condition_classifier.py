"""
Condition Classifier — Wave 14 Subsystem 2.

Maps condition graph node types to kernel condition types for detail resolution.
Fail-closed: unsupported mappings return UNSUPPORTED.
"""

from typing import Any

# Mapping from condition graph node types to kernel detail condition enums
CONDITION_TYPE_MAP: dict[str, str] = {
    "ROOF_FIELD": "ROOF_FIELD",
    "PARAPET": "PARAPET",
    "EDGE": "ROOF_TO_EDGE",
    "DRAIN": "DRAIN",
    "SCUPPER": "SCUPPER",
    "CURB": "CURB",
    "PIPE_PENETRATION": "PIPE",
    "EXPANSION_JOINT": "EXPANSION_JOINT",
}

# Kernel condition types that have canonical detail families
RESOLVABLE_CONDITIONS = frozenset([
    "PARAPET", "VERTICAL_WALL", "ROOF_TO_WALL", "ROOF_TO_EDGE",
    "PIPE", "CURB", "DRAIN", "SCUPPER", "EXPANSION_JOINT",
])

# Conditions that exist in the kernel schema but have no detail families yet
KNOWN_BUT_UNRESOLVABLE = frozenset([
    "THRESHOLD", "INSIDE_CORNER", "OUTSIDE_CORNER", "ROOF_FIELD",
])


class ConditionClassification:
    """Result of classifying a condition node."""

    def __init__(
        self,
        node_id: str,
        graph_condition_type: str,
        kernel_condition: str | None,
        status: str,
        reason: str,
    ):
        self.node_id = node_id
        self.graph_condition_type = graph_condition_type
        self.kernel_condition = kernel_condition
        self.status = status  # SUPPORTED | UNSUPPORTED | UNKNOWN
        self.reason = reason


def classify_condition(node: dict[str, Any]) -> ConditionClassification:
    """
    Classify a condition graph node for detail resolution.
    Returns classification with status and reason.
    Fail-closed: unknown types return UNSUPPORTED.
    """
    node_id = node.get("node_id", "UNKNOWN")
    condition_type = node.get("condition_type", "")

    if not condition_type:
        return ConditionClassification(
            node_id=node_id,
            graph_condition_type="",
            kernel_condition=None,
            status="UNSUPPORTED",
            reason="Empty condition_type on node.",
        )

    kernel_condition = CONDITION_TYPE_MAP.get(condition_type)

    if kernel_condition is None:
        return ConditionClassification(
            node_id=node_id,
            graph_condition_type=condition_type,
            kernel_condition=None,
            status="UNSUPPORTED",
            reason=f"Condition type '{condition_type}' has no kernel mapping.",
        )

    if kernel_condition in KNOWN_BUT_UNRESOLVABLE:
        return ConditionClassification(
            node_id=node_id,
            graph_condition_type=condition_type,
            kernel_condition=kernel_condition,
            status="UNKNOWN",
            reason=f"Kernel condition '{kernel_condition}' exists but has no canonical detail families.",
        )

    if kernel_condition in RESOLVABLE_CONDITIONS:
        return ConditionClassification(
            node_id=node_id,
            graph_condition_type=condition_type,
            kernel_condition=kernel_condition,
            status="SUPPORTED",
            reason=f"Condition '{kernel_condition}' maps to canonical detail families.",
        )

    return ConditionClassification(
        node_id=node_id,
        graph_condition_type=condition_type,
        kernel_condition=kernel_condition,
        status="UNSUPPORTED",
        reason=f"Kernel condition '{kernel_condition}' not in resolvable set.",
    )
