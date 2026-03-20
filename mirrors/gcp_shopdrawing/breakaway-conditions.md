# Breakaway Conditions: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Version:** 1.0.0
**Last Updated:** 2026-03-20

---

## Doctrine

> Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

---

## 1. What Is Breakaway

Breakaway is the controlled detachment of a mirror from its source system. It is not an emergency procedure. It is a design-time guarantee. Every mirror is built to break away cleanly. If a mirror cannot break away without damage, it was never a mirror -- it was a hard-wired integration.

Breakaway means:
- The mirror stops reflecting from the source system.
- All data already reflected into Construction OS remains intact and usable.
- No schema migration, data transformation, or consumer-side code change is required.
- Consumers of reflected data continue to operate on the last-known-good state.
- The source system (GCP) is unaffected by the detachment.

---

## 2. Breakaway Triggers

The following conditions may trigger a breakaway evaluation. A trigger does not automatically initiate breakaway. It initiates an assessment.

### 2.1 Strategic Triggers

| Trigger | Description |
|---------|-------------|
| Source system replacement | GCP is being replaced by another general contractor platform. The mirror will be replaced by a new mirror pointing at the new source. |
| Capability internalization | Construction OS is building native shop drawing capabilities that make the mirror redundant. Reflected data is promoted to OS-native data. |
| Business relationship termination | The commercial relationship with GCP's operator ends. API access will be revoked. |
| Architectural consolidation | Multiple mirrors are being consolidated into a single, more capable mirror. |

### 2.2 Operational Triggers

| Trigger | Description |
|---------|-------------|
| Sustained drift beyond tolerance | Parity measurements have been outside tolerance for more than 7 consecutive days with no resolution path. |
| Source data quality collapse | GCP's data quality has degraded to the point where reflected data is unreliable. |
| Trust boundary compromise | A trust boundary violation has been detected that cannot be remediated without architectural changes. |
| API access revocation | GCP has revoked or will revoke API access. |
| Compliance conflict | Regulatory or contractual requirements prohibit continued data exchange with GCP. |

### 2.3 Technical Triggers

| Trigger | Description |
|---------|-------------|
| Irreconcilable schema divergence | GCP has changed its data model in ways that the mediation layer cannot absorb without violating the canonical format. |
| Performance degradation | Sync cycles consistently exceed acceptable duration, creating stale data risk. |
| Security vulnerability | A vulnerability in the integration surface that cannot be patched without breaking the mirror contract. |

---

## 3. Non-Destructive Guarantee

Breakaway is **non-destructive** for both parties. This guarantee is enforced by the mirror architecture:

### 3.1 Construction OS Side

| Guarantee | Mechanism |
|-----------|-----------|
| No data loss | All reflected data is stored in Construction OS canonical format, independent of GCP. GCP's removal does not delete any data. |
| No schema migration | Construction OS data stores use the canonical schema, not GCP's schema. Removing GCP changes nothing about the storage format. |
| No consumer disruption | Consumers read from the canonical data layer, not from the mirror directly. They do not know or care whether the data came from GCP. |
| No orphaned references | All identifiers in Construction OS are mirror-scoped. They do not point back to GCP. They are self-contained. |
| Graceful degradation | After breakaway, reflected data becomes static (last-known-good). Consumers see a "freshness" indicator, not an error. |

### 3.2 GCP Side

| Guarantee | Mechanism |
|-----------|-----------|
| No data loss | The mirror is read-only from GCP's perspective. GCP data is unmodified. |
| No configuration change | GCP does not need to change any configuration when the mirror detaches. |
| No service impact | The mirror's sync agent simply stops calling GCP's APIs. GCP experiences reduced API traffic, not disruption. |

---

## 4. Breakaway Procedure

### Phase 1: Assessment (1-5 business days)

