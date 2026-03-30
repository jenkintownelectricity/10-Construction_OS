# Construction_Awareness_Cache — Specification

## System Role

Construction_Awareness_Cache is the **frozen compiled awareness layer** within Construction OS. It produces and maintains point-in-time awareness snapshots that represent the system's compiled understanding of its current state. These snapshots are frozen after compilation and made available as read-only artifacts to downstream consumers.

The cache is a cognitive-layer service. It is not an authority, not a source of truth, and not an executor. It compiles from truth-derived sources, validates its output, and locks it down for safe consumption.

---

## Awareness Compilation Process

The cache ingests intelligence signals from Construction_Resource_Intelligence (CRI) and validated events from the cognitive event and admission layer, then compiles them into a frozen point-in-time awareness snapshot.

**Compilation stages:**

1. **Signal ingestion** — The cache collects available signals from registered sources. No signal is accepted without a traceable origin.
2. **Merge** — Incoming signals are merged with the existing awareness state. Conflicts between signals are flagged rather than silently resolved.
3. **Consistency assembly** — The merged state is assembled into a coherent awareness artifact where all elements are internally consistent and all lineage chains are intact.
4. **Freeze** — The compiled artifact is locked as an immutable snapshot, assigned a version identifier, and made available for read access.

The cache does not perform speculative compilation. It does not infer or extrapolate beyond the signals it receives.

---

## Ingestion Sources

The cache accepts signals from the following registered sources:

### CRI Structural Intelligence
Construction_Resource_Intelligence provides the primary structural signals — resource states, relationships, and structural facts — that form the backbone of each awareness snapshot. The cache reads from CRI during compilation and does not write back.

### Validated Events from Construction_Cognitive_Bus
Events that have been admitted and validated through the Cognitive Bus's admission layer may feed into awareness compilation. The cache does not interact with the bus at the transport level. It consumes events that have already cleared admission and validation.

### Other Registered Cognitive-Layer Signals
Additional cognitive-layer services may register as signal sources for the cache. Each registered source must provide traceable, lineage-bearing signals. Unregistered or anonymous signals are rejected.

---

## Thaw, Compile, Validate, Refreeze Lifecycle

Each compilation cycle follows a strict four-phase lifecycle:

### 1. Thaw
The current frozen snapshot is unlocked for update. During the thaw phase, the existing snapshot state is loaded into a mutable working copy. The frozen original remains intact and continues to serve read requests until a new snapshot is promoted.

### 2. Compile
New signals are ingested from all registered sources and merged with the existing awareness state in the working copy. This phase includes:
- Ingestion of new CRI structural intelligence
- Ingestion of newly validated events from the cognitive event/admission layer
- Ingestion of any other registered cognitive-layer signals
- Merge with existing compiled awareness
- Conflict detection and flagging

### 3. Validate
The compiled working copy undergoes internal consistency checks and lineage verification:
- **Internal consistency** — All elements in the compiled state must be mutually consistent. Contradictions, dangling references, or orphaned elements cause validation failure.
- **Lineage verification** — Every element must trace back through its compilation chain to an original source. Broken or missing lineage causes validation failure.
- **Fail-closed** — If validation fails for any reason, the compilation cycle is aborted. The previous valid frozen snapshot remains in effect. No partially validated snapshot is ever promoted. The failure is recorded with full diagnostic context.

### 4. Refreeze
Upon successful validation, the compiled and validated working copy is locked as a new immutable frozen snapshot. It is assigned a version identifier, its lineage metadata is sealed, and it becomes the active snapshot for all read consumers. The previous snapshot is retained for audit purposes.

---

## Versioning Model

### Version Identifiers
Each frozen snapshot carries a unique version identifier assigned at refreeze time. Version identifiers are strictly ordered and monotonically increasing. No two snapshots share a version identifier.

### Retention
Previous snapshot versions are retained for audit. Snapshots are not discarded or garbage-collected without explicit policy authorization. The retention history provides a complete record of the system's compiled awareness over time.

### Version Lineage
The version lineage traces the full compilation history: which snapshot was the base, which signals were ingested, what was merged, and what the validation outcome was. Version lineage enables reconstruction of how any given awareness state was derived.

---

## Lineage Preservation

Every element in a frozen snapshot traces back through its compilation chain to the original sources that produced it. Lineage includes:

