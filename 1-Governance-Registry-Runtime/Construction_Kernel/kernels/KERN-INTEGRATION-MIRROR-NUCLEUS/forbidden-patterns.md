# Forbidden Patterns

**Kernel:** KERN-INTEGRATION-MIRROR-NUCLEUS
**Version:** 1.0.0
**Authority:** Construction OS Platform Architecture
**Enforcement:** Mandatory — violations must fail execution

---

## Purpose

These patterns are explicitly prohibited within the Mirror Architecture. Any occurrence of a forbidden pattern must cause the relevant operation to fail. The activation gate checks for these patterns during mirror activation evaluation.

---

## Pattern Catalog

### FP-01: Raw Code Sync Between Systems

**Description:** Directly synchronizing source code, scripts, or executable logic between an external system and Construction OS. Mirrors reflect behavior through contracts, schemas, and fixtures — never through raw code transfer.

**Detection Method:** Scan for direct file copy operations, git submodule references to external repos, or code import paths that cross system boundaries.

**Consequence:** Mirror activation denied. Code sync mechanism must be removed and replaced with schema-mediated reflection.

---

### FP-02: Direct API Coupling Bypassing Mirror

**Description:** An external system calling Construction OS internal APIs directly, or Construction OS calling external system APIs without going through the mirror's contract layer. All integration must pass through mirror contracts.

**Detection Method:** API call graph analysis for direct cross-boundary calls that do not route through mirror contract interfaces.

**Consequence:** Mirror activation denied. Direct coupling must be replaced with mirror-mediated integration.

---

### FP-03: Mirror Containing Billing or Tenant UI

**Description:** Any billing logic, payment processing, subscription management, tenant management UI, or multi-tenancy administration code present inside a mirror. These are core platform concerns that must never exist in mirrors.

**Detection Method:** Content scan for billing-related schemas, payment processing logic, tenant management interfaces, or subscription lifecycle code.

**Consequence:** Mirror activation denied. Forbidden logic must be removed entirely.

---

### FP-04: Mirror Importing Application UX Logic

**Description:** A mirror containing frontend UI components, user experience flows, dashboard rendering, or presentation logic. Mirrors are backend integration seams — they do not render UI.

**Detection Method:** Scan for UI framework imports, component definitions, template files, or CSS/styling artifacts within mirror directories.

**Consequence:** Mirror activation denied. UX logic must be removed.

---

### FP-05: ACTIVE Slice with Undeclared Dependencies

**Description:** A slice that is marked ACTIVE but has dependencies on other slices or external systems that are not declared in its slice definition or the dependency graph. Undeclared dependencies create hidden coupling.

**Detection Method:** Static analysis of slice inputs/outputs against declared dependency graph. Runtime monitoring for undeclared cross-slice calls.

**Consequence:** Slice must be disabled or dependencies must be declared. Mirror activation denied if any active slice has undeclared dependencies.

---

### FP-06: ACTIVE Mirror Without Parity Fixtures

**Description:** A mirror that is marked ACTIVE but has no parity fixtures for one or more of its active slices. Without fixtures, there is no way to verify that the mirror correctly reflects source system behavior.

**Detection Method:** Fixture directory scan per active slice. Minimum 3 fixtures per slice required.

**Consequence:** Mirror activation denied. Fixtures must be created before activation.

---

### FP-07: Transfer-Ready Slice Without Detachment Validation

**Description:** A slice marked as `BUYOUT_READY` or `FULL_HANDOFF_READY` that has not passed a detachment test. Transfer readiness without detachment validation creates risk of failed handoff.

**Detection Method:** Cross-reference transfer registry against detachment test results.

**Consequence:** Transfer readiness revoked. Detachment test must be executed and passed.

---

### FP-08: Mirror Logic Promoted Into Core Without Gate Review

**Description:** Any reflection, schema, contract, or rule that has been moved from a mirror into Construction OS core without passing through the promotion gate review process. Ungated promotion contaminates the core.

**Detection Method:** Audit trail check for promotion gate record. Diff analysis between core and mirror for duplicated artifacts without promotion records.

**Consequence:** Promoted logic must be quarantined until gate review is completed. If review fails, logic must be reverted from core.

---

### FP-09: Mirror Treated as Canonical Core by Accident

**Description:** Other systems or processes referencing mirror data or logic as if it were canonical Construction OS truth. Mirrors reflect — they do not originate. Core truth lives in Construction OS core, not in mirrors.

**Detection Method:** Reference analysis for inbound dependencies that treat mirror as source of truth. Configuration audit for canonical path references.

**Consequence:** References must be redirected to canonical core sources. Mirror must not be used as a source of truth.

---

### FP-10: Undocumented Fallback Paths

**Description:** Any fallback behavior that activates when a mirror or slice fails but is not documented in the mirror's operational documentation. Hidden fallbacks create unpredictable behavior during failures.

**Detection Method:** Code analysis for exception handlers, fallback routes, or default behaviors that are not documented in operational docs.

**Consequence:** Fallback paths must be documented or removed. Mirror activation denied if undocumented fallbacks are detected.

---

## Enforcement

- The activation gate checks for all 10 forbidden patterns during every activation evaluation.
- Forbidden pattern detection is also run during parity reviews and drift assessments.
- Any new forbidden pattern identified through operational experience must be added to this catalog through the standard kernel amendment process.
- There are no exceptions or waivers for forbidden patterns.

---

## Related Documents

- [Mirror Validity Rules](mirror-validity-rules.md)
- [Activation Policy](../../docs/architecture/mirror-activation-policy.md)
- [Doctrine](doctrine.md)