1. **Trigger identification.** Document which trigger condition has been met.
2. **Impact analysis.** Identify all consumers of this mirror's reflections. Assess their dependency on data freshness vs. historical data.
3. **Alternative sourcing.** Determine whether another source can provide equivalent capabilities. If so, plan mirror replacement. If not, plan for static data operation.
4. **Timeline.** Establish the breakaway timeline based on urgency and downstream impact.
5. **Communication.** Notify all stakeholders: Construction OS consumers, GCP liaison, platform team.

### Phase 2: Preparation (1-10 business days)

1. **Final sync.** Execute a full reconciliation sync to ensure the most current data is reflected.
2. **Snapshot.** Create a point-in-time snapshot of all reflected data with full metadata.
3. **Parity record.** Record final parity measurements for all active slices.
4. **Consumer notification.** Notify all consumers that the mirror will transition to static mode on a specific date.
5. **Breakaway dry run.** Disable the sync agent in a staging environment and verify that all consumers operate correctly on static data.

### Phase 3: Execution (1 business day)

1. **Disable sync agent.** Stop all scheduled and event-triggered syncs.
2. **Close trust boundary.** Mark the trust boundary as `SEVERED`. No further crossings.
3. **Update mirror state.** Set `lifecycle_state` to `BREAKING_AWAY` in the manifest.
4. **Preserve credentials.** Revoke or archive mirror-specific API credentials. Do not leave active credentials for a detached mirror.
5. **Verify consumer operation.** Confirm that all consumers continue to operate on static data.

### Phase 4: Completion (1 business day)

1. **Update mirror state.** Set `lifecycle_state` to `DETACHED` in the manifest.
2. **Archive mirror artifacts.** Archive all mirror documentation, manifests, and configuration.
3. **Update Construction OS registry.** Mark the mirror as detached in any central mirror registry.
4. **Post-breakaway report.** Document the breakaway: trigger, timeline, impact, lessons learned.

---

## 5. Breakaway Readiness Checklist

This checklist should be satisfiable **at all times**, not just when breakaway is imminent. If any item fails, it indicates a breakaway readiness deficiency that should be remediated immediately.

- [ ] All reflected data is stored in Construction OS canonical format (no GCP-native formats in OS stores).
- [ ] All identifiers are mirror-scoped (no GCP IDs used as primary keys).
- [ ] No consumer code directly references GCP schemas, field names, or enumeration values.
- [ ] The sync agent can be stopped without causing errors in consumer systems (consumers degrade gracefully to static data).
- [ ] A full data snapshot can be created within 1 hour.
- [ ] All consumers have been identified and their freshness requirements documented.
- [ ] The trust boundary can be severed by configuration change (no code deployment required).
- [ ] GCP API credentials are isolated (revoking them does not affect other system credentials).
- [ ] A breakaway dry run has been executed within the last 90 days.

---

## 6. Post-Breakaway State

After breakaway completes:

| Aspect | State |
|--------|-------|
| Reflected data | Static. Available for read. Marked with `last_synced_at` timestamp. |
| Data freshness | Frozen at breakaway date. New data from the domain is not available. |
| Consumer operation | Functional with static data. Freshness indicators visible. |
| Mirror manifest | Archived. `lifecycle_state: DETACHED`. |
| Trust boundary | Severed. No data flows. Configuration preserved for reference. |
| Sync agent | Stopped. Credentials revoked. |
| Documentation | Archived with the mirror. Accessible for reference. |

---

## 7. Mirror Replacement After Breakaway

If a new source system replaces GCP for shop drawing capabilities:

1. A **new mirror instance** is created (e.g., `newplatform_shopdrawing`).
2. The new mirror has its own trust boundary, its own manifest, its own slices.
3. Data from the old mirror (static) coexists with data from the new mirror (live) during transition.
4. Consumers are migrated from the old mirror's data to the new mirror's data through a controlled cutover.
5. The old mirror remains archived until all consumers have migrated.
6. The old mirror's data can be retained indefinitely as historical record or purged per data retention policy.

This is why mirrors exist. Replacing GCP is a matter of replacing a mirror, not re-architecting Construction OS.
