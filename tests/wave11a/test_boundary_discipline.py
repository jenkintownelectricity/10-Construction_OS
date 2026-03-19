"""L17 Boundary Discipline tests — verify architectural layer separation.

These tests scan source files to enforce that graph semantics don't leak
into kernel contracts, registry catalogs, VKBUS observers, or app layers.
"""

import os
import ast

import pytest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONTRACTS_DIR = os.path.join(REPO_ROOT, "contracts")
APPS_DIR = os.path.join(REPO_ROOT, "apps")


def _python_files_in(directory):
    """Yield all .py file paths under *directory*."""
    if not os.path.isdir(directory):
        return
    for root, _dirs, files in os.walk(directory):
        for fname in files:
            if fname.endswith(".py"):
                yield os.path.join(root, fname)


def _file_imports_module(filepath, module_fragment):
    """Return True if *filepath* imports anything containing *module_fragment*."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except (OSError, UnicodeDecodeError):
        return False

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if module_fragment in alias.name:
                    return True
        elif isinstance(node, ast.ImportFrom):
            if node.module and module_fragment in node.module:
                return True
    return False


class TestBoundaryDiscipline:
    """L17: Verify layer boundaries are not violated."""

    def test_kernel_no_project_graph_instances(self):
        """Kernel contracts must not import or instantiate ConditionGraph.

        The contracts/ directory should contain JSON schemas and typing
        contracts only — no runtime graph usage.
        """
        if not os.path.isdir(CONTRACTS_DIR):
            pytest.skip("contracts/ directory not found")

        violations = []
        for fpath in _python_files_in(CONTRACTS_DIR):
            if _file_imports_module(fpath, "condition_graph"):
                violations.append(fpath)
            if _file_imports_module(fpath, "ConditionGraph"):
                violations.append(fpath)

        assert violations == [], (
            f"Kernel contracts must not import ConditionGraph: {violations}"
        )

    def test_registry_no_graph_execution(self):
        """Registry files must be JSON catalogs only, not executing graph logic.

        If a registry/ directory exists, its .py files must not import
        graph modules.
        """
        registry_dir = os.path.join(REPO_ROOT, "registry")
        if not os.path.isdir(registry_dir):
            # No registry directory means the constraint is trivially satisfied
            return

        violations = []
        for fpath in _python_files_in(registry_dir):
            for fragment in ("condition_graph", "materialize_graph", "graph_node", "graph_edge"):
                if _file_imports_module(fpath, fragment):
                    violations.append((fpath, fragment))

        assert violations == [], (
            f"Registry files must not import graph modules: {violations}"
        )

    def test_vkbus_observer_only(self):
        """VKBUS observer (if present) must have no mutation methods on the graph.

        This checks that no file in a vkbus/ directory calls add_node, add_edge,
        or directly mutates a ConditionGraph.
        """
        vkbus_dir = os.path.join(REPO_ROOT, "vkbus")
        if not os.path.isdir(vkbus_dir):
            # No vkbus directory — constraint trivially satisfied
            return

        mutation_patterns = ("add_node", "add_edge", ".nodes[", ".edges[")
        violations = []
        for fpath in _python_files_in(vkbus_dir):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except (OSError, UnicodeDecodeError):
                continue
            for pat in mutation_patterns:
                if pat in content:
                    violations.append((fpath, pat))

        assert violations == [], (
            f"VKBUS observer must not contain graph mutation calls: {violations}"
        )

    def test_app_layers_no_graph_semantics(self):
        """The apps/ directory must not import graph modules directly.

        Apps should consume graph results through higher-level APIs, not
        import condition_graph, graph_node, etc. directly.
        """
        if not os.path.isdir(APPS_DIR):
            pytest.skip("apps/ directory not found")

        graph_module_fragments = (
            "runtime.graph.",
            "runtime.graph_nodes.",
            "runtime.graph_edges.",
            "runtime.graph_validation.",
            "runtime.graph_queries.",
            "runtime.graph_materialization.",
            "runtime.readiness_routing.",
            "runtime.impact_analysis.",
        )

        violations = []
        for fpath in _python_files_in(APPS_DIR):
            for fragment in graph_module_fragments:
                if _file_imports_module(fpath, fragment):
                    violations.append((fpath, fragment))

        assert violations == [], (
            f"App layer must not import graph modules directly: {violations}"
        )
