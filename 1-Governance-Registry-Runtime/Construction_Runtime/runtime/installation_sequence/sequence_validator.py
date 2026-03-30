"""
Sequence Validator — Wave 14 Subsystem 6.

Validates installation sequence manifests for contract compliance.
"""

from typing import Any

from runtime.installation_sequence.dependency_resolver import validate_dependencies

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

VALID_STATUSES = frozenset(["RESOLVED", "UNRESOLVED", "UNSUPPORTED"])


def validate_sequence_manifest(manifest: dict[str, Any]) -> list[str]:
    """
    Validate an installation sequence manifest.
    Returns list of errors. Empty means valid.
    """
    errors: list[str] = []

    for field in ("manifest_id", "contract_version", "sequences", "checksum"):
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    sequences = manifest.get("sequences", [])
    if not isinstance(sequences, list):
        errors.append("'sequences' must be an array.")
        return errors

    for i, seq in enumerate(sequences):
        detail_ref = seq.get("detail_ref", "")
        status = seq.get("status", "")

        if status not in VALID_STATUSES:
            errors.append(f"Sequence {i}: invalid status '{status}'.")

        if status == "RESOLVED":
            if detail_ref not in CANONICAL_DETAIL_FAMILIES:
                errors.append(f"Sequence {i}: detail_ref '{detail_ref}' not in canonical families.")

            dep_errors = validate_dependencies(seq)
            for err in dep_errors:
                errors.append(f"Sequence {i} ({detail_ref}): {err}")

    # Deterministic ordering
    refs = [s.get("detail_ref", "") for s in sequences]
    if refs != sorted(refs):
        errors.append("Sequences not in deterministic sorted order.")

    return errors
