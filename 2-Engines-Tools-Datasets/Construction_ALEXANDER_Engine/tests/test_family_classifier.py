"""Unit tests for family classification."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.family_classifier import classify_family
from unittest.mock import MagicMock


def _mock_kernel(families_by_domain=None):
    kernel = MagicMock()
    kernel.get_families_by_domain_key = MagicMock(return_value=families_by_domain or [])
    return kernel


def _normalized(condition_type="roof_edge", interface_condition=None):
    n = {
        "condition_id": "COND-001",
        "condition_type": condition_type,
        "zone_id": "zone-A1",
        "interface_condition": interface_condition,
        "dimensions": {},
        "material_preferences": [],
        "method_preference": None,
        "manufacturer_refs": [],
        "climate_context": {},
        "system_type": None,
    }
    return n


def test_single_family_match():
    family = {"id": "DNA-CONSTR-FAM-EDGE-001-R1", "name": "Roof Edge", "description": "Edge family"}
    kernel = _mock_kernel([family])
    result = classify_family(_normalized("roof_edge"), kernel)
    assert result["matched"] is True
    assert result["family_id"] == "DNA-CONSTR-FAM-EDGE-001-R1"
    assert result["confidence"] == 1.0


def test_no_family_match():
    kernel = _mock_kernel([])
    result = classify_family(_normalized("roof_edge"), kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] == "MISSING_TRUTH"


def test_unmappable_condition_type():
    kernel = _mock_kernel()
    result = classify_family(_normalized("interface"), kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] == "NO_FAMILY_MATCH"


def test_interface_with_interface_condition():
    family = {"id": "DNA-CONSTR-FAM-DRAIN-003-R1", "name": "Drain", "description": "Drain family"}
    kernel = _mock_kernel([family])
    result = classify_family(_normalized("interface", interface_condition="drain"), kernel)
    assert result["matched"] is True
    assert result["family_id"] == "DNA-CONSTR-FAM-DRAIN-003-R1"


def test_parapet_condition_maps():
    family = {"id": "DNA-CONSTR-FAM-PARAPET-002-R1", "name": "Parapet", "description": "Parapet family"}
    kernel = _mock_kernel([family])
    result = classify_family(_normalized("parapet"), kernel)
    assert result["matched"] is True
    assert result["family_id"] == "DNA-CONSTR-FAM-PARAPET-002-R1"


def test_drain_condition_maps():
    family = {"id": "DNA-CONSTR-FAM-DRAIN-003-R1", "name": "Drain", "description": "Drain family"}
    kernel = _mock_kernel([family])
    result = classify_family(_normalized("drain"), kernel)
    assert result["matched"] is True


def test_penetration_condition_maps():
    family = {"id": "DNA-CONSTR-FAM-PIPE-004-R1", "name": "Pipe Penetration", "description": "Pipe family"}
    kernel = _mock_kernel([family])
    result = classify_family(_normalized("penetration"), kernel)
    assert result["matched"] is True


def test_expansion_joint_condition_maps():
    family = {"id": "DNA-CONSTR-FAM-JOINT-005-R1", "name": "Expansion Joint", "description": "Joint family"}
    kernel = _mock_kernel([family])
    result = classify_family(_normalized("expansion_joint"), kernel)
    assert result["matched"] is True


def test_ambiguous_family_match():
    f1 = {"id": "DNA-CONSTR-FAM-EDGE-001-R1", "name": "Edge A", "description": "same"}
    f2 = {"id": "DNA-CONSTR-FAM-EDGE-002-R1", "name": "Edge B", "description": "same"}
    kernel = _mock_kernel([f1, f2])
    result = classify_family(_normalized("roof_edge"), kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] == "AMBIGUOUS_FAMILY"


def test_disambiguates_by_name():
    f1 = {"id": "DNA-CONSTR-FAM-EDGE-001-R1", "name": "Roof Edge", "description": "roof_edge details"}
    f2 = {"id": "DNA-CONSTR-FAM-EDGE-002-R1", "name": "Wall Edge", "description": "wall edge"}
    kernel = _mock_kernel([f1, f2])
    result = classify_family(_normalized("roof_edge"), kernel)
    assert result["matched"] is True
    assert result["family_id"] == "DNA-CONSTR-FAM-EDGE-001-R1"
