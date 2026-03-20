"""Renderer pipeline — orchestrates deterministic artifact rendering.

Pipeline: Detail DNA -> Instruction Set -> Renderers -> DXF/SVG/PDF
Entry point: render_artifacts(manifest)

All outputs are deterministic. All failures are classified.
Kernel is never mutated.
"""

from typing import Any
import uuid

from runtime.artifact_renderer.artifact_contract import (
    RenderManifest,
    ArtifactOutput,
    RenderResult,
    SUPPORTED_OUTPUT_FORMATS,
)
from runtime.artifact_renderer.instruction_builder import build_instruction_set
from runtime.artifact_renderer.artifact_lineage import (
    build_lineage_chain,
    compute_content_hash,
)
from runtime.artifact_renderer.renderer_registry import (
    RendererRegistry,
    get_global_registry,
)
from runtime.artifact_renderer.renderer_errors import (
    PipelineError,
    ManifestError,
    RendererNotFoundError,
    InvalidInstructionSetError,
)
from runtime.artifact_renderer.dxf_renderer import DxfRenderer
from runtime.artifact_renderer.svg_renderer import SvgRenderer
from runtime.artifact_renderer.pdf_renderer import PdfRenderer


PIPELINE_VERSION = "18.0"


def render_artifacts(
    manifest: RenderManifest | dict[str, Any],
    detail_dna: dict[str, Any] | None = None,
    variant_params: dict[str, Any] | None = None,
    registry: RendererRegistry | None = None,
) -> RenderResult:
    """Render artifacts from a manifest.

    This is the primary entry point for the artifact rendering pipeline.

    Args:
        manifest: RenderManifest or dict describing what to render.
        detail_dna: Resolved detail DNA from the kernel (optional if
            instruction set is pre-built).
        variant_params: Optional variant parameter overrides.
        registry: Optional renderer registry (uses global if not provided).

    Returns:
        RenderResult with artifacts, lineage, and any errors.
    """
    # Normalize manifest
    if isinstance(manifest, dict):
        manifest = _dict_to_manifest(manifest)

    # Validate manifest
    manifest_errors = manifest.validate()
    if manifest_errors:
        return RenderResult(
            manifest_id=manifest.manifest_id,
            errors=[{"code": "MANIFEST_VALIDATION", "message": e} for e in manifest_errors],
            success=False,
        )

    # Get or create registry
    if registry is None:
        registry = _ensure_default_registry()

    result = RenderResult(manifest_id=manifest.manifest_id)

    try:
        # Stage 1: Build instruction set from detail DNA
        instruction_set = _build_instructions(manifest, detail_dna, variant_params)

        # Stage 2: Render each requested format
        artifact_data = []
        for fmt in manifest.requested_formats:
            try:
                artifact = _render_format(
                    fmt, instruction_set, manifest, registry
                )
                result.artifacts.append(artifact)
                artifact_data.append({
                    "artifact_id": artifact.artifact_id,
                    "content": artifact.content,
                    "format": artifact.format,
                    "renderer_id": artifact.renderer_id,
                })
            except RendererNotFoundError as e:
                result.errors.append(e.to_dict())
            except Exception as e:
                result.errors.append({
                    "code": "RENDER_FORMAT_ERROR",
                    "message": f"Failed to render {fmt}: {e}",
                })

        # Stage 3: Build lineage chain
        if artifact_data:
            lineage = build_lineage_chain(
                detail_id=manifest.detail_id,
                instruction_set_id=instruction_set.get("instruction_set_id", ""),
                manifest_id=manifest.manifest_id,
                artifacts=artifact_data,
            )
            result.lineage = lineage.to_dict()

        result.success = len(result.artifacts) > 0 and len(result.errors) == 0

    except InvalidInstructionSetError as e:
        result.errors.append(e.to_dict())
    except PipelineError as e:
        result.errors.append(e.to_dict())
    except Exception as e:
        result.errors.append({
            "code": "PIPELINE_UNEXPECTED_ERROR",
            "message": str(e),
        })

    return result


def _build_instructions(
    manifest: RenderManifest,
    detail_dna: dict[str, Any] | None,
    variant_params: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build instruction set from detail DNA."""
    if detail_dna is None:
        # If no detail DNA provided, create a minimal one from manifest
        detail_dna = {
            "detail_id": manifest.detail_id,
            "variant_id": manifest.variant_id,
            "assembly_family": manifest.assembly_family,
            "entities": manifest.parameters.get("entities", []),
            "sheet_width": manifest.parameters.get("sheet_width", 36.0),
            "sheet_height": manifest.parameters.get("sheet_height", 24.0),
            "scale": manifest.parameters.get("scale", "1:1"),
            "display_name": manifest.metadata.get("display_name", ""),
        }

    return build_instruction_set(detail_dna, variant_params)


def _render_format(
    fmt: str,
    instruction_set: dict[str, Any],
    manifest: RenderManifest,
    registry: RendererRegistry,
) -> ArtifactOutput:
    """Render a single format from the instruction set."""
    renderer = registry.get_renderer(fmt)

    primitives = instruction_set.get("primitives", [])
    sheet = instruction_set.get("sheet", {})
    layers = instruction_set.get("layers", [])
    metadata = {
        "title": instruction_set.get("title", {}),
        "provenance": instruction_set.get("provenance", {}),
    }

    content, errors = renderer.render(primitives, sheet, layers, metadata)

    if errors:
        raise PipelineError(
            stage=f"render_{fmt}",
            reason=f"{len(errors)} error(s) during {fmt} rendering.",
        )

    artifact_id = f"ART-{manifest.detail_id}-{fmt}-{uuid.uuid4().hex[:8]}"
    content_hash = compute_content_hash(content, fmt)

    return ArtifactOutput(
        artifact_id=artifact_id,
        format=fmt,
        content=content,
        content_hash=content_hash,
        source_manifest_id=manifest.manifest_id,
        source_instruction_set_id=instruction_set.get("instruction_set_id", ""),
        source_detail_id=manifest.detail_id,
        renderer_id=renderer.renderer_id(),
        metadata={
            "pipeline_version": PIPELINE_VERSION,
            "sheet": sheet,
        },
    )


def _dict_to_manifest(d: dict[str, Any]) -> RenderManifest:
    """Convert a dictionary to a RenderManifest."""
    return RenderManifest(
        manifest_id=d.get("manifest_id", f"MAN-{uuid.uuid4().hex[:8]}"),
        detail_id=d.get("detail_id", ""),
        variant_id=d.get("variant_id", ""),
        assembly_family=d.get("assembly_family", ""),
        instruction_set_id=d.get("instruction_set_id", ""),
        requested_formats=d.get("requested_formats", ["DXF", "SVG", "PDF"]),
        parameters=d.get("parameters", {}),
        metadata=d.get("metadata", {}),
    )


def _ensure_default_registry() -> RendererRegistry:
    """Ensure the global registry has default renderers registered."""
    registry = get_global_registry()
    if not registry.has_renderer("DXF"):
        registry.register(DxfRenderer())
    if not registry.has_renderer("SVG"):
        registry.register(SvgRenderer())
    if not registry.has_renderer("PDF"):
        registry.register(PdfRenderer())
    return registry
