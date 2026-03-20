# Trust Boundary: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Boundary ID:** `gcp_shopdrawing_boundary`
**Version:** 1.0.0
**Last Updated:** 2026-03-20

---

## Doctrine

> Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

---

## 1. What Is the Trust Boundary

The trust boundary is the architectural surface where GCP's world ends and Construction OS's world begins. It is not a firewall. It is not an API gateway. It is a **schema mediation layer** that ensures:

- No GCP-native data structures leak into Construction OS.
- No Construction OS internals are exposed to GCP.
- All data crossing the boundary is validated, transformed, and audited.
- The boundary can be severed without data loss on either side.

The trust boundary exists because cooperation requires trust, but trust does not require exposure. Two systems can exchange valuable capabilities without exposing their internals to each other.

---

## 2. Boundary Architecture

```
                    TRUST BOUNDARY
                    gcp_shopdrawing_boundary

  GCP Side          |  Mediation Layer  |     Construction OS Side
  (Ingress)         |                   |     (Egress)
                    |                   |
  GCP-native  ---> | Schema Transform  | ---> Canonical Records
  JSON payloads    | Validation         |     OS Primitives
  GCP identifiers  | ID Mapping         |     Mirror-scoped IDs
  GCP timestamps   | Temporal Normalization|  UTC ISO 8601
  GCP enumerations | Vocabulary Mapping |     OS Vocabulary
  GCP references   | Reference Resolution|    Mirror-local refs
                    |                   |
                    | Audit Log Entry   |
                    | Per Crossing      |
```

### 2.1 Ingress Side (GCP-Native)

The ingress side accepts data from GCP in GCP's native format. The sync agent fetches data from GCP's APIs and presents it to the boundary in GCP's JSON schema. The ingress side:

- Accepts GCP-native field names, enumerations, and identifier formats.
- Accepts GCP's timestamp format (may vary by API version).
- Accepts GCP's reference format (project-scoped GUIDs, internal IDs).
- Rejects payloads that do not conform to the expected GCP API response schema.
- Logs all ingress events with payload hashes for audit trail.

### 2.2 Mediation Layer

The mediation layer performs the following transformations:

| Transformation | Description |
|----------------|-------------|
| Schema Transform | Maps GCP fields to Construction OS canonical fields. Handles structural differences (flat vs. nested, arrays vs. maps). |
| Validation | Validates that required fields are present, types are correct, and values are within expected ranges. |
| ID Mapping | Translates GCP identifiers to mirror-scoped identifiers. GCP IDs are stored as opaque references but are never used as primary keys on the OS side. |
| Temporal Normalization | Converts all timestamps to UTC ISO 8601 format. Handles timezone discrepancies. |
| Vocabulary Mapping | Maps GCP enumerations and status values to Construction OS vocabulary. (e.g., GCP's `APPROVED_WITH_COMMENTS` maps to OS's `approved_as_noted`). |
| Reference Resolution | Resolves internal GCP references to mirror-local references. Cross-references to out-of-scope GCP objects are flagged as `external_ref`. |
| PII Stripping | Replaces personal identifiers with opaque actor tokens. |
| Audit Logging | Creates an audit entry for every crossing event. |

### 2.3 Egress Side (Construction OS Canonical)

The egress side emits data in Construction OS canonical format. Consumers on the OS side see:

- Canonical field names following OS naming conventions.
- Mirror-scoped identifiers that are stable even if GCP changes its ID scheme.
- UTC timestamps in ISO 8601 format.
- OS vocabulary for all enumerated values.
- No trace of GCP's internal structure, naming, or conventions.

---

## 3. Data Flow Rules

### 3.1 Direction

Data flows **one direction** through this mirror: from GCP to Construction OS.

| Direction | Allowed | Notes |
|-----------|---------|-------|
| GCP to Construction OS | Yes | Primary reflection flow |
| Construction OS to GCP | No | Mirrors are read-reflections. Write-back requires a separate channel. |
| GCP to GCP (via mirror) | No | The mirror is not a pass-through for GCP's internal communication. |

### 3.2 Frequency

Data crosses the boundary according to the sync schedule:

| Sync Type | Frequency | Description |
|-----------|-----------|-------------|
| Scheduled sync | Every 15 minutes | Regular polling of GCP APIs for changes since last sync |
| Event-triggered sync | On webhook receipt | GCP sends webhook notifications for significant events. The sync agent can perform an immediate pull. |
| Full reconciliation | Daily at 02:00 UTC | Complete comparison of mirror state against GCP state to catch any missed changes. |
| Manual sync | On demand | Platform team can trigger a manual sync for investigation or recovery. |

