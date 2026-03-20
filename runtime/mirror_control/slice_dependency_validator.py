"""
slice_dependency_validator.py — Validates slice dependency graphs.

Slices are the atomic units of mirror capability. Dependencies between
slices must be explicit, acyclic, and bounded. Undeclared or circular
dependencies violate the mirror architecture's detachability guarantee.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class DependencyGraph:
    """
    A directed graph of slice dependencies.

    Attributes:
        graph_id: Unique identifier for this graph.
        mirror_id: The mirror this graph describes.
        nodes: Set of slice IDs in the graph.
        edges: Dictionary mapping each slice to its declared dependencies.
        declared_boundaries: Set of slice IDs that mark trust boundaries.
        metadata: Additional graph metadata.
    """
    graph_id: str
    mirror_id: str
    nodes: set[str] = field(default_factory=set)
    edges: dict[str, list[str]] = field(default_factory=dict)
    declared_boundaries: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_node(self, slice_id: str) -> None:
        """Add a slice node to the graph."""
        self.nodes.add(slice_id)
        if slice_id not in self.edges:
            self.edges[slice_id] = []

    def add_edge(self, from_slice: str, to_slice: str) -> None:
        """
        Add a dependency edge: from_slice depends on to_slice.

        Both nodes are added if not already present.
        """
        self.add_node(from_slice)
        self.add_node(to_slice)
        if to_slice not in self.edges[from_slice]:
            self.edges[from_slice].append(to_slice)

    def get_dependencies(self, slice_id: str) -> list[str]:
        """Get direct dependencies of a slice."""
        return list(self.edges.get(slice_id, []))

    def get_dependents(self, slice_id: str) -> list[str]:
        """Get slices that depend on the given slice."""
        return [
            node for node, deps in self.edges.items()
            if slice_id in deps
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "mirror_id": self.mirror_id,
            "nodes": sorted(self.nodes),
            "edges": {k: sorted(v) for k, v in self.edges.items()},
            "declared_boundaries": sorted(self.declared_boundaries),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DependencyGraph:
        return cls(
            graph_id=data["graph_id"],
            mirror_id=data["mirror_id"],
            nodes=set(data.get("nodes", [])),
            edges={k: list(v) for k, v in data.get("edges", {}).items()},
            declared_boundaries=set(data.get("declared_boundaries", [])),
            metadata=data.get("metadata", {}),
        )


@dataclass
class ValidationIssue:
    """A single validation issue found in the dependency graph."""
    severity: str  # "error" or "warning"
    category: str  # e.g., "circular", "undeclared", "boundary"
    message: str
    affected_slices: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "affected_slices": self.affected_slices,
        }


class SliceDependencyValidator:
    """
    Validates slice dependency graphs for structural correctness.

    Checks for:
    - Circular dependencies (prohibited)
    - Undeclared dependencies (references to non-existent nodes)
    - Boundary violations (cross-boundary dependencies without declaration)
    - Orphaned nodes (no edges, potential dead code)
    """

    def __init__(self) -> None:
        self._issues: list[ValidationIssue] = []

    @property
    def issues(self) -> list[ValidationIssue]:
        return list(self._issues)

    def validate_graph(self, graph: DependencyGraph) -> tuple[bool, list[ValidationIssue]]:
        """
        Run all validation checks on a dependency graph.

        Args:
            graph: The DependencyGraph to validate.

        Returns:
            Tuple of (is_valid, issues).
            is_valid is True only if no error-level issues are found.
        """
        self._issues.clear()

        self._issues.extend(self.check_circular_dependencies(graph))
        self._issues.extend(self.check_undeclared_dependencies(graph))
        self._issues.extend(self.validate_slice_boundaries(graph))
        self._issues.extend(self._check_orphaned_nodes(graph))

        has_errors = any(issue.severity == "error" for issue in self._issues)
        return not has_errors, list(self._issues)

    def check_circular_dependencies(self, graph: DependencyGraph) -> list[ValidationIssue]:
        """
        Detect circular dependencies in the graph using DFS cycle detection.

        Args:
            graph: The DependencyGraph to check.

        Returns:
            List of ValidationIssues for each cycle found.
        """
        issues: list[ValidationIssue] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()
        cycles_found: list[list[str]] = []

        def _dfs(node: str, path: list[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.edges.get(node, []):
                if neighbor not in visited:
                    _dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # Found a cycle — extract it
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles_found.append(cycle)

            path.pop()
            rec_stack.discard(node)

        for node in graph.nodes:
            if node not in visited:
                _dfs(node, [])

        for cycle in cycles_found:
            issues.append(ValidationIssue(
                severity="error",
                category="circular",
                message=f"Circular dependency detected: {' -> '.join(cycle)}",
                affected_slices=list(set(cycle)),
            ))

        return issues

    def check_undeclared_dependencies(self, graph: DependencyGraph) -> list[ValidationIssue]:
        """
        Check for dependencies that reference slices not declared as nodes.

        Args:
            graph: The DependencyGraph to check.

        Returns:
            List of ValidationIssues for undeclared dependencies.
        """
        issues: list[ValidationIssue] = []

        for node, deps in graph.edges.items():
            for dep in deps:
                if dep not in graph.nodes:
                    issues.append(ValidationIssue(
                        severity="error",
                        category="undeclared",
                        message=(
                            f"Slice '{node}' depends on undeclared slice '{dep}'"
                        ),
                        affected_slices=[node, dep],
                    ))

        return issues

    def validate_slice_boundaries(self, graph: DependencyGraph) -> list[ValidationIssue]:
        """
        Validate that cross-boundary dependencies are properly declared.

        A boundary slice marks a trust boundary. Dependencies that cross
        from one side of a boundary to the other must be explicitly declared
        via the boundary node.

        Args:
            graph: The DependencyGraph to check.

        Returns:
            List of ValidationIssues for boundary violations.
        """
        issues: list[ValidationIssue] = []

        if not graph.declared_boundaries:
            return issues

        # Build sets of "inside" and "outside" nodes relative to each boundary
        # For simplicity: boundary nodes should be the intermediary.
        # Any non-boundary node that depends on a node "across" a boundary
        # without going through the boundary is a violation.

        boundary_nodes = graph.declared_boundaries

        for node in graph.nodes:
            if node in boundary_nodes:
                continue

            for dep in graph.edges.get(node, []):
                if dep in boundary_nodes:
                    continue  # Direct dependency on boundary is fine

                # Check if node and dep are on opposite sides of a boundary
                # by checking if any boundary sits between them
                for boundary in boundary_nodes:
                    node_reaches_boundary = self._can_reach(graph, node, boundary)
                    dep_reaches_boundary = self._can_reach(graph, dep, boundary)

                    # If dep is reachable from boundary but node doesn't go
                    # through boundary to reach dep, flag it
                    if (dep_reaches_boundary and
                            not self._path_goes_through(graph, node, dep, boundary)):
                        # Only flag if the dependency crosses the boundary concept
                        boundary_deps = set(graph.edges.get(boundary, []))
                        boundary_dependents = set(graph.get_dependents(boundary))
                        if node in boundary_dependents and dep in boundary_deps:
                            issues.append(ValidationIssue(
                                severity="warning",
                                category="boundary",
                                message=(
                                    f"Slice '{node}' depends on '{dep}' across "
                                    f"boundary '{boundary}' without going through it"
                                ),
                                affected_slices=[node, dep, boundary],
                            ))

        return issues

    def _can_reach(self, graph: DependencyGraph, start: str, target: str) -> bool:
        """Check if target is reachable from start via dependency edges."""
        visited: set[str] = set()
        stack = [start]
        while stack:
            current = stack.pop()
            if current == target:
                return True
            if current in visited:
                continue
            visited.add(current)
            stack.extend(graph.edges.get(current, []))
        return False

    def _path_goes_through(
        self,
        graph: DependencyGraph,
        start: str,
        target: str,
        waypoint: str,
    ) -> bool:
        """Check if all paths from start to target go through waypoint."""
        # If we can reach target without visiting waypoint, return False
        visited: set[str] = set()
        stack = [start]
        while stack:
            current = stack.pop()
            if current == waypoint:
                continue  # Skip the waypoint
            if current == target:
                return False  # Reached target without going through waypoint
            if current in visited:
                continue
            visited.add(current)
            stack.extend(graph.edges.get(current, []))
        return True

    def _check_orphaned_nodes(self, graph: DependencyGraph) -> list[ValidationIssue]:
        """Check for nodes with no incoming or outgoing edges."""
        issues: list[ValidationIssue] = []

        for node in graph.nodes:
            has_outgoing = bool(graph.edges.get(node, []))
            has_incoming = any(
                node in deps for deps in graph.edges.values()
            )
            if not has_outgoing and not has_incoming and len(graph.nodes) > 1:
                issues.append(ValidationIssue(
                    severity="warning",
                    category="orphaned",
                    message=f"Slice '{node}' is orphaned (no dependencies in or out)",
                    affected_slices=[node],
                ))

        return issues
