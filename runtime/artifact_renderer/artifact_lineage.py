"""Artifact lineage tracking with SHA-256 hashing.

Every artifact emits metadata and a sha256 content hash for deterministic
lineage verification. Lineage records are immutable once created.

Lineage chain: Detail DNA -> Instruction Set -> Renderer -> Artifact
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


LINEAGE_VERSION = "18.0"


@dataclass(frozen=True)
class LineageRecord:
    """Immutable lineage record for a single artifact."""
    artifact_id: str
    content_hash: str
    source_detail_id: str
    source_instruction_set_id: str
    source_manifest_id: str
    renderer_id: str
    output_format: str
    lineage_version: str = LINEAGE_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "content_hash": self.content_hash,
            "source_detail_id": self.source_detail_id,
            "source_instruction_set_id": self.source_instruction_set_id,
            "source_manifest_id": self.source_manifest_id,
            "renderer_id": self.renderer_id,
            "output_format": self.output_format,
            "lineage_version": self.lineage_version,
        }


@dataclass
class LineageBundle:
    """Collection of lineage records for a render operation."""
    manifest_id: str = ""
    records: list[LineageRecord] = field(default_factory=list)
    bundle_hash: str = ""

    def add_record(self, record: LineageRecord) -> None:
        self.records.append(record)
        self._recompute_bundle_hash()

    def _recompute_bundle_hash(self) -> None:
        """Recompute the bundle hash from all records."""
        combined = "|".join(r.content_hash for r in sorted(self.records, key=lambda r: r.artifact_id))
        self.bundle_hash = compute_sha256(combined)

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "records": [r.to_dict() for r in self.records],
            "bundle_hash": self.bundle_hash,
            "record_count": len(self.records),
            "lineage_version": LINEAGE_VERSION,
        }


def compute_sha256(content: str) -> str:
    """Compute SHA-256 hash of content string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def compute_content_hash(content: str, format_id: str) -> str:
    """Compute a format-tagged content hash for determinism verification.

    The format_id is included so the same content in different formats
    produces different hashes (preventing format confusion).
    """
    tagged = f"{format_id}:{content}"
    return compute_sha256(tagged)


def create_lineage_record(
    artifact_id: str,
    content: str,
    output_format: str,
    source_detail_id: str,
    source_instruction_set_id: str,
    source_manifest_id: str,
    renderer_id: str,
) -> LineageRecord:
    """Create an immutable lineage record for an artifact."""
    content_hash = compute_content_hash(content, output_format)
    return LineageRecord(
        artifact_id=artifact_id,
        content_hash=content_hash,
        source_detail_id=source_detail_id,
        source_instruction_set_id=source_instruction_set_id,
        source_manifest_id=source_manifest_id,
        renderer_id=renderer_id,
        output_format=output_format,
    )


def verify_determinism(content_a: str, content_b: str, format_id: str) -> bool:
    """Verify two renderings of the same input produce identical output."""
    hash_a = compute_content_hash(content_a, format_id)
    hash_b = compute_content_hash(content_b, format_id)
    return hash_a == hash_b


def build_lineage_chain(
    detail_id: str,
    instruction_set_id: str,
    manifest_id: str,
    artifacts: list[dict[str, Any]],
) -> LineageBundle:
    """Build a complete lineage chain from rendering artifacts.

    Args:
        detail_id: Source detail DNA identifier.
        instruction_set_id: Instruction set identifier.
        manifest_id: Render manifest identifier.
        artifacts: List of {artifact_id, content, format, renderer_id}.

    Returns:
        LineageBundle with all records and bundle hash.
    """
    bundle = LineageBundle(manifest_id=manifest_id)

    for art in artifacts:
        record = create_lineage_record(
            artifact_id=art["artifact_id"],
            content=art["content"],
            output_format=art["format"],
            source_detail_id=detail_id,
            source_instruction_set_id=instruction_set_id,
            source_manifest_id=manifest_id,
            renderer_id=art["renderer_id"],
        )
        bundle.add_record(record)

    return bundle
