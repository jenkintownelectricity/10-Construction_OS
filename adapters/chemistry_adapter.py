"""Chemistry adapter.

Translates chemistry-related parsed data into MaterialModel objects.
This is a translation utility only — it does not embed kernel doctrine.
"""

from typing import Any

from runtime.models.material_model import MaterialModel


def adapt_chemistry(parsed_data: dict[str, Any]) -> MaterialModel:
    """Adapt chemistry-related parsed data into a MaterialModel.

    Args:
        parsed_data: Dictionary with chemistry/material fields from parsing.
            Expected keys (all optional):
                - material_name: str
                - manufacturer: str
                - properties: dict
                - notes: list[str]

    Returns:
        A MaterialModel populated from the parsed data.
    """
    return MaterialModel(
        material_name=parsed_data.get("material_name", ""),
        manufacturer=parsed_data.get("manufacturer", ""),
        properties=parsed_data.get("properties", {}),
        notes=parsed_data.get("notes", []),
    )
