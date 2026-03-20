"""Pipeline integration: wires the artifact renderer into the existing runtime.

Bridges:
  condition_graph -> detail_resolver -> variant_generator -> shop_drawing_prep
  -> artifact_renderer -> file storage

This is the glue that makes the full acceptance test path work:
  Condition -> resolve detail -> generate variant -> manifest -> render DXF/SVG/PDF
"""

import os
import json
import uuid
from typing import Any
from datetime import datetime, timezone

from runtime.condition_graph.condition_graph_builder import ConditionGraphBuilder
from runtime.detail_resolver.detail_resolution_engine import resolve_details
from runtime.detail_variants.variant_generator import (
    generate_variant,
    generate_variant_manifest,
    DETAIL_CONDITION_MAP,
    CONDITION_PARAMETERS,
)
from runtime.installation_sequence.sequence_engine import generate_sequence
from runtime.artifact_renderer.renderer_pipeline import render_artifacts
from runtime.artifact_renderer.artifact_contract import RenderManifest


# Default detail DNA geometry templates per canonical detail condition
# These define the actual drawing geometry for each condition type
DETAIL_DNA_TEMPLATES: dict[str, dict[str, Any]] = {
    "PARAPET": {
        "sheet_width": 36.0,
        "sheet_height": 24.0,
        "scale": "3:1",
        "entities": [
            {"type": "RECTANGLE", "layer": "A-COMP", "properties": {"x": 2, "y": 2, "width": 1.5, "height": 12}},
            {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 0, "y1": 2, "x2": 8, "y2": 2}},
            {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 0, "y1": 14, "x2": 8, "y2": 14}},
            {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 3.5, "y1": 2, "x2": 3.5, "y2": 14}},
            {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 3.5, "y1": 14, "x2": 6, "y2": 14}},
            {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 6, "y1": 13, "x2": 6, "y2": 15}},
            {"type": "HATCH", "layer": "A-HATCH", "properties": {"boundary": [[2, 2], [3.5, 2], [3.5, 14], [2, 14]], "pattern": "ANSI31"}},
            {"type": "TEXT", "layer": "A-TEXT", "properties": {"text": "EPDM MEMBRANE", "x": 4, "y": 8, "height": 0.2}},
            {"type": "TEXT", "layer": "A-TEXT", "properties": {"text": "COUNTERFLASHING", "x": 4.5, "y": 15, "height": 0.2}},
            {"type": "TEXT", "layer": "A-TEXT", "properties": {"text": "CANT STRIP", "x": 0.5, "y": 1.5, "height": 0.15}},
            {"type": "DIMENSION", "layer": "A-DIMS", "properties": {"x1": 2, "y1": 0.5, "x2": 3.5, "y2": 0.5, "text": '1 1/2"'}},
            {"type": "CALLOUT", "layer": "A-ANNO", "properties": {"ax": 1, "ay": 18, "lx": 2.5, "ly": 8, "text": "1"}},
            {"type": "ARC", "layer": "A-DETAIL", "properties": {"cx": 2, "cy": 2, "radius": 0.75, "start_angle": 0, "end_angle": 90}},
        ],
    },
    "PIPE": {
        "sheet_width": 36.0,
        "sheet_height": 24.0,
        "scale": "3:1",
        "entities": [
            {"type": "ARC", "layer": "A-DETAIL", "properties": {"cx": 5, "cy": 8, "radius": 2, "start_angle": 0, "end_angle": 360}},
            {"type": "ARC", "layer": "A-DETAIL", "properties": {"cx": 5, "cy": 8, "radius": 3, "start_angle": 0, "end_angle": 360}},
            {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 0, "y1": 4, "x2": 10, "y2": 4}},
            {"type": "TEXT", "layer": "A-TEXT", "properties": {"text": "PIPE BOOT", "x": 6, "y": 12, "height": 0.2}},
            {"type": "TEXT", "layer": "A-TEXT", "properties": {"text": "FIELD MEMBRANE", "x": 1, "y": 3.5, "height": 0.15}},
            {"type": "DIMENSION", "layer": "A-DIMS", "properties": {"x1": 3, "y1": 8, "x2": 7, "y2": 8, "text": "DIA"}},
            {"type": "CALLOUT", "layer": "A-ANNO", "properties": {"ax": 9, "ay": 14, "lx": 6, "ly": 10, "text": "1"}},
        ],
    },
    "DRAIN": {
        "sheet_width": 36.0,
        "sheet_height": 24.0,
        "scale": "3:1",
        "entities": [
            {"type": "RECTANGLE", "layer": "A-COMP", "properties": {"x": 3, "y": 2, "width": 6, "height": 2}},
            {"type": "ARC", "layer": "A-DETAIL", "properties": {"cx": 6, "cy": 6, "radius": 2.5, "start_angle": 0, "end_angle": 360}},
            {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 0, "y1": 4, "x2": 12, "y2": 4}},
            {"type": "TEXT", "layer": "A-TEXT", "properties": {"text": "DRAIN BODY", "x": 4, "y": 1.5, "height": 0.2}},
            {"type": "TEXT", "layer": "A-TEXT", "properties": {"text": "CLAMPING RING", "x": 4, "y": 9, "height": 0.15}},
            {"type": "DIMENSION", "layer": "A-DIMS", "properties": {"x1": 3.5, "y1": 6, "x2": 8.5, "y2": 6, "text": "DIA"}},
        ],
    },
}

