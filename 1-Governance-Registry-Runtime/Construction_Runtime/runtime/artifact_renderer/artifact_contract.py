"""Artifact rendering contract definitions.

Defines the contracts governing artifact rendering:
- Manifest contract: what to render
- Artifact output contract: what was rendered
- Renderer compliance contract: renderer capabilities

Authority: Construction_Runtime (execution contract)
Kernel: Read-only. Never mutated by renderers.
"""

from dataclasses import dataclass, field
from typing import Any

ARTIFACT_CONTRACT_VERSION = "18.0"
SUPPORTED_OUTPUT_FORMATS = frozenset({"DXF", "SVG", "PDF"})


@dataclass
class RenderManifest:
    """Input manifest specifying what artifacts to render.

    Produced by shop_drawing_prep or detail_resolver upstream.
    Consumed by renderer_pipeline.
    """
    manifest_id: str = ""
    detail_id: str = ""
    variant_id: str = ""
    assembly_family: str = ""
    instruction_set_id: str = ""
    requested_formats: list[str] = field(default_factory=lambda: ["DXF", "SVG", "PDF"])
    parameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        """Validate manifest completeness. Returns list of errors."""
        errors = []
        if not self.manifest_id:
            errors.append("manifest_id is required.")
        if not self.detail_id:
            errors.append("detail_id is required.")
        if not self.instruction_set_id:
            errors.append("instruction_set_id is required.")
        for fmt in self.requested_formats:
            if fmt not in SUPPORTED_OUTPUT_FORMATS:
                errors.append(f"Unsupported output format: '{fmt}'.")
        return errors


@dataclass
class ArtifactOutput:
    """Output artifact produced by a renderer.

    Each artifact carries content, metadata, and sha256 lineage hash.
    """
    artifact_id: str = ""
    format: str = ""
    content: str = ""
    content_hash: str = ""
    source_manifest_id: str = ""
    source_instruction_set_id: str = ""
    source_detail_id: str = ""
    renderer_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "format": self.format,
            "content_hash": self.content_hash,
            "source_manifest_id": self.source_manifest_id,
            "source_instruction_set_id": self.source_instruction_set_id,
            "source_detail_id": self.source_detail_id,
            "renderer_id": self.renderer_id,
            "metadata": self.metadata,
        }


@dataclass
class RenderResult:
    """Complete result from the rendering pipeline.

    Contains all artifacts, lineage records, and any errors.
    """
    manifest_id: str = ""
    artifacts: list[ArtifactOutput] = field(default_factory=list)
    lineage: dict[str, Any] = field(default_factory=dict)
    errors: list[dict[str, Any]] = field(default_factory=list)
    success: bool = False

    @property
    def artifact_count(self) -> int:
        return len(self.artifacts)

    def get_artifact_by_format(self, fmt: str) -> ArtifactOutput | None:
        for a in self.artifacts:
            if a.format == fmt:
                return a
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "lineage": self.lineage,
            "errors": self.errors,
            "success": self.success,
            "artifact_count": self.artifact_count,
            "contract_version": ARTIFACT_CONTRACT_VERSION,
        }


@dataclass
class RendererCapability:
    """Declares what a renderer can produce."""
    renderer_id: str = ""
    output_format: str = ""
    supported_primitives: list[str] = field(default_factory=list)
    version: str = ""

    def supports_primitive(self, primitive_type: str) -> bool:
        return primitive_type in self.supported_primitives
