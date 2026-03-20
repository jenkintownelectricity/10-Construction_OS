# Transfer Model

## Definition

**Transfer** is the controlled handoff of capability slices from Construction OS (via a mirror) to an external party. Transfer acknowledges that some capabilities, once proven and isolated, may need to leave the Construction OS ecosystem entirely — whether through licensing, white-labeling, acquisition, or full operational handoff.

Transfer is the most externally consequential lifecycle event. Unlike breakaway (which retires a mirror) or promotion (which absorbs into core), transfer moves capability outward. This demands the highest level of governance rigor because transferred capabilities leave Construction OS control.

---

## The 5 Transfer Classes

Every capability slice in a mirror must be assigned a transfer class. The transfer class determines what forms of external handoff are permitted. Transfer class is declared at chartering time and may only be changed through a governance review.

### Class 1: NON_TRANSFERABLE
**Definition:** The slice contains core governance logic, foundational schemas, or architectural primitives that are integral to Construction OS identity. It cannot leave the ecosystem under any circumstances.

**Examples:** Core ontology definitions, governance rule engines, kernel specifications, trust boundary enforcement logic.

**Constraints:** No external party may receive, license, or operate this capability. Transfer requests for NON_TRANSFERABLE slices are automatically rejected.

### Class 2: LICENSE_ONLY
**Definition:** The slice may be made available to external parties under a license agreement, but intellectual property is retained by Construction OS. The external party receives usage rights, not ownership.

**Examples:** Normalization rule libraries, validation schemas, reporting templates.

**Constraints:** Source code and implementation details remain Construction OS property. The licensee receives compiled/packaged artifacts or API access. Modification rights are not granted unless explicitly specified in the license. The license is revocable under terms defined in the agreement.

### Class 3: WHITE_LABELABLE
**Definition:** The slice may be rebranded and presented by an external party under their own identity. Construction OS IP is embedded but not visible to end users.

**Examples:** Detail sheet generators, compliance checkers, visualization components.

**Constraints:** The external party may apply their own branding, naming, and UI treatment. However, they may not modify the underlying logic without approval. Construction OS retains IP ownership. White-label agreements must specify attribution requirements (even if attribution is non-public). Update and maintenance obligations must be defined.

### Class 4: BUYOUT_READY
**Definition:** The slice has been designed and documented such that full intellectual property transfer is possible. An external party may acquire complete ownership, including source code, schemas, documentation, and all associated artifacts.

**Examples:** Partner-specific integration adapters, specialized domain modules built for a specific market segment.

**Constraints:** Buyout-ready slices must pass all 9 transfer gate conditions before transfer. The slice must be fully detachable — no hidden dependencies on core that would break after transfer. Post-transfer support obligations must be defined and time-bounded. Construction OS retains the right to maintain a fork for internal use unless explicitly waived.

### Class 5: FULL_HANDOFF_READY
**Definition:** The slice is prepared for complete transfer including not just IP but also operational responsibility — infrastructure, monitoring, support, SLAs, and customer relationships (if applicable).

**Examples:** Entire mirror stacks built for a partner who will eventually self-operate, dedicated integration environments.

**Constraints:** This is the most comprehensive transfer class. In addition to all BUYOUT_READY requirements, the receiving party must demonstrate operational readiness. A handoff plan covering infrastructure, monitoring, incident response, and escalation must be agreed upon. A parallel-run period is required before full handoff.

---

## Transfer Class Hierarchy

```
NON_TRANSFERABLE (most restrictive)
  └── LICENSE_ONLY
        └── WHITE_LABELABLE
              └── BUYOUT_READY
                    └── FULL_HANDOFF_READY (least restrictive)
```

A slice may only be transferred at or below its declared class. A LICENSE_ONLY slice cannot be transferred as BUYOUT_READY without a governance-approved class change.

---

## The 9 Gate Conditions for BUYOUT and FULL_HANDOFF

For BUYOUT_READY and FULL_HANDOFF_READY transfers, all 9 gate conditions must be satisfied. LICENSE_ONLY and WHITE_LABELABLE transfers require gates 1-5 only.

