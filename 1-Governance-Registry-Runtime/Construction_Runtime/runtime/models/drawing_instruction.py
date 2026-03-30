"""Drawing instruction intermediate representation.

DrawingInstructionSet is the canonical intermediate representation consumed
by both DXF and SVG generators. Parsers and engines may NOT output DXF or
SVG directly — they must produce a DrawingInstructionSet.
"""

from dataclasses import dataclass, field
from typing import Any


SUPPORTED_ENTITY_TYPES = {"LINE", "POLYLINE", "RECT", "CIRCLE", "TEXT", "DIMENSION", "CALLOUT"}

INSTRUCTION_VERSION = "0.2"


@dataclass
class DrawingEntity:
    """A single drawing entity."""
    entity_type: str = ""
    layer: str = ""
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class DrawingDimension:
    """A dimension annotation."""
    dim_type: str = "linear"
    start: tuple[float, float] = (0.0, 0.0)
    end: tuple[float, float] = (0.0, 0.0)
    value: float = 0.0
    unit: str = "in"
    label: str = ""
    layer: str = "A-DIMS"
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass
class TextAnnotation:
    """A text annotation on the drawing."""
    text: str = ""
    position: tuple[float, float] = (0.0, 0.0)
    font_size: float = 12.0
    layer: str = "A-TEXT"
    rotation: float = 0.0


@dataclass
class SheetMetadata:
    """Sheet metadata for the drawing."""
    width: float = 36.0
    height: float = 24.0
    unit: str = "in"
    scale: str = "1:1"


@dataclass
class TitleBlockData:
    """Title block content."""
    project_name: str = ""
    assembly_name: str = ""
    drawing_number: str = ""
    revision: str = "0"
    date: str = ""
    schema_version: str = INSTRUCTION_VERSION


@dataclass
class DrawingInstructionSet:
    """The canonical intermediate representation for all drawing output.

    DXF and SVG generators consume only this model.
    """
    instruction_version: str = INSTRUCTION_VERSION
    entities: list[DrawingEntity] = field(default_factory=list)
    dimensions: list[DrawingDimension] = field(default_factory=list)
    text_annotations: list[TextAnnotation] = field(default_factory=list)
    layers: list[str] = field(default_factory=list)
    sheet_metadata: SheetMetadata = field(default_factory=SheetMetadata)
    title_block_data: TitleBlockData = field(default_factory=TitleBlockData)
    provenance: dict[str, Any] = field(default_factory=dict)

    def get_entities_by_layer(self, layer: str) -> list[DrawingEntity]:
        """Return all entities assigned to a given layer."""
        return [e for e in self.entities if e.layer == layer]

    def get_all_used_layers(self) -> set[str]:
        """Return the set of all layers referenced by entities."""
        layers = {e.layer for e in self.entities}
        layers.update(d.layer for d in self.dimensions)
        layers.update(t.layer for t in self.text_annotations)
        return layers

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for contract validation."""
        return {
            "instruction_version": self.instruction_version,
            "entities": [
                {"entity_type": e.entity_type, "layer": e.layer, "properties": e.properties}
                for e in self.entities
            ],
            "dimensions": [
                {
                    "dim_type": d.dim_type, "start": list(d.start), "end": list(d.end),
                    "value": d.value, "unit": d.unit, "label": d.label,
                    "layer": d.layer, "provenance": d.provenance,
                }
                for d in self.dimensions
            ],
            "text_annotations": [
                {"text": t.text, "position": list(t.position), "font_size": t.font_size,
                 "layer": t.layer, "rotation": t.rotation}
                for t in self.text_annotations
            ],
            "layers": self.layers,
            "sheet_metadata": {
                "width": self.sheet_metadata.width,
                "height": self.sheet_metadata.height,
                "unit": self.sheet_metadata.unit,
                "scale": self.sheet_metadata.scale,
            },
            "title_block_data": {
                "project_name": self.title_block_data.project_name,
                "assembly_name": self.title_block_data.assembly_name,
                "drawing_number": self.title_block_data.drawing_number,
                "revision": self.title_block_data.revision,
                "date": self.title_block_data.date,
                "schema_version": self.title_block_data.schema_version,
            },
            "provenance": self.provenance,
        }
