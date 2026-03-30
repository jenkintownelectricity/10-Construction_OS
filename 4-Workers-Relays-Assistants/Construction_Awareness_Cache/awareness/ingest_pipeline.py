"""
Construction Awareness Cache v0.1 — Ingest pipeline.

Reads admitted Cognitive Bus records from state/events/ and extracts
event data. Only processes admission records. Rejects everything else.
"""

import json
import os

from . import config


class IngestError(Exception):
    """Raised when ingestion fails."""


class IngestPipeline:
    """Reads and filters admitted event records from the events directory."""

    def __init__(self, events_dir: str | None = None):
        self._events_dir = events_dir or config.EVENTS_DIR

    def ingest(self) -> list[dict]:
        """Read all admitted records from the events directory.

        Returns a list of the inner event dicts from valid admission records.
        Skips non-JSON files, non-admission records, and malformed files.
        """
        if not os.path.isdir(self._events_dir):
            return []

        results = []
        for fname in sorted(os.listdir(self._events_dir)):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(self._events_dir, fname)
            record = self._read_record(path)
            if record is not None:
                results.append(record)
        return results

    def _read_record(self, path: str) -> dict | None:
        """Read a single file and return the event if it is an admission record."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            if len(raw.encode("utf-8")) > config.MAX_PAYLOAD_BYTES:
                return None
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            return None

        if not isinstance(data, dict):
            return None
        if data.get("record_type") != "admitted":
            return None
        if data.get("admission_decision") != "admitted":
            return None

        event = data.get("event")
        if not isinstance(event, dict):
            return None
        return event
