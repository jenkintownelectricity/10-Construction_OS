"""
Construction Cognitive Bus v0.1 — Append-only rejection log.

Stores rejected events as individual JSON files in the rejections directory.
Records are immutable once written. No update. No delete.
"""

import json
import os
import uuid

from bus.config import REJECTIONS_DIR


def _ensure_dir() -> None:
    os.makedirs(REJECTIONS_DIR, exist_ok=True)


def append_rejection(record: dict) -> str:
    """Write a rejection record to the rejection log. Returns the file path."""
    _ensure_dir()
    ts = record["rejection_timestamp"].replace(":", "-").replace("+", "_")
    event = record.get("event")
    event_id = event.get("event_id", uuid.uuid4().hex[:12]) if event else uuid.uuid4().hex[:12]
    filename = f"{ts}_{event_id}_rejected.json"
    path = os.path.join(REJECTIONS_DIR, filename)

    data = json.dumps(record, sort_keys=True, indent=2)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        f.write(data)
    os.replace(tmp_path, path)

    return path


def list_rejection_files() -> list[str]:
    """Return sorted list of rejection record file paths."""
    _ensure_dir()
    files = [
        os.path.join(REJECTIONS_DIR, f)
        for f in sorted(os.listdir(REJECTIONS_DIR))
        if f.endswith(".json")
    ]
    return files


def read_rejection_record(path: str) -> dict:
    """Read and parse a single rejection record. Fails closed on malformed data."""
    try:
        with open(path, "r") as f:
            record = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        raise RuntimeError(f"unreadable rejection record (fail closed): {path}: {e}")

    if not isinstance(record, dict) or "rejection_reason" not in record:
        raise RuntimeError(f"malformed rejection record (fail closed): {path}")

    return record
