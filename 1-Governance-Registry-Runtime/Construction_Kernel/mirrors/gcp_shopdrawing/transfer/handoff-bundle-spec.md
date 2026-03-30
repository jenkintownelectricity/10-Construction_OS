# Handoff Bundle Specification — GCP Shop Drawing Mirror

> COMMAND E: Transfer / Buyout Doctrine
> MASTER DOCTRINE: Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

## Purpose

This document specifies exactly what a handoff bundle contains for transferable slices in the GCP Shop Drawing mirror. A handoff bundle is the complete deliverable package given to a buyer when a BUYOUT_READY or FULL_HANDOFF_READY slice is transferred. The bundle must be self-contained — the buyer must be able to build, test, deploy, and operate the slice using only the contents of the bundle, with no further access to the Construction OS platform.

Nothing implied. Nothing assumed. Everything explicit.

---

## Bundle Structure

Every handoff bundle follows the same directory structure regardless of which slice it contains. This consistency ensures buyers know exactly where to find everything and reduces onboarding friction.

```
{slice-name}-handoff-bundle-v{version}/
│
├── MANIFEST.json                    # Machine-readable bundle manifest
├── TRANSFER-CERTIFICATE.md          # Signed transfer certificate
├── README.md                        # Human-readable entry point
│
├── source/
│   ├── src/                         # Complete source code
│   ├── build/                       # Build configuration and scripts
│   ├── Dockerfile                   # Container build definition
│   ├── docker-compose.yml           # Local development environment
│   └── Makefile                     # Build and task automation
│
├── dependencies/
│   ├── lockfile                     # Pinned dependency versions
│   ├── vendor/                      # Vendored dependencies (if applicable)
│   ├── license-audit.json           # License compatibility audit results
│   └── dependency-graph.svg         # Visual dependency graph
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md              # System architecture overview
│   │   ├── component-diagram.svg    # Component relationship diagram
│   │   ├── data-flow.svg            # Data flow diagram
│   │   └── decisions/               # Architecture decision records
│   │       ├── ADR-001-*.md
│   │       ├── ADR-002-*.md
│   │       └── ...
│   ├── api/
│   │   ├── reference.md             # Complete API reference
│   │   ├── openapi.yaml             # OpenAPI specification (if HTTP API)
│   │   └── examples/                # Request/response examples
│   ├── configuration/
│   │   ├── reference.md             # Every configuration parameter
│   │   └── environments/            # Example configs for dev, staging, prod
│   ├── data-model/
│   │   ├── schema.md                # Data model documentation
│   │   ├── erd.svg                  # Entity-relationship diagram
│   │   └── migrations/              # Data migration scripts and docs
│   ├── domain/
│   │   ├── glossary.md              # Domain term definitions
│   │   └── business-rules.md        # Business rule documentation
│   └── developer/
│       ├── onboarding.md            # New developer onboarding guide
│       ├── contributing.md          # Code contribution guidelines
│       └── troubleshooting.md       # Common issues and solutions
│
├── tests/
│   ├── unit/                        # Unit test suite
│   ├── integration/                 # Integration test suite
│   ├── contract/                    # API contract tests
│   ├── detachment/                  # Detachment verification tests
│   ├── performance/
│   │   ├── benchmarks/              # Performance benchmark tests
│   │   ├── baselines/               # Baseline performance metrics
│   │   └── load-profiles/           # Load testing profiles
│   └── coverage-report/             # Test coverage reports
│
├── fixtures/
│   ├── normal/                      # Normal operation test data
│   │   ├── README.md                # What each fixture represents
│   │   └── *.json / *.dwg / ...    # Fixture files
│   ├── edge-cases/                  # Edge case test data
│   │   ├── README.md
│   │   └── *.json / *.dwg / ...
│   ├── failure-modes/               # Failure scenario test data
│   │   ├── README.md
│   │   └── *.json / *.dwg / ...
│   ├── performance/                 # Performance test data sets
│   │   └── ...
│   └── generation/                  # Scripts to regenerate fixtures
│       └── generate-fixtures.sh
│
├── operations/                      # (FULL_HANDOFF_READY only — included
│   ├── deployment/                  #  for BUYOUT_READY as basic guidance)
│   │   ├── procedure.md             # Step-by-step deployment
│   │   ├── infrastructure.md        # Infrastructure requirements
│   │   ├── automation/              # Deployment automation scripts
│   │   └── rollback.md              # Rollback procedures
│   ├── monitoring/
│   │   ├── metrics.md               # Key metrics and their meaning
│   │   ├── dashboards/              # Dashboard definitions (Grafana JSON, etc.)
│   │   ├── alerts.md                # Alert definitions and thresholds
│   │   └── health-checks.md        # Health check endpoint documentation
│   ├── runbooks/
│   │   ├── startup.md               # System startup procedure
│   │   ├── shutdown.md              # Graceful shutdown procedure
│   │   ├── scaling.md               # Scaling up and down
│   │   ├── backup-restore.md        # Backup and recovery
│   │   └── incident-response/       # Incident response playbooks
│   │       ├── high-latency.md
│   │       ├── data-corruption.md
│   │       ├── dependency-failure.md
│   │       ├── disk-full.md
│   │       └── certificate-expiry.md
│   └── maintenance/
│       ├── patching.md              # Dependency patching process
│       ├── capacity-planning.md     # Capacity planning guidance
│       └── eol-strategy.md          # End-of-life planning for dependencies
│
├── security/
│   ├── trust-boundary.md            # Trust boundary specification
│   ├── trust-boundary-diagram.svg   # Visual trust boundary
│   ├── auth-model.md                # Authentication and authorization model
│   ├── data-classification.md       # Data sensitivity classification
│   ├── encryption.md                # Encryption posture (at rest, in transit)
│   ├── security-assumptions.md      # Environment security assumptions
│   ├── vulnerability-history.md     # Past vulnerabilities and remediations
│   ├── penetration-test-report.md   # Most recent pen test results (FULL_HANDOFF_READY)
│   ├── residual-risks.md            # Accepted risks and rationale
│   └── compliance.md                # Applicable compliance requirements
│
├── provenance/
│   ├── ownership-lineage.md         # Who created what, when, under what terms
│   ├── contributor-agreements/      # IP assignment agreements
│   ├── third-party-notices.md       # Third-party license notices
│   └── change-history.md            # Significant change log
│
└── transition/                      # (FULL_HANDOFF_READY only)
    ├── plan.md                      # Transition timeline and phases
    ├── knowledge-transfer/
    │   ├── session-topics.md        # KT session topics and schedule
    │   └── materials/               # Training slide decks, recordings
    ├── shadowing/
    │   ├── shadow-plan.md           # Shadowing schedule and objectives
    │   └── checklist.md             # Shadow period completion checklist
    ├── graduation/
    │   ├── criteria.md              # What must be demonstrated for independence
    │   └── assessment-template.md   # Assessment form for graduation review
    └── escalation/
        ├── contacts.md              # Who to contact during transition
        ├── response-times.md        # Expected response times
        └── severity-definitions.md  # How to classify issue severity
```

