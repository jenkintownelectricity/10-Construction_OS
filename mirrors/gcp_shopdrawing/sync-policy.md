# Sync Policy: GCP Shop Drawing Mirror

> Defines how synchronization works between the GCP Shop Drawing source system
> and the Construction OS mirror. This is schema-mediated reflection, NOT raw code sync.

## Fundamental Principle

**This mirror does NOT sync code, binaries, or raw data from GCP.**

Synchronization in the Construction OS mirror architecture means *schema-mediated
reflection*: the mirror observes the source system's behavior through its API surface,
reflects that behavior into normalized schemas, and maintains those reflections as
independent, kernel-governed artifacts. The mirror is a structured interpretation of
the source system, not a copy of it.

If GCP's API disappeared tomorrow, the mirror's reflections would remain valid,
useful, and independently operable — they would simply stop receiving updates.

---

## Sync Model: Schema-Mediated Reflection

```
GCP Source System
       |
       | (API observation, not data replication)
       v
 Observation Layer
       |
       | (schema extraction + normalization)
       v
 Reflection Layer (mirror-local)
       |
       | (contract validation)
       v
 Validated Reflection (kernel-governed)
```

### What Gets Synced

| Category | Synced? | Mechanism | Notes |
|---|---|---|---|
| API schema shapes | YES | Schema observation + normalization | Reflected as JSON Schema artifacts |
| Field naming conventions | YES | Mapping tables in normalization rules | GCP names mapped to kernel names |
| Business rule behaviors | YES | Rule extraction + formalization | Observed behavior encoded as explicit rules |
| Validation constraints | YES | Constraint harvesting | Implicit constraints made explicit |
| Data formats and enums | YES | Format mapping tables | GCP-specific formats normalized |
| Raw source code | **NO** | — | Never. Not even indirectly. |
| Database contents | **NO** | — | Never. Mirror holds schemas, not data. |
| Authentication tokens | **NO** | — | Never cross the trust boundary. |
| Binary artifacts | **NO** | — | Never. Only schema descriptions of them. |
| User data | **NO** | — | Never. Mirror is structural, not content-bearing. |

### How Observation Works

1. **API Surface Scanning** — The mirror's observation layer periodically examines
   GCP's public and contracted API endpoints to detect schema changes, new fields,
   deprecated fields, and behavioral changes.

2. **Schema Diffing** — Observed schemas are diffed against the last known reflection.
   Changes are classified as:
   - `ADDITIVE` — New fields or endpoints (low risk)
   - `MODIFYING` — Changed types, constraints, or behaviors (medium risk)
   - `BREAKING` — Removed fields, changed semantics, incompatible changes (high risk)

3. **Reflection Update** — Based on the diff classification:
   - `ADDITIVE` changes are reflected automatically after contract validation
   - `MODIFYING` changes require rule review before reflection
   - `BREAKING` changes trigger a drift alert and require manual intervention

---

## Sync Frequency and Triggers

### Scheduled Sync

| Sync Type | Frequency | Window | Timeout |
|---|---|---|---|
| Full schema observation | Weekly (Sunday 02:00 UTC) | 4 hours | 6 hours |
| Incremental diff check | Daily (06:00 UTC) | 30 minutes | 1 hour |
| Contract validation sweep | Daily (after incremental) | 1 hour | 2 hours |
| Parity measurement | Weekly (Monday 08:00 UTC) | 2 hours | 3 hours |

### Event-Triggered Sync

| Trigger | Action | Latency Target |
|---|---|---|
| GCP API version bump detected | Full schema re-observation | Within 24 hours |
| Breaking change alert from GCP | Drift assessment + manual review | Within 48 hours |
| New slice activation in mirror | Full observation for slice scope | Within 4 hours |
| Promotion candidate extraction | Verification sync before extraction | Immediate |
| Trust boundary violation detected | Sync pause + investigation | Immediate |

---

## Sync Integrity Rules

### Rule 1: Schema Mediation Is Mandatory
Every piece of information that enters the mirror MUST pass through a schema
normalization step. No raw, unnormalized data from GCP may exist in the mirror.

### Rule 2: Reflection Independence
After sync, the reflection must be independently valid. It must pass all contract
tests without any runtime dependency on the GCP source system.

