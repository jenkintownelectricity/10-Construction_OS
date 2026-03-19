# Construction Truth Event Model

## Purpose

This document defines the canonical rule for how construction truth is represented, stored, and evolved within Construction OS. Construction truth is **stateful and event-based**. Documents are evidence surfaces, not canonical truth containers.

---

## 1. Evidence Surfaces vs. Truth Containers

Documents such as:

- Shop drawings
- Submittals
- Emails
- RFIs (Requests for Information)
- Inspection reports
- Photos
- As-builts

are **evidence surfaces**. They are not the canonical truth container.

The system must extract structured information from these artifacts and store it as **canonical truth events**. The extracted structured facts — not the documents themselves — form the canonical record.

Documents remain important as:

- **Evidence** — they prove that information existed at a point in time
- **Traceability surface** — they link extracted facts back to their source
- **Audit source** — they support verification of extracted truth

The document itself must not be treated as the truth container. Truth lives in the extracted event ledger.

---

## 2. State Model

### Canonical Construction States

| State | Description |
|-------|-------------|
| `concept` | An idea or preliminary notion exists but has not been formally proposed |
| `proposed` | A formal proposal has been submitted for review or approval |
| `approved` | The proposal has been accepted by the appropriate authority |
| `rejected` | The proposal has been explicitly denied |
| `built` | The object has been physically constructed or implemented |
| `observed` | The built condition has been independently observed and recorded |
| `documented` | The observed condition has been formally documented in the record |
| `superseded` | The object or its state has been replaced by a newer version or condition |

State describes the **truth condition** of an object at a point in time.

### Objects That Carry State

- **Assemblies** — proposed or real construction configurations
- **Conditions** — observed physical states of building components
- **Deliverables** — documents, drawings, packages produced for a purpose
- **Observations** — recorded inspections, measurements, field notes
- **Approvals** — formal acceptance or rejection decisions

### State Transition Rule

State transitions occur through **events**. No object may change state without a recorded event. Each event captures both the prior and new state, forming a complete transition history.

---

## 3. Event History Model

Each truth transition must be recorded as a canonical event. Events form a **chronological ledger** that represents the canonical history of extracted construction truth.

### Required Event Fields

| Field | Description |
|-------|-------------|
| `object_id` | Unique identifier of the object whose state changed |
| `object_type` | Type of the object (assembly, condition, deliverable, observation, approval) |
| `event_id` | Unique identifier of this event |
| `event_type` | Classification of the event (e.g., state_transition, fact_extraction, supersession) |
| `prior_state` | State of the object before this event (null for creation events) |
| `new_state` | State of the object after this event |
| `state_version` | Monotonically increasing version number for this object's state |
| `fact_version` | Version of the extracted fact set at the time of this event |
| `source_artifact_id` | Identifier of the evidence surface from which facts were extracted |
| `source_artifact_version` | Version or hash of the source artifact at extraction time |
| `authority` | The governance authority under which this event is valid |
| `actor` | The agent (human or system) that produced this event |
| `effective_timestamp` | When the real-world condition occurred or was decided |
| `recorded_timestamp` | When this event was recorded in the system |
| `extracted_facts` | Structured facts extracted from the source artifact |
| `supersedes_event_id` | If this event corrects or replaces a prior event, the ID of that event (null otherwise) |

### Ledger Properties

- Events are **append-only** — no event may be deleted or modified after recording
- Events are **chronologically ordered** by `recorded_timestamp`
- Corrections are recorded as new events that reference `supersedes_event_id`
- The current state of any object can be derived by replaying its event history

---

## 4. Assembly Truth Rule

Assemblies represent proposed or real construction configurations. An assembly's truth status depends on its state:

| Assembly State | Truth Classification |
|----------------|---------------------|
| `concept` | Preliminary — not yet truth |
| `proposed` | Proposed truth — under review |
| `approved` | Reference truth — approved but not yet physical |
| `built` | Constructed truth — physical but not yet verified |
| `built` AND `observed` | **Actual construction truth** — verified physical reality |
| `documented` | Documented truth — formally recorded verified reality |
| `superseded` | Historical truth — replaced by a newer condition |

An assembly becomes **actual construction truth** only when:

```
state = built AND state = observed
```

Until that moment it remains **reference truth** or **proposed truth**. This distinction prevents the system from treating design intent as physical reality.

---

## 5. Intelligence Signals

The event ledger enables intelligence signals that identify gaps, inconsistencies, and risks in the construction truth record:

| Signal | Meaning |
|--------|---------|
| `approved_not_built` | An approved assembly has no corresponding build event |
| `built_not_observed` | A built assembly has not been independently observed |
| `observed_not_documented` | An observed condition has not been formally documented |
| `approved_not_matching_observed` | The observed condition does not match the approved specification |

These signals are consumed by **Construction_Intelligence_Workers**. Workers must observe event history, not documents directly. Intelligence is derived from the event ledger, not from parsing raw document content.

---

## 6. Truth Flow

Construction OS truth flows through:

```
Universal_Truth_Kernel
  → Construction_Kernel (domain truth boundaries)
    → Truth Event Model (stateful event-based truth)
      → Runtime validation (Construction_Runtime)
        → Capabilities (intelligence, parsing, extraction)
          → Interfaces (applications, user surfaces)
```

The **Truth Event Model** sits between the kernel doctrine and runtime execution. It translates kernel-defined truth boundaries into a concrete event-based system that runtime components can validate against and intelligence workers can observe.

---

## 7. Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- The event model described here is a canonical architecture specification, not a runtime implementation
