# Mirror Lifecycle Model

## Overview

Every mirror in Construction OS follows a governed lifecycle with six defined states. Transitions between states are controlled — each transition has preconditions that must be met and evidence that must be recorded. No mirror may skip states, and no transition may occur without being recorded in the registry.

The lifecycle ensures that mirrors are properly proposed, vetted, tested, governed during active use, and cleanly retired when no longer needed.

---

## Lifecycle States

### PROPOSED

The mirror has been proposed but not yet approved for development. This is the intake state where the idea for an integration is evaluated against the doctrine and kernel constraints.

**Entry conditions:**
- A mirror proposal document exists identifying the source system, intended capability slices, and business justification.
- The proposal does not violate any of the 14 global hard constraints on its face.
- A proposed owner is identified.

**Allowed activities:**
- Feasibility analysis
- Doctrine compliance review
- Source system evaluation
- Preliminary trust boundary design

**Exit conditions:**
- Proposal is approved and a charter is issued (transition to CHARTERED)
- Proposal is rejected (terminal state for this proposal; a new proposal may be submitted)

---

### CHARTERED

The mirror has been approved for development. A charter document defines the scope, constraints, intended slices, and acceptance criteria. Development of the mirror may begin.

**Entry conditions:**
- Proposal has been reviewed and approved.
- Charter document exists with: scope, intended slices, trust boundary design, acceptance criteria, timeline, and assigned owner.
- Mirror ID has been assigned.
- Registry entry has been created in CHARTERED state.

**Allowed activities:**
- Mirror manifest creation and validation
- Capability slice design and declaration
- Trust boundary implementation
- Reflection development
- Parity fixture development
- Dependency graph construction

**Exit conditions:**
- Mirror manifest is valid, all intended slices are declared, trust boundary is implemented, and at least one parity fixture exists (transition to STAGED)
- Charter is revoked (transition back to PROPOSED or terminal rejection)

---

### STAGED

The mirror is fully built and has passed initial validation, but is not yet serving production traffic. This is the pre-production verification state.

**Entry conditions:**
- Mirror manifest passes schema validation.
- All declared slices have complete dependency graphs.
- Trust boundary is defined and verified.
- At least one parity fixture exists and passes.
- Reflection status is available (not necessarily ACTIVE yet).
- Breakaway conditions are documented.
- Truth ownership is defined for all reflection points.
- No mirror validity rules are violated (all 12 rules pass).

**Allowed activities:**
- Parity verification across multiple fixture sets
- Drift detection baseline establishment
- Breakaway dry-run testing
- Load and performance evaluation
- Security review of trust boundary

**Exit conditions:**
- All parity fixtures pass, drift baseline is established, breakaway dry-run succeeds, and security review is complete (transition to ACTIVE)
- Critical issues found (transition back to CHARTERED for remediation)

---

### ACTIVE

The mirror is live and serving production traffic. This is the primary operational state. Active mirrors are subject to continuous governance including drift detection, parity verification, and validity checks.

**Entry conditions:**
- All STAGED exit conditions are met.
- Parity evidence exists (GHC-12).
- Registry entry is updated to ACTIVE with timestamp and evidence reference.
- Owner confirmation that the mirror is ready for production use.

**Allowed activities:**
- Production reflection of source system value
- Continuous drift detection
- Periodic parity re-verification
- Slice enablement/disablement for individual tenants
- Incremental slice additions (each new slice must meet slice declaration requirements)
- Promotion gate requests for proven reflections
- Transfer assessment requests

**Exit conditions:**
- Operational decision to pause the mirror (transition to FROZEN)
- Decision to decommission the mirror (transition to RETIRED, requires breakaway execution)
- Critical validity violation detected that cannot be immediately remediated (forced transition to FROZEN)

**Continuous requirements while ACTIVE:**
- Parity evidence must remain current (re-verified at declared intervals)
- Drift records must be maintained
- All 12 validity rules must continue to pass
- Registry entry must reflect current state

---

### FROZEN

The mirror is temporarily suspended. It is not serving production traffic but has not been decommissioned. Frozen mirrors retain their configuration and may be reactivated.

