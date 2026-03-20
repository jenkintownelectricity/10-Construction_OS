# Transfer Gate

## Purpose

The transfer gate defines the 9 conditions that must be satisfied before a capability slice can be transferred to an external party at BUYOUT_READY or FULL_HANDOFF_READY class. For LICENSE_ONLY and WHITE_LABELABLE transfers, gates 1-5 are required. All conditions are absolute — failure at any required gate halts the transfer.

This document enumerates each condition with its detailed explanation and verification method.

---

## Condition 1: Transfer Class Declared

### Explanation
Every slice must have an explicitly declared transfer class in its manifest before any transfer can occur. The transfer class determines the maximum level of external handoff permitted. A slice without a declared transfer class is, by default, NON_TRANSFERABLE — not because it cannot be transferred, but because no governance authority has evaluated and approved its transferability.

The transfer class must have been assigned during the mirror's chartering process or updated through a formal governance review. Ad hoc class assignment at transfer time is not permitted because it bypasses the deliberation that should occur when a slice is designed.

### Verification Method
1. Inspect the mirror manifest's enabled_slices array for the target slice
2. Confirm the slice has a transfer_class field with a valid value (NON_TRANSFERABLE, LICENSE_ONLY, WHITE_LABELABLE, BUYOUT_READY, or FULL_HANDOFF_READY)
3. Confirm the declared class is equal to or more permissive than the requested transfer type
4. If the transfer class was changed from its original value, verify the change was approved through governance review
5. Record the declared class and any class change history in the transfer evaluation

---

## Condition 2: Dependency Graph Bounded

### Explanation
Before a slice can leave Construction OS, every dependency it relies on must be identified and bounded. "Bounded" means the dependency graph has defined edges — there are no open-ended references to "whatever version of service X is running" or "the current core normalization rules." Every dependency must be pinned to a specific version, interface, or artifact that can be included in or excluded from the transfer bundle.

An unbounded dependency graph means the transferred slice might break unpredictably when Construction OS evolves, or it might silently depend on capabilities the receiving party does not have.

### Verification Method
1. Generate the complete dependency graph for the slice, including transitive dependencies
2. For each dependency, verify it is classified as: core (stays in Construction OS), mirror-local (transfers with the slice), or external (third-party)
3. Confirm every dependency is pinned to a specific version or interface contract
4. Confirm the graph has no open-ended or dynamic references
5. Verify the graph is acyclic (circular dependencies prevent clean transfer)
6. Document the bounded graph with classifications in the transfer evaluation

---

## Condition 3: No Hidden Dependencies

### Explanation
Beyond the declared dependency graph, hidden dependencies may exist — runtime service discovery, implicit environment assumptions, undeclared file system paths, ambient network access, or configuration inherited from the deployment environment. Hidden dependencies are the most dangerous transfer risk because they cause the transferred capability to fail in the receiving party's environment with no obvious explanation.

This gate requires an independent verification that goes beyond reading the manifest. The slice must be tested in isolation to prove it has no hidden dependencies.

### Verification Method
1. Deploy the slice in a clean, isolated environment with only the declared dependencies available
2. Execute the slice's full test suite and parity fixtures in this isolated environment
3. Monitor for any network calls, file system access, or service discovery attempts that reach outside the declared boundary
4. Verify the slice produces correct results using only declared dependencies
5. If any hidden dependency is discovered, document it, add it to the dependency graph, and re-evaluate gates 2 and 3
6. Record the isolation test results including environment specification and test outcomes

---

## Condition 4: Handoff Bundle Specification Exists

### Explanation
The handoff bundle is the complete package the receiving party will receive. The specification must define, exhaustively, every artifact in the bundle: source code files, compiled artifacts, schemas, configuration files, documentation, test suites, sample data, operational runbooks, monitoring configurations, and any tooling required to build, deploy, and operate the capability.

The specification is not a packing list created at transfer time — it must be reviewed and agreed upon before the transfer is approved. The receiving party should review the specification to confirm it meets their expectations. Gaps discovered after transfer are costly and erode trust.

### Verification Method
1. Confirm a written handoff bundle specification document exists for the slice
2. Verify the specification covers all required categories: source code, build artifacts, schemas, configuration, documentation, tests, sample data, runbooks, monitoring, and tooling
3. Verify each category lists specific artifacts (not vague references like "relevant documentation")
4. Confirm the receiving party has reviewed the specification and acknowledged completeness
5. For FULL_HANDOFF_READY transfers, verify the specification also covers infrastructure definitions, deployment scripts, and operational procedures
6. Record the specification reference and receiving party acknowledgment in the transfer evaluation

---

## Condition 5: Trust Boundary Documented

### Explanation
The trust boundary between the slice and Construction OS core must be fully documented before transfer. Post-transfer, the receiving party inherits the external side of this boundary. They need to understand: what data the slice expects to receive (and in what format), what data the slice produces, what operations the slice requires from its environment, and what security guarantees the slice assumes.

Without this documentation, the receiving party cannot properly integrate or operate the slice. They will make incorrect assumptions about data formats, security requirements, or operational dependencies.

### Verification Method
1. Confirm the trust boundary documentation exists and covers all four boundary types: data, control, identity, and failure
2. Verify the data boundary section specifies all schemas, data formats, and data classification levels
3. Verify the control boundary section specifies all operations the slice performs and what permissions it requires
4. Verify the identity boundary section specifies authentication mechanisms and credential requirements
5. Verify the failure boundary section specifies failure modes, recovery procedures, and isolation requirements
6. Confirm the documentation is written for an external audience (not assuming Construction OS internal knowledge)
7. Record the trust boundary documentation reference in the transfer evaluation

---

## Condition 6: Ownership Lineage Documented

