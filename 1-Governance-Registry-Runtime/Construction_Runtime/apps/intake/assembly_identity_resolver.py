"""
Assembly Identity Resolver

Detects assemblies from ingested evidence, maps them to kernel-defined
assembly models, and resolves interfaces between assemblies.

This module does not define assembly identity or composition truth.
It consumes governed models from Construction_Kernel and produces
derived identity resolutions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ResolvedAssembly:
    """A derived assembly identity resolution. Non-canonical."""

    assembly_id: str = ""
    assembly_type: str = ""
    interface_types: list[str] = field(default_factory=list)
    material_classes: list[str] = field(default_factory=list)
    evidence_sources: list[str] = field(default_factory=list)


@dataclass
class IdentityResolutionResult:
    """Derived result of assembly identity resolution. Non-canonical, recomputable."""

    resolved: bool = False
    assemblies: list[ResolvedAssembly] = field(default_factory=list)
    unresolved_references: list[str] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)


def resolve_assemblies(
    project_assemblies: list[dict[str, Any]],
    evidence_items: list[dict[str, Any]],
) -> IdentityResolutionResult:
    """
    Resolve assembly identities from project data and evidence.

    Maps raw assembly references to kernel-defined assembly types
    and interface types. Fail-closed on unresolvable references.
    All output is derived and non-canonical.
    """
    result = IdentityResolutionResult()

    if not isinstance(project_assemblies, list):
        result.errors.append({
            "code": "INVALID_ASSEMBLIES_INPUT",
            "message": "Project assemblies must be a list.",
        })
        return result

    # Known assembly types from kernel models
    known_assembly_types = {
        "roof_assembly", "wall_assembly", "foundation_assembly",
        "slab_assembly", "curtain_wall_assembly",
    }

    # Known interface types from kernel models
    known_interface_types = {
        "roof_to_parapet", "roof_edge", "penetration",
        "wall_to_foundation", "wall_to_roof", "expansion_joint",
    }

    for raw_asm in project_assemblies:
        asm_id = raw_asm.get("assembly_id", "")
        asm_type = raw_asm.get("assembly_type", "")

        if not asm_id:
            result.errors.append({
                "code": "MISSING_ASSEMBLY_ID",
                "message": "Each assembly must have an assembly_id.",
            })
            continue

        if asm_type not in known_assembly_types:
            result.unresolved_references.append(asm_id)
            continue

        # Collect interface types for this assembly
        interfaces = raw_asm.get("interfaces", [])
        resolved_interfaces = []
        for iface in interfaces:
            itype = iface.get("interface_type", "")
            if itype in known_interface_types:
                resolved_interfaces.append(itype)
            else:
                result.unresolved_references.append(f"{asm_id}:{itype}")

        # Collect evidence linking
        evidence_refs = [
            e.get("evidence_id", "")
            for e in evidence_items
            if asm_id in e.get("assembly_references", [])
        ]

        resolved = ResolvedAssembly(
            assembly_id=asm_id,
            assembly_type=asm_type,
            interface_types=resolved_interfaces,
            material_classes=raw_asm.get("material_classes", []),
            evidence_sources=evidence_refs,
        )
        result.assemblies.append(resolved)

    result.resolved = len(result.assemblies) > 0 and len(result.errors) == 0
    return result
