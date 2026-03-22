"""
Construction Cognitive Bus v0.1 — Append-only event log.

Stores admitted events as individual JSON files in the events directory.
Records are immutable once written. No update. No delete.
"""

import json
import os

from bus.config import EVENTS_DIR


def _ensure_dir() -> None:
    os.makedirs(EVENTS_DIR, exist_ok=True)


def append_event(record: dict) -> str:
    """Write an admission record to the event log. Returns the file path."""
    _ensure_dir()
    event_id = record["event"]["event_id"]
    ts = record["admission_timestamp"].replace(":", "-").replace("+", "_")
    filename = f"{ts}_{event_id}.json"
    path = os.path.join(EVENTS_DIR, filename)

    if os.path.exists(path):
        raise RuntimeError(
            f"event record already exists (immutability violation): {path}"
        )

    data = json.dumps(record, sort_keys=True, indent=2)
    # Atomic-ish write: write to tmp then rename
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        f.write(data)
    os.replace(tmp_path, path)

    return path


def list_event_files() -> list[str]:
    """Return sorted list of event record file paths."""
    _ensure_dir()
    files = [
        os.path.join(EVENTS_DIR, f)
        for f in sorted(os.listdir(EVENTS_DIR))
        if f.endswith(".json")
    ]
    return files


def read_event_record(path: str) -> dict:
    """Read and parse a single event record. Fails closed on malformed data."""
    try:
        with open(path, "r") as f:
            record = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        raise RuntimeError(f"unreadable event record (fail closed): {path}: {e}")

    if not isinstance(record, dict) or "event" not in record:
        raise RuntimeError(f"malformed event record (fail closed): {path}")

    return record