**Entry conditions:**
- Mirror was previously ACTIVE or is returning from a failed activation attempt.
- Reason for freezing is recorded in the registry.
- All in-flight reflections have been gracefully stopped or timed out.

**Allowed activities:**
- Investigation and remediation of issues that caused the freeze
- Parity re-verification
- Trust boundary re-assessment
- Configuration updates
- Slice modifications

**Not allowed while FROZEN:**
- Serving production reflection traffic
- New slice enablement for tenants
- Promotion gate requests

**Exit conditions:**
- Issues are remediated and all ACTIVE entry conditions are re-verified (transition to ACTIVE)
- Decision to decommission (transition to RETIRED)
- Extended freeze beyond declared maximum duration without remediation plan (escalation to architecture team)

---

### RETIRED

The mirror has been permanently decommissioned. This is a terminal state. A retired mirror cannot be reactivated — a new mirror must be proposed if the integration is needed again.

**Entry conditions:**
- Breakaway process has been executed successfully.
- All Construction OS core data and functionality is verified intact post-breakaway.
- All tenant-facing capabilities from this mirror have been disabled or migrated.
- Registry entry is updated to RETIRED with timestamp, actor, and evidence reference.
- Archival of mirror artifacts (manifest, fixtures, drift records) is complete.

**Allowed activities:**
- Audit review of archived artifacts
- Historical reporting

**Not allowed:**
- Reactivation (a new PROPOSED mirror must be created instead)
- Any production traffic
- Any data reflection

---

## State Transition Diagram

```
                    +-----------+
                    | PROPOSED  |
                    +-----+-----+
                          |
                    [Charter approved]
                          |
                          v
                    +-----------+
                    | CHARTERED |
                    +-----+-----+
                          |
                    [Validation passed]
                          |
                          v
                    +-----------+
           +------->|  STAGED   |
           |        +-----+-----+
           |              |
           |        [Activation approved]
           |              |
           |              v
           |        +-----------+
           |   +--->|  ACTIVE   |<---+
           |   |    +-----+-----+    |
           |   |          |          |
           |   |    [Freeze]   [Reactivate]
           |   |          |          |
           |   |          v          |
           |   |    +-----------+    |
           |   |    |  FROZEN   +----+
           |   |    +-----+-----+
           |   |          |
           |   |    [Decommission]
           |   |          |
           |   |          v
           |   |    +-----------+
           +---+    |  RETIRED  |  (terminal)
                    +-----------+
```

**Valid transitions:**
| From | To | Trigger |
|---|---|---|
| PROPOSED | CHARTERED | Charter approved |
| CHARTERED | STAGED | Validation passed |
| CHARTERED | PROPOSED | Charter revoked |
| STAGED | ACTIVE | Activation approved |
| STAGED | CHARTERED | Critical issues found |
| ACTIVE | FROZEN | Operational freeze or validity violation |
| FROZEN | ACTIVE | Issues remediated, re-verified |
| FROZEN | RETIRED | Decommission decision |
| ACTIVE | RETIRED | Decommission decision with breakaway |

**Invalid transitions (never allowed):**
- Any state to PROPOSED (except CHARTERED reverting)
- PROPOSED directly to STAGED, ACTIVE, FROZEN, or RETIRED
- CHARTERED directly to ACTIVE, FROZEN, or RETIRED
- STAGED directly to FROZEN or RETIRED
- RETIRED to any state (terminal)

---

## Registry Requirements

Every state transition must be recorded in the registry with:

1. **Mirror ID** — The unique identifier of the mirror
2. **Previous state** — The state before transition
3. **New state** — The state after transition
4. **Timestamp** — When the transition occurred (UTC)
5. **Actor** — Who or what triggered the transition
6. **Reason** — Why the transition occurred
7. **Evidence reference** — Pointer to the evidence supporting the transition (e.g., parity fixture results, breakaway verification, charter document)

Missing any of these fields makes the transition record invalid, which in turn makes the mirror's lifecycle state inconsistent (violating validity rule 11).