- **Source origin** — The registered source (CRI, Cognitive Bus event, other cognitive-layer signal) that provided the original signal.
- **Compilation path** — The sequence of compilation cycles through which the element was ingested, merged, or carried forward.
- **Snapshot versions** — The specific snapshot versions in which the element appeared, enabling point-in-time tracing.

**Lineage is never truncated.** Even when elements are carried forward across many compilation cycles without change, their original lineage chain remains intact. Lineage is not summarized, compressed, or approximated.

---

## Read Interface for Construction_Assistant

Construction_Assistant reads frozen compiled awareness from the cache for **live consciousness and safe operation**.

- **Access mode**: Read-only.
- **What the Assistant reads**: The current active frozen snapshot, representing the system's compiled present-state awareness.
- **What the Assistant does NOT do**: The Assistant does not modify the cache, does not trigger compilation, does not write signals, and does not influence snapshot content.
- **Contract**: The Assistant can rely on the frozen snapshot being internally consistent, fully validated, and lineage-complete at the time of read. If no valid snapshot exists (e.g., after a failed compilation with no prior snapshot), the cache returns an explicit absence signal rather than partial or invalid data.

---

## Read Interface for Construction_Intelligence_Workers

Construction_Intelligence_Workers read frozen compiled awareness from the cache for **context during active thought and proposal generation**.

- **Access mode**: Read-only.
- **What Workers read**: The current active frozen snapshot, used as contextual grounding for intelligence work such as analysis, proposal drafting, and evaluation.
- **What Workers do NOT do**: Workers do not modify the cache, do not trigger compilation, do not write signals, and do not influence snapshot content.
- **Contract**: Workers can rely on the same consistency, validation, and lineage guarantees as the Assistant. The frozen snapshot provides stable, immutable context that does not shift during a worker's active thought cycle.

---

## Relationship to Construction_Cognitive_Bus

- Admitted and validated events from the Cognitive Bus may feed into the cache's awareness compilation cycle.
- The cache **does not read from or write to the bus directly** at the transport level. It is not a bus participant in the pub/sub or routing sense.
- Events reach the cache only after passing through the bus's admission and validation layer. The cache does not perform its own event admission — it trusts the bus's admission guarantees and verifies lineage on ingestion.
- The cache does not emit events onto the bus. It is a consumer, not a producer, in the cognitive event flow.

---

## Relationship to Construction_Resource_Intelligence (CRI)

- The cache ingests CRI's structural intelligence as a primary source during awareness compilation.
- CRI provides foundational structural signals: resource states, resource relationships, and structural facts about the Construction OS environment.
- The cache reads from CRI during the compile phase of its lifecycle. It does not write to CRI, modify CRI's data, or send feedback to CRI.
- CRI's structural intelligence forms the backbone of each awareness snapshot. Without CRI input, the cache's structural awareness is incomplete.

---

## Non-Authority Guarantees

1. **NOT root truth.** Construction_Awareness_Cache does not originate, define, or guarantee truth. It compiles from sources that are themselves truth-derived, but the cache's output is a compiled artifact, not a truth assertion.

2. **NOT a registry.** The cache does not serve as the authoritative record of system components, service identities, configurations, or capabilities. That function belongs elsewhere in the system.

3. **NOT a kernel.** The cache does not orchestrate system behavior, schedule processes, manage lifecycle, or control execution flow. It operates within its own compilation lifecycle and does not govern other components.

4. **Is a compiled present-state awareness artifact.** The cache's output is a frozen, versioned, lineage-complete snapshot of compiled awareness at a specific point in time. It is an artifact — produced, validated, and locked — not a live, mutable state.

5. **Fail-closed on invalid compilation.** If any phase of the thaw-compile-validate-refreeze lifecycle encounters an error, inconsistency, broken lineage, or unresolvable conflict, the cycle fails closed. The previous valid snapshot remains active. No invalid, partial, or unvalidated snapshot is ever promoted or served to consumers.

6. **Lineage preservation.** Every element in every frozen snapshot carries a complete, untampered lineage chain from its original source through every compilation cycle it has traversed. Lineage is never truncated, summarized, or discarded. This guarantee enables full auditability and source tracing for any element in any snapshot at any point in the version history.
