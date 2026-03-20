"""
Tests for GraphValidator — Wave 17A.

Tests: validation correctness, kernel immutability checks, partition compliance.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.identity_allocator import IdentityAllocator
from runtime.reference_graph.node_registry import NodeRegistry
from runtime.reference_graph.edge_registry import EdgeRegistry
from runtime.reference_graph.lineage_engine import LineageEngine
from runtime.reference_graph.validator import GraphValidator


def _make_valid_graph():
    alloc = IdentityAllocator()
    nodes = NodeRegistry(alloc)
    edges = EdgeRegistry(nodes)

    detail = nodes.register(
        object_type="DETAIL", scope="global",
        partition="global_kernel_partition",
        source_system="CK", source_reference="D-001",
        authority_type="kernel_canonical",
    )
    variant = nodes.register(
        object_type="VARIANT", scope="p1",
        partition="global_runtime_partition",
        source_system="CR", source_reference="V-001",
        authority_type="runtime_derived",
    )

    edges.register("derived_from", variant["graph_id"], detail["graph_id"])

    lineage = LineageEngine(nodes, edges)
    validator = GraphValidator(nodes, edges, lineage)

    return nodes, edges, validator, {"detail": detail, "variant": variant}


class TestValidGraphPasses:
    """Valid graphs must pass all checks."""

    def test_valid_graph_passes_all_checks(self):
        _, _, validator, _ = _make_valid_graph()
        report = validator.validate_reference_graph()
        assert report["valid"] is True
        assert report["total_errors"] == 0

    def test_check_count(self):
        _, _, validator, _ = _make_valid_graph()
        report = validator.validate_reference_graph()
        assert report["checks_run"] >= 5


class TestKernelImmutability:
    """Kernel nodes must have kernel_canonical authority."""

    def test_kernel_node_with_correct_authority_passes(self):
        _, _, validator, _ = _make_valid_graph()
        report = validator.validate_reference_graph()
        # Find the kernel_immutability result
        ki = [r for r in report["results"] if r["check"] == "kernel_immutability"]
        assert len(ki) == 1
        assert ki[0]["valid"] is True


class TestPartitionValidation:
    """Partition compliance checks."""

    def test_partition_compliance_passes(self):
        _, _, validator, _ = _make_valid_graph()
        report = validator.validate_reference_graph()
        pc = [r for r in report["results"] if r["check"] == "partition_compliance"]
        assert len(pc) == 1
        assert pc[0]["valid"] is True


class TestRelationshipRuleValidation:
    """Relationship rules must be enforced."""

    def test_relationship_rules_pass(self):
        _, _, validator, _ = _make_valid_graph()
        report = validator.validate_reference_graph()
        rr = [r for r in report["results"] if r["check"] == "relationship_rules"]
        assert len(rr) == 1
        assert rr[0]["valid"] is True
