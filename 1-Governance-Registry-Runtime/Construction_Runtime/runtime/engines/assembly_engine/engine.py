"""Assembly engine.

Combines geometry, chemistry, and assembly runtime objects to produce
buildable assembly structures ready for output generation.
"""

from typing import Any

from runtime.models.assembly_model import AssemblyModel
from runtime.models.geometry_model import GeometryModel
from runtime.models.material_model import MaterialModel


def run_assembly_engine(
    assembly: AssemblyModel,
    geometry: GeometryModel | None = None,
    materials: list[MaterialModel] | None = None,
) -> dict[str, Any]:
    """Process assembly runtime objects into a buildable assembly structure.

    Combines geometry, material, and assembly data into a unified structure
    suitable for deliverable generation.

    Args:
        assembly: The assembly runtime model.
        geometry: Optional geometry model for spatial data.
        materials: Optional list of material models.

    Returns:
        Dictionary with:
            - assembly_name: str
            - components: list of component dicts with enriched data
            - constraints: list of constraint dicts
            - geometry: geometry data if provided
            - materials: material data if provided
            - build_status: 'ready' or 'incomplete'
    """
    materials = materials or []

    enriched_components = []
    for comp in assembly.components:
        enriched = dict(comp)
        enriched["material_resolved"] = len(materials) > 0
        enriched["geometry_resolved"] = geometry is not None
        enriched_components.append(enriched)

    has_components = len(enriched_components) > 0
    has_geometry = geometry is not None and (
        geometry.dimensions or geometry.spatial_refs
    )

    build_status = "ready" if has_components else "incomplete"

    return {
        "assembly_name": assembly.name,
        "components": enriched_components,
        "constraints": assembly.constraints,
        "geometry": {
            "dimensions": geometry.dimensions if geometry else {},
            "spatial_refs": geometry.spatial_refs if geometry else [],
        },
        "materials": [
            {
                "material_name": m.material_name,
                "manufacturer": m.manufacturer,
                "properties": m.properties,
            }
            for m in materials
        ],
        "build_status": build_status,
    }
