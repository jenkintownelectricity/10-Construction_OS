# REPO MANIFEST: Construction_Intelligence_Workers

## Identity

- **Repository**: Construction_Intelligence_Workers
- **Organization**: jenkintownelectricity
- **Layer**: Cognitive Layer
- **Primary Role**: Active thought / proposal generation

## Purpose

Construction_Intelligence_Workers is the active thought and proposal generation layer for Construction OS. It performs analysis, generates proposals, emits observations, and produces signals. All outputs are non-authoritative and must pass through governed validation and admission surfaces before entering the system of record.

## Classification

- **Service type**: Cognitive-layer service
- **Authority level**: Non-authority
- **Self-canonicalization**: Prohibited — this repo must never self-canonicalize

## What It IS

- The active thought and proposal generation layer for Construction OS
- A producer of proposals, observations, and signals
- A consumer of structural intelligence (from CRI) and frozen compiled awareness (from Awareness Cache)
- A cognitive worker pool that performs extraction, classification, analysis, and proposal formation
- A lineage-preserving emitter that attaches provenance to every output

## What It IS NOT

- **NOT truth authorities** — workers do not produce validated, canonical facts
- **NOT self-canonicalizing** — workers never write their own outputs into any system of record
- **NOT a kernel** — workers do not govern system structure, schema, or authority rules
- **NOT a registry** — workers do not maintain canonical entity registries or identity resolution
- **NOT the cognitive bus** — workers do not validate, route, or admit events into the system
- **NOT the awareness cache** — workers do not compile, freeze, or serve awareness snapshots

## Interactions with Other Repos

### Construction_Kernel
Workers operate under structural governance defined by the Kernel. The Kernel defines schemas, authority rules, and validation contracts that constrain what workers may emit and how outputs must be formed. Workers consume Kernel-published contracts but never modify or override them.

### Construction_Registry
Workers consume registry-resolved entities as reference data for analysis and proposal generation. Workers do not write to, update, or modify the registry. Entity identity resolution is the registry's authority, not the workers'.

### Construction_CRI (Contextual/Relational Intelligence)
Workers consume CRI structural intelligence as a primary input for active thought. CRI provides the relational and contextual data that workers analyze to generate proposals and observations. Workers read from CRI but do not write structural intelligence back.

### Construction_Cognitive_Bus
Workers emit all proposals, observations, and signals into the Cognitive Bus. The bus independently validates, routes, and admits these outputs according to its own governance rules. Workers do not validate their own outputs, do not route events, and do not bypass the bus under any circumstances.

### Construction_Awareness_Cache
Workers read frozen compiled awareness from the Awareness Cache as contextual input for analysis and proposal generation. Workers do not write to, trigger compilation of, or modify the cache in any way. The cache is a read-only source of compiled context for worker consumption.

### Construction_Assistant
Workers do not direct or control the assistant. Worker outputs reach the assistant indirectly — only after passing through bus admission and awareness compilation. There is no direct communication channel from workers to the assistant.

## Components

### Bus Adapters v0.1

| Component | Path | Purpose |
|---|---|---|
| Worker Config | `workers/config.py` | Identity constants, schema version, allowed/denied event classes |
| Schema Builder | `workers/schema_builder.py` | Builds valid Cognitive Bus event envelopes; refuses ExternallyValidatedEvent |
| Event Adapter | `workers/event_adapter.py` | Submits envelopes to Cognitive Bus admission gate (local call) |
| Observation Emitter | `workers/observation_emitter.py` | Convenience wrapper: build + submit Observation events |
| Proposal Emitter | `workers/proposal_emitter.py` | Convenience wrapper: build + submit Proposal events |
| Format Tests | `tests/test_worker_event_format.py` | Validates envelope structure, field presence, uniqueness, size limits |
| Submission Tests | `tests/test_worker_bus_submission.py` | Validates bus admission/rejection for valid and invalid events |

## Non-Authority Guarantees

1. **Emit proposals/observations/signals only** — workers produce non-authoritative cognitive outputs exclusively
2. **NOT truth authorities** — no worker output constitutes validated fact or canonical record
3. **Never self-canonicalize** — workers are structurally prohibited from writing their own outputs into any system of record or truth store
4. **Must hand off into governed validation/admission surfaces** — all outputs are emitted into the Cognitive Bus, which independently validates and admits them
5. **Fail-closed** — if validation or emission fails, the output is dropped, not forced through; workers do not retry around governance
6. **Lineage preservation** — every output carries full provenance and lineage metadata from source through processing to emission
