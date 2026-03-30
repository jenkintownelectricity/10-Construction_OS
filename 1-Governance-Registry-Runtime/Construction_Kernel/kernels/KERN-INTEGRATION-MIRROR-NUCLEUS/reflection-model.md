# Reflection Model

## Overview

A reflection is the mechanism by which a mirror surfaces value from an external source system into the Construction OS ecosystem. Reflections are the primary unit of information flow across a mirror boundary. They carry **compatible truth** — information that has been translated from the source system's native representation into a form that Construction OS can consume, reason about, and present, without directly mutating or replacing Construction OS canonical core truth.

This document defines what a reflection is, how reflections operate, the lifecycle of a reflection, how reflections surface value, and the statuses a reflection may hold.

---

## What a Reflection Is

A reflection is not a copy, not a sync, and not a replication. It is a governed, one-directional surfacing of external value across a trust boundary. The word "reflection" is intentional — just as a mirror reflects an image without absorbing the object, a Construction OS mirror reflects external system value without absorbing the external system itself.

**A reflection:**
- Translates external system concepts into Construction OS-compatible forms
- Makes external information available for consumption by Construction OS modules
- Preserves the semantic intent of the source while conforming to kernel governance
- Is verifiable through parity fixtures
- Is traceable through lineage records
- Is bounded by the trust boundary of its parent mirror

**A reflection is NOT:**
- A database replication or sync channel
- A direct pass-through of raw external API responses
- A mutation path into Construction OS canonical core truth
- A substitute for proper domain modeling within Construction OS
- An unstructured data dump from an external system

---

## How Reflections Surface Value

### Step 1: Source Observation

The mirror observes or queries the source system within the bounds declared in its manifest. The observation may be event-driven (the source system pushes changes) or poll-driven (the mirror queries the source on a schedule). The observation mechanism is an implementation detail of the mirror — it is not visible to Construction OS core.

### Step 2: Translation

The mirror translates the source system's native data structures, terminology, and semantics into Construction OS-compatible forms. Translation is governed by the mirror's declared mapping rules and must be deterministic — the same source input must always produce the same reflection output, given the same mapping version.

### Step 3: Trust Boundary Crossing

The translated information crosses the mirror's trust boundary. At this point, the information is no longer "external system data" — it is a reflection. The trust boundary enforces isolation: the reflection does not carry references to external system internals, does not require external system availability to be read, and does not expose external system credentials or connection details.

### Step 4: Availability

The reflection is made available within Construction OS for consumption. Consumers read the reflection through governed interfaces. Consumers do not know or care which source system produced the reflection — they interact with it as a Construction OS-native structure.

### Step 5: Verification

Parity fixtures compare the reflection against the source system's actual state to verify that the reflection is accurate within declared tolerances. Verification may occur immediately after reflection or on a periodic schedule, depending on the mirror's parity strategy.

---

## Reflection Directionality

Reflections are **read-directional from the perspective of Construction OS core**. This means:

- Construction OS core reads reflections. It does not write to them.
- If Construction OS needs to send information to an external system, that is a separate governed operation (an outbound command), not a reflection.
- Reflections do not create bidirectional coupling. The source system does not read Construction OS state through the reflection path.

Some mirrors may support bidirectional communication, but each direction is independently governed. An inbound reflection and an outbound command are separate capability slices with separate governance, even if they share the same mirror.

---

## Reflection Statuses

Every reflection carries a status indicating its current operational condition. Reflection status is distinct from mirror lifecycle state and mirror operational status — a mirror may be ACTIVE and HEALTHY while an individual reflection is STALE.

### ACTIVE

The reflection is current and verified. Parity fixtures confirm that the reflection accurately represents the source system's state within declared tolerances. Consumers may rely on this reflection for operational decisions.

**Conditions for ACTIVE:**
- The parent mirror is in ACTIVE lifecycle state
- The reflection has been updated within its declared freshness window
- Parity fixtures for this reflection are passing
- No unresolved drift has been detected for this reflection's data points

**Transitions from ACTIVE:**
- To STAGED: The reflection is being prepared but not yet verified in a new context
- To FROZEN: The reflection is intentionally preserved at a point-in-time snapshot
- To DEPRECATED: The reflection is scheduled for removal

