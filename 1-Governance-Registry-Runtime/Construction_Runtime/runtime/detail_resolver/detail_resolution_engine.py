"""
Detail Resolution Engine — Wave 14 Subsystem 2.

Orchestrates condition classification and detail selection to produce
a resolved detail manifest from a project condition graph.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from runtime.detail_resolver.condition_classifier import classify_condition
from runtime.detail_resolver.detail_selector import (
    CANONICAL_DETAIL_FAMILIES,
    select_detail,
)

CONTRACT_VERSION = "14.2.0"


class DetailResolutionError(Exception):
    """Raised when resolution encounters a fatal error."""


def resolve_details(
    condition_graph: dict[str, Any],
    material_context: str | None = None,
) -> dict[str, Any]:
    """
    Resolve canonical detail families for all nodes in a condition graph.
    Returns a resolved_detail_manifest.

    Args:
        condition_graph: A valid project_condition_graph.json
        material_context: Optional assembly family context (e.g., "EPDM", "TPO")

    Returns:
        Resolved detail manifest with deterministic output.
    """
    nodes = condition_graph.get("nodes", [])
    if not nodes:
        raise DetailResolutionError("Condition graph has no nodes to resolve.")

    resolved_items: list[dict[str, Any]] = []

    for node in sorted(nodes, key=lambda n: n.get("node_id", "")):
        classification = classify_condition(node)

        if classification.status == "UNSUPPORTED":
            resolved_items.append({
                "condition_ref": classification.node_id,
                "canonical_detail_id": None,
                "resolution_status": "UNSUPPORTED",
                "resolution_reason": classification.reason,
                "material_context_ref": material_context or "",
                "route_context_ref": "",
                "ambiguity_flags": [],
            })
            continue

        if classification.status == "UNKNOWN":
            resolved_items.append({
                "condition_ref": classification.node_id,
                "canonical_detail_id": None,
                "resolution_status": "UNKNOWN",
                "resolution_reason": classification.reason,
                "material_context_ref": material_context or "",
                "route_context_ref": "",
                "ambiguity_flags": [],
            })
            continue

        # Use node-level material_context if available, else fall back to global
        node_material = node.get("material_context", material_context)

        selection = select_detail(
            kernel_condition=classification.kernel_condition,
            material_context=node_material,
        )

        # Verify selected ID exists in canonical families
        if selection.canonical_detail_id and selection.canonical_detail_id not in CANONICAL_DETAIL_FAMILIES:
            resolved_items.append({
                "condition_ref": classification.node_id,
                "canonical_detail_id": None,
                "resolution_status": "UNRESOLVED",
                "resolution_reason": f"Selected ID '{selection.canonical_detail_id}' not found in canonical families. Aborting.",
                "material_context_ref": node_material or "",
                "route_context_ref": "",
                "ambiguity_flags": ["CANONICAL_VALIDATION_FAILED"],
            })
            continue

        resolved_items.append({
            "condition_ref": classification.node_id,
            "canonical_detail_id": selection.canonical_detail_id,
            "resolution_status": selection.status,
            "resolution_reason": f"{classification.reason} → {selection.reason}",
            "material_context_ref": node_material or "",
            "route_context_ref": "",
            "ambiguity_flags": selection.ambiguity_flags,
        })

    manifest = {
        "manifest_id": f"resolved-{condition_graph.get('graph_id', 'unknown')}",
        "source_graph_id": condition_graph.get("graph_id", ""),
        "contract_version": CONTRACT_VERSION,
        "resolution_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "material_context": material_context or "",
        "resolved_items": resolved_items,
        "summary": {
            "total": len(resolved_items),
            "resolved": sum(1 for r in resolved_items if r["resolution_status"] == "RESOLVED"),
            "unresolved": sum(1 for r in resolved_items if r["resolution_status"] == "UNRESOLVED"),
            "unknown": sum(1 for r in resolved_items if r["resolution_status"] == "UNKNOWN"),
            "unsupported": sum(1 for r in resolved_items if r["resolution_status"] == "UNSUPPORTED"),
        },
    }

    content_for_checksum = json.dumps(
        manifest["resolved_items"], sort_keys=True, separators=(",", ":")
    )
    manifest["checksum"] = hashlib.sha256(content_for_checksum.encode("utf-8")).hexdigest()

    return manifest
