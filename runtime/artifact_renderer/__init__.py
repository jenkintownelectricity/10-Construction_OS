"""Artifact renderer — deterministic DXF/SVG/PDF rendering pipeline.

Wave 18: Construction_Runtime artifact rendering subsystem.

Pipeline: Detail DNA -> Instruction Set -> Renderers -> DXF/SVG/PDF
Entry point: render_artifacts(manifest)

Authority: Construction_Runtime (execution only)
Kernel: Read-only, never mutated by renderers.
All outputs are deterministic with SHA-256 lineage tracking.
"""

from runtime.artifact_renderer.renderer_pipeline import render_artifacts
from runtime.artifact_renderer.artifact_contract import (
    RenderManifest,
    ArtifactOutput,
    RenderResult,
    RendererCapability,
    SUPPORTED_OUTPUT_FORMATS,
    ARTIFACT_CONTRACT_VERSION,
)
from runtime.artifact_renderer.geometry_primitives import (
    Point2D,
    LinePrimitive,
    ArcPrimitive,
    PolylinePrimitive,
    RectanglePrimitive,
    TextPrimitive,
    HatchPrimitive,
    DimensionPrimitive,
    CalloutPrimitive,
    Primitive,
    SUPPORTED_PRIMITIVES,
)
from runtime.artifact_renderer.instruction_builder import (
    build_instruction_set,
    primitives_to_drawing_instruction_set,
)
from runtime.artifact_renderer.renderer_registry import (
    RendererRegistry,
    get_global_registry,
    register_renderer,
    get_renderer,
)
from runtime.artifact_renderer.dxf_renderer import DxfRenderer
from runtime.artifact_renderer.svg_renderer import SvgRenderer
from runtime.artifact_renderer.pdf_renderer import PdfRenderer
from runtime.artifact_renderer.artifact_lineage import (
    compute_sha256,
    compute_content_hash,
    create_lineage_record,
    verify_determinism,
    build_lineage_chain,
    LineageRecord,
    LineageBundle,
)