### Rule 3: Provenance Tracking
Every synced reflection must carry provenance metadata indicating:
- Source system identifier (`gcp_shopdrawing`)
- Observation timestamp (ISO 8601)
- Schema version observed
- Normalization rule version applied
- Contract validation result

### Rule 4: Non-Destructive Updates
Sync operations MUST be non-destructive. A sync may:
- Add new reflections
- Update existing reflections (with version bump)
- Mark reflections as `STALE` or `DEPRECATED`

A sync may NOT:
- Delete existing reflections
- Overwrite without version history
- Modify reflections outside the sync scope

### Rule 5: Rollback Capability
Every sync operation must be rollback-capable. The previous state of all affected
reflections must be preserved for a minimum of 90 days, allowing full rollback
to the pre-sync state.

---

## Conflict Resolution

When a sync produces a conflict (e.g., a local modification to a reflection that
conflicts with an upstream observation), the following resolution order applies:

1. **Kernel contracts win** — If the upstream change would violate a kernel contract,
   the upstream change is rejected and a drift alert is raised.
2. **Local modifications are preserved** — If a reflection has been locally modified
   (e.g., during promotion preparation), the local modification takes precedence and
   the upstream change is queued for manual review.
3. **Upstream wins by default** — If no local modifications exist and no contracts
   are violated, the upstream observation is reflected automatically.

---

## Sync Scope by Slice

### Active Slices

| Slice | Sync Scope | Special Considerations |
|---|---|---|
| `detail_normalization` | GCP detail API schemas, field types, naming | Core sync target; highest change frequency |
| `rules_engine` | GCP business rule behaviors, constraint patterns | Rules are inferred from behavior, not copied |
| `validation` | GCP validation endpoint responses, error formats | Constraint harvesting from error patterns |
| `artifact_manifest` | GCP artifact types, lifecycle states, relationships | Manifest structure changes are rare but impactful |
| `lineage` | GCP provenance metadata, parent-child relationships | Lineage depth may vary by artifact type |

### Staged Slices (Pre-Sync Configuration)

Staged slices do not yet participate in active sync, but their sync scopes are
pre-defined to ensure smooth activation:

| Slice | Planned Sync Scope |
|---|---|
| `governance` | GCP access control patterns, approval workflows |
| `registry` | GCP artifact registry structure, naming conventions |
| `receipt_audit` | GCP receipt/acknowledgment patterns |
| `artifact_generation` | GCP generation templates, output formats |
| `execution_orchestration` | GCP workflow execution patterns |
| `review_support` | GCP review cycle structures |
| `delivery_packaging` | GCP delivery bundle formats |
| `standards_mapping` | GCP standards references (AISC, ACI, etc.) |
| `spec_ingestion` | GCP specification import formats |
| `submittal_analysis` | GCP submittal structure and metadata |

---

## Sync Health Metrics

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Sync success rate (30-day) | > 95% | 85-95% | < 85% |
| Average sync latency | < 30 min | 30-60 min | > 60 min |
| Unresolved drift alerts | 0 | 1-2 | 3+ |
| Stale reflections (no update in 30 days) | 0 | 1-3 | 4+ |
| Contract validation pass rate | 100% | 95-99% | < 95% |
| Rollback events (90-day) | 0 | 1 | 2+ |

---

## Sync Audit Trail

All sync operations are logged to `reports/sync-audit-log.yaml` with the following
structure per entry:

```yaml
- sync_id: "sync-20260320-001"
  timestamp: "2026-03-20T06:00:00Z"
  type: "incremental"
  scope:
    slices: ["detail_normalization", "validation"]
  observations:
    schemas_checked: 12
    changes_detected: 2
    changes_reflected: 2
    changes_rejected: 0
  validation:
    contracts_tested: 45
    contracts_passed: 45
    contracts_failed: 0
  duration_seconds: 847
  status: "SUCCESS"
  rollback_available: true
  rollback_expiry: "2026-06-18T06:00:00Z"
```

---

## Emergency Sync Halt

Sync can be halted immediately by any of the following:
- Trust boundary violation detected
- 3+ contract validation failures in a single sync
- Kernel-level emergency freeze directive
- Mirror maintainer manual halt

To resume sync after a halt, the halt condition must be resolved and a manual
sync-resume approval must be granted by the mirror maintainer and one kernel
architect.
