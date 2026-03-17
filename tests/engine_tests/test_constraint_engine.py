"""Tests for constraint engine."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.engines.constraint_engine.engine import run_constraint_engine
from runtime.models.assembly_model import AssemblyModel


class TestConstraintEngine:
    def test_valid_assembly(self):
        assembly = AssemblyModel(
            name="Valid Assembly",
            components=[{"name": "Beam", "type": "component"}],
            constraints=[{"description": "1 inch", "type": "clearance"}],
            source_text="test input",
        )
        result = run_constraint_engine(assembly)
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0

    def test_empty_assembly_fails(self):
        """Constraint engine must fail when assembly has no components."""
        assembly = AssemblyModel(name="Empty")
        result = run_constraint_engine(assembly)
        assert result["is_valid"] is False
        assert any("no components" in e.lower() for e in result["errors"])

    def test_missing_name_warns(self):
        assembly = AssemblyModel(
            components=[{"name": "Beam", "type": "component"}],
            source_text="test",
        )
        result = run_constraint_engine(assembly)
        assert result["is_valid"] is True
        assert any("no name" in w.lower() for w in result["warnings"])

    def test_unnamed_component_fails(self):
        assembly = AssemblyModel(
            name="Bad Components",
            components=[{"name": "", "type": "component"}],
            source_text="test",
        )
        result = run_constraint_engine(assembly)
        assert result["is_valid"] is False
        assert any("no name" in e.lower() for e in result["errors"])

    def test_empty_interface_constraint_fails(self):
        assembly = AssemblyModel(
            name="Interface Test",
            components=[{"name": "Beam", "type": "component"}],
            constraints=[{"description": "", "type": "interface"}],
            source_text="test",
        )
        result = run_constraint_engine(assembly)
        assert result["is_valid"] is False

    def test_checks_run_reported(self):
        assembly = AssemblyModel(name="Check Test", components=[{"name": "A", "type": "c"}])
        result = run_constraint_engine(assembly)
        assert len(result["checks_run"]) > 0
        assert "components_present" in result["checks_run"]
