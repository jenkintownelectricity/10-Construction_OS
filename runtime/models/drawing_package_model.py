"""Drawing package and export models for construction deliverables."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DrawingView:
    """A single view within a drawing sheet.

    Represents a specific projection or detail view of construction elements.
    """

    view_id: str = ""
    view_type: str = ""  # plan | elevation | section | detail | isometric
    assembly_refs: list[str] = field(default_factory=list)
    scale: str = ""
    origin_x: float = 0.0
    origin_y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    annotations: list[dict] = field(default_factory=dict)


@dataclass
class DrawingSheet:
    """A single sheet in a drawing package.

    Contains one or more views, a titleblock, and metadata.
    """

    sheet_id: str = ""
    sheet_number: str = ""
    sheet_title: str = ""
    views: list[DrawingView] = field(default_factory=list)
    titleblock: dict = field(default_factory=dict)
    revision_id: str = ""
    scale: str = ""
    paper_size: str = "ARCH D"


@dataclass
class DrawingPackage:
    """A complete drawing package ready for export.

    Contains sheets, metadata, and integrity hash for deterministic output.
    """

    package_id: str = ""
    package_name: str = ""
    sheets: list[DrawingSheet] = field(default_factory=list)
    revision_id: str = ""
    release_id: str = ""
    created_at: str = ""
    integrity_hash: str = ""
    export_format: str = ""  # pdf | dwg | dxf
    metadata: dict = field(default_factory=dict)


@dataclass
class ExportArtifact:
    """An exported artifact from the drawing generation pipeline.

    Represents a file or data blob produced by deterministic export.
    """

    artifact_id: str = ""
    artifact_type: str = ""  # drawing | report | schedule | manifest
    file_path: str = ""
    file_format: str = ""
    file_hash: str = ""
    source_package_id: str = ""
    created_at: str = ""
    metadata: dict = field(default_factory=dict)