### Gate 1: Transfer Class Declared
The slice must have a declared transfer class in its manifest. The class must have been assigned during chartering or updated through a governance review. Undeclared slices cannot be transferred.

### Gate 2: Dependency Graph Bounded
The complete dependency graph of the slice must be documented and bounded. Every dependency must be identified, classified (core vs. mirror vs. external), and its transfer implications documented.

### Gate 3: No Hidden Dependencies
An independent verification must confirm that no undeclared dependencies exist. This means running the slice in an isolated environment and confirming it functions without access to any undeclared services, data sources, or libraries.

### Gate 4: Handoff Bundle Specification Exists
A formal handoff bundle specification must define exactly what the receiving party will receive: source code, compiled artifacts, documentation, test suites, configuration, schemas, sample data, and operational runbooks.

### Gate 5: Trust Boundary Documented
The trust boundary between the slice and Construction OS must be fully documented, including what data crosses the boundary, what operations are permitted, and what guarantees each side provides. Post-transfer, the receiving party inherits the external side of this boundary.

### Gate 6: Ownership Lineage Documented
The complete ownership history of the slice must be documented: who created it, who modified it, who reviewed it, what IP went into it, and whether any third-party IP is embedded. This protects both parties in the transfer.

### Gate 7: Detachment Test Passes
The slice must pass a detachment test: it is deployed in a clean environment with no access to Construction OS infrastructure, and it must function correctly. This proves that the transfer will result in a working capability for the receiving party.

### Gate 8: Replacement Obligations Defined
If Construction OS currently depends on the slice (e.g., other mirrors consume it), a replacement plan must be defined and approved. Transfer cannot orphan internal consumers.

### Gate 9: Security Assumptions Documented
All security assumptions embedded in the slice must be documented: authentication mechanisms, encryption expectations, data classification levels, access control models, and any security dependencies on Construction OS infrastructure that the receiving party must replicate.

---

## Transfer Process

### Phase 1: Transfer Request
An external party or internal stakeholder requests transfer of a specific slice. The request must identify the slice, the receiving party, the desired transfer class, and the business rationale.

### Phase 2: Eligibility Check
The slice's declared transfer class is compared against the requested transfer. If the request exceeds the declared class, a governance review for class change must occur first.

### Phase 3: Gate Evaluation
Each applicable gate is formally evaluated. For BUYOUT and FULL_HANDOFF, all 9 gates. For LICENSE_ONLY and WHITE_LABELABLE, gates 1-5.

### Phase 4: Agreement
Legal and business terms are formalized in a transfer agreement. This includes IP terms, support obligations, liability boundaries, and confidentiality requirements.

### Phase 5: Bundle Preparation
The handoff bundle is assembled per the specification from Gate 4. The bundle is verified for completeness and integrity.

### Phase 6: Transfer Execution
The bundle is delivered to the receiving party. For FULL_HANDOFF, this includes a parallel-run period where both parties operate the capability simultaneously.

### Phase 7: Verification
The receiving party confirms they can operate the capability independently. For FULL_HANDOFF, this includes passing an operational readiness review.

### Phase 8: Registry Recording
The transfer event is recorded in the mirror registry with: slice_id, transfer class, receiving party, transfer date, gate evaluation results, agreement reference, and any ongoing obligations.

### Phase 9: Post-Transfer Cleanup
Construction OS updates its internal state: the slice is marked as transferred in the manifest, any internal references are updated or removed, and ongoing obligations (if any) are tracked.

---

## Post-Transfer Obligations

1. **Support window.** If a support period is defined in the agreement, Construction OS must honor it.
2. **Security notification.** If a security vulnerability is discovered in transferred code within a defined period, the receiving party should be notified (terms per agreement).
3. **Audit trail.** Transfer records must be retained permanently in the registry.
4. **Non-compete clarity.** The transfer agreement must clarify whether Construction OS retains the right to build similar capabilities.
