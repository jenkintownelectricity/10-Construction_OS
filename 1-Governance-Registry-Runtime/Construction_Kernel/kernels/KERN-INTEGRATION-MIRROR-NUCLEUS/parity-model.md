# Parity Model

## Overview

Parity is the verified condition in which a mirror's reflection faithfully represents the source system's truth within declared tolerances. Parity is not identity — a mirror does not need to reproduce the source system exactly. It needs to accurately reflect the aspects it claims to reflect, within the bounds it declares.

This document defines what parity is, how parity is measured, the role of fixtures in establishing parity evidence, parity levels, and the rules governing parity assessment.

---

## What Parity Means

Parity answers a single question: **Does the mirror's reflection match the source system's reality, within the tolerances the mirror declares?**

This question is deceptively simple. Consider a mirror reflecting project data from an external project management system. The source system may represent a project with 200 fields. The mirror may only reflect 30 of those fields. Parity does not require that all 200 fields match — it requires that the 30 declared reflection points match the source system's values for those 30 fields, within whatever tolerances have been declared (e.g., timestamps may be within a 5-minute window; currency amounts may be within rounding tolerance).

Parity is:
- **Declared** — The mirror explicitly states which aspects it reflects and what tolerances apply
- **Measured** — Parity is verified through structured fixtures, not assumed or asserted
- **Evidenced** — Parity verification produces artifacts that can be audited
- **Periodic** — Parity is not verified once and forgotten; it is re-verified on a schedule
- **Scoped** — Parity applies to declared reflection points, not to the entire source system

Parity is NOT:
- A guarantee that the mirror is a perfect copy of the source system
- A one-time certification that never expires
- An assertion without evidence
- A binary state that covers all aspects of a mirror simultaneously

---

## How Parity Is Measured

### Parity Fixtures

Parity is measured through **fixtures** — structured test artifacts that compare the mirror's reflection against the source system's actual state. A fixture is not a unit test in the traditional software sense. It is an evidence-producing verification that crosses the mirror boundary to check agreement between two independent systems.

**Anatomy of a parity fixture:**

| Component | Purpose |
|---|---|
| `fixture_id` | Unique identifier for this fixture |
| `mirror_id` | The mirror being verified |
| `reflection_points` | The specific data points being compared |
| `tolerance_spec` | Acceptable deviation for each data point |
| `source_query` | How to retrieve the reference value from the source system |
| `reflection_query` | How to retrieve the reflected value from the mirror |
| `comparison_logic` | How to compare the two values given the tolerance |
| `last_run` | Timestamp of the most recent execution |
| `last_result` | PASS, FAIL, or ERROR |
| `evidence_artifact` | Reference to the stored evidence from the last run |

### Fixture Execution

When a parity fixture executes, it:

1. **Retrieves the source value** — Queries the source system for the reference data points
2. **Retrieves the reflected value** — Queries the mirror's reflection for the same data points
3. **Applies tolerance comparison** — Compares the two values using the declared tolerance specification
4. **Records the result** — Stores the comparison result as a structured evidence artifact
5. **Updates parity state** — Contributes to the mirror's overall parity assessment

Fixtures execute independently. A failure in one fixture does not prevent other fixtures from executing. Each fixture produces its own evidence artifact.

### Fixture Scheduling

Fixtures are executed on a schedule declared in the mirror manifest. The schedule may vary by fixture — high-criticality reflection points may be verified hourly, while low-criticality points may be verified daily or weekly. The freshness window of the underlying reflection constrains the maximum fixture interval: a fixture must run at least once within each freshness window period.

---

## Parity Levels

Every mirror's parity state is assessed as one of four levels. Parity level is determined by aggregating the results of all parity fixtures associated with the mirror.

### FULL

All declared parity fixtures are passing. Every reflection point that the mirror claims to reflect has been verified against the source system within declared tolerances. The mirror's reflections can be relied upon with full confidence.

**Conditions for FULL parity:**
- All parity fixtures have executed within their scheduled windows
- All fixture results are PASS
- No fixture is in ERROR state
- No declared reflection point lacks a corresponding fixture