---

## MANIFEST.json Specification

The bundle manifest is the machine-readable description of the bundle contents. It is used by automated tools to verify bundle completeness and integrity.

```json
{
  "bundle_format_version": "1.0",
  "slice_name": "string — the slice identifier",
  "slice_version": "string — semantic version of the slice",
  "transfer_class": "BUYOUT_READY | FULL_HANDOFF_READY",
  "bundle_created": "ISO 8601 timestamp",
  "bundle_created_by": "string — who generated the bundle",
  "platform_version": "string — Construction OS version at time of bundle creation",
  "mirror": "gcp_shopdrawing",

  "checksums": {
    "algorithm": "SHA-256",
    "files": {
      "source/src/...": "hex digest",
      "...": "..."
    }
  },

  "dependencies": {
    "direct_count": "integer",
    "transitive_count": "integer",
    "all_public": "boolean",
    "license_audit_passed": "boolean"
  },

  "tests": {
    "unit_count": "integer",
    "integration_count": "integer",
    "contract_count": "integer",
    "detachment_count": "integer",
    "performance_count": "integer",
    "all_passing": "boolean",
    "coverage_percentage": "float"
  },

  "l08_gate": {
    "transfer_class_declared": "boolean",
    "dependency_graph_bounded": "boolean",
    "no_hidden_platform_dependency": "boolean",
    "handoff_bundle_spec_exists": "boolean",
    "trust_boundary_documented": "boolean",
    "ownership_lineage_documented": "boolean",
    "detachment_test_passes": "boolean",
    "replacement_obligations_defined": "boolean",
    "security_assumptions_documented": "boolean",
    "all_gates_passed": "boolean"
  },

  "readiness_scores": {
    "dependency_audit": "0-3",
    "documentation_completeness": "0-3",
    "test_coverage": "0-3",
    "fixture_availability": "0-3",
    "operational_procedures": "0-3",
    "support_transition_plan": "0-3",
    "security_review": "0-3"
  }
}
```

