"""
Constraint Engine Module.

Enforces constraint profiles against the selected pattern/variant
and condition context. Fail-closed on any constraint violation.
"""

from engine.config import FAIL_CONSTRAINT_VIOLATION
from contracts.pattern_kernel_consumer import PatternKernelConsumer


def enforce_constraints(
    normalized: dict,
    pattern_id: str,
    variant_id: str | None,
    family_id: str,
    kernel: PatternKernelConsumer,
) -> dict:
    """
    Enforce all applicable constraint profiles.

    Returns:
        {"passed": True, "violations": [], "checked_constraints": [...]}
        {"passed": False, "violations": [...], "checked_constraints": [...], "fail_reason": {...}}
    """
    violations = []
    checked = []

    # Gather constraints for the pattern and family
    pattern_constraints = kernel.get_constraints_for_pattern(pattern_id)
    family_constraints = kernel.get_constraints_for_family(family_id)

    all_constraints = {c["id"]: c for c in pattern_constraints}
    for c in family_constraints:
        if c["id"] not in all_constraints:
            all_constraints[c["id"]] = c

    for cns_id, constraint in all_constraints.items():
        checked.append(cns_id)
        cns_type = constraint.get("constraint_type", "")

        if cns_type == "manufacturer":
            v = _check_manufacturer(constraint, normalized)
            if v:
                violations.append(v)

        elif cns_type == "code":
            v = _check_code(constraint, normalized)
            if v:
                violations.append(v)

        elif cns_type == "dimensional":
            v = _check_dimensional(constraint, normalized)
            if v:
                violations.append(v)

        elif cns_type == "environmental":
            v = _check_environmental(constraint, normalized)
            if v:
                violations.append(v)

    if violations:
        return {
            "passed": False,
            "violations": violations,
            "checked_constraints": checked,
            "fail_reason": {
                "code": FAIL_CONSTRAINT_VIOLATION,
                "stage": "constraint_enforcement",
                "message": f"{len(violations)} constraint violation(s) detected",
                "details": {"violation_count": len(violations)},
            },
        }

    return {
        "passed": True,
        "violations": [],
        "checked_constraints": checked,
    }


def _check_manufacturer(constraint: dict, normalized: dict) -> dict | None:
    """Check manufacturer constraints."""
    params = constraint.get("parameters", {})
    if not params:
        return None

    mfr_refs = normalized.get("manufacturer_refs", [])
    mat_prefs = normalized.get("material_preferences", [])

    # Check material options if specified
    material_options = params.get("material_options", [])
    if material_options and mat_prefs:
        for pref in mat_prefs:
            normalized_options = [m.lower().replace(" ", "_") for m in material_options]
            if pref.lower().replace(" ", "_") not in normalized_options:
                return {
                    "constraint_id": constraint["id"],
                    "constraint_type": "manufacturer",
                    "violation": f"Material '{pref}' not in approved options",
                    "parameter": "material_options",
                    "expected": material_options,
                    "actual": pref,
                }

    return None


def _check_code(constraint: dict, normalized: dict) -> dict | None:
    """Check code compliance constraints."""
    params = constraint.get("parameters", {})
    dims = normalized.get("dimensions", {})

    # Check min_drain_size if applicable
    min_size = params.get("min_drain_size_inches")
    actual_diameter = dims.get("diameter_inches")
    if min_size is not None and actual_diameter is not None:
        if actual_diameter < min_size:
            return {
                "constraint_id": constraint["id"],
                "constraint_type": "code",
                "violation": f"Diameter {actual_diameter}\" below minimum {min_size}\"",
                "parameter": "min_drain_size_inches",
                "expected": min_size,
                "actual": actual_diameter,
            }

    return None


def _check_dimensional(constraint: dict, normalized: dict) -> dict | None:
    """Check dimensional constraints."""
    params = constraint.get("parameters", {})
    dims = normalized.get("dimensions", {})
    validation = constraint.get("validation", [])

    for check in validation:
        check_name = check.get("check", "")
        fail_action = check.get("fail_action", "reject")

        if "min" in check_name and "height" in check_name:
            min_val = check.get("min_inches")
            actual = dims.get("height_inches")
            if min_val is not None and actual is not None:
                if actual < min_val:
                    return {
                        "constraint_id": constraint["id"],
                        "constraint_type": "dimensional",
                        "violation": f"Height {actual}\" below minimum {min_val}\"",
                        "parameter": check_name,
                        "expected": min_val,
                        "actual": actual,
                    }

        if "range" in check_name or "max" in check_name:
            min_val = check.get("min_inches")
            max_val = check.get("max_inches")
            # Find matching dimension
            for dim_key in ["width_inches", "height_inches", "thickness_inches"]:
                actual = dims.get(dim_key)
                if actual is not None:
                    if min_val is not None and actual < min_val:
                        return {
                            "constraint_id": constraint["id"],
                            "constraint_type": "dimensional",
                            "violation": f"{dim_key} {actual}\" below minimum {min_val}\"",
                            "parameter": check_name,
                            "expected": f">= {min_val}",
                            "actual": actual,
                        }
                    if max_val is not None and actual > max_val:
                        return {
                            "constraint_id": constraint["id"],
                            "constraint_type": "dimensional",
                            "violation": f"{dim_key} {actual}\" above maximum {max_val}\"",
                            "parameter": check_name,
                            "expected": f"<= {max_val}",
                            "actual": actual,
                        }

    return None


def _check_environmental(constraint: dict, normalized: dict) -> dict | None:
    """Check environmental/climate constraints."""
    params = constraint.get("parameters", {})
    climate = normalized.get("climate_context", {})

    # Check wind zone
    wind_zones = params.get("wind_zones", [])
    condition_wind_zone = climate.get("wind_zone")
    if wind_zones and condition_wind_zone is not None:
        if condition_wind_zone not in wind_zones:
            return {
                "constraint_id": constraint["id"],
                "constraint_type": "environmental",
                "violation": f"Wind zone {condition_wind_zone} not in allowed zones {wind_zones}",
                "parameter": "wind_zones",
                "expected": wind_zones,
                "actual": condition_wind_zone,
            }

    # Check moisture exposure
    moisture_levels = params.get("moisture_exposure_levels", [])
    condition_moisture = climate.get("moisture_exposure")
    if moisture_levels and condition_moisture:
        if condition_moisture not in moisture_levels:
            return {
                "constraint_id": constraint["id"],
                "constraint_type": "environmental",
                "violation": f"Moisture exposure '{condition_moisture}' not compatible",
                "parameter": "moisture_exposure_levels",
                "expected": moisture_levels,
                "actual": condition_moisture,
            }

    return None
