# Mirror Validity Rules

## Purpose

These rules define the minimum conditions a mirror must satisfy to be considered valid. A mirror that violates any of these rules is INVALID and must not be in ACTIVE lifecycle state. Invalid mirrors must remain STAGED (or be frozen if already active) and **fail closed** — meaning they reject operations rather than operating in a degraded or ungoverned state.

These rules are non-negotiable. There are no exceptions, waivers, or temporary overrides. A mirror either satisfies all 12 rules or it is invalid.

---

## The 12 Invalidity Rules

### Rule 1: Manifest Missing or Invalid
**A mirror is INVALID if its manifest is missing, unparseable, or does not conform to the mirror-manifest.schema.json.**

The manifest is the mirror's identity document. Without a valid manifest, the mirror has no declared identity, no lifecycle state, no owner, and no governance context. A mirror without a manifest is an ungoverned artifact and must not operate.

**Detection:** Validate the manifest against mirror-manifest.schema.json using standard JSON Schema validation. Check for file existence, parse validity, and schema conformance.

**Consequence:** Mirror cannot transition to ACTIVE. If already ACTIVE, must be immediately frozen pending manifest remediation.

---

### Rule 2: Enabled Slices Not Declared
**A mirror is INVALID if it contains operational slices that are not declared in the manifest's enabled_slices array.**

Every slice must be declared. Undeclared slices are ungoverned — they have no status, no transfer class, no dependency information, and no governance oversight. An undeclared slice is a shadow capability that undermines the entire mirror governance model.

**Detection:** Compare the set of actually deployed/running slices against the manifest's enabled_slices list. Any slice present in the deployment but absent from the manifest is a violation.

**Consequence:** Undeclared slices must be either added to the manifest (with full metadata) or removed from the deployment.

---

### Rule 3: Slice Dependency Graph Missing or Invalid
**A mirror is INVALID if its slice dependency graph is missing, incomplete, or contains undeclared dependencies.**

The dependency graph is required for breakaway planning, promotion evaluation, and transfer gate assessment. Without it, the system cannot determine what breaks when a slice is removed, promoted, or transferred.

**Detection:** Verify that a dependency graph exists for the mirror. Validate that every node in the graph corresponds to a declared slice. Verify that every edge references valid slice_ids. Check for circular dependencies (which are a separate violation but detected here).

**Consequence:** Mirror cannot be ACTIVE until the dependency graph is complete and valid.

---

### Rule 4: Trust Boundary Undefined
**A mirror is INVALID if its trust boundary with Construction OS core is not defined and documented.**

The trust boundary is the fundamental isolation mechanism. Without a defined trust boundary, there is no governance over what data crosses between mirror and core, what operations are permitted, or what guarantees exist. An undefined trust boundary means the non-destructive guarantee cannot be enforced.

**Detection:** Check the manifest's trust_boundary field. Verify that the referenced trust boundary specification exists and contains definitions for at least data boundary and failure boundary types.

**Consequence:** Mirror must remain STAGED. No data flow between mirror and core is permitted until the trust boundary is defined.

---

### Rule 5: Reflection Status Missing
**A mirror is INVALID if its reflection status — the current state of what it is reflecting and whether that reflection is current, stale, or broken — is not tracked.**

A mirror that does not know whether its reflections are current is a mirror that might be serving stale or incorrect data without anyone knowing. Reflection status tracking is the minimum observability requirement.

**Detection:** Verify that the mirror maintains a reflection status record that is updated on a governance-defined schedule. Check that the status includes last-reflection timestamp, source version, and health indicator.

**Consequence:** Mirror may not serve reflections to consumers until reflection status tracking is operational.

---

### Rule 6: No Parity Fixtures Exist
**A mirror is INVALID if no parity fixtures exist for verifying that its reflections accurately match the source.**

Parity fixtures are the test infrastructure that proves a mirror works correctly. Without parity fixtures, there is no way to verify that the mirror's reflections are accurate, complete, and current. The mirror is operating on faith, not evidence.

**Detection:** Check for the existence of parity fixture files/configurations for the mirror. Verify that at least one fixture covers the primary reflection path. Verify that fixtures are executable and have been run at least once.

**Consequence:** Mirror may not transition to ACTIVE. Existing ACTIVE mirrors discovered without parity fixtures must be frozen.

---

### Rule 7: Drift Record Schema Missing
**A mirror is INVALID if it does not have a drift record schema defining how drift between source and reflection is measured, recorded, and reported.**

Drift is inevitable. The question is not whether a mirror will drift, but whether drift is detected and managed. Without a drift record schema, drift accumulates silently until it causes a failure or a governance crisis.

