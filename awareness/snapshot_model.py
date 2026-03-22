"""
Construction Awareness Cache v0.1 — Snapshot model.

Immutable frozen awareness snapshot with deterministic hash.
"""

import hashlib
import json
from datetime import datetime, timezone


def compute_snapshot_hash(entries: list[dict]) -> str:
    """Deterministic SHA-256 hash of compiled snapshot entries."""
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def make_snapshot(
    snapshot_id: str,
    entries: list[dict],
    source_summary: dict,
) -> dict:
    """Create a frozen awareness snapshot artifact.

    Once created, a snapshot must not be mutated. It is a frozen record.
    """
    content_hash = compute_snapshot_hash(entries)
    return {
        "snapshot_id": snapshot_id,
        "schema_version": "0.1",
        "frozen": True,
        "content_hash": content_hash,
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "entry_count": len(entries),
        "source_summary": dict(source_summary),
        "entries": list(entries),
    }
