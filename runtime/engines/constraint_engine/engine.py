"""Constraint engine.

Validates simple construction constraints and emits warnings/errors.
This is a foundational v0.1 engine, not a full constraint solver.
"""

from typing import Any

from runtime.models.assembly_model import AssemblyModel


def run_constraint_engine(assembly: AssemblyModel) -> dict[str, Any]:
    """Validate construction constraints on an assembly.

    Checks for:
        - Missing components
        - Unresolved interfaces
        - Spacing/clearance placeholders
        - Incomplete assembly definitions

    Emits warnings and errors — never silently passes.

    Args:
        assembly: The assembly runtime model to validate.

    Returns:
        Dictionary with:
            - is_valid: bool
            - warnings: list of warning strings
            - errors: list of error strings
            - checks_run: list of check names that were executed
    """
    warnings: list[str] = []
    errors: list[str] = []
    checks_run: list[str] = []

    # Check: assembly has a name
    checks_run.append("assembly_name_present")
    if not assembly.name:
        warnings.append("Assembly has no name defined.")

    # Check: assembly has components
    checks_run.append("components_present")
    if not assembly.components:
        errors.append("Assembly has no components. Cannot proceed.")

    # Check: components have names
    checks_run.append("component_names_valid")
    for i, comp in enumerate(assembly.components):
        if not comp.get("name"):
            errors.append(f"Component at index {i} has no name.")

    # Check: constraints are present
    checks_run.append("constraints_present")
    if not assembly.constraints:
        warnings.append("No constraints defined for assembly.")

    # Check: interface constraints reference something meaningful
    checks_run.append("interface_constraints_resolved")
    for constraint in assembly.constraints:
        desc = constraint.get("description", "")
        ctype = constraint.get("type", "")
        if ctype == "interface" and not desc:
            errors.append("Interface constraint has empty description.")
        if ctype in ("clearance", "spacing") and not desc:
            warnings.append(f"{ctype.capitalize()} constraint has no value specified.")

    # Check: minimum assembly completeness
    checks_run.append("assembly_minimum_completeness")
    if not assembly.source_text:
        warnings.append("Assembly has no source text — may indicate incomplete input.")

    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "warnings": warnings,
        "errors": errors,
        "checks_run": checks_run,
    }
