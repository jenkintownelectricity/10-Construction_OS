"""Boundary discipline tests — verify architectural constraints of Wave 12.

These tests scan source files to ensure:
- App surfaces do not import graph internals directly
- Navigation services do not duplicate BFS/traversal logic
- FilterEngine does not mutate the graph
- OverlayEngine does not create truth
- VisualStateMapper only maps, never computes readiness
"""

import os
import pytest


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPS_NAV_DIR = os.path.join(REPO_ROOT, "apps", "navigation")
RUNTIME_NAV_DIRS = [
    os.path.join(REPO_ROOT, "runtime", d)
    for d in [
        "navigation", "navigation_queries", "navigation_views",
        "navigation_filters", "navigation_state", "navigation_panels",
        "navigation_map", "navigation_list", "navigation_detail",
        "navigation_overlays",
    ]
]


def _read_py_files(directory: str) -> list[tuple[str, str]]:
    """Return (filename, content) for all .py files in directory."""
    results = []
    if not os.path.isdir(directory):
        return results
    for fname in os.listdir(directory):
        if fname.endswith(".py") and fname != "__init__.py":
            fpath = os.path.join(directory, fname)
            with open(fpath) as f:
                results.append((fname, f.read()))
    return results


# Forbidden direct graph imports in app surfaces
_FORBIDDEN_GRAPH_IMPORTS = [
    "from runtime.graph.graph_node import",
    "from runtime.graph.graph_edge import",
    "from runtime.graph.graph_index import",
    "from runtime.graph.materialize_graph import",
    "from runtime.graph_queries.query_engine import",
    "from runtime.readiness_routing.router import",
    "from runtime.impact_analysis.analyzer import",
]


class TestAppSurfacesNoGraphImports:
    def test_app_surfaces_no_graph_imports(self):
        """App surfaces must not import graph internals directly."""
        violations = []
        for fname, content in _read_py_files(APPS_NAV_DIR):
            for forbidden in _FORBIDDEN_GRAPH_IMPORTS:
                if forbidden in content:
                    violations.append(f"{fname} contains: {forbidden}")
        assert violations == [], (
            f"App surfaces import graph internals directly:\n"
            + "\n".join(violations)
        )


# BFS/traversal markers that indicate duplicated logic
_TRAVERSAL_MARKERS = [
    "deque(",
    "collections.deque",
    "queue.pop(0)",
    "queue.append(",
    "visited.add(",
    "BFS",
    "DFS",
]


class TestNavigationServicesNoTraversalDuplication:
    def test_navigation_services_no_traversal_duplication(self):
        """Runtime navigation modules must not duplicate BFS/traversal logic."""
        violations = []
        for nav_dir in RUNTIME_NAV_DIRS:
            for fname, content in _read_py_files(nav_dir):
                for marker in _TRAVERSAL_MARKERS:
                    if marker in content:
                        violations.append(f"{nav_dir}/{fname} contains traversal marker: {marker}")
        assert violations == [], (
            f"Navigation services duplicate traversal logic:\n"
            + "\n".join(violations)
        )


# Graph mutation patterns
_MUTATION_PATTERNS = [
    "add_node(",
    "add_edge(",
    ".nodes[",
    ".edges[",
    "graph.nodes =",
    "graph.edges =",
]


class TestFilterEngineNoGraphMutation:
    def test_filter_engine_no_graph_mutation(self):
        """FilterEngine must not mutate the graph."""
        fpath = os.path.join(REPO_ROOT, "runtime", "navigation_filters", "filter_engine.py")
        with open(fpath) as f:
            content = f.read()
        for pattern in _MUTATION_PATTERNS:
            assert pattern not in content, (
                f"filter_engine.py contains mutation pattern: {pattern}"
            )


# Truth-creating patterns
_TRUTH_CREATION_PATTERNS = [
    "readiness_state =",
    "owner_state =",
    "state_summary =",
]


class TestOverlayEngineNoTruthCreation:
    def test_overlay_engine_no_truth_creation(self):
        """OverlayEngine must not create truth — only annotate from runtime."""
        fpath = os.path.join(REPO_ROOT, "runtime", "navigation_overlays", "overlay_engine.py")
        with open(fpath) as f:
            content = f.read()
        # The overlay engine reads node.state_summary (via _node_summary helper)
        # which is fine. We check that it does not ASSIGN to graph node attrs directly.
        assert "node.state_summary =" not in content, (
            "overlay_engine.py mutates node.state_summary directly"
        )
        assert "node.readiness_state =" not in content, (
            "overlay_engine.py assigns node.readiness_state directly"
        )
        assert "node.owner_state =" not in content, (
            "overlay_engine.py assigns node.owner_state directly"
        )


class TestVisualStateDoesNotRedefineReadiness:
    def test_visual_state_does_not_redefine_readiness(self):
        """VisualStateMapper must only map, not compute readiness."""
        fpath = os.path.join(REPO_ROOT, "runtime", "navigation_state", "visual_state.py")
        with open(fpath) as f:
            content = f.read()
        # Should not import graph traversal engines
        assert "from runtime.graph_queries" not in content
        assert "from runtime.readiness_routing" not in content
        assert "from runtime.impact_analysis" not in content
        # Should not do BFS/DFS
        assert "deque" not in content
        assert "queue" not in content
