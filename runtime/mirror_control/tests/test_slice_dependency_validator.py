"""
Tests for slice_dependency_validator.py — DependencyGraph and SliceDependencyValidator.
"""

from __future__ import annotations

import unittest

from runtime.mirror_control.slice_dependency_validator import (
    DependencyGraph,
    SliceDependencyValidator,
)


class TestDependencyGraph(unittest.TestCase):
    """Tests for the DependencyGraph dataclass."""

    def test_add_node(self) -> None:
        graph = DependencyGraph(graph_id="g-1", mirror_id="m-1")
        graph.add_node("slice-a")
        self.assertIn("slice-a", graph.nodes)
        self.assertEqual(graph.edges["slice-a"], [])

    def test_add_edge(self) -> None:
        graph = DependencyGraph(graph_id="g-1", mirror_id="m-1")
        graph.add_edge("slice-a", "slice-b")
        self.assertIn("slice-a", graph.nodes)
        self.assertIn("slice-b", graph.nodes)
        self.assertIn("slice-b", graph.edges["slice-a"])

    def test_add_edge_no_duplicate(self) -> None:
        graph = DependencyGraph(graph_id="g-1", mirror_id="m-1")
        graph.add_edge("a", "b")
        graph.add_edge("a", "b")
        self.assertEqual(graph.edges["a"].count("b"), 1)

    def test_get_dependencies(self) -> None:
        graph = DependencyGraph(graph_id="g-1", mirror_id="m-1")
        graph.add_edge("a", "b")
        graph.add_edge("a", "c")
        deps = graph.get_dependencies("a")
        self.assertIn("b", deps)
        self.assertIn("c", deps)

    def test_get_dependencies_empty(self) -> None:
        graph = DependencyGraph(graph_id="g-1", mirror_id="m-1")
        graph.add_node("orphan")
        self.assertEqual(graph.get_dependencies("orphan"), [])

    def test_get_dependents(self) -> None:
        graph = DependencyGraph(graph_id="g-1", mirror_id="m-1")
        graph.add_edge("a", "c")
        graph.add_edge("b", "c")
        dependents = graph.get_dependents("c")
        self.assertIn("a", dependents)
        self.assertIn("b", dependents)

    def test_to_dict_roundtrip(self) -> None:
        graph = DependencyGraph(
            graph_id="g-rt",
            mirror_id="m-rt",
            declared_boundaries={"boundary-1"},
        )
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")

        d = graph.to_dict()
        restored = DependencyGraph.from_dict(d)
        self.assertEqual(restored.graph_id, "g-rt")
        self.assertEqual(restored.nodes, {"a", "b", "c"})
        self.assertIn("b", restored.edges["a"])
        self.assertIn("boundary-1", restored.declared_boundaries)


class TestSliceDependencyValidator(unittest.TestCase):
    """Tests for the SliceDependencyValidator class."""

    def setUp(self) -> None:
        self.validator = SliceDependencyValidator()

    def test_valid_acyclic_graph(self) -> None:
        graph = DependencyGraph(graph_id="g-1", mirror_id="m-1")
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        is_valid, issues = self.validator.validate_graph(graph)
        errors = [i for i in issues if i.severity == "error"]
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_circular_dependency_detected(self) -> None:
        graph = DependencyGraph(graph_id="g-2", mirror_id="m-1")
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("c", "a")
        is_valid, issues = self.validator.validate_graph(graph)
        self.assertFalse(is_valid)
        circular_issues = [i for i in issues if i.category == "circular"]
        self.assertGreater(len(circular_issues), 0)

    def test_self_loop_detected(self) -> None:
        graph = DependencyGraph(graph_id="g-3", mirror_id="m-1")
        graph.add_edge("a", "a")
        is_valid, issues = self.validator.validate_graph(graph)
        self.assertFalse(is_valid)

    def test_undeclared_dependency(self) -> None:
        graph = DependencyGraph(graph_id="g-4", mirror_id="m-1")
        graph.add_node("a")
        # Manually add an edge referencing a non-existent node
        graph.edges["a"] = ["phantom"]
        issues = self.validator.check_undeclared_dependencies(graph)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].category, "undeclared")
        self.assertIn("phantom", issues[0].affected_slices)

    def test_orphaned_node_warning(self) -> None:
        graph = DependencyGraph(graph_id="g-5", mirror_id="m-1")
        graph.add_node("connected-a")
        graph.add_node("connected-b")
        graph.add_edge("connected-a", "connected-b")
        graph.add_node("orphan")
        is_valid, issues = self.validator.validate_graph(graph)
        orphan_issues = [i for i in issues if i.category == "orphaned"]
        self.assertGreater(len(orphan_issues), 0)
        self.assertEqual(orphan_issues[0].severity, "warning")

    def test_single_node_not_orphaned(self) -> None:
        graph = DependencyGraph(graph_id="g-6", mirror_id="m-1")
        graph.add_node("solo")
        is_valid, issues = self.validator.validate_graph(graph)
        orphan_issues = [i for i in issues if i.category == "orphaned"]
        self.assertEqual(len(orphan_issues), 0)

    def test_boundary_validation_no_boundaries(self) -> None:
        graph = DependencyGraph(graph_id="g-7", mirror_id="m-1")
        graph.add_edge("a", "b")
        issues = self.validator.validate_slice_boundaries(graph)
        self.assertEqual(len(issues), 0)

    def test_complex_valid_graph(self) -> None:
        graph = DependencyGraph(graph_id="g-8", mirror_id="m-1")
        graph.add_edge("auth", "user-store")
        graph.add_edge("auth", "token-service")
        graph.add_edge("api", "auth")
        graph.add_edge("api", "data-layer")
        graph.add_edge("data-layer", "user-store")
        is_valid, issues = self.validator.validate_graph(graph)
        errors = [i for i in issues if i.severity == "error"]
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_issues_property(self) -> None:
        graph = DependencyGraph(graph_id="g-9", mirror_id="m-1")
        graph.add_edge("a", "b")
        self.validator.validate_graph(graph)
        issues = self.validator.issues
        self.assertIsInstance(issues, list)

    def test_validate_clears_previous_issues(self) -> None:
        graph1 = DependencyGraph(graph_id="g-10a", mirror_id="m-1")
        graph1.add_edge("a", "b")
        graph1.add_edge("b", "a")
        self.validator.validate_graph(graph1)
        count1 = len(self.validator.issues)

        graph2 = DependencyGraph(graph_id="g-10b", mirror_id="m-1")
        graph2.add_edge("x", "y")
        self.validator.validate_graph(graph2)
        count2 = len([i for i in self.validator.issues if i.severity == "error"])
        self.assertEqual(count2, 0)
        self.assertNotEqual(len(self.validator.issues), count1)

    def test_issue_to_dict(self) -> None:
        graph = DependencyGraph(graph_id="g-11", mirror_id="m-1")
        graph.add_edge("a", "b")
        graph.add_edge("b", "a")
        self.validator.validate_graph(graph)
        for issue in self.validator.issues:
            d = issue.to_dict()
            self.assertIn("severity", d)
            self.assertIn("category", d)
            self.assertIn("message", d)


if __name__ == "__main__":
    unittest.main()
