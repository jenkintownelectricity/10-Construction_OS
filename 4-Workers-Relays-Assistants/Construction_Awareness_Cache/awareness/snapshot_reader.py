"""
Construction Awareness Cache v0.1 — Snapshot reader.

Read-only access to frozen snapshots. Fails closed on malformed data.
"""

import json
import os

from . import config


class SnapshotReadError(Exception):
    """Raised when a snapshot cannot be read or is malformed."""


class SnapshotReader:
    """Read-only access to frozen snapshots."""

    def __init__(self, snapshots_dir: str | None = None):
        self._dir = snapshots_dir or config.SNAPSHOTS_DIR

    def list_snapshots(self) -> list[str]:
        """List available snapshot IDs."""
        if not os.path.isdir(self._dir):
            return []
        ids = []
        for fname in sorted(os.listdir(self._dir)):
            if fname.endswith(".json"):
                ids.append(fname[:-5])
        return ids

    def get(self, snapshot_id: str) -> dict:
        """Read a frozen snapshot by ID. Fails closed on any issue."""
        path = os.path.join(self._dir, f"{snapshot_id}.json")
        if not os.path.isfile(path):
            raise SnapshotReadError(f"Snapshot not found: {snapshot_id}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            raise SnapshotReadError(
                f"Malformed snapshot file: {snapshot_id}"
            ) from exc

        if not isinstance(data, dict):
            raise SnapshotReadError(f"Snapshot is not a dict: {snapshot_id}")
        if not data.get("frozen"):
            raise SnapshotReadError(
                f"Snapshot is not frozen: {snapshot_id}"
            )
        if data.get("snapshot_id") != snapshot_id:
            raise SnapshotReadError(
                f"Snapshot ID mismatch: expected {snapshot_id}"
            )
        return data
