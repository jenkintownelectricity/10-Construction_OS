"""
Installation Sequence Engine — Wave 14 Subsystem 6.

Generates derived installation sequences from resolved details.
Sequences reference valid canonical detail IDs only.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

CONTRACT_VERSION = "14.6.0"

CANONICAL_DETAIL_FAMILIES = frozenset([
    "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
    "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01",
    "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01",
    "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01",
    "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01",
    "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01",
    "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01",
    "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01",
    "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01",
])

# Installation sequences derived from construction practice
DETAIL_SEQUENCES: dict[str, list[dict[str, Any]]] = {
    "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01": [
        {"step_number": 1, "action": "Install cant strip at base of parapet", "detail_context": "base_preparation", "dependencies": []},
        {"step_number": 2, "action": "Apply base flashing membrane to parapet face", "detail_context": "membrane_application", "dependencies": [1]},
        {"step_number": 3, "action": "Fasten termination bar at top of membrane", "detail_context": "mechanical_fastening", "dependencies": [2]},
        {"step_number": 4, "action": "Apply sealant above termination bar", "detail_context": "sealant_application", "dependencies": [3]},
        {"step_number": 5, "action": "Install counterflashing over termination", "detail_context": "counterflashing", "dependencies": [4]},
    ],
    "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01": [
        {"step_number": 1, "action": "Install cant strip at base of wall", "detail_context": "base_preparation", "dependencies": []},
        {"step_number": 2, "action": "Heat-weld TPO base flashing to field membrane", "detail_context": "membrane_welding", "dependencies": [1]},
        {"step_number": 3, "action": "Fasten termination bar at required height", "detail_context": "mechanical_fastening", "dependencies": [2]},
        {"step_number": 4, "action": "Apply sealant at top of termination bar", "detail_context": "sealant_application", "dependencies": [3]},
    ],
    "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01": [
        {"step_number": 1, "action": "Install cant strip at wall transition", "detail_context": "base_preparation", "dependencies": []},
        {"step_number": 2, "action": "Heat-weld PVC membrane up wall face", "detail_context": "membrane_welding", "dependencies": [1]},
        {"step_number": 3, "action": "Cut reglet into masonry wall", "detail_context": "reglet_preparation", "dependencies": []},
        {"step_number": 4, "action": "Insert membrane into reglet", "detail_context": "membrane_insertion", "dependencies": [2, 3]},
        {"step_number": 5, "action": "Seal reglet with appropriate sealant", "detail_context": "sealant_application", "dependencies": [4]},
    ],
    "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01": [
        {"step_number": 1, "action": "Install wood nailer at roof edge", "detail_context": "substrate_preparation", "dependencies": []},
        {"step_number": 2, "action": "Extend TPO membrane over nailer", "detail_context": "membrane_application", "dependencies": [1]},
        {"step_number": 3, "action": "Install metal edge flashing", "detail_context": "metal_installation", "dependencies": [2]},
        {"step_number": 4, "action": "Fasten metal edge through membrane", "detail_context": "mechanical_fastening", "dependencies": [3]},
    ],
    "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01": [
        {"step_number": 1, "action": "Clean pipe surface and surrounding membrane", "detail_context": "surface_preparation", "dependencies": []},
        {"step_number": 2, "action": "Apply primer to pipe and membrane", "detail_context": "primer_application", "dependencies": [1]},
        {"step_number": 3, "action": "Install pipe boot over penetration", "detail_context": "boot_installation", "dependencies": [2]},
        {"step_number": 4, "action": "Apply adhesive and seal boot to field membrane", "detail_context": "membrane_bonding", "dependencies": [3]},
        {"step_number": 5, "action": "Install clamp at top of pipe boot", "detail_context": "clamping", "dependencies": [4]},
    ],
    "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01": [
        {"step_number": 1, "action": "Install cant strip around curb perimeter", "detail_context": "base_preparation", "dependencies": []},
        {"step_number": 2, "action": "Heat-weld TPO membrane up curb faces", "detail_context": "membrane_welding", "dependencies": [1]},
        {"step_number": 3, "action": "Install counterflashing at top of curb", "detail_context": "counterflashing", "dependencies": [2]},
        {"step_number": 4, "action": "Seal all curb flashing terminations", "detail_context": "sealant_application", "dependencies": [3]},
    ],
    "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01": [
        {"step_number": 1, "action": "Set drain body in deck opening", "detail_context": "drain_placement", "dependencies": []},
        {"step_number": 2, "action": "Heat-weld TPO membrane to drain flange", "detail_context": "membrane_welding", "dependencies": [1]},
        {"step_number": 3, "action": "Install clamping ring over membrane", "detail_context": "clamping", "dependencies": [2]},
        {"step_number": 4, "action": "Install drain dome or strainer", "detail_context": "accessory_installation", "dependencies": [3]},
    ],
    "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01": [
        {"step_number": 1, "action": "Frame scupper opening in parapet wall", "detail_context": "opening_preparation", "dependencies": []},
        {"step_number": 2, "action": "Install metal scupper box", "detail_context": "metal_installation", "dependencies": [1]},
        {"step_number": 3, "action": "Torch-apply SBS membrane into and around scupper", "detail_context": "membrane_application", "dependencies": [2]},
        {"step_number": 4, "action": "Seal all membrane-to-metal transitions", "detail_context": "sealant_application", "dependencies": [3]},
    ],
    "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01": [
        {"step_number": 1, "action": "Install backer rod in expansion joint gap", "detail_context": "joint_preparation", "dependencies": []},
        {"step_number": 2, "action": "Apply primer to both sides of joint", "detail_context": "primer_application", "dependencies": [1]},
        {"step_number": 3, "action": "Apply self-adhered EPDM expansion joint cover", "detail_context": "membrane_application", "dependencies": [2]},
        {"step_number": 4, "action": "Roll and press membrane for full adhesion", "detail_context": "adhesion_verification", "dependencies": [3]},
    ],
}


class SequenceGenerationError(Exception):
    """Raised when sequence generation fails."""


def generate_sequence(canonical_detail_id: str) -> dict[str, Any]:
    """
    Generate an installation sequence for a canonical detail.
    Fails closed if no sequence is defined.
    """
    if canonical_detail_id not in CANONICAL_DETAIL_FAMILIES:
        raise SequenceGenerationError(
            f"Detail ID '{canonical_detail_id}' not in canonical families."
        )

    steps = DETAIL_SEQUENCES.get(canonical_detail_id)
    if not steps:
        return {
            "sequence_id": f"seq-{canonical_detail_id}",
            "detail_ref": canonical_detail_id,
            "steps": [],
            "status": "UNRESOLVED",
            "reason": f"No installation sequence defined for '{canonical_detail_id}'.",
        }

    return {
        "sequence_id": f"seq-{canonical_detail_id}",
        "detail_ref": canonical_detail_id,
        "steps": steps,
        "status": "RESOLVED",
        "reason": f"Installation sequence generated for '{canonical_detail_id}'.",
    }


def generate_sequence_manifest(
    resolved_detail_ids: list[str],
    manifest_id: str = "installation-sequence-manifest",
) -> dict[str, Any]:
    """
    Generate installation sequences for all resolved details.
    Returns a manifest with deterministic ordering.
    """
    sequences: list[dict[str, Any]] = []
    for detail_id in sorted(set(resolved_detail_ids)):
        if detail_id not in CANONICAL_DETAIL_FAMILIES:
            sequences.append({
                "sequence_id": f"seq-{detail_id}",
                "detail_ref": detail_id,
                "steps": [],
                "status": "UNSUPPORTED",
                "reason": f"Detail ID '{detail_id}' not in canonical families.",
            })
            continue
        sequences.append(generate_sequence(detail_id))

    manifest = {
        "manifest_id": manifest_id,
        "contract_version": CONTRACT_VERSION,
        "generation_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sequences": sequences,
        "summary": {
            "total": len(sequences),
            "resolved": sum(1 for s in sequences if s["status"] == "RESOLVED"),
            "unresolved": sum(1 for s in sequences if s["status"] == "UNRESOLVED"),
            "unsupported": sum(1 for s in sequences if s["status"] == "UNSUPPORTED"),
        },
    }

    content_for_checksum = json.dumps(
        sequences, sort_keys=True, separators=(",", ":")
    )
    manifest["checksum"] = hashlib.sha256(content_for_checksum.encode("utf-8")).hexdigest()

    return manifest
