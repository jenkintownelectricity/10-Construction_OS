# Construction_Awareness_Cache

Frozen compiled awareness runtime for Construction OS. Compiles governed awareness snapshots from admitted Cognitive Bus events through a strict lifecycle: thaw, ingest, validate, compile, freeze, expose read-only.

## Quickstart

```bash
# Run all tests
cd Construction_Awareness_Cache
python -m unittest discover -s tests -v
```

### Programmatic usage

```python
from awareness.thaw_manager import ThawManager
from awareness.ingest_pipeline import IngestPipeline
from awareness.validation_gate import ValidationGate
from awareness.freeze_compiler import FreezeCompiler
from awareness.snapshot_store import SnapshotStore
from awareness.snapshot_reader import SnapshotReader

# 1. Thaw
mgr = ThawManager()
mgr.thaw()

# 2. Ingest admitted events from state/events/
pipeline = IngestPipeline()
events = pipeline.ingest()

# 3. Validate
gate = ValidationGate()
valid, rejected = gate.validate(events)

# 4. Add validated events to session and freeze
mgr.add_validated(valid)
frozen_data = mgr.freeze()

# 5. Compile into frozen snapshot
compiler = FreezeCompiler()
snapshot = compiler.compile(frozen_data)

# 6. Store (append-only, immutable)
store = SnapshotStore()
store.store(snapshot)

# 7. Read frozen snapshots (read-only)
reader = SnapshotReader()
ids = reader.list_snapshots()
snap = reader.get(ids[0])
```

## What it IS

- A compiled present-state awareness artifact: frozen snapshots representing system understanding at a point in time
- An awareness compiler: ingests admitted Cognitive Bus events and compiles them into coherent snapshots
- A frozen snapshot store: once compiled, snapshots are immutable and append-only
- Read-only during normal operation: only changes through the governed thaw/freeze lifecycle

## What it is NOT

- **NOT truth.** Compiles from truth-derived sources but is not itself the source of truth
- **NOT a registry.** Does not serve as authoritative record of system components
- **NOT a mutable state store.** Snapshots are frozen and immutable once compiled
- **NOT a kernel or runtime executor.** Does not orchestrate or execute tasks
- **NOT the cognitive bus.** Does not transport or route events

## Architecture

```
state/events/     <- Admitted Cognitive Bus records (input)
state/snapshots/  <- Frozen snapshot artifacts (output, append-only)
awareness/        <- Runtime modules
tests/            <- Unit tests
```

## Dependencies

Python standard library only: json, os, hashlib, datetime, uuid, unittest, collections, tempfile, shutil.
