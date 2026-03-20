# Drift Model

## Overview

Drift is the condition in which a mirror's reflection diverges from its source system's actual state beyond declared tolerances. Drift is the inverse of parity: where parity means "the reflection matches the source," drift means "the reflection no longer matches the source." Drift is not inherently a failure — source systems change, environments evolve, and some temporary drift is expected. What matters is that drift is detected, recorded, assessed, and responded to within governed timeframes.

This document defines what drift is, how drift is detected and recorded, drift severity levels, and the response options available when drift is identified.

---

## What Drift Is

Drift occurs when the source system's state has changed in ways that the mirror's reflection no longer accurately represents, or when the mirror's translation logic has become stale relative to source system changes.

**Examples of drift:**
- A source system adds a new required field that the mirror does not yet reflect
- A source system changes the format of a data element (e.g., date format change)
- A source system's API version advances and the mirror's integration has not been updated
- A source system modifies business rules that change the meaning of reflected data
- Network or infrastructure changes cause intermittent data loss in the reflection path

**Drift is NOT:**
- A planned pause in reflection (that is FROZEN status)
- A deliberate decision to stop reflecting a data point (that is a scope change)
- A mirror operating within its declared tolerances (tolerance-within-range is parity, not drift)
- A mirror that was never in parity (that is UNKNOWN or NONE parity, not drift)

Drift specifically describes a **change from a previously established parity state**. A mirror must have been in parity at some point for drift to be a meaningful concept.

---

## How Drift Is Detected

### Detection Methods

**Fixture-Based Detection (Primary)**

Parity fixtures are the primary drift detection mechanism. When a fixture that was previously passing begins to fail, drift has been detected. The fixture's evidence artifact records exactly what diverged, by how much, and when.

**Schedule-Based Detection**

Fixtures run on declared schedules. If a fixture has not run within its scheduled window, the mirror's drift state is UNCERTAIN for the corresponding reflection points. Missed fixture execution is itself a governance event that must be recorded.

**Event-Based Detection**

Some mirrors subscribe to source system change notifications. When the source system reports a change affecting reflected data points, the mirror can proactively check parity rather than waiting for the next scheduled fixture execution.

**Manual Detection**

An operator, auditor, or consumer may report suspected drift based on observed anomalies. Manual drift reports trigger an immediate fixture execution for the affected reflection points.

### How Drift Is Recorded

When drift is detected, a **drift record** is created. Every drift record captures:

| Field | Description |
|---|---|
| `drift_id` | Unique identifier for this drift event |
| `mirror_id` | The affected mirror |
| `detected_at` | Timestamp of detection |
| `detection_method` | How the drift was detected (FIXTURE, SCHEDULE, EVENT, MANUAL) |
| `affected_reflection_points` | Which reflection points are affected |
| `expected_value_summary` | What the reflection expected (summarized, not full data) |
| `actual_value_summary` | What the source system reports (summarized) |
| `deviation_magnitude` | How far the values diverge |
| `severity` | Assessed severity level (LOW, MEDIUM, HIGH, CRITICAL) |
| `status` | Current drift record status (OPEN, INVESTIGATING, MITIGATING, RESOLVED, ACCEPTED) |
| `response_action` | The chosen response (if determined) |
| `resolved_at` | Timestamp of resolution (if resolved) |

---

## Drift Severity Levels

Drift severity is assessed based on the impact of the divergence on mirror reliability and downstream consumer decisions. Severity is not solely determined by the magnitude of the data deviation — a small deviation in a safety-critical field may be CRITICAL, while a large deviation in a cosmetic field may be LOW.

### LOW

The divergence is minor, affects non-critical reflection points, and does not impact downstream operational decisions. The mirror remains reliable for its primary use cases.

**Characteristics:**
- Deviation is within or near declared tolerance boundaries
- Affected reflection points are informational, not decision-critical
- No downstream consumer has reported an issue
- Parity can likely be restored by the next scheduled fixture execution

**Required response timeframe:** Address within the next scheduled maintenance cycle. No immediate action required.

**Example:** A display name field in the source system was updated from "Project Alpha" to "Project Alpha (Phase 2)" and the mirror has not yet picked up the change.

---

### MEDIUM

The divergence affects meaningful reflection points and may impact some downstream decisions if not addressed. The mirror is still broadly reliable but specific reflection points should be treated with caution.

**Characteristics:**
- Deviation exceeds declared tolerance for one or more non-critical reflection points
- OR deviation is detected in a moderate-criticality reflection point
- Some downstream consumers may make incorrect assumptions based on stale data
- Parity restoration requires active intervention, not just the next scheduled run

**Required response timeframe:** Investigate within 48 hours. Establish a remediation plan within one week.

**Example:** A cost estimate field in the source system was updated with a revised figure, and the mirror still reflects the previous estimate. Consumers using this data for budgeting decisions may have outdated information.

---

### HIGH

The divergence affects critical reflection points and is likely impacting downstream operational decisions. The mirror's reliability for affected reflection points is compromised.

**Characteristics:**
- Deviation exceeds declared tolerance for one or more high-criticality reflection points
- OR multiple MEDIUM-severity drifts are detected simultaneously
- Downstream consumers are likely making decisions based on incorrect data
- Parity restoration requires focused effort and may require source system coordination

