# Slice Transfer Matrix — GCP Shop Drawing Mirror

> COMMAND E: Transfer / Buyout Doctrine
> MASTER DOCTRINE: Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

## Purpose

This document provides the authoritative transfer classification for every slice in the GCP Shop Drawing mirror. Each of the 15 slices is assigned exactly one transfer class, with a current readiness status against the L0.8 Transfer Gate conditions. This matrix governs what can be sold, licensed, white-labeled, or fully transferred from this mirror.

---

## Transfer Classes Reference

| Class | Code | Summary |
|---|---|---|
| NON_TRANSFERABLE | NT | Cannot leave the platform. Core governance and registry functions. |
| LICENSE_ONLY | LO | Can be licensed for use. IP and control remain with Construction OS. |
| WHITE_LABELABLE | WL | Can be rebranded by partner. Underlying engine remains Construction OS. |
| BUYOUT_READY | BR | Can be purchased outright after all L0.8 gate conditions are met. |
| FULL_HANDOFF_READY | FH | Complete transfer including source, docs, tests, fixtures, and support transition. |

---

## The 15 Slices — Transfer Matrix

### Overview Table

| # | Slice Name | Transfer Class | Readiness Status | Gate Score | Notes |
|---|---|---|---|---|---|
| 1 | Drawing Ingestion Gateway | NT | N/A | N/A | Core platform function — handles intake routing |
| 2 | Format Normalization Engine | LO | Ready | 7/7 | Converts diverse drawing formats to canonical form |
| 3 | Dimensional Extraction Pipeline | LO | Ready | 7/7 | Extracts dimensions, tolerances, and measurements |
| 4 | Specification Cross-Reference Engine | LO | In Progress | 5/7 | Cross-checks drawings against project specifications |
| 5 | Compliance Validation Rules Engine | LO | Ready | 7/7 | Validates drawings against code and standard requirements |
| 6 | Trade-Specific Annotation Processor | WL | In Progress | 4/7 | Processes trade-specific markups and annotations |
| 7 | Revision Comparison Engine | WL | Ready | 7/7 | Compares drawing revisions and highlights changes |
| 8 | Submittal Package Assembler | WL | In Progress | 5/7 | Assembles drawings into submittal packages |
| 9 | Review Workflow Coordinator | NT | N/A | N/A | Orchestrates multi-party review — platform-bound |
| 10 | Comment and Markup Aggregator | WL | Ready | 7/7 | Aggregates review comments from multiple reviewers |
| 11 | Drawing Compliance Report Generator | BR | In Progress | 6/9 | Generates compliance reports for drawing sets |
| 12 | Material Takeoff Calculator | BR | In Progress | 5/9 | Calculates material quantities from shop drawings |
| 13 | Fabrication Data Exporter | FH | Not Started | 2/9 | Exports fabrication-ready data packages |
| 14 | Shop Drawing Validation Bundle | BR | In Progress | 7/9 | Bundled validation capability for standalone use |
| 15 | Mirror Trust Anchor | NT | N/A | N/A | Trust chain root for the GCP mirror — never transfers |

---

## Detailed Slice Profiles

### Slice 1: Drawing Ingestion Gateway

| Field | Value |
|---|---|
| Transfer Class | NON_TRANSFERABLE |
| Rationale | This slice is the entry point for all drawings into the platform. It handles authentication, rate limiting, format detection, and routing to downstream processing slices. Removing it would break the entire mirror's intake pipeline. It is structurally coupled to the platform bus and registry. |
| Dependencies | Platform bus, registry identity service, format detection library |
| Readiness Status | N/A — not eligible for transfer |

---

### Slice 2: Format Normalization Engine

| Field | Value |
|---|---|
| Transfer Class | LICENSE_ONLY |
| Rationale | Converts DWG, DXF, PDF, and IFC files to a canonical internal format. The conversion logic is valuable IP that should not be transferred, but can be offered as a service. Partners benefit from calling it without needing to own or maintain the complex format handling. |
| Dependencies | LibreCAD libraries (open source), internal format spec, PDF parsing libraries |
| L0.8 Gate Status | All 7 LICENSE_ONLY criteria met |
| API Surface | `POST /normalize` — accepts drawing file, returns canonical format |
| Licensing Model | Usage-based: $0.25 per normalization |

