#!/usr/bin/env python3
"""
Detail Atlas Constraint Validator

Evaluates assembly constraint rules against project parameters.
Returns PASS / WARN / HALT status with rule-level results.

Authority: 10-Construction_OS (domain plane)
Design: fail-closed, deterministic, no network calls
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_assembly(assembly_path: str) -> dict:
    """Load assembly JSON from path."""
    with open(assembly_path, "r") as f:
        return json.load(f)


def build_component_map(assembly: dict) -> dict:
    """Build lookup map of components by component_id."""
    return {c["component_id"]: c for c in assembly.get("components", [])}


def evaluate_rule(rule: dict, components: dict, project: dict) -> dict:
    """Evaluate a single constraint rule against components and project data.

    Returns rule result dict with status, message, and remediation.
    """
    rule_id = rule["rule_id"]
    severity = rule.get("severity", "HALT")

    # --- RULE_SUBSTRATE ---
    if rule_id == "RULE_SUBSTRATE":
        substrate = components.get("substrate")
        if not substrate:
            return _fail(rule_id, severity, "Substrate component missing",
                         "Add approved substrate to assembly")
        material = project.get("substrate_material", substrate.get("material", ""))
        approved = substrate.get("parameters", {}).get("approved_types", [])
        if material not in approved:
            return _fail(rule_id, severity,
                         f"Substrate '{material}' not in approved types {approved}",
                         f"Use one of: {', '.join(approved)}")
        return _pass(rule_id, f"Substrate '{material}' is approved")

    # --- RULE_BASE_SHEET ---
    if rule_id == "RULE_BASE_SHEET":
        base = components.get("base_sheet")
        if not base or not base.get("required"):
            return _fail(rule_id, severity, "Base sheet missing or not required",
                         "Add required base sheet component")
        attachment = base.get("parameters", {}).get("attachment", "")
        if attachment != "mechanically_fastened":
            return _fail(rule_id, severity,
                         f"Base sheet attachment '{attachment}' must be mechanically_fastened",
                         "Set base sheet attachment to mechanically_fastened")
        return _pass(rule_id, "Base sheet present and mechanically fastened")

    # --- RULE_CAP_SHEET ---
    if rule_id == "RULE_CAP_SHEET":
        cap = components.get("cap_sheet")
        if not cap or not cap.get("required"):
            return _fail(rule_id, severity, "Cap sheet missing or not required",
                         "Add required cap sheet component")
        overlap = cap.get("parameters", {}).get("min_overlap_inches", 0)
        if overlap < 6:
            return _fail(rule_id, severity,
                         f"Cap sheet overlap {overlap}\" below minimum 6\"",
                         "Set cap sheet min_overlap_inches >= 6")
        return _pass(rule_id, f"Cap sheet present with {overlap}\" overlap")

    # --- RULE_CANT_STRIP ---
    if rule_id == "RULE_CANT_STRIP":
        cant = components.get("cant_strip")
        project_has_cant = project.get("cant_strip", True)
        if not cant or not cant.get("required"):
            return _fail(rule_id, severity, "Cant strip component missing from assembly",
                         "Add required cant strip at wall-to-roof transition")
        if not project_has_cant:
            return _fail(rule_id, severity,
                         "Cant strip removed or absent in project configuration",
                         "Install cant strip at all wall-to-roof transitions")
        size = cant.get("parameters", {}).get("min_size_inches", 0)
        if size < 4:
            return _fail(rule_id, severity,
                         f"Cant strip size {size}\" below minimum 4\"",
                         "Use cant strip >= 4 inches")
        return _pass(rule_id, f"Cant strip present, {size}\" minimum")

    # --- RULE_FLASHING_HEIGHT ---
    if rule_id == "RULE_FLASHING_HEIGHT":
        flashing = components.get("flashing")
        if not flashing:
            return _fail(rule_id, severity, "Flashing component missing",
                         "Add flashing component to assembly")
        height = flashing.get("parameters", {}).get("min_height_inches", 0)
        project_height = project.get("flashing_height_inches", height)
        if project_height < 8:
            return _fail(rule_id, severity,
                         f"Flashing height {project_height}\" below minimum 8\"",
                         "Extend flashing to minimum 8 inches above roof surface")
        return _pass(rule_id, f"Flashing height {project_height}\" meets minimum")

    # --- RULE_TERMINATION_BAR ---
    if rule_id == "RULE_TERMINATION_BAR":
        term = components.get("termination_bar")
        if not term or not term.get("required"):
            return _fail(rule_id, severity, "Termination bar missing",
                         "Add termination bar at top of flashing")
        sealant = term.get("parameters", {}).get("sealant_required", False)
        if not sealant:
            return _fail(rule_id, severity, "Termination bar missing sealant",
                         "Apply polyurethane sealant at termination bar")
        return _pass(rule_id, "Termination bar present with sealant")

    # --- RULE_ADHESIVE ---
    if rule_id == "RULE_ADHESIVE":
        adhesive = components.get("adhesive")
        if not adhesive:
            return _pass(rule_id, "Adhesive not specified (optional component)")
        material = adhesive.get("material", "")
        prohibited = adhesive.get("parameters", {}).get("prohibited_with", [])
        project_membrane = project.get("membrane_type", "SBS")
        if project_membrane in prohibited:
            return _fail(rule_id, severity,
                         f"Adhesive '{material}' prohibited with '{project_membrane}'",
                         f"Use SBS-compatible adhesive; prohibited with: {', '.join(prohibited)}")
        return _pass(rule_id, f"Adhesive '{material}' compatible")

    # --- RULE_INSULATION ---
    if rule_id == "RULE_INSULATION":
        insulation = components.get("insulation")
        if not insulation:
            return _fail(rule_id, severity, "Insulation component missing",
                         "Add insulation meeting minimum R-value")
        r_value = insulation.get("parameters", {}).get("min_r_value", 0)
        project_r = project.get("insulation_r_value", r_value)
        if project_r < 20:
            return _fail(rule_id, "WARN",
                         f"Insulation R-value {project_r} below recommended R-20",
                         "Upgrade insulation to meet R-20 minimum for warranty")
        return _pass(rule_id, f"Insulation R-{project_r} meets minimum")

    # Unknown rule — fail closed
    return _fail(rule_id, "HALT", f"Unknown rule '{rule_id}' — fail closed",
                 "Contact system administrator")


def _pass(rule_id: str, message: str) -> dict:
    return {"rule_id": rule_id, "status": "PASS", "message": message, "remediation": None}


def _fail(rule_id: str, severity: str, message: str, remediation: str) -> dict:
    return {"rule_id": rule_id, "status": severity, "message": message, "remediation": remediation}


def validate(assembly: dict, project: dict) -> dict:
    """Run all assembly constraints against project data.

    Returns normalized validation result with overall status.
    """
    components = build_component_map(assembly)
    rules = assembly.get("assembly_constraints", [])

    rule_results = []
    has_halt = False
    has_warn = False

    for rule in rules:
        result = evaluate_rule(rule, components, project)
        rule_results.append(result)
        if result["status"] == "HALT":
            has_halt = True
        elif result["status"] == "WARN":
            has_warn = True

    if has_halt:
        status = "HALT"
    elif has_warn:
        status = "WARN"
    else:
        status = "PASS"

    failed_rule_ids = [r["rule_id"] for r in rule_results if r["status"] in ("HALT", "WARN")]

    return {
        "status": status,
        "assembly_id": assembly.get("assembly_id"),
        "assembly_version": assembly.get("assembly_version"),
        "node_id": assembly.get("node_id"),
        "manufacturer_id": assembly.get("manufacturer_id"),
        "condition_type": assembly.get("condition_type"),
        "rule_results": rule_results,
        "failed_rule_ids": failed_rule_ids,
        "total_rules": len(rules),
        "passed_rules": len([r for r in rule_results if r["status"] == "PASS"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "logic_logs": [
            f"Evaluated {len(rules)} rules",
            f"Status: {status}",
            f"Failed: {', '.join(failed_rule_ids) if failed_rule_ids else 'none'}",
        ],
    }


def main():
    """CLI entry point for validator."""
    if len(sys.argv) < 2:
        print("Usage: python validator.py <assembly_json> [project_json]")
        print("  assembly_json: path to assembly truth object")
        print("  project_json:  optional path to project overrides")
        sys.exit(1)

    assembly_path = sys.argv[1]
    assembly = load_assembly(assembly_path)

    project = {}
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "r") as f:
            project = json.load(f)

    result = validate(assembly, project)

    print(json.dumps(result, indent=2))

    if result["status"] == "HALT":
        sys.exit(1)
    elif result["status"] == "WARN":
        sys.exit(0)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
