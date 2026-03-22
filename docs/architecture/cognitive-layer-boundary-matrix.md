# Cognitive Layer Boundary Matrix

> **Authority**: This document is the wording authority for the cognitive-layer specification pass only.
> All repository-specific documents must conform to it exactly.
> No near-synonyms or repo-local rephrasings are permitted for the core roles defined herein.

---

## Locked Vocabulary

The following terms are defined for verbatim reuse across all cognitive-layer repositories. These definitions must be used exactly as written.

| Term | Definition |
|---|---|
| **memory formation** | The process by which Construction_Reference_Intelligence ingests, synthesizes, and structures intelligence signals from construction-domain sources. |
| **structural intelligence** | The organized, queryable knowledge artifacts produced by memory formation, available for consumption by downstream cognitive-layer components. |
| **governed relay / observation / guidance** | The operating mode of ValidKernelOS_VKBUS — it relays messages under governance rules, observes system state, and provides guidance packets. It does not merely transport. |
| **topology authority** | The exclusive role of Construction_OS_Registry — it is the only component authorized to define and validate the Construction OS repository topology. |
| **cognitive event/admission layer** | The role of Construction_Cognitive_Bus — it governs admission of cognitive events (observations, proposals, validated events) into the system via schema validation and trust verification. |
| **frozen compiled awareness** | The state of Construction_Awareness_Cache — a point-in-time compiled snapshot of system awareness, frozen for safe read access. |
| **live consciousness / safe operation** | The operating mode of Construction_Assistant — it reads frozen compiled awareness and operates safely within bounded emission constraints. |
| **active thought / proposal generation** | The role of Construction_Intelligence_Workers — they generate proposals, observations, and signals through active computation. |
| **observation** | A cognitive event class representing a factual signal about system state, emitted by workers or other components into the cognitive event/admission layer. |
| **proposal** | A cognitive event class representing a suggested action or change, emitted by workers into the cognitive event/admission layer for governed admission. |
| **validated event** | A cognitive event that has passed schema validation and trust verification in the cognitive event/admission layer. |
| **non-authority** | The explicit classification of all cognitive-layer components — none may serve as truth authority; only kernels hold truth authority. |
| **fail-closed** | The required behavior on invalid state — all cognitive-layer components must reject and halt rather than proceed with unvalidated data. |
| **lineage** | The provenance chain that must be preserved for all cognitive events, awareness compilations, and intelligence signals. |
| **append-only record** | The storage model for the cognitive event/admission layer's event ledger — events are appended and never mutated. |

---

## Boundary Matrix

### Construction_Reference_Intelligence (CRI)

| Dimension | Value |
|---|---|
| **Primary Role** | memory formation + structural intelligence |
| **What It Is** | The memory formation and structural intelligence layer for Construction OS. |
| **What It Is NOT** | NOT truth authority. NOT the cognitive bus. NOT the awareness cache. NOT a kernel. NOT a registry. |
| **Can Emit** | Yes — intelligence signals. |
| **Can Consume** | Yes — construction-domain source data. |
| **Can Compile** | No. |
| **Can Route** | No. |
| **Can Validate** | No (not in the topology or event-admission sense). |
| **Can Store** | Yes — structured intelligence artifacts. |
| **Relationship to Truth** | non-authority. Does not define or hold canonical truth. Defers to kernels. |
| **Relationship to Registries** | Registered as a cognitive-layer component by Construction_OS_Registry. Does not define topology. |
| **Relationship to VKBUS** | Receives governed relay / observation / guidance from VKBUS. Does not govern VKBUS. |
| **Relationship to CRI** | Self. |
| **Relationship to Awareness Cache** | Provides intelligence signals that may be ingested during awareness compilation. Does not read or write the cache directly. |
| **Relationship to Workers** | Workers may consume CRI's structural intelligence as input for active thought / proposal generation. CRI does not direct workers. |
| **Relationship to Assistant** | Assistant may reference CRI's structural intelligence indirectly through frozen compiled awareness. CRI does not interact with Assistant directly. |

---

### ValidKernelOS_VKBUS

