"""
Dependency Resolver — Wave 14 Subsystem 6.

Validates that installation sequence dependencies are acyclic
and all referenced steps exist.
"""

from typing import Any


class DependencyResolutionError(Exception):
    """Raised when dependency resolution fails."""


def validate_dependencies(sequence: dict[str, Any]) -> list[str]:
    """
    Validate that a sequence's step dependencies are valid and acyclic.
    Returns list of errors. Empty means valid.
    """
    errors: list[str] = []
    steps = sequence.get("steps", [])
    if not steps:
        return errors

    step_numbers = {s["step_number"] for s in steps}

    # Check for duplicate step numbers
    if len(step_numbers) != len(steps):
        errors.append("Duplicate step numbers detected.")

    # Check dependencies reference valid steps
    for step in steps:
        sn = step["step_number"]
        deps = step.get("dependencies", [])
        for dep in deps:
            if dep not in step_numbers:
                errors.append(f"Step {sn}: dependency {dep} does not exist.")
            if dep >= sn:
                errors.append(f"Step {sn}: dependency {dep} is not a prior step (forward reference).")

    # Check for circular dependencies
    adjacency: dict[int, list[int]] = {s["step_number"]: s.get("dependencies", []) for s in steps}
    cycle = _detect_cycle(adjacency)
    if cycle:
        errors.append(f"Circular dependency detected in installation sequence.")

    return errors


def _detect_cycle(adjacency: dict[int, list[int]]) -> bool:
    """Detect cycles in dependency graph using DFS."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[int, int] = {node: WHITE for node in adjacency}

    def dfs(node: int) -> bool:
        color[node] = GRAY
        for dep in adjacency.get(node, []):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                return True
            if color[dep] == WHITE and dfs(dep):
                return True
        color[node] = BLACK
        return False

    for node in sorted(adjacency):
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False


def get_execution_order(sequence: dict[str, Any]) -> list[int]:
    """
    Compute a valid execution order (topological sort) for sequence steps.
    Returns ordered list of step numbers.
    """
    steps = sequence.get("steps", [])
    if not steps:
        return []

    adjacency: dict[int, list[int]] = {}
    in_degree: dict[int, int] = {}

    for step in steps:
        sn = step["step_number"]
        adjacency.setdefault(sn, [])
        in_degree.setdefault(sn, 0)

    for step in steps:
        sn = step["step_number"]
        for dep in step.get("dependencies", []):
            adjacency.setdefault(dep, []).append(sn)
            in_degree[sn] = in_degree.get(sn, 0) + 1

    # Kahn's algorithm
    queue = sorted([n for n in in_degree if in_degree[n] == 0])
    order: list[int] = []

    while queue:
        node = queue.pop(0)
        order.append(node)
        for neighbor in sorted(adjacency.get(node, [])):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
        queue.sort()

    if len(order) != len(steps):
        raise DependencyResolutionError("Cannot compute execution order — cycle detected.")

    return order
