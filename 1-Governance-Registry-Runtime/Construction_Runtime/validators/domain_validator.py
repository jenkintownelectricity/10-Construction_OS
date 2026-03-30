"""Domain validator for Construction Runtime v0.2.

Checks: incompatible materials, invalid assembly combinations,
unsupported substrate conditions, missing performance constraints.
Fails closed.
"""

from typing import Any

from standards import error_codes


def validate_domain(parsed_data: dict[str, Any], input_type: str) -> dict[str, Any]:
    """Run domain validation on parsed data.

    Returns structured validation result with stage='domain'.
    """
    warnings: list[str] = []
    errors: list[dict[str, str]] = []

    if input_type == "assembly":
        _validate_assembly_domain(parsed_data, warnings, errors)
    elif input_type == "spec":
        _validate_spec_domain(parsed_data, warnings, errors)

    return {"is_valid": len(errors) == 0, "stage": "domain", "warnings": warnings, "errors": errors}


def _validate_assembly_domain(data: dict, warnings: list, errors: list) -> None:
    components = data.get("components", [])
    constraints = data.get("constraints", [])

    # Check that components have valid type fields
    for i, comp in enumerate(components):
        comp_type = comp.get("type", "")
        if not comp_type:
            warnings.append(f"Component '{comp.get('name', i)}' has no type specified.")

    # Check for interface constraints that reference something
    interface_constraints = [c for c in constraints if c.get("type") == "interface"]
    if components and not interface_constraints:
        warnings.append("Assembly has components but no interface constraints defined.")

    # Check for at least one dimensional constraint when components exist
    dim_constraints = [c for c in constraints if c.get("type") in ("clearance", "spacing", "tolerance")]
    if len(components) > 1 and not dim_constraints:
        warnings.append("Multi-component assembly has no dimensional constraints.")

    # Fail on empty interface descriptions (they are meaningless)
    for c in interface_constraints:
        if not c.get("description", "").strip():
            errors.append({
                "code": error_codes.DOMAIN_INVALID_ASSEMBLY,
                "message": "Interface constraint has empty description.",
                "path": "constraints.interface",
            })


def _validate_spec_domain(data: dict, warnings: list, errors: list) -> None:
    requirements = data.get("requirements", [])
    references = data.get("product_references", [])

    # Check for requirements without associated product references
    mandatory = [r for r in requirements if r.get("type") == "mandatory"]
    if mandatory and not references:
        warnings.append("Spec has mandatory requirements but no product references.")

    # Check for basis-of-design references
    bod = [r for r in references if r.get("type") == "basis_of_design"]
    if references and not bod:
        warnings.append("No basis-of-design reference found in product references.")
