# Source System Profile: GCP (General Contractor Platform)

**Mirror ID:** `gcp_shopdrawing`
**Profile Version:** 1.0.0
**Last Updated:** 2026-03-20

---

## 1. System Identity

| Field | Value |
|-------|-------|
| System Name | GCP (General Contractor Platform) |
| System Type | Construction project management platform |
| Domain | Construction management |
| Subdomain (mirrored) | Shop drawing management |
| Operator | General contractor organization |
| Deployment Model | Cloud-hosted SaaS with on-premise gateway options |

---

## 2. System Overview

GCP is a construction project management platform used by general contractors to manage the lifecycle of construction projects. It covers a broad range of functions including project scheduling, cost management, document control, field operations, and subcontractor coordination.

This mirror reflects only the **shop drawing management** subdomain of GCP. The rest of GCP's capabilities are out of scope for this mirror instance. If other GCP capabilities need to be reflected into Construction OS, they will require separate mirror instances with their own trust boundaries.

---

## 3. Shop Drawing Capabilities

GCP's shop drawing management pipeline is a mature subsystem that handles the full lifecycle of shop drawings from initial submission by a subcontractor or supplier through final release to fabrication. The following describes the capabilities relevant to this mirror.

### 3.1 Drawing Ingestion

GCP accepts shop drawings in multiple formats from dozens of trades:

- **File formats:** PDF, DWG, DXF, DGN, RVT (Revit families), IFC, STEP, and raster images (PNG, TIFF) for legacy hand-drawn details.
- **Submission channels:** Direct upload through GCP web interface, email-to-project ingestion, API submission from subcontractor systems, bulk upload via FTP gateway.
- **Metadata extraction:** GCP extracts metadata from submitted drawings including title block information, revision numbers, scale, sheet size, and discipline classification. Extraction is a mix of OCR, template matching, and manual entry.

### 3.2 Detail Normalization

GCP normalizes shop drawing details across construction trades into a consistent internal representation:

- **Structural steel:** Connection details, member schedules, erection plans, anchor bolt layouts.
- **Mechanical (HVAC):** Ductwork fabrication details, equipment schedules, piping isometrics, control diagrams.
- **Electrical:** Panel schedules, one-line diagrams, conduit routing, fixture layouts, circuit schedules.
- **Plumbing:** Riser diagrams, fixture schedules, drainage plans, water distribution layouts.
- **Fire protection:** Sprinkler layouts, riser diagrams, hydraulic calculations, hanger details.
- **Architectural:** Curtain wall details, door and hardware schedules, finish schedules, millwork details.
- **Civil/Sitework:** Grading details, utility connections, paving sections, retaining wall details.

Normalization produces a canonical detail record that abstracts trade-specific conventions into a common structure with trade-specific extensions.

### 3.3 Rules Engine

GCP maintains a rules engine for validating shop drawings against:

- **Contract documents:** Design drawings, specifications, addenda, and change orders.
- **Building codes:** IBC, local amendments, ADA/accessibility requirements.
- **Industry standards:** AISC, ASHRAE, NFPA, NEC, UPC, and trade-specific standards.
- **Project-specific requirements:** Owner requirements, sustainability certifications (LEED, WELL), commissioning specifications.

Rules are organized by trade, severity (critical, major, minor, advisory), and applicability phase (submission, revision, final). GCP currently maintains approximately 2,400 active rules across all trades.

### 3.4 Validation Pipeline

When a shop drawing is submitted or revised, GCP runs it through a validation pipeline:

1. **Format validation:** File integrity, format compliance, resolution requirements.
2. **Metadata validation:** Required fields present, revision numbering correct, discipline classification valid.
3. **Content validation:** Rule engine evaluation against applicable rules.
4. **Cross-reference validation:** References to other drawings, specifications, and RFIs are valid.
5. **Conformance report generation:** A structured report detailing all findings.

### 3.5 Artifact Management

GCP tracks all shop drawing artifacts:

- **Drawing files:** The primary shop drawing files in their submitted and processed formats.
- **Supporting documents:** Calculations, material certifications, product data sheets, test reports.
- **Markups:** Reviewer annotations, redline markups, and correction requests.
- **Transmittals:** Formal transmittal documents for submittal packages.

Each artifact has a version history, format metadata, and a release state (draft, submitted, under_review, approved, approved_as_noted, revise_and_resubmit, rejected, released_for_fabrication).

### 3.6 Revision Lineage

GCP maintains a complete revision history for every shop drawing:

- **Revision chain:** Ordered sequence of revisions with timestamps and change descriptions.
- **Approval chain:** Who reviewed, what they decided, when, and their comments.
- **Change provenance:** What triggered each revision (reviewer markup, RFI response, design change, code violation).
- **Lineage graph:** Parent-child relationships between drawings when a drawing is split, merged, or superseded.

---

## 4. Data Characteristics

| Characteristic | Value |
|----------------|-------|
| Typical project volume | 500-10,000 shop drawings per project |
| Average drawing revisions | 2.3 revisions per drawing |
| Active rules | ~2,400 across all trades |
| Supported trades | 15+ construction trades |
| File format support | 10+ drawing formats |
| Typical sync payload | 50-500 records per sync cycle |
| Data freshness at source | Near real-time (minutes) |
| Historical depth available | Full project lifecycle |

---

## 5. API and Integration Surface

GCP exposes the following integration surface relevant to this mirror:

| Interface | Type | Notes |
|-----------|------|-------|
| Shop Drawing API | REST (JSON) | CRUD operations on shop drawing records |
| Rules Export API | REST (JSON) | Exports rule definitions in declarative format |
| Validation Results API | REST (JSON) | Retrieves validation results by drawing or batch |
| Artifact Registry API | REST (JSON) | Artifact metadata and download URLs |
| Lineage Query API | GraphQL | Traverses revision and approval lineage |
| Webhook Events | HTTP callbacks | Drawing submitted, reviewed, approved, released |

All APIs require OAuth 2.0 authentication with project-scoped tokens. Rate limits apply. The mirror's sync agent handles authentication and rate limiting transparently.

---

## 6. Data Quality Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Completeness | High | Core fields reliably populated. Optional fields vary by trade. |
| Consistency | Medium-High | Normalization handles most inconsistencies. Edge cases in legacy data. |
| Timeliness | High | Data updated within minutes of source events. |
| Accuracy | Medium-High | Metadata extraction accuracy ~94%. Manual corrections supplement. |
| Uniqueness | High | Strong deduplication in place. Revision chains prevent phantom duplicates. |

---

## 7. Known Limitations

1. **Legacy drawing formats.** Raster-only shop drawings (scanned hand-drawn details) have limited metadata extraction. These are flagged as `low_confidence` in normalization.
2. **Cross-project lineage.** GCP tracks lineage within a project but not across projects. If a detail is reused across projects, the lineage breaks at the project boundary.
3. **Rule versioning.** Rule definitions are versioned but historical validation results reference the rule version at time of evaluation. Retroactive re-evaluation is not automatic.
4. **Approval workflow variance.** Different projects configure different approval workflows. The rules for routing are project-specific and not fully generalizable.
5. **File size limits.** GCP enforces a 500MB per-file limit. Extremely large 3D model-based shop drawings may be split, affecting artifact integrity.

---

## 8. Relationship to Mirror

This source system profile describes GCP as it exists today. The mirror does not depend on these specifics. If GCP changes its internal architecture, API versions, or data model, the mirror's trust boundary absorbs the change through schema mediation. Construction OS consumers never see GCP's internals directly.

The profile is maintained for operational awareness, capacity planning, and drift investigation. It is not a binding specification.
