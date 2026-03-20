# Exclusions: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Version:** 1.0.0
**Last Updated:** 2026-03-20

---

## Doctrine

> Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

---

## 1. Purpose of This Document

This document explicitly lists what the `gcp_shopdrawing` mirror does **not** reflect. Exclusions are not accidental omissions. Each item below has been deliberately excluded for a stated reason. If a capability is not listed in `scope.md` and not listed here, it is excluded by default.

Exclusions protect the mirror from scope creep, prevent entanglement with GCP's non-shop-drawing concerns, and enforce the detachability guarantee.

---

## 2. Categorical Exclusions

### 2.1 Billing and Financial Data

**Excluded:** All billing, invoicing, payment, cost tracking, budget, change order financial impact, and procurement financial data.

**Reason:** Financial data requires its own trust boundary, compliance controls, and audit trail. Mixing financial data with technical shop drawing data violates the principle of capability isolation. If financial reflections from GCP are needed, they require a separate mirror instance (e.g., `gcp_financials`).

**Specifically excluded:**
- Subcontractor payment applications tied to shop drawing milestones
- Cost codes associated with shop drawing packages
- Budget line items for submittal preparation
- Change order cost impacts from shop drawing revisions
- Material cost data embedded in shop drawing calculations

### 2.2 Tenant UI and Presentation Logic

**Excluded:** All GCP user interface components, presentation logic, UI state, user preferences, dashboard configurations, and rendering templates.

**Reason:** Presentation is an internal concern of each system. Construction OS maintains its own UI layer. Reflecting GCP's UI logic would create a hard-wired visual dependency, violating the detachability guarantee. No consumer should depend on how GCP displays information.

**Specifically excluded:**
- GCP dashboard widget configurations
- Drawing viewer settings and preferences
- Color coding schemes for review status
- User-customized views and filters
- Mobile app presentation logic
- Report templates and formatting

### 2.3 Authentication and Authorization

**Excluded:** All GCP authentication mechanisms, user identity records, access control lists, permission models, session management, and security tokens.

**Reason:** Identity and access control are sovereignty concerns. Each system manages its own identity. Sharing authentication creates a hard-wired dependency on GCP's identity provider. If GCP changes its auth model, that change must not propagate into Construction OS.

**Specifically excluded:**
- GCP user accounts and profiles
- Role-based access control (RBAC) configurations
- OAuth tokens and API keys (the sync agent uses its own credentials)
- Session cookies and state
- IP allowlists and network security rules
- Multi-factor authentication configurations
- SSO integration details

### 2.4 Customer Dashboard and Reporting

**Excluded:** GCP's customer-facing dashboards, analytics, reporting engines, and business intelligence configurations.

**Reason:** Reporting and analytics are consumer-side concerns. Construction OS generates its own reports from reflected data. GCP's reporting logic embeds assumptions about GCP's user base, licensing tiers, and feature flags that are irrelevant to Construction OS.

**Specifically excluded:**
- GCP analytics dashboard configurations
- Custom report definitions
- Scheduled report jobs
- Export templates and formatting
- KPI definitions and calculation logic
- Historical trend analysis configurations

### 2.5 Presentation Logic and Rendering

**Excluded:** All logic related to how shop drawings are rendered, displayed, annotated on-screen, zoomed, panned, or measured within GCP.

**Reason:** Drawing rendering is an implementation detail of GCP's viewer. Construction OS does not need to replicate GCP's viewer. If Construction OS displays shop drawings, it does so through its own rendering pipeline.

**Specifically excluded:**
- Drawing viewer engine and configuration
- Zoom, pan, and navigation state
- On-screen measurement tools and their calibration
- Overlay and comparison view logic
- Print layout and plotting configurations
- Watermark and stamp rendering logic

---

## 3. Operational Exclusions

### 3.1 GCP Internal Infrastructure

**Excluded:** All details of GCP's hosting, deployment, scaling, monitoring, and operational infrastructure.

**Reason:** Infrastructure is an internal concern. The mirror interacts with GCP through defined APIs. How GCP runs those APIs is opaque to the mirror.