---

### Slice 3: Dimensional Extraction Pipeline

| Field | Value |
|---|---|
| Transfer Class | LICENSE_ONLY |
| Rationale | Extracts precise dimensions, tolerances, and spatial relationships from normalized drawings. Uses proprietary extraction algorithms that represent significant R&D investment. High value as a licensed service; transfer would undermine platform differentiation. |
| Dependencies | Geometry processing library, unit conversion library, canonical format spec |
| L0.8 Gate Status | All 7 LICENSE_ONLY criteria met |
| API Surface | `POST /extract-dimensions` — accepts canonical drawing, returns dimension set |
| Licensing Model | Usage-based: $0.50 per extraction |

---

### Slice 4: Specification Cross-Reference Engine

| Field | Value |
|---|---|
| Transfer Class | LICENSE_ONLY |
| Rationale | Cross-references drawing elements against project specifications to identify mismatches, missing items, and compliance gaps. The rule sets are continuously updated and represent ongoing domain expertise investment. |
| Dependencies | Specification parser, rule set database, canonical format spec |
| L0.8 Gate Status | 5 of 7 criteria met — outstanding: rule set documentation incomplete, edge case test coverage at 65% |
| Blocking Items | Complete rule set documentation; increase edge case test coverage to 80% |
| API Surface | `POST /cross-reference` — accepts drawing + spec set, returns match report |
| Licensing Model | Subscription: $3,000/month Professional tier |

---

### Slice 5: Compliance Validation Rules Engine

| Field | Value |
|---|---|
| Transfer Class | LICENSE_ONLY |
| Rationale | Validates drawings against building codes, industry standards (AISC, ACI, AWS), and project-specific requirements. The validation rule library is a core competitive advantage and is continuously expanded. Licensing allows broad market access without IP exposure. |
| Dependencies | Rule set library, code database, validation framework |
| L0.8 Gate Status | All 7 LICENSE_ONLY criteria met |
| API Surface | `POST /validate` — accepts drawing + rule set selector, returns validation report |
| Licensing Model | Subscription: $5,000/month Professional tier |

---

### Slice 6: Trade-Specific Annotation Processor

| Field | Value |
|---|---|
| Transfer Class | WHITE_LABELABLE |
| Rationale | Processes annotations specific to individual trades (structural steel, mechanical, electrical, plumbing). Partners serving specific trades want their own branding on the annotation tools. The processing engine is shared; the presentation is customizable. |
| Dependencies | Annotation parsing library, trade-specific vocabularies, rendering engine |
| L0.8 Gate Status | 4 of 7 criteria met — outstanding: HVAC trade vocabulary incomplete, rendering customization surface not fully documented, integration tests at 70% |
| Blocking Items | Complete HVAC vocabulary; document all customization points; increase integration test coverage to 90% |
| Customization Surface | Logo, color scheme, annotation labels, trade terminology mapping |

---

### Slice 7: Revision Comparison Engine

| Field | Value |
|---|---|
| Transfer Class | WHITE_LABELABLE |
| Rationale | Compares two drawing revisions and produces a visual and data-level difference report. Partners want to present this capability with their own branding in their drawing management products. The comparison algorithm is the engine; the report presentation is the skin. |
| Dependencies | Geometry comparison library, visual diff renderer, report template engine |
| L0.8 Gate Status | All 7 WHITE_LABELABLE criteria met |
| Customization Surface | Report header/footer, color coding for additions/deletions/modifications, terminology, export format preferences |

---

### Slice 8: Submittal Package Assembler

| Field | Value |
|---|---|
| Transfer Class | WHITE_LABELABLE |
| Rationale | Assembles individual drawings into organized submittal packages with cover sheets, table of contents, and specification cross-references. Partners serving GCs and subcontractors want their branding on the assembled packages. |
| Dependencies | PDF assembly library, template engine, specification reference database |
| L0.8 Gate Status | 5 of 7 criteria met — outstanding: cover sheet template customization not fully tested, integration with external document management systems not verified |
| Blocking Items | Complete cover sheet template testing; verify DMS integration patterns |
| Customization Surface | Cover sheet design, table of contents format, branding elements, numbering scheme |

