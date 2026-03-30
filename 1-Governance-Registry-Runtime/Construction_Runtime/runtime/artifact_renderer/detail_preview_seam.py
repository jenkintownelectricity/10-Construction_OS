"""Detail preview seam — bounded callable for artifact preview generation.

Provides a single entry point for generating artifact metadata and SVG preview
from the existing artifact renderer pipeline. Reuses the migrated DXF renderer
lineage: same instruction set, same primitives, same deterministic pipeline.

Seam contract:
    Input:  Assembly draft dict (from UI) + detail category
    Output: DetailPreviewResult with SVG content, DXF availability, artifact metadata

Authority: Construction_Runtime (execution only)
Fail-closed: unsupported categories return diagnostic, never fake output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import uuid

from runtime.artifact_renderer.renderer_pipeline import render_artifacts
from runtime.artifact_renderer.artifact_contract import (
    RenderManifest,
    RenderResult,
    ArtifactOutput,
)


SEAM_ID = "detail_preview_seam_v1"
SUPPORTED_CATEGORIES = frozenset({"roofing"})


@dataclass
class DetailPreviewResult:
    """Result from the detail preview seam."""

    success: bool = False
    category: str = ""
    detail_id: str = ""
    seam_id: str = SEAM_ID

    # Artifact metadata
    artifact_type: str = ""
    artifact_filename: str = ""
    generation_status: str = "pending"
    generator_seam: str = SEAM_ID

    # SVG preview (same lineage as DXF)
    svg_content: str = ""
    svg_artifact_id: str = ""
    svg_content_hash: str = ""

    # DXF availability
    dxf_available: bool = False
    dxf_artifact_id: str = ""
    dxf_content: str = ""
    dxf_content_hash: str = ""

    # Lineage
    manifest_id: str = ""
    instruction_set_id: str = ""
    lineage: dict[str, Any] = field(default_factory=dict)

    # Diagnostics
    diagnostics: list[str] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "category": self.category,
            "detail_id": self.detail_id,
            "seam_id": self.seam_id,
            "artifact_type": self.artifact_type,
            "artifact_filename": self.artifact_filename,
            "generation_status": self.generation_status,
            "generator_seam": self.generator_seam,
            "svg_content": self.svg_content,
            "svg_artifact_id": self.svg_artifact_id,
            "svg_content_hash": self.svg_content_hash,
            "dxf_available": self.dxf_available,
            "dxf_artifact_id": self.dxf_artifact_id,
            "dxf_content_hash": self.dxf_content_hash,
            "manifest_id": self.manifest_id,
            "instruction_set_id": self.instruction_set_id,
            "lineage": self.lineage,
            "diagnostics": self.diagnostics,
            "errors": self.errors,
        }


def generate_detail_preview(
    assembly_draft: dict[str, Any],
    category: str,
) -> DetailPreviewResult:
    """Generate a detail preview from an assembly draft.

    Uses the artifact renderer pipeline to produce SVG + DXF from
    the same instruction set (same lineage). The SVG is returned
    for in-UI preview; the DXF is available for download.

    Fail-closed: unsupported categories return a result with
    diagnostics explaining why generation was not attempted.

    Args:
        assembly_draft: Canonical assembly draft dict from the UI.
        category: Detail category (e.g. "roofing", "fireproofing").

    Returns:
        DetailPreviewResult with SVG preview and DXF availability.
    """
    result = DetailPreviewResult(category=category)

    # Gate: category support check (fail-closed)
    if category not in SUPPORTED_CATEGORIES:
        result.generation_status = "unsupported"
        result.diagnostics.append(
            f"FAIL_CLOSED: Category '{category}' is not supported for "
            f"detail generation. Supported categories: "
            f"{sorted(SUPPORTED_CATEGORIES)}."
        )
        result.errors.append({
            "code": "UNSUPPORTED_CATEGORY",
            "message": f"No generator exists for category '{category}'.",
        })
        return result

    # Gate: assembly draft must have layers
    layers = assembly_draft.get("layers", [])
    if not layers:
        result.generation_status = "validation_failed"
        result.diagnostics.append(
            "FAIL_CLOSED: Assembly draft has no layers. "
            "Cannot generate detail without layer stack."
        )
        result.errors.append({
            "code": "NO_LAYERS",
            "message": "Assembly draft contains no layers.",
        })
        return result

    # Build detail DNA from assembly draft layers
    detail_id = assembly_draft.get(
        "system_id", f"DETAIL-{uuid.uuid4().hex[:8]}"
    )
    result.detail_id = detail_id

    detail_dna = _assembly_draft_to_detail_dna(assembly_draft, detail_id)

    # Build manifest requesting SVG + DXF (same instruction set)
    manifest_id = f"MAN-PREVIEW-{uuid.uuid4().hex[:8]}"
    instruction_set_id = f"IS-{detail_id}-preview"

    manifest = RenderManifest(
        manifest_id=manifest_id,
        detail_id=detail_id,
        variant_id="",
        assembly_family=assembly_draft.get("assembly_type", ""),
        instruction_set_id=instruction_set_id,
        requested_formats=["SVG", "DXF"],
        parameters={
            "entities": detail_dna.get("entities", []),
            "sheet_width": 36.0,
            "sheet_height": 24.0,
            "scale": "1:1",
        },
        metadata={
            "display_name": assembly_draft.get("title", ""),
            "source_seam": SEAM_ID,
        },
    )

    # Render through the artifact pipeline (same path as production)
    render_result: RenderResult = render_artifacts(
        manifest=manifest,
        detail_dna=detail_dna,
    )

    result.manifest_id = manifest_id
    result.instruction_set_id = render_result.lineage.get(
        "instruction_set_id", instruction_set_id
    )
    result.lineage = render_result.lineage

    if not render_result.success:
        result.generation_status = "generation_error"
        result.errors.extend(render_result.errors)
        result.diagnostics.append(
            f"Artifact rendering failed with {len(render_result.errors)} error(s)."
        )
        # Even on partial failure, check for any artifacts produced
        _extract_artifacts(render_result, result, detail_id)
        return result

    _extract_artifacts(render_result, result, detail_id)
    result.generation_status = "success"
    result.success = True
    result.artifact_type = "roofing_detail"
    result.artifact_filename = f"{detail_id}.dxf"

    result.diagnostics.append(
        f"Generated SVG preview + DXF from same artifact lineage. "
        f"Renderer seam: {SEAM_ID}. "
        f"Artifacts: {render_result.artifact_count}."
    )

    return result


def _extract_artifacts(
    render_result: RenderResult,
    preview_result: DetailPreviewResult,
    detail_id: str,
) -> None:
    """Extract SVG and DXF artifacts from the render result."""
    svg_artifact: ArtifactOutput | None = render_result.get_artifact_by_format("SVG")
    dxf_artifact: ArtifactOutput | None = render_result.get_artifact_by_format("DXF")

    if svg_artifact:
        preview_result.svg_content = svg_artifact.content
        preview_result.svg_artifact_id = svg_artifact.artifact_id
        preview_result.svg_content_hash = svg_artifact.content_hash

    if dxf_artifact:
        preview_result.dxf_available = True
        preview_result.dxf_artifact_id = dxf_artifact.artifact_id
        preview_result.dxf_content = dxf_artifact.content
        preview_result.dxf_content_hash = dxf_artifact.content_hash
        preview_result.artifact_filename = f"{detail_id}.dxf"


def _assembly_draft_to_detail_dna(
    draft: dict[str, Any],
    detail_id: str,
) -> dict[str, Any]:
    """Convert an assembly draft to detail DNA for the renderer pipeline.

    Maps assembly layers to geometric entities that the instruction builder
    can process into primitives for rendering.
    """
    entities: list[dict[str, Any]] = []
    layers = draft.get("layers", [])
    title = draft.get("title", detail_id)

    sheet_width = 36.0
    sheet_height = 24.0
    margin = 2.0
    usable_width = sheet_width - 2 * margin
    layer_height = min(2.0, (sheet_height - 8.0) / max(len(layers), 1))
    start_y = sheet_height - 4.0

    # Title text
    entities.append({
        "type": "TEXT",
        "layer": "A-TEXT",
        "properties": {
            "text": title,
            "x": sheet_width / 2,
            "y": sheet_height - 1.5,
            "height": 0.25,
            "alignment": "center",
        },
    })

    # Detail boundary
    entities.append({
        "type": "RECTANGLE",
        "layer": "A-DETAIL",
        "properties": {
            "x": margin,
            "y": margin,
            "width": usable_width,
            "height": sheet_height - 2 * margin,
        },
    })

    # Layer stack — each layer as a rectangle with label and dimension
    for i, layer in enumerate(layers):
        y = start_y - (i * (layer_height + 0.3))
        material_ref = layer.get("material_ref", "")
        control_layer = layer.get("control_layer_id", "")
        notes = layer.get("notes", "")
        label = notes if notes else f"{control_layer} ({material_ref})"

        # Layer rectangle
        entities.append({
            "type": "RECTANGLE",
            "layer": "A-COMP",
            "properties": {
                "x": margin + 1.0,
                "y": y - layer_height,
                "width": usable_width - 2.0,
                "height": layer_height,
            },
        })

        # Layer label
        entities.append({
            "type": "TEXT",
            "layer": "A-TEXT",
            "properties": {
                "text": label[:60],
                "x": margin + 1.5,
                "y": y - layer_height / 2,
                "height": 0.12,
            },
        })

        # Control layer annotation
        entities.append({
            "type": "TEXT",
            "layer": "A-ANNO",
            "properties": {
                "text": control_layer.replace("_", " ").upper(),
                "x": sheet_width - margin - 1.0,
                "y": y - layer_height / 2,
                "height": 0.10,
                "alignment": "right",
            },
        })

        # Thickness dimension (if available)
        thickness = layer.get("thickness", "")
        if thickness:
            entities.append({
                "type": "DIMENSION",
                "layer": "A-DIMS",
                "properties": {
                    "x1": margin + 0.5,
                    "y1": y,
                    "x2": margin + 0.5,
                    "y2": y - layer_height,
                    "text": thickness,
                    "unit": "in",
                    "offset": 0.3,
                },
            })

    # Assembly type callout
    assembly_type = draft.get("assembly_type", "")
    if assembly_type:
        entities.append({
            "type": "CALLOUT",
            "layer": "A-ANNO",
            "properties": {
                "ax": sheet_width / 2,
                "ay": 1.5,
                "lx": sheet_width / 2,
                "ly": 3.0,
                "text": assembly_type.replace("_", " ").upper(),
                "bubble_radius": 0.3,
            },
        })

    return {
        "detail_id": detail_id,
        "variant_id": "",
        "assembly_family": draft.get("assembly_type", ""),
        "entities": entities,
        "sheet_width": sheet_width,
        "sheet_height": sheet_height,
        "scale": "1:1",
        "display_name": title,
    }
