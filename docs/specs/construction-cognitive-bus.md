# Construction Cognitive Bus Specification

## System Role

Construction_Cognitive_Bus is the cognitive event/admission layer for Construction OS. It is the single governed entry point through which all cognitive events must pass before they are admitted into the broader cognitive system. It validates event structure, verifies emitter trust, records every event in an append-only ledger, and routes admitted events to their designated consumers.

## Architecture Position

Construction_Cognitive_Bus sits at the admission boundary between event emitters and the broader cognitive system. No cognitive event enters the system without passing through this boundary. Emitters (human operators, automated systems, intelligence services, sensors) submit events to the bus. The bus decides whether each event is admitted or rejected. Only admitted events proceed downstream.

```
Emitters --> [Admission Boundary: Construction_Cognitive_Bus] --> Cognitive System
                |                                        |
                |  validate schema                       |  route to consumers
                |  verify emitter trust                  |  record in ledger
                |  reject invalid / untrusted            |
                v                                        v
         Rejection Log                           Downstream Consumers
```

The bus does not exist inside the kernel. It does not exist inside the awareness cache. It is the boundary layer that sits in front of them.

## Canonical Event Envelope

Every event that enters the bus must carry the canonical event envelope. Events that do not conform to this envelope are rejected at the schema validation stage.

| Field            | Type     | Description                                                                 |
|------------------|----------|-----------------------------------------------------------------------------|
| `emitter_id`     | string   | Unique identifier of the emitter that produced this event                   |
| `event_class`    | enum     | Classification of the event: `Observation`, `Proposal`, or `ValidatedEvent` |
| `timestamp`      | ISO 8601 | Time at which the emitter produced the event                                |
| `schema_version` | string   | Version of the event schema this event conforms to                          |
| `payload`        | object   | The event-class-specific content of the event                               |
| `lineage_chain`  | array    | Ordered list of upstream event references that led to this event            |

The envelope is the minimum required structure. Event-class-specific schemas define additional requirements for the `payload` field.

## Event Classes

### Observation

An Observation is a factual signal about state. It reports something that has been perceived, measured, or detected. Observations do not request action and do not propose changes. They are declarative statements about the world as the emitter perceives it.

- **Intent**: Report state
- **Authority**: None. An Observation asserts what the emitter perceived, not what is true. Truth is the province of kernels.
- **Examples**: Sensor reading, status report, detected condition, measured value

### Proposal

A Proposal is a suggested action or change. It represents an emitter's recommendation that something should happen. Proposals do not execute; they are submitted for evaluation by downstream consumers who hold the appropriate authority.

- **Intent**: Suggest action or change
- **Authority**: None. A Proposal is a suggestion, not a command.
- **Examples**: Recommended schedule adjustment, suggested resource reallocation, proposed configuration change

### Validated Event

A Validated Event is an event that has passed schema validation and trust verification within the admission pipeline. This class designation is applied by the bus itself during admission processing. Emitters do not submit events with this class; the bus elevates admitted Observations and Proposals to Validated Event status upon successful admission.

- **Intent**: Mark an event as admitted
- **Authority**: Structural validation authority only. The bus validates that the event conforms to schema and that the emitter is trusted. It does not validate truth.
- **Examples**: An admitted Observation, an admitted Proposal

## Emitter Trust Model

All emitters must be registered and assigned a defined trust level before they can submit events to the bus. The trust model operates as follows:

1. **Registered emitters** are known to the system and carry a trust level that determines what event classes they are permitted to emit and what payload schemas they may use.
2. **Unregistered emitters** are rejected. The bus does not admit events from unknown sources. This is a fail-closed posture.
3. **Trust levels** are not determined by the bus. The bus consumes emitter trust information from authoritative sources (registry services, kernel directives). The bus enforces trust; it does not define it.
4. **Trust verification** occurs on every event. There is no session-based trust. Each event is independently verified against the emitter's current trust level.

## Schema Validation

All events must pass schema validation before admission. Schema validation confirms that:

1. The canonical event envelope is complete and well-formed.
2. The `event_class` is a recognized class.
3. The `schema_version` corresponds to a known schema.
4. The `payload` conforms to the schema defined for the declared `event_class` and `schema_version`.
5. The `lineage_chain` is structurally valid.

Invalid events are rejected. Schema validation is structural only. The bus validates that the event is well-formed, not that its content is true or correct.

## Admission Pipeline

The admission pipeline processes every incoming event through a fixed sequence of stages. No stage may be skipped.

```
1. RECEIVE
   Event arrives at the bus from an emitter.

2. VALIDATE SCHEMA
   The event envelope and payload are validated against the declared schema.
   - Pass: proceed to stage 3.
   - Fail: reject. Log rejection with reason. Event is recorded in the ledger as rejected.

3. VERIFY EMITTER TRUST
   The emitter_id is checked against registered emitters and trust levels.
   - Pass: emitter is registered and trusted for this event class. Proceed to stage 4.
   - Fail: reject. Log rejection with reason. Event is recorded in the ledger as rejected.

4. ADMIT
   The event is marked as admitted. Its event_class may be elevated to ValidatedEvent.

5. RECORD IN APPEND-ONLY LEDGER
   The admitted event is appended to the event ledger. This record is immutable.

6. ROUTE TO TARGETS
   The admitted event is routed to designated consumers based on event class and routing rules.
```