| Dimension | Value |
|---|---|
| **Primary Role** | governed relay / observation / guidance |
| **What It Is** | The governed relay / observation / guidance layer for the ValidKernel OS ecosystem. |
| **What It Is NOT** | NOT a registry. NOT a kernel. NOT a runtime executor. NOT the construction-domain cognitive bus (Construction_Cognitive_Bus). NOT truth authority. |
| **Can Emit** | Yes — guidance packets and observation signals. |
| **Can Consume** | Yes — system state for observation. |
| **Can Compile** | No. |
| **Can Route** | Yes — governed messages under governance rules. |
| **Can Validate** | No (not topology or event-admission validation). |
| **Can Store** | No — does not store canonical data. |
| **Relationship to Truth** | non-authority. Relays truth-derived guidance but does not originate or hold truth. |
| **Relationship to Registries** | Topology-aware via Construction_OS_Registry. Does not define topology. |
| **Relationship to VKBUS** | Self. |
| **Relationship to CRI** | May relay guidance relevant to CRI. Does not direct CRI's memory formation. |
| **Relationship to Awareness Cache** | Does not read or write the awareness cache. |
| **Relationship to Workers** | Does not direct workers. May relay system-level guidance observable by workers. |
| **Relationship to Assistant** | Does not interact with Assistant directly in the construction cognitive layer. |

---

### Construction_OS_Registry

| Dimension | Value |
|---|---|
| **Primary Role** | topology authority |
| **What It Is** | The Construction OS topology and repository governance authority. |
| **What It Is NOT** | NOT a kernel. NOT truth authority (for doctrine). NOT a cognitive bus. NOT an awareness cache. NOT a runtime executor. |
| **Can Emit** | Yes — registration confirmations. |
| **Can Consume** | Yes — registration requests. |
| **Can Compile** | No. |
| **Can Route** | No. |
| **Can Validate** | Yes — topology and dependency validation. |
| **Can Store** | Yes — topology maps and dependency records. |
| **Relationship to Truth** | topology authority only. Does not own doctrine. Defers to kernels for truth. |
| **Relationship to Registries** | Self. The authoritative registry for Construction OS. |
| **Relationship to VKBUS** | Registers VKBUS as a component. Does not govern VKBUS relay behavior. |
| **Relationship to CRI** | Registers CRI as a cognitive-layer component. |
| **Relationship to Awareness Cache** | Registers Awareness Cache as a cognitive-layer component. |
| **Relationship to Workers** | Registers Workers as a cognitive-layer component. |
| **Relationship to Assistant** | Registers Assistant as a cognitive-layer component. |

---

### Construction_Cognitive_Bus

| Dimension | Value |
|---|---|
| **Primary Role** | cognitive event/admission layer |
| **What It Is** | The governed cognitive event/admission layer for Construction OS. |
| **What It Is NOT** | NOT a kernel. NOT truth. NOT a registry. NOT runtime. NOT the awareness cache. |
| **Can Emit** | Yes — routing of validated events to targets. |
| **Can Consume** | Yes — cognitive events from emitters. |
| **Can Compile** | No. |
| **Can Route** | Yes — admitted events to designated targets. |
| **Can Validate** | Yes — schema validation and trust verification of incoming events. |
| **Can Store** | Yes — append-only record of events. |
| **Relationship to Truth** | non-authority. Validates event structure but does not judge truth content. |
| **Relationship to Registries** | Registered by Construction_OS_Registry. Does not define topology. |
| **Relationship to VKBUS** | Distinct from VKBUS. VKBUS operates at the ValidKernel OS level with governed relay / observation / guidance. The Cognitive Bus operates at the construction cognitive layer with cognitive event/admission. |
| **Relationship to CRI** | Receives intelligence signals from CRI as cognitive events. Does not direct CRI. |
| **Relationship to Awareness Cache** | Admitted events may feed into awareness compilation. Does not read or write the cache directly. |
| **Relationship to Workers** | Receives proposals, observations, and signals from workers. Routes validated events to appropriate targets. |
| **Relationship to Assistant** | May route validated events observable by Assistant. Does not direct Assistant. |

---

### Construction_Assistant

| Dimension | Value |
|---|---|
| **Primary Role** | live consciousness / safe operation |
| **What It Is** | The live consciousness and safe operation layer for Construction OS. |
| **What It Is NOT** | NOT truth authority. NOT the primary proposal generator. NOT a kernel. NOT a registry. NOT the cognitive bus. |
| **Can Emit** | Yes — bounded outputs (truth, uncertainty, insufficiency, next valid action). |
| **Can Consume** | Yes — frozen compiled awareness (read-only). |
| **Can Compile** | No. |
| **Can Route** | No. |
| **Can Validate** | No (not topology or event-admission validation). |
| **Can Store** | No. |
| **Relationship to Truth** | non-authority. Reads truth-derived awareness but does not hold or define truth. |
| **Relationship to Registries** | Registered by Construction_OS_Registry. Does not define topology. |
| **Relationship to VKBUS** | Does not interact with VKBUS directly in the cognitive layer. |
| **Relationship to CRI** | Accesses CRI's structural intelligence indirectly through frozen compiled awareness. |
| **Relationship to Awareness Cache** | Primary reader of frozen compiled awareness for safe operation. |
| **Relationship to Workers** | Does not direct workers. May receive worker outputs indirectly through awareness or bus. |
| **Relationship to Assistant** | Self. |

