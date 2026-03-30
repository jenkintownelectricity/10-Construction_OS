"""
Construction Awareness Cache v0.1 — Freeze compiler.

Compiles validated events into a frozen snapshot artifact with
deterministic content hash and source summary.
"""

import uuid
from collections import Counter

from .snapshot_model import make_snapshot


class FreezeCompiler:
    """Compiles validated events into a frozen snapshot."""

    def compile(self, validated_events: list[dict]) -> dict:
        """Compile a list of validated events into a frozen snapshot.

        Always produces a valid snapshot, even if the input list is empty.
        """
        snapshot_id = str(uuid.uuid4())
        entries = self._build_entries(validated_events)
        source_summary = self._build_source_summary(validated_events)
        return make_snapshot(snapshot_id, entries, source_summary)

    def _build_entries(self, events: list[dict]) -> list[dict]:
        """Build snapshot entries from validated events."""
        entries = []
        for event in events:
            entries.append({
                "event_id": event.get("event_id"),
                "event_class": event.get("event_class"),
                "event_type": event.get("event_type"),
                "source_component": event.get("source_component"),
                "source_repo": event.get("source_repo"),
                "timestamp": event.get("timestamp"),
                "payload": event.get("payload"),
            })
        return entries

    def _build_source_summary(self, events: list[dict]) -> dict:
        """Build a summary of event sources."""
        class_counts = Counter(e.get("event_class") for e in events)
        source_counts = Counter(e.get("source_component") for e in events)
        return {
            "total_events": len(events),
            "by_class": dict(class_counts),
            "by_source": dict(source_counts),
        }