---

### Slice 9: Review Workflow Coordinator

| Field | Value |
|---|---|
| Transfer Class | NON_TRANSFERABLE |
| Rationale | Orchestrates the multi-party review process including assignment, deadline tracking, approval chains, and conflict resolution. This slice is deeply integrated with the platform's identity, notification, and governance systems. It cannot function outside the platform. |
| Dependencies | Platform identity service, notification bus, governance engine, state machine framework |
| Readiness Status | N/A — not eligible for transfer |

---

### Slice 10: Comment and Markup Aggregator

| Field | Value |
|---|---|
| Transfer Class | WHITE_LABELABLE |
| Rationale | Aggregates comments and markups from multiple reviewers into a consolidated view with conflict detection and resolution suggestions. Partners want their own interface around this aggregation capability. |
| Dependencies | Comment parsing library, conflict detection engine, markup normalization |
| L0.8 Gate Status | All 7 WHITE_LABELABLE criteria met |
| Customization Surface | Comment display format, conflict visualization, reviewer identity presentation, export templates |

---

### Slice 11: Drawing Compliance Report Generator

| Field | Value |
|---|---|
| Transfer Class | BUYOUT_READY |
| Rationale | Generates detailed compliance reports for drawing sets, including pass/fail status, deficiency descriptions, and remediation recommendations. This is a standalone capability that produces high-value output. A buyer in the compliance consulting space could operate this independently. |
| Dependencies | Report template engine, PDF generation library, compliance rule interpreter |
| L0.8 Gate Status | 6 of 9 conditions met |

**L0.8 Transfer Gate Progress:**

| # | Condition | Status | Notes |
|---|---|---|---|
| 1 | Transfer class declared | PASS | `transfer_class: BUYOUT_READY` in manifest |
| 2 | Dependency graph bounded | PASS | 12 direct, 34 transitive — all public |
| 3 | No hidden platform dependency | PASS | Detachment scan clean |
| 4 | Handoff bundle spec exists | FAIL | Bundle spec drafted, not reviewed |
| 5 | Trust boundary documented | PASS | Trust boundary diagram complete |
| 6 | Ownership lineage documented | PASS | Full provenance chain documented |
| 7 | Detachment test passes | FAIL | 3 of 47 tests fail in isolated environment |
| 8 | Replacement obligations defined | PASS | Construction OS will use Slice 5 output directly |
| 9 | Security assumptions documented | FAIL | Encryption assumptions not yet documented |

---

### Slice 12: Material Takeoff Calculator

| Field | Value |
|---|---|
| Transfer Class | BUYOUT_READY |
| Rationale | Calculates material quantities from shop drawings for specific trades. Self-contained calculation logic with bounded inputs and outputs. Valuable as a standalone tool for estimating firms. |
| Dependencies | Geometry measurement library, material database, unit conversion library |
| L0.8 Gate Status | 5 of 9 conditions met |

**L0.8 Transfer Gate Progress:**

| # | Condition | Status | Notes |
|---|---|---|---|
| 1 | Transfer class declared | PASS | `transfer_class: BUYOUT_READY` in manifest |
| 2 | Dependency graph bounded | PASS | 8 direct, 21 transitive — all public |
| 3 | No hidden platform dependency | PASS | Detachment scan clean |
| 4 | Handoff bundle spec exists | FAIL | Not started |
| 5 | Trust boundary documented | FAIL | Not started |
| 6 | Ownership lineage documented | PASS | Full provenance chain documented |
| 7 | Detachment test passes | PASS | All 31 tests pass in isolated environment |
| 8 | Replacement obligations defined | FAIL | Not yet determined what Construction OS replaces with |
| 9 | Security assumptions documented | FAIL | Not started |

---

### Slice 13: Fabrication Data Exporter

