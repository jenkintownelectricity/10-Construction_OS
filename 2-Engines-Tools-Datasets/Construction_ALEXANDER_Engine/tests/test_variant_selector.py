"""Unit tests for variant selection."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.variant_selector import select_variant
from unittest.mock import MagicMock


def _mock_kernel(variants=None):
    kernel = MagicMock()
    kernel.get_variants_for_pattern = MagicMock(return_value=variants or [])
    return kernel


def _normalized(**overrides):
    base = {
        "condition_id": "COND-001",
        "condition_type": "roof_edge",
        "zone_id": "zone-A1",
        "interface_condition": None,
        "dimensions": {},
        "material_preferences": [],
        "method_preference": None,
        "manufacturer_refs": [],
        "climate_context": {},
        "system_type": None,
    }
    base.update(overrides)
    return base


def test_single_variant_match():
    var = {"id": "CHEM-CONSTR-VAR-DRIPMECH-101-R1", "name": "Mechanical Drip Edge", "description": "mech", "method": "mechanical_fastening", "materials": [{"name": "galvanized steel"}]}
    kernel = _mock_kernel([var])
    result = select_variant(_normalized(), "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", kernel)
    assert result["matched"] is True
    assert result["variant_id"] == "CHEM-CONSTR-VAR-DRIPMECH-101-R1"
    assert result["confidence"] == 1.0


def test_no_variants_found():
    kernel = _mock_kernel([])
    result = select_variant(_normalized(), "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] == "MISSING_TRUTH"


def test_selects_by_method_preference():
    v1 = {"id": "CHEM-CONSTR-VAR-DRIPMECH-101-R1", "name": "Mechanical Drip Edge", "description": "mechanical fastening", "method": "mechanical_fastening", "materials": []}
    v2 = {"id": "CHEM-CONSTR-VAR-DRIPADH-102-R1", "name": "Adhered Drip Edge", "description": "adhesive method", "method": "adhesive", "materials": []}
    kernel = _mock_kernel([v1, v2])
    result = select_variant(_normalized(method_preference="mechanical"), "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", kernel)
    assert result["matched"] is True
    assert result["variant_id"] == "CHEM-CONSTR-VAR-DRIPMECH-101-R1"


def test_selects_by_material_preference():
    v1 = {"id": "CHEM-CONSTR-VAR-A-101-R1", "name": "Steel Variant", "description": "steel", "method": "fastening", "materials": [{"name": "galvanized steel"}]}
    v2 = {"id": "CHEM-CONSTR-VAR-B-102-R1", "name": "Aluminum Variant", "description": "aluminum", "method": "fastening", "materials": [{"name": "aluminum"}]}
    kernel = _mock_kernel([v1, v2])
    result = select_variant(_normalized(material_preferences=["aluminum"]), "PAT-001", kernel)
    assert result["matched"] is True
    assert result["variant_id"] == "CHEM-CONSTR-VAR-B-102-R1"


def test_ambiguous_variants():
    v1 = {"id": "CHEM-CONSTR-VAR-A-101-R1", "name": "V1", "description": "same", "method": "same", "materials": []}
    v2 = {"id": "CHEM-CONSTR-VAR-B-102-R1", "name": "V2", "description": "same", "method": "same", "materials": []}
    kernel = _mock_kernel([v1, v2])
    result = select_variant(_normalized(), "PAT-001", kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] in ("AMBIGUOUS_VARIANT", "NO_VARIANT_MATCH")
