# Promotion Gate

## Purpose

The promotion gate defines the 7 conditions that must be satisfied before any mirror reflection can be promoted into Construction OS core. These conditions are absolute — all 7 must pass. There is no partial promotion and no conditional approval.

This document enumerates each condition with its detailed explanation and verification method.

---

## Condition 1: Parity Verified Across 2+ Reviews

### Explanation
The reflection being promoted must have demonstrated sustained accuracy against its source system. A single parity check proves the reflection worked once; two or more prove it works reliably. The reviews must be distinct events separated by meaningful time (not two runs on the same day). Each review must have been conducted under normal operating conditions, not under special test conditions that do not reflect production reality.

Parity verification must cover the full scope of the reflection — not just a subset of fields or a sample of records. If the reflection covers 50 data fields, all 50 must be verified in each review. If the reflection processes 10,000 records daily, the parity fixture must validate a statistically significant sample or the full set.

### Verification Method
1. Retrieve the mirror's parity review history from the drift/parity records
2. Confirm at least 2 review records exist with PASS status
3. Confirm the reviews occurred on different dates with at least the governance-defined minimum interval between them
4. Confirm each review covered the full scope of the reflection (not partial)
5. Confirm reviews were conducted under production-equivalent conditions
6. Record the review dates, reviewers, and scope in the promotion evaluation

---

## Condition 2: Reusable Beyond One Mirror

### Explanation
Core is the shared foundation of Construction OS. Capabilities promoted to core must serve the broader system, not just one integration. If a reflection solves a problem that only one partner faces, it belongs in that partner's mirror — not in core. Promotion to core is justified only when the capability addresses a pattern that multiple mirrors encounter or that core itself would benefit from natively.

Reusability is assessed by examining the capability's interface and logic. A capability is reusable if: (a) its inputs and outputs use core-standard schemas rather than partner-specific formats, (b) its logic addresses a general construction domain problem rather than a partner-specific workflow, and (c) at least one other mirror or core module could consume it without modification.

### Verification Method
1. Document at least one additional use case beyond the originating mirror
2. Review the capability's public interface — confirm it uses core-standard types and schemas
3. Confirm no partner-specific workflow assumptions are embedded in the logic
4. If possible, prototype consumption of the capability by a second mirror or core module
5. Obtain written confirmation from a second team or mirror owner that the capability would be useful
6. Record the reusability analysis in the promotion evaluation

---

## Condition 3: No Partner-Specific Naming Contaminates Core

### Explanation
When a capability enters core, it becomes part of the Construction OS identity. Partner names, brand identifiers, partner system names, and partner-specific terminology must be completely absent. This is not merely a cosmetic concern — partner-specific naming creates implicit coupling, confuses future developers who encounter unfamiliar partner references, and may create legal or contractual complications.

The naming review covers everything: module names, function names, class names, variable names, database fields, API endpoints, configuration keys, log messages, error messages, comments, and documentation. Every string that a developer or operator might encounter must use Construction OS domain language exclusively.

### Verification Method
1. Compile a list of all partner-specific names, brands, and system identifiers associated with the originating mirror
2. Run an automated scan of all code, schemas, configuration, and documentation for any occurrence of these terms
3. Conduct a manual review of all public interfaces (APIs, schemas, function signatures) for subtle partner references
4. Review internal comments and documentation for partner-specific language
5. Confirm that all names follow Construction OS naming conventions
6. Record the naming review results, including any items that were renamed

---

## Condition 4: No Forbidden External Dependency

### Explanation
A capability promoted to core must not depend on anything outside Construction OS governance. This includes external APIs, third-party libraries not already approved for core use, partner-hosted services, external data sources, and any runtime dependency that Construction OS does not control. If the capability stops working because an external service changes its API, that is an unacceptable fragility for core.

The dependency check is transitive. It is not sufficient to verify that the capability's direct dependencies are core-governed — every dependency of every dependency must also be verified. A single ungoverned leaf node in the dependency tree is a violation.

### Verification Method
1. Generate the complete transitive dependency graph for the capability
2. For each dependency, verify it is either: (a) already part of core, or (b) an approved core library/service
3. Flag any external service calls, API integrations, or network dependencies
4. Flag any third-party libraries not on the core-approved list
5. For flagged items, determine if they can be removed, replaced with core alternatives, or independently promoted
6. Run the capability in an isolated environment with no external network access — it must function correctly
7. Record the dependency analysis with the full dependency tree