# Fallback minimal template for any unspecified condition
DEFAULT_TEMPLATE: dict[str, Any] = {
    "sheet_width": 36.0,
    "sheet_height": 24.0,
    "scale": "1:1",
    "entities": [
        {"type": "RECTANGLE", "layer": "A-COMP", "properties": {"x": 2, "y": 2, "width": 10, "height": 8}},
        {"type": "LINE", "layer": "A-DETAIL", "properties": {"x1": 0, "y1": 2, "x2": 14, "y2": 2}},
        {"type": "TEXT", "layer": "A-TEXT", "properties": {"text": "DETAIL", "x": 5, "y": 12, "height": 0.25}},
        {"type": "DIMENSION", "layer": "A-DIMS", "properties": {"x1": 2, "y1": 0.5, "x2": 12, "y2": 0.5, "text": '10"'}},
    ],
}


def build_detail_dna(
    canonical_detail_id: str,
    variant_params: dict[str, Any] | None = None,
    display_name: str = "",
) -> dict[str, Any]:
    """Build detail DNA from a canonical detail ID and optional variant parameters."""
    condition = DETAIL_CONDITION_MAP.get(canonical_detail_id, "")
    template = DETAIL_DNA_TEMPLATES.get(condition, DEFAULT_TEMPLATE)

    return {
        "detail_id": canonical_detail_id,
        "variant_id": "",
        "assembly_family": condition.lower() if condition else "unknown",
        "display_name": display_name or canonical_detail_id.replace("-", " ").title(),
        "sheet_width": template["sheet_width"],
        "sheet_height": template["sheet_height"],
        "scale": template["scale"],
        "entities": template["entities"],
    }


