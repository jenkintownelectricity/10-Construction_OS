# Promotion Candidates: GCP Shop Drawing Mirror

> Reflections that have demonstrated sufficient maturity, stability, and generalizability
> to be considered for promotion from mirror-local reflection into Construction OS core.

## Promotion Philosophy

Promotion is not a reward; it is a recognition that a reflection has outgrown its
mirror-specific context and now serves a broader architectural purpose. A promoted
reflection ceases to be a mirror artifact and becomes a kernel primitive, subject to
kernel governance, versioning, and stability guarantees.

Promotion does NOT mean the mirror loses access. The mirror retains full access to
the promoted reflection through the standard kernel API surface. What changes is
ownership, maintenance burden, and the scope of breaking-change review.

---

## Promotion Criteria (All Must Be Met)

| # | Criterion | Threshold | Measurement |
|---|-----------|-----------|-------------|
| 1 | **Cross-mirror applicability** | Applicable to 2+ mirrors beyond GCP | Reviewed by kernel architecture team |
| 2 | **Schema stability** | No breaking schema changes in 90+ days | Schema changelog audit |
| 3 | **Test coverage** | 85%+ contract test pass rate across fixtures | Automated test suite |
| 4 | **Drift tolerance** | Drift score below 0.05 for 60+ consecutive days | Drift monitoring reports |
| 5 | **Zero trust violations** | No trust boundary violations in 120+ days | Trust boundary audit log |
| 6 | **Documentation completeness** | Full contract, schema, fixture, and rule docs | Documentation review |
| 7 | **Non-destructive detachability** | Can be extracted without breaking mirror integrity | Detachment dry-run test |

---

## Current Promotion Candidates

### Tier 1: Strong Candidates (Approaching Readiness)

#### 1. `detail_normalization` — Normalized Detail Schema

- **Status:** CANDIDATE_REVIEW
- **Readiness Score:** 78/100
- **Rationale:** The normalized detail schema addresses a universal problem across all
  construction mirrors: shop drawing details arrive in wildly different formats from
  different source systems. The normalization schema developed for GCP has proven
  stable for 6+ months and maps cleanly to detail formats from other systems including
  Procore, PlanGrid, and Bluebeam.
- **What would be promoted:** The `normalized-detail.schema.json` and the core
  normalization rule set (not GCP-specific field mappings).
- **Remaining gaps:**
  - Need cross-mirror fixture validation with at least 2 additional source systems
  - Rule set needs abstraction to remove GCP-specific field assumptions
  - Schema version needs to be frozen at a stable release candidate
- **Estimated readiness:** 30-45 days with focused effort

#### 2. `validation` — Validation Rule Framework

- **Status:** CANDIDATE_REVIEW
- **Readiness Score:** 72/100
- **Rationale:** The validation framework built for GCP shop drawings implements a
  generalizable pattern: schema-driven validation with pluggable rule sets, severity
  classification, and structured violation reporting. This pattern is needed by every
  mirror that ingests external data.
- **What would be promoted:** The validation framework scaffold (rule loader, severity
  classifier, violation reporter) — NOT the GCP-specific validation rules themselves.
- **Remaining gaps:**
  - Framework needs to be decoupled from GCP-specific rule format
  - Plugin interface needs formalization as a kernel contract
  - Performance benchmarks needed for rule sets exceeding 500 rules
  - Error taxonomy needs alignment with kernel-level error classification
- **Estimated readiness:** 45-60 days

### Tier 2: Potential Candidates (Needs More Maturation)

#### 3. `lineage` — Artifact Lineage Tracking

- **Status:** WATCHING
- **Readiness Score:** 55/100
- **Rationale:** Lineage tracking (knowing which source artifact produced which
  normalized output, through which rule application) is a universal concern. The
  lineage model developed for GCP captures parent-child relationships, transformation
  history, and provenance metadata.
- **What would be promoted:** The lineage data model and query interface.
- **Remaining gaps:**
  - Lineage model is still tightly coupled to GCP artifact types
  - No cross-mirror lineage has been tested (e.g., an artifact that crosses mirror boundaries)
  - Graph storage assumptions need abstraction
  - Performance under deep lineage chains (10+ levels) is untested
- **Estimated readiness:** 90+ days

#### 4. `artifact_manifest` — Artifact Manifest Structure

- **Status:** WATCHING
- **Readiness Score:** 48/100
- **Rationale:** The manifest structure that inventories all artifacts within a
  reflection slice has potential as a kernel primitive. Every mirror needs to track
  what artifacts exist, their states, and their relationships.
- **What would be promoted:** The manifest schema and state machine definitions.
- **Remaining gaps:**
  - Manifest schema still encodes GCP-specific artifact lifecycle states
  - State machine transitions need generalization
  - Conflict resolution strategy is GCP-specific
  - No formal comparison with manifest patterns in other mirrors
- **Estimated readiness:** 90-120 days

### Tier 3: Not Ready (Retain in Mirror)

#### 5. `rules_engine` — GCP-Specific Rules Engine

- **Status:** NOT_CANDIDATE
- **Readiness Score:** 25/100
- **Rationale:** While the rules engine is mature and well-tested within the GCP
  context, it is deeply coupled to GCP's data model, field naming conventions, and
  business logic. The engine itself is not generalizable — what IS generalizable is
  the validation framework it plugs into (see Tier 1, item 2).
- **Decision:** Retain as mirror-local. The generalizable parts are being promoted
  through the `validation` candidate instead.

---

## Staged Slices — Promotion Outlook

These slices are not yet active and therefore cannot be promotion candidates, but
their design should account for future promotability.

| Staged Slice | Promotion Potential | Notes |
|---|---|---|
| `governance` | HIGH | Governance patterns are inherently cross-cutting |
| `registry` | HIGH | Registry is a kernel-level concern by nature |
| `receipt_audit` | MEDIUM | Audit patterns are generalizable but GCP audit specifics are not |
| `artifact_generation` | LOW | Generation is deeply source-system-specific |
| `execution_orchestration` | MEDIUM | Orchestration patterns may generalize |
| `review_support` | LOW | Review workflows are highly partner-specific |
| `delivery_packaging` | MEDIUM | Packaging formats may standardize across mirrors |
| `standards_mapping` | HIGH | Standards (AISC, ACI, etc.) are universal |
| `spec_ingestion` | MEDIUM | Ingestion patterns generalize; field mappings do not |
| `submittal_analysis` | LOW | Submittal formats are partner-specific |

---

## Promotion Process

1. **Nomination** — Mirror maintainer or kernel architect files a promotion nomination
   with rationale, readiness score, and gap analysis.
2. **Cross-mirror review** — At least two other mirror maintainers review the candidate
   for applicability to their contexts.
3. **Extraction dry-run** — The candidate is extracted into a standalone package and
   tested in isolation to verify it functions without mirror-specific dependencies.
4. **Kernel integration test** — The extracted candidate is integrated into a kernel
   test environment and validated against kernel contracts.
5. **Promotion vote** — Kernel architecture team votes. Requires unanimous approval.
6. **Migration** — Candidate is moved from mirror space to kernel space. Mirror is
   updated to reference the kernel version. A 90-day backward-compatibility shim is
   maintained in the mirror.

---

## Promotion History

| Date | Reflection | Outcome | Notes |
|---|---|---|---|
| — | — | — | No promotions have occurred yet for this mirror |

---

## Review Schedule

- Promotion candidate review occurs quarterly.
- Next scheduled review: Q2 2026
- Review owner: Kernel Architecture Team
- Mirror representative: GCP Shop Drawing Mirror Maintainer
