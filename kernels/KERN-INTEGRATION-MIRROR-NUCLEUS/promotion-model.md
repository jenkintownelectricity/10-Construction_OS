# Promotion Model

## Definition

**Promotion** is the controlled process of moving a proven, stable, and reusable reflection from a mirror into Construction OS core. When a mirror's reflection demonstrates sustained value that transcends the specific partner integration it was built for, promotion elevates that capability from reflected knowledge into canonical core truth.

Promotion is not automatic. It is a governed, gated process that ensures only high-quality, broadly applicable capabilities enter core, and that they do so without introducing partner-specific contamination, hidden dependencies, or ungoverned complexity.

---

## Why Promotion Matters

Mirrors are designed as reflections — they observe and replicate, but they are not the source of truth. Over time, some reflections prove so valuable that they should become first-class citizens in Construction OS. Without a formal promotion path:

- Valuable patterns remain trapped in mirror-specific implementations
- Teams duplicate effort reimplementing what mirrors already solved
- The boundary between "reflected knowledge" and "core truth" becomes ambiguous
- Mirrors accumulate governance weight they were never designed to carry

Promotion resolves these problems by providing a clean, auditable path from mirror to core.

---

## The 7 Gate Conditions

No reflection may be promoted into core unless ALL seven gate conditions are satisfied. Partial satisfaction is not sufficient. Gates are evaluated in order; failure at any gate halts promotion until the condition is remediated.

### Gate 1: Parity Verified Across 2+ Reviews
The reflection must have passed parity verification in at least two independent review cycles. This confirms that the reflection accurately represents its source and has been stable over time, not just in a single snapshot.

- **Evidence required:** Two or more parity review records showing PASS status with different review dates
- **Verification method:** Examine the mirror's parity fixture history; confirm at least two distinct review cycles with passing results
- **Rationale:** A single parity pass could be coincidental. Two or more passes demonstrate sustained accuracy.

### Gate 2: Reusable Beyond One Mirror
The capability must be demonstrably useful beyond the single mirror where it originated. It must solve a problem that other mirrors face or will face, or that core itself would benefit from having natively.

- **Evidence required:** Written analysis showing at least one additional mirror or core use case that would benefit from the capability
- **Verification method:** Review the capability's interface and logic; confirm it addresses a general pattern, not a partner-specific need
- **Rationale:** Core should not absorb capabilities that serve only one integration. That is what mirrors are for.

### Gate 3: No Partner-Specific Naming Contaminates Core
All naming — functions, modules, schemas, fields, variables, constants — must be free of partner-specific identifiers. A capability promoted to core must use Construction OS naming conventions and domain language exclusively.

- **Evidence required:** Code and schema review confirming no partner names, brand references, or partner-system-specific terminology
- **Verification method:** Automated scan for partner name patterns plus manual review of all public interfaces
- **Rationale:** Core is partner-agnostic. Partner-specific names in core create confusion, coupling, and governance violations.

### Gate 4: No Forbidden External Dependency
The capability must not depend on external services, APIs, libraries, or data sources that are outside Construction OS governance. All dependencies must either already exist in core or be promotable themselves.

- **Evidence required:** Dependency graph showing all transitive dependencies resolve to core-governed components
- **Verification method:** Trace the dependency tree; confirm every leaf node is core-owned or core-approved
- **Rationale:** Promoting a capability with ungoverned dependencies smuggles external coupling into core.

### Gate 5: Ownership Reassignment Approved
The current owner of the reflection (typically the mirror owner or partner team) must formally approve the transfer of ownership to the Construction OS core team. Ownership reassignment includes responsibility for maintenance, bug fixes, evolution, and governance.

- **Evidence required:** Written approval from current owner and acceptance from core team
- **Verification method:** Signed ownership transfer document in the governance record
- **Rationale:** Promotion without ownership clarity creates orphaned capabilities in core.

### Gate 6: Decision Recorded in Registry
The promotion decision — including all gate evaluations, approvals, and the rationale for promotion — must be recorded in the mirror registry before the migration begins.

- **Evidence required:** Registry entry with promotion decision record
- **Verification method:** Query the registry for the promotion record; confirm all fields are populated
- **Rationale:** Unrecorded promotions are ungoverned promotions. The registry is the system of record.

### Gate 7: Breakaway Cost Documented
The cost of NOT promoting — i.e., the cost of breaking away the mirror instead — must be documented. This ensures that promotion is a deliberate choice, not simply the path of least resistance.

- **Evidence required:** Breakaway cost analysis including effort, data loss risk, stakeholder impact, and alternative approaches
- **Verification method:** Review the breakaway cost document; confirm it addresses all four cost dimensions
- **Rationale:** If breakaway is cheap and promotion is risky, promotion may not be the right choice. This gate forces the comparison.

---

## Promotion Process

### Phase 1: Nomination
A mirror owner, core team member, or governance reviewer nominates a reflection for promotion. The nomination must include:
- The specific capability or reflection being nominated
- The mirror it originates from
- A preliminary case for why it belongs in core
- Initial assessment of the 7 gate conditions

### Phase 2: Gate Evaluation
Each of the 7 gates is formally evaluated. Gate evaluation may be conducted by different reviewers for different gates (e.g., a security reviewer for Gate 4, a naming standards reviewer for Gate 3). All evaluations are recorded.

- If any gate fails, the promotion is paused. The nominator may remediate and resubmit.
- If all gates pass, the promotion advances to approval.

### Phase 3: Approval
The governance team reviews the complete gate evaluation package and approves or rejects the promotion. Approval requires:
- All 7 gates passed
- No unresolved objections from any gate reviewer
- Core team confirms capacity to accept ownership

### Phase 4: Migration
The capability is extracted from the mirror and integrated into core. Migration includes:
- Code and schema migration with partner-specific elements removed
- Test migration — all parity fixtures adapted to core testing framework
- Documentation migration — capability documented in core standards
- Configuration migration — any configuration adapted to core conventions

### Phase 5: Verification
After migration, the capability is verified in its new core context:
- All migrated tests pass
- The capability functions correctly without mirror infrastructure
- No regressions in existing core functionality
- Performance meets core standards

### Phase 6: Core Integration
The capability is officially part of core:
- Registry updated to reflect promotion complete
- Mirror's copy of the capability is deprecated or removed
- Mirror manifest updated to reflect the slice is no longer mirror-owned
- Downstream consumers redirected to the core version

---

## Post-Promotion Obligations

1. **Mirror update.** The originating mirror must be updated to consume the promoted capability from core rather than maintaining its own copy.
2. **Deprecation period.** The mirror's version of the capability should remain available (read-only) for a governance-defined deprecation period to allow smooth transition.
3. **Monitoring.** The core team must monitor the promoted capability for at least two review cycles after promotion to confirm stability in its new context.
4. **Registry maintenance.** The promotion record in the registry must be kept current with any post-promotion adjustments.

---

## Promotion Anti-Patterns

- **Premature promotion:** Promoting after a single parity pass without sustained verification.
- **Contaminated promotion:** Allowing partner-specific naming or dependencies to enter core.
- **Orphan promotion:** Promoting without clear core ownership assignment.
- **Silent promotion:** Promoting without registry recording.
- **Forced promotion:** Promoting despite a failed gate by overriding governance.