| Field | Value |
|---|---|
| Transfer Class | FULL_HANDOFF_READY |
| Rationale | Exports fabrication-ready data packages (CNC programs, cut lists, assembly sequences) from validated shop drawings. This is a highly specialized capability that a fabrication technology company could operate and evolve independently. Full handoff including operational support is the appropriate transfer model. |
| Dependencies | CNC code generator, cut optimization library, assembly sequence planner, material database |
| L0.8 Gate Status | 2 of 9 conditions met |

**L0.8 Transfer Gate Progress:**

| # | Condition | Status | Notes |
|---|---|---|---|
| 1 | Transfer class declared | PASS | `transfer_class: FULL_HANDOFF_READY` in manifest |
| 2 | Dependency graph bounded | PASS | 15 direct, 42 transitive — 2 require platform replacement |
| 3 | No hidden platform dependency | FAIL | 2 dependencies on platform metric service |
| 4 | Handoff bundle spec exists | FAIL | Not started |
| 5 | Trust boundary documented | FAIL | Not started |
| 6 | Ownership lineage documented | FAIL | Partial — 3 contributors missing IP assignments |
| 7 | Detachment test passes | FAIL | Not yet attempted |
| 8 | Replacement obligations defined | FAIL | Not started |
| 9 | Security assumptions documented | FAIL | Not started |

---

### Slice 14: Shop Drawing Validation Bundle

| Field | Value |
|---|---|
| Transfer Class | BUYOUT_READY |
| Rationale | A pre-packaged bundle combining format normalization, dimensional extraction, compliance validation, and report generation into a standalone validation system. Designed specifically for buyout — all components are self-contained versions of the platform capabilities. |
| Dependencies | Bundled: normalization engine (standalone fork), dimension extractor (standalone fork), validation rules (exported snapshot), report generator |
| L0.8 Gate Status | 7 of 9 conditions met |

**L0.8 Transfer Gate Progress:**

| # | Condition | Status | Notes |
|---|---|---|---|
| 1 | Transfer class declared | PASS | `transfer_class: BUYOUT_READY` in manifest |
| 2 | Dependency graph bounded | PASS | All dependencies bundled |
| 3 | No hidden platform dependency | PASS | Fully standalone verified |
| 4 | Handoff bundle spec exists | PASS | Complete and reviewed |
| 5 | Trust boundary documented | PASS | Trust boundary diagram complete |
| 6 | Ownership lineage documented | PASS | Full provenance documented |
| 7 | Detachment test passes | PASS | All 128 tests pass in isolated environment |
| 8 | Replacement obligations defined | FAIL | Document not yet signed off |
| 9 | Security assumptions documented | FAIL | Draft exists, not reviewed |

---

### Slice 15: Mirror Trust Anchor

| Field | Value |
|---|---|
| Transfer Class | NON_TRANSFERABLE |
| Rationale | The trust chain root for the GCP Shop Drawing mirror. Manages mirror identity, validates slice authenticity, and enforces governance rules within the mirror boundary. This is the mirror itself — it cannot be transferred without destroying the mirror. |
| Dependencies | Platform trust chain, certificate infrastructure, governance engine |
| Readiness Status | N/A — not eligible for transfer |

---

## Summary Statistics

| Transfer Class | Count | Ready | In Progress | Not Started |
|---|---|---|---|---|
| NON_TRANSFERABLE | 3 | N/A | N/A | N/A |
| LICENSE_ONLY | 4 | 3 | 1 | 0 |
| WHITE_LABELABLE | 4 | 2 | 2 | 0 |
| BUYOUT_READY | 3 | 0 | 3 | 0 |
| FULL_HANDOFF_READY | 1 | 0 | 0 | 1 |
| **Total** | **15** | **5** | **6** | **1** |

**Commercially Available Now:** 5 slices (3 LICENSE_ONLY, 2 WHITE_LABELABLE)
**Near-Ready (1-2 blocking items):** 4 slices
**Significant Work Remaining:** 2 slices

---

## Document Metadata

| Field | Value |
|---|---|
| Command | E — Transfer / Buyout Doctrine |
| Mirror | GCP Shop Drawing |
| Status | Active |
| Classification | Commercial / Technical |
| Last Updated | 2026-03-20 |