---

## TRANSFER-CERTIFICATE.md Specification

The transfer certificate is the legal and governance document that authorizes the transfer. It is generated after all L0.8 Transfer Gate conditions are met and the buyout readiness checklist is completed.

```
TRANSFER CERTIFICATE

Certificate ID: [unique identifier]
Issue Date: [date]

SLICE IDENTIFICATION
  Name: [slice name]
  Version: [version]
  Mirror: GCP Shop Drawing
  Transfer Class: [BUYOUT_READY | FULL_HANDOFF_READY]

BUYER IDENTIFICATION
  Organization: [buyer name]
  Contact: [buyer contact]
  Agreement Reference: [link to transfer agreement]

L0.8 TRANSFER GATE CLEARANCE
  Gate clearance date: [date]
  Independent reviewer: [name]
  All 9 conditions: PASSED

BUNDLE VERIFICATION
  Bundle checksum: [SHA-256 of entire bundle]
  Bundle created: [date]
  Bundle verified by: [name]

SIGNATURES
  Construction OS authorized representative: ____________
  Buyer authorized representative: ____________
  Independent reviewer: ____________
  Governance authority: ____________
```

---

## Bundle Completeness Requirements by Transfer Class

### BUYOUT_READY Bundles Must Include

| Section | Required | Notes |
|---|---|---|
| MANIFEST.json | Yes | Complete and accurate |
| TRANSFER-CERTIFICATE.md | Yes | Signed by all parties |
| source/ | Yes | Complete, buildable source |
| dependencies/ | Yes | Pinned, audited, all public |
| docs/architecture/ | Yes | Overview and diagrams |
| docs/api/ | Yes | Complete API reference |
| docs/configuration/ | Yes | All parameters documented |
| docs/data-model/ | Yes | Schema and ERD |
| docs/domain/ | Yes | Glossary and business rules |
| docs/developer/ | Recommended | Onboarding guide at minimum |
| tests/unit/ | Yes | >= 80% coverage |
| tests/integration/ | Yes | All interactions tested |
| tests/contract/ | Yes | All API contracts |
| tests/detachment/ | Yes | Must all pass |
| tests/performance/ | Recommended | Baselines if available |
| fixtures/normal/ | Yes | Representative test data |
| fixtures/edge-cases/ | Yes | Boundary conditions |
| fixtures/failure-modes/ | Yes | Error scenarios |
| operations/deployment/ | Yes | Basic deployment guide |
| operations/monitoring/ | Yes | Key metrics and health checks |
| operations/runbooks/ | Recommended | Startup and shutdown at minimum |
| security/ | Yes | All security docs required |
| provenance/ | Yes | Complete ownership lineage |
| transition/ | No | Not required for BUYOUT_READY |

### FULL_HANDOFF_READY Bundles Must Include

Everything required for BUYOUT_READY, plus:

| Section | Required | Notes |
|---|---|---|
| docs/developer/ (all) | Yes | Full developer onboarding package |
| tests/performance/ | Yes | Benchmarks with baselines |
| fixtures/performance/ | Yes | Performance test data |
| fixtures/generation/ | Yes | Fixture regeneration scripts |
| operations/ (all) | Yes | Complete operational documentation |
| transition/ (all) | Yes | Full transition plan and materials |

---

## Slice-Specific Bundle Specifications

### Slice 11: Drawing Compliance Report Generator (BUYOUT_READY)

