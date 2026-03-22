# Construction_Cognitive_Bus

Governed cognitive event/admission layer for Construction OS.

## What This Is

- **Cognitive event/admission layer** — the single governed entry point for cognitive events
- **Append-only** — all admitted and rejected events are recorded immutably
- **Fail-closed** — unknown emitters, invalid schemas, and uncertain state result in rejection
- **Non-authority** — validates structure and emitter policy only; defers to kernels for truth
- **Schema/policy admission only** — does not validate domain truth

## What This Is NOT

- Not a kernel. Not truth. Not a registry. Not runtime. Not a distributed streaming system.

## Quickstart

Emitters submit an **incoming event envelope** — the bus validates it and produces an **admission record** containing bus-derived metadata.

```python
from bus.admission_gate import receive_event

# Incoming event envelope (emitter-supplied fields only)
event = {
    "event_id": "evt-001",
    "event_class": "Observation",
    "event_type": "sensor_reading",
    "schema_version": "0.1",
    "source_component": "Construction_Intelligence_Workers",
    "source_repo": "Construction_Intelligence_Workers",
    "timestamp": "2026-03-22T00:00:00+00:00",
    "payload": {"temperature": 72.5},
}

result = receive_event(event)
print(result)
# {'admitted': True, 'reason': 'admitted', 'admission_path': '...', 'content_hash': '...', 'routing': {...}}
```

The admitted record stored on disk includes the original event plus bus-derived metadata: `content_hash` (deterministic SHA-256 of event content, computed by the bus at admission time — not emitter-supplied), `admission_timestamp`, and `admission_decision`. Replay reads these admitted records, not raw emitter submissions.

## Event Classes

| Class | Description |
|---|---|
| `Observation` | Factual signal about state. Routes to diagnostics. |
| `Proposal` | Suggested action or change. Routes to awareness_cache + diagnostics. |
| `ExternallyValidatedEvent` | Validated by an upstream governed system (not by the bus). Routes to awareness_cache. Requires `authority_status` field. |

## Allowed Emitters (v0.1)

- `Construction_Intelligence_Workers`
- `Construction_Reference_Intelligence`
- `Construction_Runtime`

`Construction_Assistant` is explicitly denied in v0.1.

## Running Tests

```bash
cd Construction_Cognitive_Bus
python -m unittest discover -s tests -v
```

## Dependencies

Python 3.10+ standard library only. No third-party dependencies.

## Repository Structure

```
schemas/
  event-envelope.schema.json   # Canonical event envelope JSON Schema
bus/
  __init__.py
  config.py                    # Local configuration constants
  models.py                    # Record types and content hashing
  admission_gate.py            # Admission pipeline entry point
  emitter_policy.py            # Emitter allow/deny validation
  event_log.py                 # Append-only admitted event storage
  rejection_log.py             # Append-only rejection storage
  router.py                    # Routing decision generator
  replay.py                    # Deterministic replay reader
tests/
  test_admission_gate.py       # Admission pipeline tests
  test_rejection_behavior.py   # Rejection logging tests
  test_event_log.py            # Event log tests
  test_replay.py               # Replay and fail-closed tests
state/
  events/                      # Admitted event records (append-only)
  rejections/                  # Rejection records (append-only)
docs/
  specs/                       # Architecture specifications
  system/                      # System manifest
```