### 3.3 Volume Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max records per sync cycle | 5,000 | Prevents unbounded load on the mediation layer. Larger batches are split. |
| Max payload size per record | 1 MB | Individual records exceeding this are flagged for manual review. |
| Max total payload per cycle | 100 MB | Aggregate limit per sync cycle. |
| Rate limit (GCP API) | 100 requests/minute | Respects GCP's API rate limits. |

### 3.4 Error Handling

| Scenario | Response |
|----------|----------|
| GCP API unavailable | Sync skipped. Retry at next interval. Alert after 3 consecutive failures. |
| Schema validation failure | Record quarantined. Remaining records processed. Alert raised. |
| ID mapping failure | Record quarantined. Likely indicates a new entity type not yet mapped. |
| Vocabulary mapping failure | Record flagged with `unmapped_value`. Processing continues with raw value preserved in metadata. |
| Payload size exceeded | Record deferred. Alert raised for manual review. |
| Duplicate detection | Idempotent processing. Duplicate crossings produce no new state. |

---

## 4. What Crosses the Boundary

### 4.1 Allowed Data Types

| Data Type | Crosses? | Form |
|-----------|----------|------|
| Shop drawing detail records | Yes | Canonical detail records |
| Validation rule definitions | Yes | Declarative rule sets |
| Validation results | Yes | Conformance records |
| Artifact metadata | Yes | Manifest entries (URIs to files, not files themselves) |
| Lineage records | Yes | Revision and approval chain records |
| Trade taxonomy | Yes | Standardized trade classification |
| Status enumerations | Yes | Mapped to OS vocabulary |
| Timestamps | Yes | Normalized to UTC ISO 8601 |

### 4.2 Prohibited Data Types

| Data Type | Crosses? | Reason |
|-----------|----------|--------|
| GCP user PII | No | Replaced with opaque actor tokens |
| GCP authentication credentials | No | Sovereignty violation |
| GCP internal IDs (as primary keys) | No | Creates coupling. Mapped to mirror-scoped IDs. |
| Raw file content | No | Out of scope. Referenced by URI only. |
| Financial data | No | Requires separate trust boundary |
| GCP configuration data | No | Internal concern |
| GCP audit logs | No | Sovereignty concern |

---

## 5. Trust Boundary Guarantees

### 5.1 Isolation Guarantee
No GCP-native data structure appears on the Construction OS side of the boundary. If a GCP-native field name, ID format, or enumeration value is found in a Construction OS data store, it is a trust boundary violation.

### 5.2 Severing Guarantee
The trust boundary can be severed (the mirror detached) without:
- Data loss on either side.
- Schema migration on the Construction OS side.
- Consumer-side code changes.
- Service interruption beyond the loss of fresh reflections.

### 5.3 Audit Guarantee
Every crossing event produces an audit log entry that includes:
- Crossing timestamp (UTC).
- Payload hash (for integrity verification).
- Source record identifier (GCP-side).
- Target record identifier (mirror-scoped).
- Transformation summary (what was mapped, what was dropped, what was flagged).

### 5.4 Idempotency Guarantee
Processing the same source record through the boundary multiple times produces the same result. There are no side effects from duplicate crossings.

---

## 6. Boundary Violation Response

If a trust boundary violation is detected:

1. **Immediate:** The violating record is quarantined. It does not enter Construction OS.
2. **Alert:** The platform team is notified with violation details.
3. **Investigation:** Root cause analysis determines whether the violation is a mediation bug, a GCP schema change, or a configuration error.
4. **Remediation:** The mediation layer is corrected. Quarantined records are reprocessed.
5. **Baseline update:** If the violation reveals a gap in the mediation rules, the schema transform is updated and the parity baseline is recalculated.

Boundary violations are treated as high-severity incidents. They indicate that the architectural guarantee of isolation has been breached.

---

## 7. Boundary Evolution

The trust boundary evolves when:
- New slices are activated (new data types cross the boundary).
- GCP changes its API schema (ingress-side transforms are updated).
- Construction OS changes its canonical format (egress-side transforms are updated).
- New exclusions are identified (additional data types are blocked).

All boundary changes are versioned and documented. The boundary configuration is stored in `mirror-manifest.yaml` and validated by the mirror activation checklist.