**Required response timeframe:** Investigate immediately. Begin remediation within 24 hours. Notify affected consumers.

**Example:** A mirror reflecting compliance status from a regulatory source system is reporting "compliant" while the source system has recorded a compliance violation. Consumers relying on this reflection may be making incorrect compliance assertions.

---

### CRITICAL

The divergence represents a fundamental breakdown in the reflection's reliability. The mirror's affected reflection points cannot be trusted. Continued reliance on the reflection for the affected data points poses significant risk.

**Characteristics:**
- Deviation is severe and affects the highest-criticality reflection points
- OR the source system has undergone a structural change that invalidates the mirror's translation logic
- OR multiple HIGH-severity drifts are detected simultaneously
- Downstream decisions based on the affected reflections are likely incorrect
- Parity restoration may require mirror redesign, not just data refresh

**Required response timeframe:** Immediate response required. Affected reflections should be flagged as unreliable or suspended. All consumers must be notified. Remediation begins immediately.

**Example:** The source system has migrated to a new API version with fundamentally different data structures. The mirror's translation logic is producing garbled output. All reflections from this mirror are unreliable.

---

## Drift Response Options

When drift is detected, one of the following response actions must be selected and recorded in the drift record.

### REMEDIATE

Restore parity by updating the mirror's reflection to match the source system's current state. This is the default response for most drift events.

**When to use:** The source system change is legitimate and the mirror should reflect the new state.

**Actions:**
- Update translation mappings if source system structure changed
- Re-execute the reflection to pick up new source data
- Re-run parity fixtures to verify restoration
- Record remediation evidence in the drift record

### ACCEPT

Acknowledge the drift and declare it acceptable. The mirror will continue operating with the known divergence. Acceptance requires documentation of why the drift is acceptable and what the impact boundary is.

**When to use:** The drift is within an acceptable range for business purposes, or the cost of remediation exceeds the impact of the drift.

**Actions:**
- Record acceptance decision with justification
- Update tolerance specifications if the accepted drift exceeds current tolerances
- Notify affected consumers of the accepted divergence
- Set a review date to re-evaluate the acceptance

### ESCALATE

The drift requires attention beyond the mirror team's authority or capability. Escalation routes the drift to platform architecture, the source system owner, or executive decision-makers.

**When to use:** The drift indicates a systemic issue, requires source system changes, or has compliance or contractual implications.

**Actions:**
- Record escalation with routing and urgency
- Notify the escalation target with full drift context
- Continue monitoring the drift while awaiting escalation response
- Do not close the drift record until the escalation is resolved

### FREEZE

Freeze the affected reflections at their current state while the drift is investigated. This prevents further divergence from propagating to consumers while the issue is being resolved.

**When to use:** The drift is severe enough that continued reflection updates might introduce further errors, or investigation requires a stable baseline.

**Actions:**
- Set affected reflection status to FROZEN
- Record freeze decision with justification
- Notify affected consumers that reflections are frozen
- Continue investigation using the frozen baseline as a reference point

### SUSPEND

Suspend the affected reflections entirely. Consumers will receive no data rather than potentially incorrect data. This is the most aggressive response and is reserved for situations where incorrect data poses greater risk than no data.

**When to use:** CRITICAL severity drift where continuing to serve reflections could cause harm.

**Actions:**
- Set affected reflection status to SUSPENDED
- Notify all consumers immediately
- Record suspension decision with justification
- Begin emergency remediation

---

## Drift Lifecycle

A drift record progresses through the following statuses:

1. **OPEN** — Drift has been detected and recorded. No response action has been determined yet.
2. **INVESTIGATING** — The drift is being analyzed to determine severity, scope, and root cause.
3. **MITIGATING** — A response action has been selected and is in progress.
4. **RESOLVED** — Parity has been restored or the drift has been formally accepted. Evidence of resolution is recorded.
5. **ACCEPTED** — The drift has been formally accepted as tolerable. Periodic review is scheduled.

---

## Drift Rules

1. **All drift must be recorded.** Every detected drift event produces a drift record. Drift must never be silently corrected without a record.

2. **Severity must be assessed.** Every drift record must carry a severity level. Severity assessment must consider downstream impact, not just data magnitude.

3. **Response must be chosen.** Every OPEN drift record must have a response action selected within the timeframe dictated by its severity level.

4. **CRITICAL drift requires immediate action.** CRITICAL drift records must be responded to immediately. Delayed response to CRITICAL drift is itself a governance violation.

5. **Acceptance requires justification.** Accepting drift without documented justification is forbidden. Every ACCEPTED drift must have a review date.

6. **Drift records are auditable.** All drift records, including their response actions and resolution evidence, must be retained for the mirror's governance retention period.

---

## Relationship to Other Models

| Related Model | Relationship |
|---|---|
| **Parity Model** | Drift is detected through parity fixture failures |
| **Reflection Model** | Drift affects specific reflections and their statuses |
| **Status Model** | Drift severity influences mirror operational status (DRIFTED, IMPAIRED) |
| **Trust Boundary Model** | Drift investigation may require crossing the trust boundary to inspect source data |
| **Mirror Lifecycle** | Sustained unresolved CRITICAL drift may trigger lifecycle state changes |
| **Validity Rules** | Rule 7 requires drift record schema to exist |