---

## Condition 5: Ownership Reassignment Approved

### Explanation
Every capability has an owner. In a mirror, the owner is typically the mirror team or the partner integration team. When a capability moves to core, ownership must transfer to the core team. This is not a formality — it means the core team accepts responsibility for maintenance, bug fixes, security patches, performance tuning, and future evolution.

Both sides must explicitly agree. The current owner must be willing to release ownership (including any claim to the capability's evolution direction). The core team must be willing and able to accept it (including having the expertise and capacity to maintain it).

### Verification Method
1. Obtain written approval from the current capability owner agreeing to transfer ownership
2. Obtain written acceptance from the designated core team owner
3. Confirm the core team has reviewed the capability and understands its purpose, implementation, and maintenance requirements
4. Confirm the core team has capacity to maintain the capability (not just willingness)
5. Document the ownership transfer in a formal record including: previous owner, new owner, transfer date, maintenance expectations
6. Record the ownership reassignment in the promotion evaluation

---

## Condition 6: Decision Recorded in Registry

### Explanation
The mirror registry is the system of record for all governance decisions. A promotion that is not recorded in the registry is an ungoverned promotion — it cannot be audited, traced, or reversed if problems are discovered later. The registry record must be created before the actual migration begins, not after. This ensures that even if the migration fails partway through, the decision and its context are preserved.

The registry record must be comprehensive: it must capture not just the decision (promote/reject) but the full context — who nominated, who evaluated each gate, what evidence was reviewed, what the outcome was, and why.

### Verification Method
1. Before migration begins, create a registry entry for the promotion decision
2. Confirm the entry includes: mirror_id, slice_id (if applicable), nomination date, nominator, gate evaluation results for all 7 gates, approval decision, approver, and approval date
3. Confirm the entry references all supporting evidence documents
4. Verify the registry entry is queryable and returns correct data
5. Record the registry entry ID in the promotion evaluation

---

## Condition 7: Breakaway Cost Documented

### Explanation
Promotion is a one-way door — once a capability is in core, extracting it is extremely difficult. Before walking through that door, the team must understand the alternative: what would it cost to simply break away the mirror instead? If breakaway is cheap and low-risk, promotion may be unnecessary complexity. If breakaway is expensive and would lose valuable capability, promotion is better justified.

The breakaway cost analysis must be honest and comprehensive. It must consider: engineering effort to replace the capability if the mirror is broken away, data loss risk if reflections stop, impact on stakeholders who depend on the mirror's output, and whether alternative integration patterns could provide the same value without promotion.

### Verification Method
1. Document the estimated engineering effort (person-hours) to replace the capability if the mirror is broken away instead of promoted
2. Document the data loss risk — what information would become unavailable if breakaway occurs
3. Document stakeholder impact — which teams, systems, or users would be affected by breakaway
4. Document alternative approaches — could the capability's value be preserved without promotion (e.g., by chartering a new mirror, by licensing, by manual processes)
5. Compare the total breakaway cost against the promotion cost (migration effort, core maintenance burden, governance overhead)
6. Record the breakaway cost analysis in the promotion evaluation
7. Confirm the analysis has been reviewed by someone other than the nominator (to avoid bias)

---

## Gate Evaluation Summary Template

For each promotion evaluation, the following summary must be completed:

| Gate | Condition | Status | Evidence Reference | Evaluator | Date |
|------|-----------|--------|--------------------|-----------|------|
| 1 | Parity verified 2+ reviews | PASS/FAIL | [ref] | [name] | [date] |
| 2 | Reusable beyond one mirror | PASS/FAIL | [ref] | [name] | [date] |
| 3 | No partner naming | PASS/FAIL | [ref] | [name] | [date] |
| 4 | No forbidden dependency | PASS/FAIL | [ref] | [name] | [date] |
| 5 | Ownership reassigned | PASS/FAIL | [ref] | [name] | [date] |
| 6 | Decision in registry | PASS/FAIL | [ref] | [name] | [date] |
| 7 | Breakaway cost documented | PASS/FAIL | [ref] | [name] | [date] |

**Overall Result:** ALL PASS required for promotion approval.

**Decision:** APPROVED / REJECTED

**Approver:** [name]

**Date:** [date]
