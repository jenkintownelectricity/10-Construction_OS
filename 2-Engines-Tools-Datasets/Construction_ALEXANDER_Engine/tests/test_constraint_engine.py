"""Unit tests for constraint enforcement."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.constraint_engine import enforce_constraints
from unittest.mock import MagicMock


def _mock_kernel(pattern_constraints=None, family_constraints=None):
    kernel = MagicMock()
    kernel.get_constraints_for_pattern = MagicMock(return_value=pattern_constraints or [])
    kernel.get_constraints_for_family = MagicMock(return_value=family_constraints or [])
    return kernel


def _normalized(**overrides):
    base = {
        "condition_id": "COND-001",
        "condition_type": "roof_edge",
        "zone_id": "zone-A1",
        "dimensions": {},
        "material_preferences": [],
        "method_preference": None,
        "manufacturer_refs": [],
        "climate_context": {},
    }
    base.update(overrides)
    return base


def test_no_constraints_passes():
    kernel = _mock_kernel()
    result = enforce_constraints(_normalized(), "PAT-001", "VAR-001", "FAM-001", kernel)
    assert result["passed"] is True
    assert result["violations"] == []


def test_manufacturer_constraint_passes():
    cns = {
        "id": "TEXTURE-CONSTR-CNS-EDGEMFR-001-R1",
        "constraint_type": "manufacturer",
        "parameters": {
            "material_options": ["galvanized_steel", "aluminum"],
        },
    }
    kernel = _mock_kernel(pattern_constraints=[cns])
    result = enforce_constraints(
        _normalized(material_preferences=["galvanized_steel"]),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is True


def test_manufacturer_constraint_fails():
    cns = {
        "id": "TEXTURE-CONSTR-CNS-EDGEMFR-001-R1",
        "constraint_type": "manufacturer",
        "parameters": {
            "material_options": ["galvanized_steel", "aluminum"],
        },
    }
    kernel = _mock_kernel(pattern_constraints=[cns])
    result = enforce_constraints(
        _normalized(material_preferences=["copper"]),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is False
    assert len(result["violations"]) == 1
    assert result["violations"][0]["constraint_type"] == "manufacturer"


def test_code_constraint_passes():
    cns = {
        "id": "TEXTURE-CONSTR-CNS-DRAINCODE-002-R1",
        "constraint_type": "code",
        "parameters": {
            "min_drain_size_inches": 4,
        },
    }
    kernel = _mock_kernel(pattern_constraints=[cns])
    result = enforce_constraints(
        _normalized(dimensions={"diameter_inches": 6}),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is True


def test_code_constraint_fails_small_drain():
    cns = {
        "id": "TEXTURE-CONSTR-CNS-DRAINCODE-002-R1",
        "constraint_type": "code",
        "parameters": {
            "min_drain_size_inches": 4,
        },
    }
    kernel = _mock_kernel(pattern_constraints=[cns])
    result = enforce_constraints(
        _normalized(dimensions={"diameter_inches": 2}),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is False
    assert result["violations"][0]["constraint_type"] == "code"


def test_dimensional_constraint_passes():
    cns = {
        "id": "TEXTURE-CONSTR-CNS-PARAPETDIM-003-R1",
        "constraint_type": "dimensional",
        "parameters": {},
        "validation": [
            {"check": "min_parapet_height", "min_inches": 30, "fail_action": "reject"},
        ],
    }
    kernel = _mock_kernel(family_constraints=[cns])
    result = enforce_constraints(
        _normalized(dimensions={"height_inches": 36}),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is True


def test_dimensional_constraint_fails():
    cns = {
        "id": "TEXTURE-CONSTR-CNS-PARAPETDIM-003-R1",
        "constraint_type": "dimensional",
        "parameters": {},
        "validation": [
            {"check": "min_parapet_height", "min_inches": 30, "fail_action": "reject"},
        ],
    }
    kernel = _mock_kernel(family_constraints=[cns])
    result = enforce_constraints(
        _normalized(dimensions={"height_inches": 20}),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is False
    assert result["violations"][0]["constraint_type"] == "dimensional"


def test_environmental_constraint_passes():
    cns = {
        "id": "CLIMATE-CONSTR-CNS-WINDZONE-001-R1",
        "constraint_type": "environmental",
        "parameters": {
            "wind_zones": [1, 2, 3],
        },
    }
    kernel = _mock_kernel(family_constraints=[cns])
    result = enforce_constraints(
        _normalized(climate_context={"wind_zone": 2}),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is True


def test_environmental_constraint_fails_invalid_zone():
    cns = {
        "id": "CLIMATE-CONSTR-CNS-WINDZONE-001-R1",
        "constraint_type": "environmental",
        "parameters": {
            "wind_zones": [1, 2, 3],
        },
    }
    kernel = _mock_kernel(family_constraints=[cns])
    result = enforce_constraints(
        _normalized(climate_context={"wind_zone": 5}),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is False
    assert result["violations"][0]["constraint_type"] == "environmental"


def test_constraint_fail_reason_has_correct_code():
    cns = {
        "id": "TEXTURE-CONSTR-CNS-TEST-001-R1",
        "constraint_type": "code",
        "parameters": {"min_drain_size_inches": 4},
    }
    kernel = _mock_kernel(pattern_constraints=[cns])
    result = enforce_constraints(
        _normalized(dimensions={"diameter_inches": 2}),
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["fail_reason"]["code"] == "CONSTRAINT_VIOLATION"
    assert result["fail_reason"]["stage"] == "constraint_enforcement"
