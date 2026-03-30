# Status Model

## Overview

This document defines the status model for mirrors and capability slices within the Mirror Kernel Nucleus. Statuses represent the current operational condition of an entity at a point in time. Statuses are distinct from lifecycle states — a lifecycle state represents where an entity is in its overall journey (PROPOSED through RETIRED), while a status represents its current operational health or readiness.

---

## Mirror Statuses

Mirror statuses describe the operational condition of an ACTIVE or FROZEN mirror. Mirrors in other lifecycle states (PROPOSED, CHARTERED, STAGED, RETIRED) do not carry an operational status — their lifecycle state is sufficient.

### HEALTHY

The mirror is operating normally. All parity fixtures are passing, no critical or high drift is detected, all validity rules pass, and all enabled slices are functioning.

**Conditions for HEALTHY:**
- Mirror lifecycle state is ACTIVE
- All parity fixtures passing within declared tolerance
- No CRITICAL or HIGH drift detected
- All 12 validity rules pass
- All enabled slices are in OPERATIONAL status

**Transitions from HEALTHY:**
- To DEGRADED: One or more slices are impaired, or partial parity loss detected
- To DRIFTED: Drift detected above declared tolerance
- To IMPAIRED: Multiple issues detected simultaneously
- To UNAVAILABLE: Mirror cannot reflect from source system

---

### DEGRADED

The mirror is operational but with reduced capability. Some slices may be impaired or some parity fixtures may be failing, but core reflection capability is maintained.

**Conditions for DEGRADED:**
- Mirror lifecycle state is ACTIVE
- At least one enabled slice is in IMPAIRED or UNAVAILABLE status, but not all
- OR partial parity loss (some fixtures failing, others passing)
- Core reflection capability is still functional

**Transitions from DEGRADED:**
- To HEALTHY: All issues resolved, all slices operational, all parity restored
- To IMPAIRED: Additional failures accumulate
- To UNAVAILABLE: Source system becomes unreachable or all slices fail

---

### DRIFTED

The mirror's reflection has diverged from its source system beyond declared tolerances. The mirror is still operational, but the accuracy of its reflections is in question.

**Conditions for DRIFTED:**
- Drift detected at MEDIUM severity or above
- Parity fixtures are failing or showing out-of-tolerance results
- Mirror is still able to connect to and reflect from source system

**Transitions from DRIFTED:**
- To HEALTHY: Drift resolved, parity re-established
- To IMPAIRED: Drift severity escalates to CRITICAL
- To UNAVAILABLE: Source system becomes unreachable

---

### IMPAIRED

The mirror has significant operational issues. Multiple problems are present — combinations of drift, parity failures, slice failures, or validity violations. Immediate attention is required.

**Conditions for IMPAIRED:**
- Multiple simultaneous issues (drift + slice failures, parity loss + validity violations, etc.)
- OR any single CRITICAL severity issue
- Mirror may still be partially functional

**Transitions from IMPAIRED:**
- To HEALTHY: All issues resolved (unlikely to skip intermediate states, but valid)
- To DEGRADED: Critical issues resolved, non-critical issues remain
- To UNAVAILABLE: Mirror loses all reflection capability
- Lifecycle transition to FROZEN may be triggered if issues persist

---

### UNAVAILABLE

The mirror cannot perform its reflection function. The source system may be unreachable, or the mirror itself may have a critical failure that prevents all reflection.

**Conditions for UNAVAILABLE:**
- Source system is unreachable
- OR mirror infrastructure has failed
- OR all slices are in UNAVAILABLE status
- No reflection is occurring

**Transitions from UNAVAILABLE:**
- To HEALTHY: Full recovery (source available, all systems nominal)
- To DEGRADED: Partial recovery
- To IMPAIRED: Recovery with residual issues
- Lifecycle transition to FROZEN if UNAVAILABLE persists beyond declared threshold

---

## Mirror Status Transition Summary

```
    +----------+       +----------+       +-----------+
    | HEALTHY  |<----->| DEGRADED |<----->|  IMPAIRED |
    +----+-----+       +----+-----+       +-----+-----+
         |                  |                    |
         |    +--------+    |                    |
         +--->| DRIFTED|<---+                    |
         |    +--------+    |                    |
         |                  |                    |
         v                  v                    v
    +-------------+    +-------------+    +-------------+
    | UNAVAILABLE |<-->| UNAVAILABLE |<-->| UNAVAILABLE |
    +-------------+    +-------------+    +-------------+
              (all paths can reach UNAVAILABLE)
```

---

## Slice Statuses

