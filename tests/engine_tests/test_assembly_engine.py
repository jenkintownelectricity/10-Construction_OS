"""Tests for assembly engine."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.engines.assembly_engine.engine import run_assembly_engine
from runtime.models.assembly_model import AssemblyModel
from runtime.models.geometry_model import GeometryModel
from runtime.models.material_model import MaterialModel


class TestAssemblyEngine:
    def test_basic_assembly(self):
        assembly = AssemblyModel(
            name="Test Assembly",
            components=[{"name": "Beam", "type": "component"}],
            constraints=[{"description": "1 inch clearance", "type": "clearance"}],
            source_text="test",
        )
        result = run_assembly_engine(assembly)
        assert result["assembly_name"] == "Test Assembly"
        assert len(result["components"]) == 1
        assert result["build_status"] == "ready"

    def test_empty_assembly(self):
        assembly = AssemblyModel(name="Empty")
        result = run_assembly_engine(assembly)
        assert result["build_status"] == "incomplete"
        assert result["components"] == []

    def test_with_geometry_and_materials(self):
        assembly = AssemblyModel(
            name="Enriched",
            components=[{"name": "Beam", "type": "component"}],
        )
        geometry = GeometryModel(dimensions={"width": 12, "height": 26})
        materials = [MaterialModel(material_name="A992 Steel", manufacturer="Nucor")]

        result = run_assembly_engine(assembly, geometry=geometry, materials=materials)
        assert result["build_status"] == "ready"
        assert result["components"][0]["material_resolved"] is True
        assert result["components"][0]["geometry_resolved"] is True
        assert len(result["materials"]) == 1