---

### Construction_Intelligence_Workers

| Dimension | Value |
|---|---|
| **Primary Role** | active thought / proposal generation |
| **What It Is** | The active thought and proposal generation layer for Construction OS. |
| **What It Is NOT** | NOT truth authorities. NOT self-canonicalizing. NOT a kernel. NOT a registry. NOT the cognitive bus. NOT the awareness cache. |
| **Can Emit** | Yes — proposals, observations, and signals. |
| **Can Consume** | Yes — structural intelligence from CRI and frozen compiled awareness from Awareness Cache. |
| **Can Compile** | No. |
| **Can Route** | No. |
| **Can Validate** | No (not topology or event-admission validation). |
| **Can Store** | No. |
| **Relationship to Truth** | non-authority. Workers must never self-canonicalize. All outputs must hand off into governed validation/admission surfaces. |
| **Relationship to Registries** | Registered by Construction_OS_Registry. Does not define topology. |
| **Relationship to VKBUS** | Does not interact with VKBUS directly in the cognitive layer. |
| **Relationship to CRI** | Consumes CRI's structural intelligence as input for active thought / proposal generation. |
| **Relationship to Awareness Cache** | Reads frozen compiled awareness for context during active thought / proposal generation. |
| **Relationship to Workers** | Self. Workers operate independently and do not self-canonicalize. |
| **Relationship to Assistant** | Workers provide proposals and observations that may eventually reach Assistant through the cognitive event/admission layer and awareness compilation. Workers do not direct Assistant. |

---

### Construction_Awareness_Cache

| Dimension | Value |
|---|---|
| **Primary Role** | frozen compiled awareness |
| **What It Is** | A compiled present-state awareness artifact — the frozen compiled awareness layer for Construction OS. |
| **What It Is NOT** | NOT root truth. NOT a registry. NOT a kernel. NOT the cognitive bus. NOT a runtime executor. |
| **Can Emit** | No (provides read interfaces, does not emit events). |
| **Can Consume** | Yes — intelligence signals, validated events, and other inputs during compilation. |
| **Can Compile** | Yes — awareness compilation from ingestion sources. |
| **Can Route** | No. |
| **Can Validate** | Yes — compilation validation (internal consistency checks during compile). |
| **Can Store** | Yes — frozen compiled awareness snapshots. |
| **Relationship to Truth** | non-authority. Compiles awareness from truth-derived sources but is not itself truth. fail-closed on invalid compilation state. |
| **Relationship to Registries** | Registered by Construction_OS_Registry. Does not define topology. |
| **Relationship to VKBUS** | Does not interact with VKBUS directly in the cognitive layer. |
| **Relationship to CRI** | Ingests CRI's structural intelligence during awareness compilation. |
| **Relationship to Awareness Cache** | Self. |
| **Relationship to Workers** | Workers read frozen compiled awareness. Cache does not direct workers. |
| **Relationship to Assistant** | Assistant reads frozen compiled awareness for safe operation. Cache does not direct Assistant. |

---

## Internal Consistency Verification

This matrix has been verified for the following consistency properties:

1. **No component claims truth authority.** All are classified as non-authority. Only kernels (not in scope of this pass) hold truth authority.
2. **No component duplicates another's primary role.** Each primary role is unique.
3. **Topology authority is exclusive to Construction_OS_Registry.** No other component claims topology governance.
4. **The cognitive event/admission layer is exclusive to Construction_Cognitive_Bus.** VKBUS is explicitly distinguished as governed relay / observation / guidance at the ValidKernel OS level.
5. **Frozen compiled awareness is exclusive to Construction_Awareness_Cache.** No other component compiles or stores awareness.
6. **All components preserve lineage and exhibit fail-closed behavior.** These are universal requirements.
7. **No circular authority dependencies exist.** Each component's relationships are directed and non-circular.

---

*This matrix is the wording authority for the cognitive-layer specification pass only. All repository-specific documents must conform to it exactly. No near-synonyms or repo-local rephrasings are permitted.*
