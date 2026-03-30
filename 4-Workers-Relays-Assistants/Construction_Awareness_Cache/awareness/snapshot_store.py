"""
Construction Awareness Cache v0.1 — Snapshot store.

Append-only store for frozen snapshots. No update. No delete.
"""

import json
import os

from . import config


class SnapshotStoreError(Exception):
    """Raised on snapshot store violations."""


class SnapshotStore:
    """Stores frozen snapshots as immutable JSON files. Append-only."""

    def __init__(self, snapshots_dir: str | None = None):
        self._dir = snapshots_dir or config.SNAPSHOTS_DIR

    def store(self, snapshot: dict) -> str:
        """Store a frozen snapshot. Returns the file path.

        Raises SnapshotStoreError if the snapshot is not frozen or
        if a snapshot with the same ID already exists.
        """
        if not snapshot.get("frozen"):
            raise SnapshotStoreError("Cannot store unfrozen snapshot")

        sid = snapshot.get("snapshot_id")
        if not sid:
            raise SnapshotStoreError("Snapshot has no snapshot_id")

        os.makedirs(self._dir, exist_ok=True)
        path = os.path.join(self._dir, f"{sid}.json")

        if os.path.exists(path):
            raise SnapshotStoreError(f"Snapshot already exists: {sid}")

        data = json.dumps(snapshot, sort_keys=True, indent=2)
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        return path

    def list_ids(self) -> list[str]:
        """List all stored snapshot IDs, sorted."""
        if not os.path.isdir(self._dir):
            return []
        ids = []
        for fname in sorted(os.listdir(self._dir)):
            if fname.endswith(".json"):
                ids.append(fname[:-5])
        return ids