**Unique bundle requirements for this slice:**
- Compliance rule sets must be exported as standalone configuration files (not platform-dependent)
- Report templates must be included with all formatting assets (fonts, logos placeholder, CSS)
- Sample compliance reports must be included showing all report variants
- Rule set versioning documentation must explain how rules are updated independently

**Expected bundle size:** ~150 MB (including fixture drawings)
**Expected test count:** 47 unit + 23 integration + 12 contract + 8 detachment = 90 tests

---

### Slice 12: Material Takeoff Calculator (BUYOUT_READY)

**Unique bundle requirements for this slice:**
- Material database must be exported as a standalone database (SQLite or CSV)
- Unit conversion tables must be self-contained
- Trade-specific calculation rules must be documented per trade (structural steel, mechanical, electrical)
- Sample takeoff reports for each supported trade must be included

**Expected bundle size:** ~80 MB (including material database and fixture drawings)
**Expected test count:** 31 unit + 18 integration + 9 contract + 6 detachment = 64 tests

---

### Slice 13: Fabrication Data Exporter (FULL_HANDOFF_READY)

**Unique bundle requirements for this slice:**
- CNC code generator must include post-processor configurations for major machine brands
- Cut optimization algorithms must be documented with mathematical foundations
- Assembly sequence planner must include trade-specific assembly logic
- Machine-specific output format specifications must be included
- Safety validation rules for fabrication outputs must be thoroughly documented
- Training materials must include fabrication domain knowledge, not just software operation

**Expected bundle size:** ~500 MB (including CNC post-processors, fixture data, training materials)
**Expected test count:** 82 unit + 45 integration + 18 contract + 15 detachment + 12 performance = 172 tests

---

### Slice 14: Shop Drawing Validation Bundle (BUYOUT_READY)

**Unique bundle requirements for this slice:**
- This is a meta-bundle containing standalone forks of normalization, extraction, validation, and reporting
- Each sub-component must be independently buildable and testable within the bundle
- Integration tests must verify the full validation pipeline end-to-end
- Rule set export must include versioning and update procedures for standalone operation
- The bundle must include a CLI tool for running validations without any web infrastructure

**Expected bundle size:** ~300 MB (including all sub-components and fixture drawings)
**Expected test count:** 128 unit + 56 integration + 24 contract + 16 detachment = 224 tests

---

## Bundle Verification Process

Before a bundle is delivered to a buyer, it must pass automated verification:

### Step 1: Structural Verification
- Verify all required directories and files exist per transfer class
- Verify MANIFEST.json is valid and complete
- Verify all checksums match

### Step 2: Build Verification
- Clone the bundle to a clean environment with no platform access
- Execute the build using only the bundle contents
- Verify the build succeeds

### Step 3: Test Verification
- Run the complete test suite in the clean environment
- Verify all tests pass
- Verify coverage meets minimum thresholds

### Step 4: Documentation Verification
- Verify all documentation files are non-empty and well-formed
- Verify all diagrams render correctly
- Verify API documentation matches actual API behavior

### Step 5: Security Verification
- Scan for hardcoded secrets or credentials
- Verify no platform-internal URLs or endpoints
- Verify dependency vulnerability scan is current

### Verification Script

The bundle includes a self-verification script:

```bash
# Run from bundle root
./verify-bundle.sh

# Output:
# [PASS] Structural verification: all required files present
# [PASS] Build verification: build succeeded in clean environment
# [PASS] Test verification: 90/90 tests passed, 83% coverage
# [PASS] Documentation verification: all docs present and well-formed
# [PASS] Security verification: no secrets, no platform references
#
# BUNDLE VERIFICATION: PASSED
```

---

## Bundle Delivery

### Delivery Method
- Encrypted archive (AES-256) delivered via secure file transfer
- Decryption key delivered separately through a different channel
- Bundle checksum published in the transfer certificate

### Delivery Verification
- Buyer verifies the archive checksum against the transfer certificate
- Buyer decrypts and runs the self-verification script
- Buyer confirms receipt and verification in writing
- Transfer is considered complete when buyer confirms successful verification

---

## Document Metadata

| Field | Value |
|---|---|
| Command | E — Transfer / Buyout Doctrine |
| Mirror | GCP Shop Drawing |
| Status | Active |
| Classification | Technical Specification |
| Last Updated | 2026-03-20 |
