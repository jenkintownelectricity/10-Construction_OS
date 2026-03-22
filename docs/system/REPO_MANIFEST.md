# REPO_MANIFEST

## Identity

- **Repository**: Construction_Awareness_Cache
- **Owner**: jenkintownelectricity
- **Layer**: Cognitive Layer
- **Primary Role**: Frozen compiled awareness

---

## Purpose

Construction_Awareness_Cache is the frozen compiled awareness layer for current system operation in Construction OS. It ingests truth-derived signals, compiles them into a point-in-time awareness snapshot, and freezes that snapshot for safe, read-only consumption by other system components. It does not generate truth. It compiles from truth-derived sources and preserves the lineage of every element it holds.

---

## Classification

- **Layer**: Cognitive-layer service
- **Authority**: Non-authority
- **Source posture**: Compiles from truth-derived sources but is not truth itself

---

## What It IS

- A **compiled present-state awareness artifact** — a frozen snapshot representing the system's current compiled understanding at a specific point in time.
- An **awareness compiler** — takes raw intelligence signals and validated events, merges them into a coherent awareness state.
- A **frozen snapshot store** — once compiled, snapshots are locked for safe read access and are not mutated in place.
- An **ingestion consumer** — receives and processes signals from upstream sources; it does not produce or emit signals of its own into the cognitive bus.

## What It IS NOT

- **NOT root truth.** The cache compiles awareness from truth-derived sources. It does not originate, define, or guarantee truth.
- **NOT a registry.** It does not serve as the authoritative record of system components, identities, or configurations.
- **NOT a kernel.** It does not orchestrate, schedule, or control execution of other system processes.
- **NOT the cognitive bus.** It does not transport, route, or broker events between system components.
- **NOT a runtime executor.** It does not execute tasks, run workers, or perform active computation beyond its own compilation cycle.

---

## Interactions

### Construction_Resource_Intelligence (CRI)
Construction_Awareness_Cache ingests CRI's structural intelligence as a primary source during awareness compilation. CRI provides the foundational structural signals that the cache compiles into its frozen snapshots. The cache reads from CRI; it does not write back to CRI.

### Construction_Cognitive_Bus
Admitted and validated events from the Cognitive Bus may feed into the cache's awareness compilation cycle. The cache does not read from or write to the bus directly at the transport level — it receives events that have already passed through the bus's admission and validation layer.

### Construction_Assistant
Construction_Assistant reads frozen compiled awareness from the cache for live consciousness and safe operation. This is a read-only relationship. The Assistant does not modify, write to, or trigger recompilation of the cache.

### Construction_Intelligence_Workers
Intelligence Workers read frozen compiled awareness from the cache to obtain context during active thought and proposal generation. This is a read-only relationship. Workers do not modify the cache or initiate compilation cycles.

### Construction_Homebase
Construction_Homebase may reference cached awareness state for surface-level presentation and status. The cache does not depend on Homebase and does not receive signals from it.

### Construction_Kernel
The Kernel governs system-level orchestration. The cache operates within the boundaries the Kernel defines but does not receive direct runtime instructions from the Kernel during its compilation cycle. The cache is not the Kernel and does not perform kernel functions.

---

## Non-Authority Guarantees

1. **Not truth.** Construction_Awareness_Cache is a compiled artifact. It reflects truth-derived sources at the time of compilation but is not itself the source of truth for any system element.
2. **Compiles from truth-derived sources.** Every element in a frozen snapshot originates from a source that is itself derived from or validated against root truth. The cache does not fabricate or infer awareness independently.
3. **Fail-closed on invalid compilation.** If any step in the thaw-compile-validate-refreeze lifecycle encounters an invalid state, inconsistency, or unresolvable conflict, the compilation fails closed. The previous valid frozen snapshot remains in effect. No partially compiled or unvalidated snapshot is ever promoted to active status.
4. **Lineage preservation.** Every element in a frozen snapshot carries a full lineage chain tracing it back through the compilation history to its original source. Lineage is never truncated, rewritten, or discarded.

---

## v0.1 Runtime Components

### awareness/config.py
Configuration constants: paths, schema version, allowed event classes, required event fields, payload size limits. All values are deterministic local defaults. No external config sources.

### awareness/snapshot_model.py
Immutable frozen snapshot model. Provides `compute_snapshot_hash()` for deterministic SHA-256 content hashing and `make_snapshot()` to create frozen snapshot artifacts with metadata, entries, and source summary.

### awareness/thaw_manager.py
Thaw/freeze lifecycle manager. Enforces single-session constraint: only one thaw session at a time. Provides `thaw()`, `add_validated()`, `get_session_data()`, and `freeze()`. Fails closed on lifecycle violations.

### awareness/ingest_pipeline.py
Ingestion pipeline for admitted Cognitive Bus records. Reads JSON files from `state/events/`, filters for admission records (`record_type: admitted`, `admission_decision: admitted`), extracts inner event dicts. Skips non-JSON, non-admission, and malformed files.

### awareness/validation_gate.py
Validation gate for ingested events. Checks required fields, valid event classes, schema version, and payload structure. Returns `(valid, rejected)` tuple. Fail closed: any malformed record is rejected.

### awareness/freeze_compiler.py
Freeze compiler. Takes validated events and compiles them into a frozen snapshot artifact via `FreezeCompiler.compile()`. Builds snapshot entries and source summary (counts by event class and source component). Always produces a valid snapshot, even for empty input.

### awareness/snapshot_store.py
Append-only snapshot store. Writes frozen snapshots as immutable JSON files to `state/snapshots/`. Enforces: snapshot must be frozen, must have an ID, and cannot overwrite existing snapshots. No update, no delete.

### awareness/snapshot_reader.py
Read-only snapshot reader. Lists available snapshots and retrieves by ID. Validates on read: must be valid JSON, must be a dict, must be frozen, and snapshot ID must match filename. Fails closed on any malformation.