**Specifically excluded:**
- Server and container configurations
- Database schemas and query patterns
- Caching layer configurations
- CDN and file storage infrastructure
- Load balancer and auto-scaling rules
- Deployment pipelines and CI/CD configurations
- Internal monitoring and alerting

### 3.2 GCP Internal Messaging

**Excluded:** GCP's internal event bus, message queues, notification systems, and pub/sub infrastructure.

**Reason:** Internal messaging is a coupling vector. If the mirror subscribed to GCP's internal events, it would be hard-wired to GCP's messaging infrastructure. The mirror uses its own sync agent to pull data at defined intervals.

**Specifically excluded:**
- Internal event topics and schemas
- Message queue configurations
- Notification routing rules
- Email notification templates
- Push notification configurations
- In-app notification state

### 3.3 GCP Internal Workflows

**Excluded:** GCP's internal workflow engine, state machines, business process definitions, and automation rules that are not shop-drawing-specific.

**Reason:** Workflow engines are deeply coupled to the host system's state model. Reflecting them would create entanglement. The mirror reflects workflow *outcomes* (e.g., approval decisions) but not workflow *engines*.

**Specifically excluded:**
- Workflow engine configuration
- State machine definitions
- Business process automation rules
- Trigger conditions and routing logic
- Escalation policies
- SLA enforcement rules

---

## 4. Data-Type Exclusions

### 4.1 Raw File Content

**Excluded:** The actual binary content of shop drawing files.

**Reason:** The mirror reflects metadata about artifacts, not the artifacts themselves. File storage, transfer, and access control are handled separately. The mirror provides URIs to files; it does not store or relay file content.

### 4.2 Personal Identifiable Information (PII)

**Excluded:** GCP user names, email addresses, phone numbers, and other PII beyond opaque actor identifiers.

**Reason:** PII requires specific data protection controls. The mirror uses opaque actor identifiers (e.g., `actor:gcp:a3f9b2c1`) that can be resolved through a separate identity mapping service when needed. PII never transits the mirror boundary.

### 4.3 Audit Logs

**Excluded:** GCP's internal audit logs, access logs, and security event logs.

**Reason:** Audit logs are a sovereignty concern. GCP's audit logs serve GCP's compliance needs. Construction OS maintains its own audit trail for data that crosses the trust boundary.

### 4.4 Configuration Data

**Excluded:** GCP project configurations, feature flags, tenant settings, and system administration data.

**Reason:** Configuration is an internal concern of GCP. The mirror adapts to GCP's behavior through its API surface, not by reading GCP's configuration.

---

## 5. Process Exclusions

### 5.1 Pre-Submission Processes

**Excluded:** All processes that occur before a shop drawing is formally submitted in GCP, including subcontractor drafting, internal QC reviews, and preliminary coordination.

**Reason:** Pre-submission activity is outside the scope of the managed shop drawing lifecycle. The mirror's scope begins at formal submission.

### 5.2 Post-Fabrication Processes

**Excluded:** All processes that occur after a shop drawing is released for fabrication, including field verification, as-built documentation, and closeout.

**Reason:** Post-fabrication activity enters different domains (field operations, closeout) that have their own data models and would require separate mirror slices if needed.

### 5.3 Procurement Processes

**Excluded:** Material procurement, purchase orders, vendor management, and supply chain logistics triggered by shop drawing approvals.

**Reason:** Procurement is a distinct domain with its own data model, compliance requirements, and system integrations. It requires its own mirror if needed.

---

## 6. Exclusion Governance

Exclusions are reviewed alongside scope changes. To move an item from excluded to in-scope:

1. Document the business justification.
2. Assess the entanglement risk. Would including this item create a hard-wired dependency?
3. Determine if the item belongs in this mirror or requires a separate mirror instance.
4. If appropriate, propose a new slice with its own activation criteria.
5. Update this document and `scope.md` together. They must remain consistent.

An exclusion can never be silently overridden. If data from an excluded category appears in the mirror's reflections, it is a trust boundary violation that triggers an immediate investigation.