### Explanation
The ownership lineage traces who created, modified, reviewed, and approved every component of the slice. This is essential for IP (intellectual property) clarity. The receiving party needs to know: who wrote the code, whether any third-party IP is embedded, whether any open-source components are included (and under what licenses), and whether any contributor has claims that might complicate the transfer.

Ownership lineage also protects Construction OS. If a dispute arises after transfer about IP ownership, the lineage record provides the evidence needed to resolve it.

### Verification Method
1. Compile a complete list of contributors to the slice (code, schemas, documentation, tests)
2. For each contributor, document their role and the scope of their contribution
3. Identify any third-party code, libraries, or IP embedded in the slice
4. For each third-party component, document the license and confirm the license permits transfer
5. Confirm no contributor has outstanding IP claims that would block transfer
6. Verify the lineage document has been reviewed by legal or IP governance
7. Record the ownership lineage document reference in the transfer evaluation

---

## Condition 7: Detachment Test Passes

### Explanation
The detachment test is the ultimate proof that a slice can be transferred. The slice is deployed in a clean environment that simulates the receiving party's infrastructure — with no access to Construction OS services, no ambient credentials, no shared databases, and no network path back to Construction OS. The slice must function correctly in this environment.

The detachment test is more rigorous than the hidden dependency test (Gate 3). Gate 3 verifies that no undeclared dependencies exist. Gate 7 verifies that the slice works end-to-end in a representative external environment, including startup, normal operation, error handling, and graceful shutdown.

### Verification Method
1. Provision an environment that simulates the receiving party's infrastructure (based on their stated environment specifications)
2. Deploy the slice using only the artifacts defined in the handoff bundle specification
3. Configure the slice using only the documentation in the handoff bundle
4. Execute the full test suite — all tests must pass
5. Execute representative operational scenarios — normal data processing, error conditions, and recovery
6. Verify the slice starts, operates, handles errors, and shuts down gracefully
7. Confirm no communication with Construction OS infrastructure occurred during the test
8. Record the detachment test results, environment specification, and any issues encountered

---

## Condition 8: Replacement Obligations Defined

### Explanation
If Construction OS or other mirrors currently depend on the slice being transferred, a replacement plan must exist. Transfer removes the slice from the Construction OS ecosystem — any internal consumers must have an alternative. This gate prevents transfer from creating orphaned dependencies within Construction OS.

The replacement plan must be concrete: it must identify every internal consumer, specify how each will be served after transfer (replacement capability, alternative data source, or acknowledgment that the dependency is being retired), and include a timeline for the transition.

### Verification Method
1. Identify all internal consumers of the slice — other mirrors, core modules, or downstream systems
2. For each consumer, document how they will be served after the slice is transferred
3. Verify that replacement capabilities exist or are planned with committed timelines
4. Confirm each internal consumer has acknowledged the plan and accepted the transition
5. If any consumer cannot be served after transfer, the transfer must be delayed until a replacement is available
6. Record the replacement plan with consumer acknowledgments in the transfer evaluation

---

## Condition 9: Security Assumptions Documented

### Explanation
Every capability slice embeds security assumptions — what encryption is expected, what authentication model is used, what data classification levels are processed, what access control model governs operations, and what security services are assumed to be present in the environment. These assumptions must be explicitly documented because the receiving party's security posture may differ from Construction OS.

If security assumptions are not documented, the receiving party may deploy the slice in an environment that does not meet its security requirements, leading to data exposure, unauthorized access, or compliance violations. Neither party benefits from this outcome.

### Verification Method
1. Document all encryption assumptions: data at rest, data in transit, key management expectations
2. Document the authentication model: what credentials the slice uses, how they are provisioned, how they are rotated
3. Document data classification: what classification levels the slice processes and what handling requirements apply
4. Document access control: what permissions model the slice expects, how authorization decisions are made
5. Document security service dependencies: what security infrastructure the slice assumes (firewalls, intrusion detection, certificate authorities, etc.)
6. Document incident response assumptions: how security incidents involving the slice should be handled
7. Confirm the receiving party has reviewed and acknowledged all security assumptions
8. Record the security documentation reference and receiving party acknowledgment in the transfer evaluation

---

## Gate Evaluation Summary Template

For each transfer evaluation, the following summary must be completed:

| Gate | Condition | Required For | Status | Evidence Reference | Evaluator | Date |
|------|-----------|-------------|--------|--------------------|-----------|------|
| 1 | Transfer class declared | All transfers | PASS/FAIL | [ref] | [name] | [date] |
| 2 | Dependency graph bounded | All transfers | PASS/FAIL | [ref] | [name] | [date] |
| 3 | No hidden dependencies | All transfers | PASS/FAIL | [ref] | [name] | [date] |
| 4 | Handoff bundle spec exists | All transfers | PASS/FAIL | [ref] | [name] | [date] |
| 5 | Trust boundary documented | All transfers | PASS/FAIL | [ref] | [name] | [date] |
| 6 | Ownership lineage documented | BUYOUT / HANDOFF | PASS/FAIL | [ref] | [name] | [date] |
| 7 | Detachment test passes | BUYOUT / HANDOFF | PASS/FAIL | [ref] | [name] | [date] |
| 8 | Replacement obligations defined | BUYOUT / HANDOFF | PASS/FAIL | [ref] | [name] | [date] |
| 9 | Security assumptions documented | BUYOUT / HANDOFF | PASS/FAIL | [ref] | [name] | [date] |

**Transfer Class Requested:** [LICENSE_ONLY / WHITE_LABELABLE / BUYOUT_READY / FULL_HANDOFF_READY]

**Gates Required:** [1-5 / 1-9]

**Overall Result:** ALL required gates must PASS.

**Decision:** APPROVED / REJECTED

**Approver:** [name]

**Receiving Party:** [name]

**Date:** [date]
