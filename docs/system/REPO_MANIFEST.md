# REPO MANIFEST: Construction_Cognitive_Bus

## Identity

- **Repository**: Construction_Cognitive_Bus
- **Organization**: jenkintownelectricity
- **Layer**: Cognitive Layer
- **Primary Role**: Cognitive event/admission layer
- **Runtime Version**: v0.1

## Purpose

Construction_Cognitive_Bus is the governed cognitive event/admission layer for Construction OS. It serves as the admission boundary through which all cognitive events must pass before entering the broader cognitive system. It validates event structure, verifies emitter trust, and maintains an append-only record of all admitted and rejected events.

## Classification

- **Service type**: Cognitive-layer service
- **Authority status**: Non-authority
- **Authority posture**: Defers to kernels for truth

Construction_Cognitive_Bus does not hold truth, does not govern runtime, and does not act as a kernel. It is a service layer that validates structure and routes events. All questions of truth, governance, and authoritative state are deferred to the appropriate kernels.

## What It IS

- **Cognitive event/admission layer** — the governed entry point for cognitive events in Construction OS
- **Event schema validator** — validates that every event conforms to its declared schema before admission
- **Event router** — routes admitted events to designated consumers based on event class and routing rules
- **Append-only record keeper** — maintains an immutable, append-only ledger of all events (admitted and rejected) for auditability and replay

## What It IS NOT

- **NOT a kernel** — it does not hold governing authority over any domain
- **NOT truth** — it validates structure, not the truthfulness or correctness of event content
- **NOT a registry** — it does not serve as a system of record for entities, identities, or configurations
- **NOT runtime** — it does not execute workloads, manage processes, or orchestrate services
- **NOT the awareness cache** — it does not maintain cognitive state, working memory, or awareness context
- **NOT a distributed streaming system** — v0.1 is local, deterministic, and self-contained

## v0.1 Runtime Components

| Component | File | Purpose |
|---|---|---|
| Event Envelope Schema | `schemas/event-envelope.schema.json` | Canonical event structure definition |
| Admission Gate | `bus/admission_gate.py` | Schema, emitter, class, field, and size validation pipeline |
| Emitter Policy | `bus/emitter_policy.py` | Emitter allow/deny enforcement |
| Event Log | `bus/event_log.py` | Append-only admitted event storage |
| Rejection Log | `bus/rejection_log.py` | Append-only rejection record storage |
| Router | `bus/router.py` | Routing decision generation (no delivery) |
| Replay Reader | `bus/replay.py` | Deterministic replay with filtering |
| Configuration | `bus/config.py` | Local constants: paths, limits, allowed emitters/classes |
| Models | `bus/models.py` | Record types, content hashing, routing decisions |

## Admission Pipeline

```
receive_event(event)
  → validate required fields
  → validate schema version
  → validate event_class
  → validate emitter policy
  → validate payload type and size
  → validate ExternallyValidatedEvent authority_status
  → admit → append to event log → produce routing decision
  or
  → reject → append to rejection log
```

## Fail-Closed Guarantees

- Schema invalid → reject
- Emitter not allowed → reject
- Event class invalid → reject
- Required fields missing → reject
- Payload too large → reject
- Policy uncertain → reject
- Malformed replay record → RuntimeError
- No silent failures

## Dependencies

Python 3.10+ standard library only. Zero third-party dependencies.

## Interactions with Other Repositories

### 1. ValidKernel Bus (VKBUS)
Construction_Cognitive_Bus and VKBUS operate as distinct layers. VKBUS is the governed relay, observation, and guidance layer at the ValidKernel OS level. Construction_Cognitive_Bus operates at the construction cognitive layer, handling cognitive event admission. Events that cross the boundary between these layers do so through defined interfaces, with each layer maintaining its own admission and validation responsibilities.

### 2. Construction Reasoning Intelligence (CRI)
Construction_Cognitive_Bus receives intelligence signals from CRI as cognitive events. CRI emits observations, analyses, and proposals that enter the cognitive system through the bus. The bus does not direct CRI; it admits and routes CRI's signals according to the same schema validation and emitter trust rules applied to all emitters.

### 3. ValidKernel (Kernel)
As a non-authority service, Construction_Cognitive_Bus defers to ValidKernel for all questions of truth and governance. The bus validates event structure but never asserts truth. When kernel-level decisions are required, they are the province of ValidKernel, not the bus.

### 4. Construction Awareness Cache
The awareness cache maintains cognitive state and working memory. Construction_Cognitive_Bus routes admitted events toward the awareness cache as a downstream consumer but does not itself maintain awareness state. The bus is a transport and admission layer, not a state holder.

### 5. Registry Services
Construction_Cognitive_Bus is not a registry. It may consume registry information (such as emitter registration and trust levels) to perform emitter trust verification during admission, but it does not serve as the authoritative source for that registration data.

### 6. Runtime / Orchestration Services
Construction_Cognitive_Bus does not participate in runtime orchestration. It does not start, stop, or manage services. Its role ends at admission, recording, and routing of cognitive events.

## Non-Authority Guarantees

1. **Validates structure, not truth content** — the bus confirms that events conform to their declared schemas; it makes no assertion about whether the content of an event is correct or true.
2. **Append-only record** — all events, whether admitted or rejected, are appended to the ledger and never mutated. The historical record is immutable.
3. **Fail-closed** — when the bus encounters ambiguous state, unrecognized emitters, or invalid schemas, it rejects the event. It does not silently pass uncertain events through.
4. **Lineage preservation** — every event carries provenance through source_component and source_repo, and the bus preserves this through admission and routing, ensuring full traceability.
