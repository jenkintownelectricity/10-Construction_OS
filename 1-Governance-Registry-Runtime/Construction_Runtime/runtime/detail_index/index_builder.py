"""
Detail Index Builder — Wave 15.

Loads canonical Detail DNA records and builds deterministic lookup indexes.
Consumes Construction_Kernel truth. Does not redefine it.
"""

import hashlib
import json
import os
from collections import defaultdict
from typing import Any

from runtime.detail_index.contract import (
    CONTRACT_VERSION,
    WAVE,
    REQUIRED_DETAIL_FIELDS,
    VALID_CLASSES,
    VALID_SYSTEMS,
)


class DetailIndexBuildError(Exception):
    """Raised when index construction fails validation. Fail closed."""


def load_detail_dna_records(detail_dna_dir: str) -> list[dict[str, Any]]:
    """Load all Detail DNA JSON files from a directory."""
    records = []
    if not os.path.isdir(detail_dna_dir):
        raise DetailIndexBuildError(f"Detail DNA directory not found: {detail_dna_dir}")

    for filename in sorted(os.listdir(detail_dna_dir)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(detail_dna_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            record = json.load(f)
        records.append(record)

    return records


def build_detail_index(
    detail_dna_records: list[dict[str, Any]],
    tag_index_data: dict[str, Any] | None = None,
    route_index_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build a complete detail index from canonical Detail DNA records.

    Args:
        detail_dna_records: List of Detail DNA record dicts.
        tag_index_data: Optional pre-built tag index from kernel.
        route_index_data: Optional route index from kernel.

    Returns:
        Deterministic detail index artifact.

    Raises:
        DetailIndexBuildError on any validation failure.
    """
    if not detail_dna_records:
        raise DetailIndexBuildError("Cannot build index from empty detail_dna_records.")

    detail_lookup: dict[str, dict[str, Any]] = {}
    family_index: dict[str, list[str]] = defaultdict(list)
    tag_idx: dict[str, list[str]] = defaultdict(list)
    condition_index: dict[str, list[str]] = defaultdict(list)
    system_index: dict[str, list[str]] = defaultdict(list)
    class_index: dict[str, list[str]] = defaultdict(list)

    for record in detail_dna_records:
        _validate_record(record)

        detail_id = record["detail_id"]
        if detail_id in detail_lookup:
            raise DetailIndexBuildError(f"Duplicate detail_id: {detail_id}")

        detail_lookup[detail_id] = record
        family_index[record["assembly_family"]].append(detail_id)
        condition_index[record["condition"]].append(detail_id)
        system_index[record["system"]].append(detail_id)
        class_index[record["class"]].append(detail_id)

        for tag in record.get("tags", []):
            tag_idx[tag].append(detail_id)

    # Deterministic sorting
    detail_lookup_sorted = dict(sorted(detail_lookup.items()))
    family_index_sorted = {k: sorted(v) for k, v in sorted(family_index.items())}
    tag_index_sorted = {k: sorted(v) for k, v in sorted(tag_idx.items())}
    condition_index_sorted = {k: sorted(v) for k, v in sorted(condition_index.items())}
    system_index_sorted = {k: sorted(v) for k, v in sorted(system_index.items())}
    class_index_sorted = {k: sorted(v) for k, v in sorted(class_index.items())}

    index_artifact = {
        "version": CONTRACT_VERSION,
        "wave": WAVE,
        "detail_count": len(detail_lookup_sorted),
        "detail_lookup": detail_lookup_sorted,
        "family_index": family_index_sorted,
        "tag_index": tag_index_sorted,
        "condition_index": condition_index_sorted,
        "system_index": system_index_sorted,
        "class_index": class_index_sorted,
    }

    # Compute deterministic checksum
    content_for_checksum = json.dumps(
        {
            "detail_lookup": detail_lookup_sorted,
            "family_index": family_index_sorted,
            "tag_index": tag_index_sorted,
            "condition_index": condition_index_sorted,
            "system_index": system_index_sorted,
            "class_index": class_index_sorted,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    index_artifact["checksum"] = hashlib.sha256(
        content_for_checksum.encode("utf-8")
    ).hexdigest()

    return index_artifact


def _validate_record(record: dict[str, Any]) -> None:
    """Validate a single Detail DNA record. Fail closed on any issue."""
    missing = REQUIRED_DETAIL_FIELDS - set(record.keys())
    if missing:
        detail_id = record.get("detail_id", "<unknown>")
        raise DetailIndexBuildError(
            f"Detail {detail_id} missing required fields: {sorted(missing)}"
        )

    if record["system"] not in VALID_SYSTEMS:
        raise DetailIndexBuildError(
            f"Detail {record['detail_id']} has invalid system: {record['system']}"
        )

    if record["class"] not in VALID_CLASSES:
        raise DetailIndexBuildError(
            f"Detail {record['detail_id']} has invalid class: {record['class']}"
        )
