# Breakaway Model

## Definition

A **breakaway** is the controlled separation of a mirror from its source system when continued reflection is unsustainable, harmful, or strategically unnecessary. Breakaway is not failure — it is a governed lifecycle event that acknowledges that the conditions under which a mirror was created no longer hold.

A breakaway ensures that the mirror ceases operation cleanly, its state is preserved for audit, and Construction OS core remains untouched and fully operational.

---

## Breakaway Conditions

A breakaway is triggered when one or more of the following conditions are met:

### 1. Irreconcilable Drift
The source system and the mirror have diverged to the point where parity cannot be restored without disproportionate effort. Drift records show persistent, unresolvable discrepancies across multiple review cycles. The reflection no longer represents a meaningful image of the source.

**Indicators:**
- Parity verification fails across 3+ consecutive review cycles
- Drift magnitude exceeds thresholds defined in the mirror charter
- Source system has undergone schema changes that fundamentally break reflection mappings
- Cost of remediation exceeds the value the mirror provides

### 2. Trust Violation
The partner or source system has violated the trust boundary contract. This includes unauthorized data exfiltration, schema manipulation outside agreed channels, injection of unauthorized dependencies, or breach of the identity boundary. A single confirmed trust violation is sufficient grounds for immediate breakaway.

**Indicators:**
- Unauthorized data access attempts detected at the trust boundary
- Schema mutations performed without governance approval
- Identity boundary compromised — credentials shared or leaked
- Data classified as FORBIDDEN accessed or transmitted through the mirror

### 3. Partner Relationship Termination
The business relationship with the partner who owns or consumes the mirror has ended. This may be a contractual termination, acquisition, dissolution, or mutual agreement to discontinue collaboration. The mirror has no consumer and no reason to continue reflecting.

**Indicators:**
- Contractual termination notice received
- Partner organization dissolved or acquired
- Mutual written agreement to end the integration
- Partner system decommissioned

### 4. Strategic Divergence
The strategic direction of Construction OS no longer aligns with the purpose of the mirror. The domain the mirror serves has been deprecated, replaced by a different integration pattern, or absorbed into core through promotion. Maintaining the mirror creates confusion or governance overhead without corresponding value.

**Indicators:**
- Mirror's domain has been fully promoted into core
- New integration pattern supersedes the mirror's purpose
- Governance review determines mirror provides negative net value
- Product roadmap explicitly deprecates the mirror's function

---

## The Non-Destructive Guarantee

**Breakaway must never corrupt, delete, or destabilize Construction OS core.**

This is an absolute constraint. Regardless of the reason for breakaway, the process must satisfy every one of the following guarantees:

- **No core data loss.** Core data is owned by Construction OS. The mirror holds reflections, not originals. Breakaway removes reflections only.
- **No core schema mutation.** The breakaway process does not alter any schema, table, or data structure in core.
- **No cascading failure.** Mirror failure boundaries ensure that any error during breakaway is contained within the mirror's isolation perimeter.
- **No orphaned references.** All references from core to the mirror (if any exist through governed channels) are resolved or redirected before the mirror is retired.
- **No silent breakaway.** Every breakaway is recorded in the registry with full context, timestamp, and responsible party.
- **No service degradation.** Core services that previously consumed mirror data must gracefully degrade or switch to alternative sources. They must not error or hang.
- **No security exposure.** Credentials, tokens, and access grants associated with the mirror must be revoked during breakaway. No lingering access paths may remain.

---

## Breakaway Process

The breakaway process follows a strict sequence. No step may be skipped.

### Step 1: Evaluate Conditions
Review the triggering condition against the four recognized breakaway conditions. Document the evidence. If the condition is ambiguous, escalate to governance review before proceeding.

- **Input:** Trigger event or drift report
- **Output:** Breakaway evaluation record with condition classification
- **Gate:** At least one recognized breakaway condition must be confirmed
- **Responsible:** Mirror owner with governance oversight

### Step 2: Freeze Mirror
Transition the mirror lifecycle state to FROZEN. While frozen, the mirror accepts no new reflections, processes no inbound data, and serves no outbound queries. Existing state is preserved exactly as-is.

- **Input:** Confirmed breakaway evaluation
- **Output:** Mirror manifest updated to lifecycle_state: FROZEN
- **Gate:** All active slices must acknowledge freeze before proceeding
- **Responsible:** Mirror operator

### Step 3: Archive State
Capture the complete mirror state for audit and historical reference. This includes the manifest, all slice configurations, drift records, parity fixtures, reflection logs, and the breakaway evaluation record.

- **Input:** Frozen mirror
- **Output:** Timestamped archive bundle stored in the designated archive location
- **Gate:** Archive integrity hash must be computed and recorded
- **Responsible:** Mirror operator with audit team verification

### Step 4: Disable Slices
Each enabled slice is individually disabled. Slice disablement follows the slice's own shutdown protocol, which must include dependency notification and graceful connection termination.

- **Input:** Archived mirror with frozen slices
- **Output:** All slices transitioned to DISABLED status
- **Gate:** No slice may remain in ACTIVE or PENDING status
- **Responsible:** Slice owners coordinated by mirror operator

### Step 5: Record Breakaway
Write the breakaway event to the mirror registry. The record must include: mirror_id, breakaway timestamp, triggering condition, evaluation evidence summary, responsible party, archive location reference, and any downstream notifications sent.

- **Input:** Disabled mirror with completed archive
- **Output:** Registry entry with breakaway record
- **Gate:** Registry write must be confirmed before proceeding
- **Responsible:** Governance team

### Step 6: Retire Mirror
Transition the mirror lifecycle state to RETIRED. A retired mirror cannot be reactivated. If the same source system requires a new mirror in the future, a new mirror must be chartered from scratch.

- **Input:** Recorded breakaway
- **Output:** Mirror manifest updated to lifecycle_state: RETIRED
- **Gate:** Final registry update confirming retirement
- **Responsible:** Governance team with mirror owner acknowledgment

---

## Post-Breakaway Obligations

After breakaway is complete:

1. **Notify stakeholders.** Any team or system that consumed the mirror's reflections must be notified of the retirement with sufficient lead time or immediate notice (for trust violations).
2. **Review dependent mirrors.** If other mirrors depended on this mirror's slices (through governed channels), those mirrors must be evaluated for impact and potentially frozen themselves.
3. **Audit trail preservation.** The archive must be retained for the period specified by governance policy. It must not be deleted or modified.
4. **Credential revocation.** All access tokens, API keys, service accounts, and credentials associated with the mirror must be revoked.
5. **Lessons learned.** If the breakaway was caused by drift or trust violation, the root cause should be documented to improve future mirror chartering.

---

## Breakaway vs. Other Lifecycle Events

| Event | Purpose | Reversible | Core Impact |
|-------|---------|------------|-------------|
| Freeze | Temporary suspension | Yes | None |
| Breakaway | Permanent separation | No | None (guaranteed) |
| Promotion | Absorption into core | No | Additive only |
| Transfer | Handoff to external party | No | None |

Breakaway is the only lifecycle event that results in permanent retirement without any artifact moving into core or to an external party. It is the clean termination path.

---

## Emergency Breakaway

In cases of confirmed trust violation or active security incident, an **emergency breakaway** may bypass the normal evaluation period:

1. Immediately freeze the mirror (Step 2)
2. Disable all slices (Step 4)
3. Revoke all credentials
4. Perform evaluation, archival, and recording after the fact

Emergency breakaway still must satisfy the non-destructive guarantee. The only difference is that evaluation documentation is completed retrospectively rather than prospectively. The archive step may occur after slice disablement rather than before, but must still be completed.
