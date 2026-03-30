"""
Drawing Manifest Builder — Wave 14 Subsystem 7.

Builds the project shop drawing manifest from packaged details,
sheet index, and variant data. Output is deterministic.
No rendering occurs — manifests are for downstream renderer consumption.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

CONTRACT_VERSION = "14.7.0"


class DrawingManifestError(Exception):
    """Raised when manifest building fails."""


def build_drawing_manifest(
    project_id: str,
    sheet_index: dict[str, Any],
    packaged_details: list[dict[str, Any]],
    variant_manifest: dict[str, Any] | None = None,
    sequence_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build the complete shop drawing manifest.
    All entries must reference resolved canonical detail IDs or derived variant IDs.
    """
    # Build drawing entries from sheet index
    drawing_entries: list[dict[str, Any]] = []
    for sheet in sorted(sheet_index.get("sheets", []), key=lambda s: s.get("sheet_number", 0)):
        detail_id = sheet.get("canonical_detail_id", "")
        # Find matching package entry
        package_match = next(
            (p for p in packaged_details if p.get("canonical_detail_id") == detail_id),
            None,
        )

        entry: dict[str, Any] = {
            "sheet_id": sheet.get("sheet_id", ""),
            "sheet_number": sheet.get("sheet_number", 0),
            "canonical_detail_id": detail_id,
            "title": sheet.get("title", ""),
            "render_type": package_match.get("render_type", "canonical") if package_match else "canonical",
        }

        if package_match and package_match.get("variant_id"):
            entry["variant_id"] = package_match["variant_id"]
            entry["parameters"] = package_match.get("parameters", {})

        drawing_entries.append(entry)

    manifest = {
        "manifest_id": f"shop-drawing-{project_id}",
        "project_id": project_id,
        "contract_version": CONTRACT_VERSION,
        "generation_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "drawing_entries": drawing_entries,
        "summary": {
            "total_drawings": len(drawing_entries),
            "canonical_count": sum(1 for e in drawing_entries if e["render_type"] == "canonical"),
            "variant_count": sum(1 for e in drawing_entries if e["render_type"] == "variant"),
        },
    }

    if variant_manifest:
        manifest["variant_manifest_ref"] = variant_manifest.get("manifest_id", "")
    if sequence_manifest:
        manifest["sequence_manifest_ref"] = sequence_manifest.get("manifest_id", "")

    content = json.dumps(drawing_entries, sort_keys=True, separators=(",", ":"))
    manifest["checksum"] = hashlib.sha256(content.encode("utf-8")).hexdigest()

    return manifest


def build_drawing_package_manifest(
    project_id: str,
    shop_drawing_manifest: dict[str, Any],
    sheet_index: dict[str, Any],
) -> dict[str, Any]:
    """
    Build the drawing package manifest that combines shop drawing and sheet index.
    """
    package = {
        "package_id": f"pkg-{project_id}",
        "project_id": project_id,
        "contract_version": CONTRACT_VERSION,
        "generation_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "shop_drawing_manifest_ref": shop_drawing_manifest.get("manifest_id", ""),
        "sheet_index_ref": f"sheet-index-{project_id}",
        "total_sheets": sheet_index.get("total_sheets", 0),
        "total_drawings": shop_drawing_manifest.get("summary", {}).get("total_drawings", 0),
    }

    content = json.dumps(package, sort_keys=True, separators=(",", ":"))
    package["checksum"] = hashlib.sha256(content.encode("utf-8")).hexdigest()

    return package
