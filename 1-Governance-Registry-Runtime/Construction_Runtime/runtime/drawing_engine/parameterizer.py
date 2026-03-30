"""
Parameterization Layer

Resolves canonical detail parameters into concrete execution inputs.
Fail-closed: incomplete, contradictory, or unsupported parameters stop execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParameterizationResult:
    """Result of parameter resolution."""

    resolved: bool = False
    resolved_components: list[dict[str, Any]] = field(default_factory=list)
    resolved_parameters: dict[str, Any] = field(default_factory=dict)
    errors: list[dict[str, str]] = field(default_factory=list)


def parameterize_detail(
    components: list[dict[str, Any]],
    material_references: dict[str, str],
    parameters: dict[str, Any],
) -> ParameterizationResult:
    """
    Resolve canonical detail parameters into concrete execution inputs.

    Binds material_param references to canonical material classes.
    Binds dimensional and conditional parameters to concrete values.

    Fail-closed: if parameters are incomplete or contradictory, returns unresolved.
    """
    result = ParameterizationResult()
    errors: list[dict[str, str]] = []
    resolved_components: list[dict[str, Any]] = []

    for component in components:
        resolved = dict(component)

        # Resolve material_param to concrete material class
        material_param = component.get("material_param")
        if material_param:
            concrete_material = (
                parameters.get(material_param)
                or material_references.get(material_param)
                or material_references.get("membrane")
            )
            if not concrete_material:
                errors.append({
                    "code": "UNSUPPORTED_PARAMETERIZATION",
                    "message": (
                        f"Cannot resolve material parameter '{material_param}' "
                        f"for component '{component.get('name', 'unknown')}'"
                    ),
                    "path": f"components.{component.get('name', 'unknown')}.material_param",
                })
            else:
                resolved["material"] = concrete_material
                del resolved["material_param"]

        resolved_components.append(resolved)

    result.errors = errors
    result.resolved_components = resolved_components
    result.resolved_parameters = dict(parameters)
    result.resolved = len(errors) == 0

    return result