Slice statuses describe the operational condition of individual capability slices within a mirror.

### OPERATIONAL

The slice is functioning normally. Its inputs are available, its outputs are being produced, and its declared dependencies are satisfied.

**Conditions for OPERATIONAL:**
- Slice is enabled
- All declared dependencies are available
- Inputs are being received normally
- Outputs are being produced within expected parameters

---

### IMPAIRED

The slice is functioning but with reduced capability or performance. Some inputs may be delayed, some outputs may be degraded, or some optional dependencies may be unavailable.

**Conditions for IMPAIRED:**
- Slice is enabled
- Required dependencies are available but one or more optional dependencies are not
- OR inputs are arriving but with delays or quality issues
- OR outputs are being produced but outside normal parameters

---

### UNAVAILABLE

The slice cannot perform its function. Required dependencies are missing, inputs are not arriving, or a critical failure has occurred.

**Conditions for UNAVAILABLE:**
- One or more required dependencies are unavailable
- OR critical input source has failed
- OR slice infrastructure has failed
- No useful output is being produced

---

### DISABLED

The slice has been intentionally disabled. It is not operational and is not expected to be operational. This is a deliberate administrative action, not a failure condition.

**Conditions for DISABLED:**
- Administrative decision to disable the slice
- Slice configuration is set to disabled
- No traffic is being routed to the slice

---

### PENDING_ACTIVATION

The slice has been declared and configured but has not yet been activated for the first time. This is the initial status for newly declared slices.

**Conditions for PENDING_ACTIVATION:**
- Slice declaration is complete
- Dependencies are declared
- Slice has never been in OPERATIONAL status

---

## Slice Status Transition Summary

```
    +---------------------+
    | PENDING_ACTIVATION  |
    +---------+-----------+
              |
        [First activation]
              |
              v
    +-------------+        +-----------+
    | OPERATIONAL |<------>|  IMPAIRED |
    +------+------+        +-----+-----+
           |                     |
           +-------+-------+----+
                   |       |
                   v       v
           +---------------+
           |  UNAVAILABLE  |
           +-------+-------+
                   |
           [Admin disable]
                   |
                   v
           +---------------+
           |   DISABLED    |
           +---------------+
```

**Valid slice status transitions:**

| From | To | Trigger |
|---|---|---|
| PENDING_ACTIVATION | OPERATIONAL | First successful activation |
| PENDING_ACTIVATION | DISABLED | Admin decision before activation |
| OPERATIONAL | IMPAIRED | Partial degradation detected |
| OPERATIONAL | UNAVAILABLE | Critical failure |
| OPERATIONAL | DISABLED | Admin decision to disable |
| IMPAIRED | OPERATIONAL | Issues resolved |
| IMPAIRED | UNAVAILABLE | Degradation escalates to failure |
| IMPAIRED | DISABLED | Admin decision to disable |
| UNAVAILABLE | OPERATIONAL | Full recovery |
| UNAVAILABLE | IMPAIRED | Partial recovery |
| UNAVAILABLE | DISABLED | Admin decision to disable |
| DISABLED | PENDING_ACTIVATION | Re-enablement after significant reconfiguration |
| DISABLED | OPERATIONAL | Re-enablement |

---

## Reflection Statuses

Reflections (the data-surfacing mechanism of mirrors) carry their own status independent of the mirror and slice status.

### ACTIVE

The reflection is actively surfacing current data from the source system.

### STALE

The reflection contains data but it is not current. The last successful reflection occurred longer ago than the declared freshness threshold.

### UNAVAILABLE

The reflection cannot surface data. The source is unreachable or the reflection mechanism has failed.

### SUSPENDED

The reflection has been deliberately paused. No data is being surfaced, but the reflection is configured and can be resumed.

---

## Status vs. Lifecycle State

| Concept | Lifecycle State | Operational Status |
|---|---|---|
| What it describes | Where the entity is in its overall journey | How the entity is performing right now |
| Applicable to | All mirrors in all lifecycle states | Only ACTIVE and FROZEN mirrors |
| Granularity | Coarse (6 states) | Fine (5 mirror statuses, 5 slice statuses) |
| Transition governance | Requires evidence and registry recording | Determined by automated monitoring and manual assessment |
| Persistence | Permanent record in registry | Current state, updated continuously |

A mirror's lifecycle state and operational status are independent dimensions. An ACTIVE mirror may have a status of HEALTHY, DEGRADED, DRIFTED, IMPAIRED, or UNAVAILABLE. A FROZEN mirror retains its last known operational status for diagnostic purposes.
