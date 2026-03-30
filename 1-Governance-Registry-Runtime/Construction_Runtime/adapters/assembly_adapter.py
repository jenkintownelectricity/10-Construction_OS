"""Assembly adapter.

Translates parsed assembly structures into AssemblyModel objects.
This is a translation utility only — it does not embed kernel doctrine.
"""

from typing import Any

from runtime.models.assembly_model import AssemblyModel


def adapt_assembly(parsed_data: dict[str, Any]) -> AssemblyModel:
    """Adapt a parsed assembly payload into an AssemblyModel.

    Args:
        parsed_data: Dictionary from assembly parser output.
            Expected keys:
                - name: str
                - components: list[dict]
                - constraints: list[dict]
                - source_text: str
                - metadata: dict

    Returns:
        An AssemblyModel populated from the parsed data.
    """
    return AssemblyModel(
        name=parsed_data.get("name", ""),
        components=parsed_data.get("components", []),
        constraints=parsed_data.get("constraints", []),
        source_text=parsed_data.get("source_text", ""),
        metadata=parsed_data.get("metadata", {}),
    )