## Rejection Model

Rejected events are never silently dropped. Every rejection produces:

1. **Rejection record** — appended to the ledger with the original event, the stage at which rejection occurred, and the rejection reason.
2. **Rejection reason** — a structured explanation of why the event was rejected (schema violation, unregistered emitter, trust level insufficient, ambiguous state).
3. **Fail-closed behavior** — when the bus encounters ambiguous state (unknown schema version, partially corrupted envelope, indeterminate emitter status), it rejects the event. The bus does not guess. It does not pass uncertain events through.

## Append-Only Event Ledger

The event ledger is the permanent, immutable record of all events processed by the bus. Its properties are:

1. **Append-only** — events are appended and never mutated. Once written, a ledger entry cannot be changed, deleted, or reordered.
2. **Complete** — every event is recorded, whether admitted or rejected. The ledger is a full history of everything the bus has processed.
3. **Auditable** — the ledger provides a complete, tamper-evident trail for audit purposes. Any event can be traced from its emitter through admission (or rejection) to its downstream routing.
4. **Replayable** — the ledger supports deterministic replay from any point for audit and recovery purposes.

## Replay Semantics

The ledger supports deterministic replay. This means:

1. **From any point** — replay can begin at any event in the ledger. There is no requirement to replay from the beginning.
2. **Deterministic** — replaying the same sequence of events produces the same admission decisions, the same rejections, and the same routing outcomes, given the same schema definitions and emitter trust state.
3. **Audit use** — replay enables auditors to verify that the bus processed events correctly at any historical point.
4. **Recovery use** — replay enables downstream consumers to recover state by replaying admitted events from the ledger.

Replay does not re-execute downstream effects. It replays the admission pipeline's decisions. Downstream consumers are responsible for their own replay and recovery semantics.

## Routing Targets

Validated events are routed to designated consumers based on:

1. **Event class** — different event classes may have different default routing targets.
2. **Routing rules** — configurable rules that determine which consumers receive which events. Rules may filter on event class, emitter identity, payload attributes, or other envelope fields.
3. **Fan-out** — a single event may be routed to multiple consumers.
4. **No fan-in at the routing stage** — the bus routes events outward. It does not aggregate responses from consumers at the routing stage.

Routing is delivery, not execution. The bus delivers events to consumers. What consumers do with those events is outside the bus's scope.

## Relationship to VKBUS

Construction_Cognitive_Bus and VKBUS are distinct layers that must not be conflated.

| Aspect              | VKBUS                                              | Construction_Cognitive_Bus                          |
|---------------------|-----------------------------------------------------|-----------------------------------------------------|
| **Layer**           | ValidKernel OS level                                | Construction cognitive layer                        |
| **Role**            | Governed relay, observation, and guidance            | Cognitive event admission and routing                |
| **Scope**           | OS-level inter-service communication and governance  | Construction-domain cognitive event processing       |
| **Authority**       | Operates under kernel governance                     | Non-authority; defers to kernels for truth           |

Events may cross between these layers through defined interfaces, but each layer maintains independent admission, validation, and routing responsibilities. The cognitive bus does not relay for VKBUS, and VKBUS does not admit for the cognitive bus.

## Relationship to CRI

Construction Reasoning Intelligence (CRI) is an intelligence service that emits cognitive events. Its relationship to the bus is:

1. **CRI emits events to the bus** — CRI produces observations, analyses, and proposals that are submitted to the bus as cognitive events.
2. **The bus admits CRI events through the standard pipeline** — CRI events are subject to the same schema validation, emitter trust verification, and admission processing as all other events.
3. **The bus does not direct CRI** — the bus is an admission and routing layer. It does not issue commands to CRI, does not control CRI's reasoning, and does not influence CRI's outputs. The relationship is unidirectional: CRI emits, the bus admits and routes.

## Non-Authority Guarantees

Construction_Cognitive_Bus provides the following non-authority guarantees:

1. **NOT a kernel** — the bus does not hold governing authority over any domain. It does not make authoritative decisions about state, policy, or truth.
2. **NOT truth** — the bus validates structure, not truth. An admitted event is structurally valid and from a trusted emitter. It is not certified as true.
3. **NOT a registry** — the bus consumes registration and trust data but does not serve as the authoritative source for that data.
4. **NOT runtime** — the bus does not execute workloads, manage processes, or orchestrate services. It admits and routes events.
5. **NOT the awareness cache** — the bus does not maintain cognitive state, working memory, or awareness context. It is a transport and admission layer.
6. **Validates structure, not truth content** — schema validation confirms well-formedness. It does not confirm correctness, accuracy, or truthfulness of event payloads.
