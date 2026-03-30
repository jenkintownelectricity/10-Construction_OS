"""
Evidence Ingestion

Accepts construction evidence: drawings, specifications, photos, RFIs,
and submittals. Classifies evidence by type and associates it with
project assemblies.

This module does not define construction truth. Evidence classification
is a derived operation — canonical truth remains in Construction_Kernel.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


VALID_EVIDENCE_TYPES = {
    "drawing",
    "specification",
    "photo",
    "rfi",
    "submittal",
}


@dataclass
class EvidenceItem:
    """A single piece of construction evidence."""

    evidence_id: str = ""
    evidence_type: str = ""
    source_reference: str = ""
    assembly_references: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class IngestionResult:
    """Derived result of evidence ingestion. Non-canonical, recomputable."""

    accepted: bool = False
    evidence_items: list[EvidenceItem] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)


def ingest_evidence(evidence_batch: list[dict[str, Any]]) -> IngestionResult:
    """
    Ingest a batch of evidence items.

    Fail-closed: rejects evidence with unknown types or missing identifiers.
    All output is derived and non-canonical.
    """
    result = IngestionResult()

    if not isinstance(evidence_batch, list) or len(evidence_batch) == 0:
        result.errors.append({
            "code": "EMPTY_EVIDENCE_BATCH",
            "message": "Evidence batch must be a non-empty list.",
        })
        return result

    for raw in evidence_batch:
        eid = raw.get("evidence_id", "")
        etype = raw.get("evidence_type", "")

        if not eid:
            result.errors.append({
                "code": "MISSING_EVIDENCE_ID",
                "message": "Each evidence item must have an evidence_id.",
            })
            continue

        if etype not in VALID_EVIDENCE_TYPES:
            result.errors.append({
                "code": "UNKNOWN_EVIDENCE_TYPE",
                "message": f"Evidence '{eid}' has unknown type '{etype}'. "
                           f"Valid types: {sorted(VALID_EVIDENCE_TYPES)}",
            })
            continue

        item = EvidenceItem(
            evidence_id=eid,
            evidence_type=etype,
            source_reference=raw.get("source_reference", ""),
            assembly_references=raw.get("assembly_references", []),
            metadata=raw.get("metadata", {}),
        )
        result.evidence_items.append(item)

    result.accepted = len(result.evidence_items) > 0 and len(result.errors) == 0
    return result