---

### STAGED

The reflection exists but is not yet verified for production use. It may be in development, undergoing initial parity verification, or awaiting approval. Consumers must not rely on STAGED reflections for operational decisions.

**Conditions for STAGED:**
- The parent mirror is in CHARTERED or STAGED lifecycle state, or the reflection is newly added to an ACTIVE mirror
- The reflection may or may not have parity fixtures yet
- Initial translation mappings are in place but may not be fully verified

**Transitions from STAGED:**
- To ACTIVE: Parity fixtures pass, freshness window is met, parent mirror is ACTIVE
- To DEPRECATED: The reflection is abandoned before reaching ACTIVE

---

### FROZEN

The reflection is intentionally held at a point-in-time snapshot. No updates are being applied from the source system. The data is valid as of the freeze timestamp but is not being refreshed. Consumers may read FROZEN reflections but must be aware that the data represents a historical snapshot.

**Conditions for FROZEN:**
- A freeze decision has been recorded with a reason and timestamp
- The reflection's last-verified parity state is recorded at freeze time
- The freeze is intentional — it is not the result of a failure (that would be a drift or unavailability condition)

**Use cases for FROZEN:**
- Source system is undergoing a migration and data should not be refreshed until migration completes
- A point-in-time snapshot is needed for audit, compliance, or dispute resolution
- The mirror is transitioning lifecycle states and reflections are preserved during the transition

**Transitions from FROZEN:**
- To ACTIVE: Freeze is lifted, source observation resumes, parity is re-verified
- To DEPRECATED: The frozen reflection is no longer needed

---

### DEPRECATED

The reflection is scheduled for removal. It may still be readable, but consumers must transition away from it. New consumers must not begin depending on a DEPRECATED reflection.

**Conditions for DEPRECATED:**
- A deprecation decision has been recorded with a reason, timestamp, and removal target date
- All current consumers have been notified
- A migration path or replacement has been identified (if applicable)

**Transitions from DEPRECATED:**
- To removal: The reflection is deleted after the removal target date and after all consumers have confirmed migration
- DEPRECATED is a terminal trajectory — a reflection does not transition back to ACTIVE from DEPRECATED. If the same data is needed again, a new reflection is created.

---

## Reflection Identity

Every reflection has a unique identity composed of:

| Field | Description |
|---|---|
| `reflection_id` | Unique identifier within the mirror |
| `mirror_id` | The parent mirror that owns this reflection |
| `source_entity` | The source system concept being reflected |
| `target_form` | The Construction OS-compatible structure the reflection produces |
| `freshness_window` | Maximum acceptable age of the reflection before it is considered stale |
| `parity_strategy` | How and when parity is verified for this reflection |
| `status` | Current reflection status (ACTIVE, STAGED, FROZEN, DEPRECATED) |

---

## Reflection Rules

1. **No raw pass-through.** Every reflection must involve translation. Raw source system responses must never be exposed directly to Construction OS consumers.

2. **No core mutation.** Reflections do not write to Construction OS canonical core truth. If reflected data should become core truth, it must go through the promotion gate.

3. **Deterministic translation.** The same source input with the same mapping version must always produce the same reflection output.

4. **Declared freshness.** Every reflection must declare its freshness window. If the reflection is older than its freshness window, it must be flagged as stale.

5. **Independent failure.** A single reflection's failure must not cascade to other reflections in the same mirror. Each reflection is independently observable and independently recoverable.

6. **Traceable lineage.** Every reflection must record its source observation timestamp, translation mapping version, and parity verification timestamp.

7. **Status accuracy.** A reflection's status must accurately represent its current condition. A reflection that has not been verified within its freshness window must not carry ACTIVE status.

---

## Relationship to Other Models

| Related Model | Relationship |
|---|---|
| **Parity Model** | Parity fixtures verify reflection accuracy |
| **Drift Model** | Drift is detected when a reflection diverges from its source |
| **Trust Boundary Model** | Reflections cross the trust boundary during surfacing |
| **Promotion Model** | Reflections may be promoted into core through the promotion gate |
| **Mirror Lifecycle** | Reflection status is constrained by parent mirror lifecycle state |
| **Status Model** | Reflection statuses contribute to overall mirror operational status |