**Implications:**
- The mirror may hold ACTIVE lifecycle state
- The mirror's operational status may be HEALTHY
- Consumers may rely on reflections for operational decisions

---

### PARTIAL

Some parity fixtures are passing while others are failing or have not yet been executed. The mirror's reflections are partially reliable — some reflection points are verified, others are not.

**Conditions for PARTIAL parity:**
- At least one parity fixture is passing
- At least one parity fixture is failing, in ERROR state, or has not executed within its scheduled window
- The failing fixtures do not cover all declared reflection points

**Implications:**
- The mirror may hold ACTIVE lifecycle state but its operational status should be DEGRADED
- Consumers may rely on verified reflection points but must not assume unverified points are accurate
- A drift investigation should be initiated for failing fixtures
- A remediation timeline must be established

---

### NONE

No parity fixtures are passing. Either all fixtures are failing, all are in ERROR state, or no fixtures have been executed. The mirror's reflections cannot be relied upon.

**Conditions for NONE parity:**
- All parity fixtures are failing or in ERROR state
- OR no parity fixtures have been executed since the mirror was last updated
- OR no parity fixtures exist for the mirror

**Implications:**
- The mirror must not hold ACTIVE lifecycle state with HEALTHY operational status
- Consumers must not rely on reflections for operational decisions
- Immediate investigation and remediation is required
- If the mirror is ACTIVE, its operational status must be IMPAIRED or UNAVAILABLE

---

### UNKNOWN

Parity has not been assessed. This is the initial state for a new mirror or a mirror that has not yet had its fixtures executed. UNKNOWN is not the same as NONE — NONE means "we checked and nothing passes," while UNKNOWN means "we have not checked."

**Conditions for UNKNOWN parity:**
- The mirror is newly created and fixtures have not yet been developed or executed
- OR the mirror is transitioning between lifecycle states and parity assessment is pending
- OR a system failure has prevented fixture execution and no prior results are available

**Implications:**
- The mirror must not hold ACTIVE lifecycle state
- UNKNOWN is acceptable in PROPOSED, CHARTERED, and STAGED lifecycle states
- Transition from STAGED to ACTIVE requires parity to be assessed (UNKNOWN must be resolved)

---

## Parity Rules

1. **No parity without fixtures.** Parity cannot be asserted without fixture evidence. A statement that "the mirror is in parity" without corresponding fixture results is invalid.

2. **No ACTIVE without parity.** A mirror cannot transition to or remain in ACTIVE lifecycle state without at least PARTIAL parity. FULL parity is required for HEALTHY operational status.

3. **Fixtures must be independent.** Each fixture verifies a specific set of reflection points. Fixture failures must not cascade — one fixture's failure must not prevent other fixtures from executing.

4. **Tolerances must be declared.** Every fixture must declare its tolerance specification. Exact-match, range, percentage, and temporal window tolerances are all valid, but they must be explicit.

5. **Evidence must be retained.** Parity fixture results must be stored as auditable evidence artifacts. Evidence must be retained for the duration specified in the mirror's governance requirements.

6. **Parity is not permanent.** A passing fixture result has a limited validity window. Parity must be re-verified on schedule. Stale fixture results do not constitute current parity evidence.

7. **Parity scope must match reflection scope.** Every declared reflection point must have at least one corresponding parity fixture. A reflection point without a fixture is an unverified claim.

8. **Fixture development is not optional.** Parity fixtures are a required artifact for mirror activation, not a nice-to-have. A mirror without fixtures cannot be activated.

---

## Relationship to Other Models

| Related Model | Relationship |
|---|---|
| **Reflection Model** | Parity verifies the accuracy of reflections |
| **Drift Model** | Drift is detected when parity fixtures fail after previously passing |
| **Status Model** | Parity level contributes to mirror operational status |
| **Mirror Lifecycle** | Parity is a precondition for ACTIVE lifecycle state |
| **Promotion Model** | Parity must be verified across at least two reviews before promotion |
| **Validity Rules** | Rule 6 requires parity fixtures to exist |