**Detection:** Verify that a drift record schema exists for the mirror. Check that the schema defines drift measurement methodology, recording format, severity thresholds, and escalation rules.

**Consequence:** Mirror must remain STAGED until drift record infrastructure is in place.

---

### Rule 8: Breakaway Conditions Missing
**A mirror is INVALID if its breakaway conditions — the circumstances under which the mirror should be separated from core — are not defined.**

Every mirror must be built with breakaway in mind. If the conditions for breakaway are not defined at chartering time, the mirror becomes a permanent dependency by default. This violates the fundamental principle that mirrors are separable.

**Detection:** Check the manifest for breakaway_conditions. Verify that at least one condition is declared with a description and, where applicable, a measurable threshold.

**Consequence:** Mirror may not transition beyond CHARTERED until breakaway conditions are defined.

---

### Rule 9: Truth Ownership Undefined
**A mirror is INVALID if the truth ownership for the data domains it touches is not defined in the truth ownership matrix.**

A mirror must know what it owns, what it reflects, and what it must never touch. Without truth ownership definitions, the mirror risks overwriting core truth, ignoring source truth, or accessing forbidden domains.

**Detection:** For each data domain the mirror interacts with, verify that a corresponding entry exists in truth-ownership-matrix.yaml. Verify that the mirror's access level is consistent with the declared ownership.

**Consequence:** Mirror may not process data in any domain where truth ownership is undefined.

---

### Rule 10: Contains Forbidden App-Local Logic
**A mirror is INVALID if it contains application-local logic that belongs in Construction OS core — including billing logic, tenant UI components, authentication/authorization logic, or core workflow engines.**

Mirrors reflect; they do not replicate core application functionality. Forbidden app-local logic in a mirror creates governance confusion, security risk, and makes breakaway destructive (because removing the mirror removes capabilities that should be in core).

**Detection:** Code and configuration review for the presence of billing modules, tenant UI frameworks, auth provider integrations, or core workflow definitions. Automated scanning for imports/dependencies on core-only packages.

**Consequence:** Forbidden logic must be removed from the mirror before it can be ACTIVE. If the logic is needed, it belongs in core and the mirror should consume it through governed channels.

---

### Rule 11: Lifecycle State Inconsistent with Evidence
**A mirror is INVALID if its declared lifecycle state does not match the evidence.**

A mirror claiming to be ACTIVE must have passing parity fixtures, current reflection status, valid drift records, and all slices in declared states. A mirror claiming to be STAGED must not be serving production traffic. A mirror claiming to be FROZEN must not be accepting new reflections. State must match reality.

**Detection:** For each lifecycle state, verify the conditions that define that state:
- PROPOSED: Charter exists, no deployment
- CHARTERED: Charter approved, manifest exists, no operational slices
- STAGED: Deployed in non-production, slices being validated
- ACTIVE: All validity rules pass, serving production reflections
- FROZEN: No new reflections, existing state preserved
- RETIRED: No operational components, archive exists

**Consequence:** The mirror must be transitioned to the state that matches its actual evidence, or the evidence must be brought into alignment with the declared state.

---

### Rule 12: Registry Entry Missing
**A mirror is INVALID if it does not have a corresponding entry in the central mirror registry.**

The registry is the system of record for all mirrors. A mirror without a registry entry is invisible to governance — it cannot be audited, reviewed, frozen, or broken away through standard processes. It is a ghost mirror.

**Detection:** Query the mirror registry for an entry matching the mirror's mirror_id. Verify that the registry entry is consistent with the manifest.

**Consequence:** Mirror must be registered before it can transition beyond PROPOSED.

---

## Enforcement

### Fail Closed Principle
When a validity rule is violated, the mirror **fails closed**. This means:
- It does not serve reflections to consumers
- It does not accept new data from sources
- It does not process pending operations
- It reports its invalid status through monitoring channels

Failing closed is safer than failing open. A mirror that fails open might serve incorrect data, violate trust boundaries, or create governance gaps.

### Continuous Validation
Validity rules are not checked once — they are checked continuously. A mirror that was valid yesterday may be invalid today if its parity fixtures were deleted, its drift records expired, or its manifest was corrupted. Continuous validation ensures that invalidity is detected promptly.

### Remediation Path
For each rule violation, the mirror owner must:
1. Acknowledge the violation
2. Identify the root cause
3. Implement the fix
4. Request revalidation
5. Receive governance confirmation before returning to ACTIVE

No self-certification is permitted. An independent governance review must confirm remediation.
