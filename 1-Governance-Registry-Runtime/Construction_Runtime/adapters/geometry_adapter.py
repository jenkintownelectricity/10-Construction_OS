"""Geometry adapter.

Translates geometry-related parsed data into GeometryModel objects.
This is a translation utility only — it does not embed kernel doctrine.
"""

from typing import Any

from runtime.models.geometry_model import GeometryModel


def adapt_geometry(parsed_data: dict[str, Any]) -> GeometryModel:
    """Adapt geometry-related parsed data into a GeometryModel.

    Args:
        parsed_data: Dictionary with geometry fields from parsing.
            Expected keys (all optional):
                - dimensions: dict
                - spatial_refs: list[str]
                - notes: list[str]

    Returns:
        A GeometryModel populated from the parsed data.
    """
    return GeometryModel(
        dimensions=parsed_data.get("dimensions", {}),
        spatial_refs=parsed_data.get("spatial_refs", []),
        notes=parsed_data.get("notes", []),
    )
