"""
Construction Cognitive Bus v0.1 — Replay reader.

Returns admitted events in deterministic (filename-sorted) order.
Supports filtering by event_class and source_component.
Fails closed on any malformed record.
"""

from bus.event_log import list_event_files, read_event_record


def replay(
    event_class: str | None = None,
    source_component: str | None = None,
) -> list[dict]:
    """Replay admitted events in deterministic order.

    Args:
        event_class: If provided, only return events matching this class.
        source_component: If provided, only return events from this component.

    Returns:
        List of admission records in filename-sorted order.

    Raises:
        RuntimeError: On any malformed record (fail closed).
    """
    records = []
    for path in list_event_files():
        record = read_event_record(path)  # raises on malformed
        event = record["event"]

        if event_class is not None and event.get("event_class") != event_class:
            continue
        if source_component is not None and event.get("source_component") != source_component:
            continue

        records.append(record)

    return records