def run_full_render_pipeline(
    condition_graph: dict[str, Any],
    material_context: str | None = None,
    output_dir: str = "artifacts",
    requested_formats: list[str] | None = None,
) -> dict[str, Any]:
    """Run the full pipeline: condition graph -> render artifacts.

    Returns a pipeline result dict with all outputs.
    """
    requested_formats = requested_formats or ["DXF", "SVG", "PDF"]
    results: dict[str, Any] = {
        "pipeline_id": f"pipeline-{uuid.uuid4().hex[:8]}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "condition_graph_id": condition_graph.get("graph_id", ""),
        "resolved_details": [],
        "variants": [],
        "sequences": [],
        "render_results": [],
        "stored_artifacts": [],
        "errors": [],
    }

    # Stage 1: Resolve details from condition graph
    try:
        resolved_manifest = resolve_details(condition_graph, material_context)
        results["resolved_manifest"] = resolved_manifest
    except Exception as e:
        results["errors"].append({"stage": "resolution", "error": str(e)})
        return results

    resolved_items = [
        item for item in resolved_manifest.get("resolved_items", [])
        if item.get("resolution_status") == "RESOLVED" and item.get("canonical_detail_id")
    ]
    results["resolved_details"] = resolved_items

    if not resolved_items:
        results["errors"].append({"stage": "resolution", "error": "No details resolved."})
        return results

    # Stage 2: For each resolved detail, generate variant + sequence + render
    os.makedirs(output_dir, exist_ok=True)

    for item in resolved_items:
        canonical_id = item["canonical_detail_id"]
        condition = DETAIL_CONDITION_MAP.get(canonical_id, "")

        # Generate a default variant
        allowed_params = CONDITION_PARAMETERS.get(condition, [])
        default_params = {}
        if "parapet_height" in allowed_params:
            default_params["parapet_height"] = 36.0
        if "membrane_thickness" in allowed_params:
            default_params["membrane_thickness"] = 0.060
        if "pipe_diameter" in allowed_params:
            default_params["pipe_diameter"] = 4.0
        if "drain_diameter" in allowed_params:
            default_params["drain_diameter"] = 4.0

        variant = None
        if default_params:
            try:
                variant = generate_variant(canonical_id, default_params)
                results["variants"].append(variant)
            except Exception as e:
                results["errors"].append({"stage": "variant", "detail": canonical_id, "error": str(e)})

        # Generate installation sequence
        try:
            sequence = generate_sequence(canonical_id)
            results["sequences"].append(sequence)
        except Exception as e:
            results["errors"].append({"stage": "sequence", "detail": canonical_id, "error": str(e)})

        # Build detail DNA
        detail_dna = build_detail_dna(canonical_id, default_params)

        # Create render manifest
        manifest = RenderManifest(
            manifest_id=f"MAN-{canonical_id}-{uuid.uuid4().hex[:6]}",
            detail_id=canonical_id,
            variant_id=variant["variant_id"] if variant else "",
            assembly_family=condition.lower() if condition else "",
            instruction_set_id=f"IS-{canonical_id}",
            requested_formats=requested_formats,
            metadata={
                "display_name": detail_dna["display_name"],
                "condition_ref": item.get("condition_ref", ""),
            },
        )

        # Render artifacts
        try:
            render_result = render_artifacts(
                manifest=manifest,
                detail_dna=detail_dna,
                variant_params=default_params if default_params else None,
            )
            results["render_results"].append(render_result.to_dict())

            # Store artifacts to disk
            if render_result.success:
                for artifact in render_result.artifacts:
                    stored = store_artifact(artifact, output_dir)
                    results["stored_artifacts"].append(stored)

        except Exception as e:
            results["errors"].append({"stage": "render", "detail": canonical_id, "error": str(e)})

    # Build summary
    results["summary"] = {
        "details_resolved": len(resolved_items),
        "variants_generated": len(results["variants"]),
        "sequences_generated": len(results["sequences"]),
        "artifacts_rendered": sum(r.get("artifact_count", 0) for r in results["render_results"]),
        "artifacts_stored": len(results["stored_artifacts"]),
        "errors": len(results["errors"]),
        "success": len(results["errors"]) == 0 and len(results["stored_artifacts"]) > 0,
    }

    # Write pipeline result to disk
    result_path = os.path.join(output_dir, "pipeline_result.json")
    with open(result_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    return results


def store_artifact(artifact, output_dir: str) -> dict[str, Any]:
    """Write artifact content to disk and return file metadata."""
    fmt = artifact.format.lower()
    detail_id = artifact.source_detail_id
    safe_name = detail_id.replace("/", "_").replace(" ", "_")

    extensions = {"dxf": ".dxf", "svg": ".svg", "pdf": ".pdf"}
    ext = extensions.get(fmt, f".{fmt}")
    filename = f"{safe_name}{ext}"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(artifact.content)

    return {
        "artifact_id": artifact.artifact_id,
        "format": artifact.format,
        "filename": filename,
        "filepath": filepath,
        "content_hash": artifact.content_hash,
        "source_detail_id": artifact.source_detail_id,
        "renderer_id": artifact.renderer_id,
        "file_size": len(artifact.content),
    }
