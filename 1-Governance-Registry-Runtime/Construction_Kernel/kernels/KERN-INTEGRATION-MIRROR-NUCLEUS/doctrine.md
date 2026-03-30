# Master Doctrine: Mirror Kernel Nucleus

## The Doctrine

> **Connected by mirrors, never hard-wired.**
> **Sold by capability, detachable by design.**
> **Cooperate without entanglement.**

These three statements form the non-negotiable foundation of every integration decision in Construction OS. They are not aspirational goals — they are absolute constraints. Every mirror, every slice, every reflection, every integration decision must satisfy all three statements simultaneously.

---

## Principle 1: Connected by Mirrors, Never Hard-Wired

### Statement
All connections between Construction OS and external systems must flow through governed mirror boundaries. Direct wiring between Construction OS internals and external system internals is forbidden.

### Rationale
Hard-wired integrations create invisible dependencies. When system A is hard-wired to system B, changes in B can break A without warning, and removing B requires surgery on A. In the construction industry, external systems (estimating tools, accounting platforms, scheduling software, subcontractor portals) change frequently — vendors are acquired, products are discontinued, customers switch providers. Construction OS must survive all of these events without damage.

A mirror is an explicit, governed, observable boundary. It makes the connection visible, measurable, and reversible. When something breaks, you know where to look. When you need to disconnect, you know what to detach.

### Principles
- Every external system connection must be represented as a declared mirror with a manifest.
- The mirror boundary is the only place where external system concepts cross into Construction OS.
- Construction OS core code must never import, reference, or depend on external system libraries, APIs, or data structures directly.
- Mirror internals may know about the external system. Construction OS core must not.

### Anti-Patterns
- **Direct API call from core to external system.** Core code makes an HTTP call to an external vendor API without going through a mirror boundary. This creates an invisible dependency that will break when the vendor changes their API.
- **Shared database between Construction OS and external system.** Two systems reading and writing to the same database tables. This creates coupling at the data layer that is nearly impossible to untangle.
- **External system SDK embedded in core.** A vendor's SDK is imported directly into Construction OS core modules. Version changes in the SDK now require core changes.
- **Configuration-driven direct coupling.** "We just put the external API URL in a config file." Configuration does not create a governance boundary. The coupling is still direct — it is just parameterized.

---

## Principle 2: Sold by Capability, Detachable by Design

### Statement
Mirrors expose discrete capability slices that can be individually enabled, disabled, sold, or detached. No mirror is an indivisible monolith. Every capability must be independently governable.

### Rationale
Construction OS serves diverse customers with different needs. One customer may need an integration with Procore for project management but not for financials. Another may need QuickBooks for accounting but plan to switch to Sage next year. If integrations are monolithic — all or nothing — then customers are forced to take capabilities they do not need, and removing capabilities requires removing the entire integration.

By structuring mirrors as collections of discrete capability slices, Construction OS can sell individual capabilities, respond to customer changes by enabling or disabling specific slices, and detach any slice without affecting others.

Detachability is not an afterthought — it is a design requirement. Every slice must be built with its own removal in mind. If you cannot describe how to remove a slice without breaking anything, the slice is not ready for deployment.

### Principles
- Every capability exposed by a mirror must be declared as a distinct slice with its own identity, inputs, outputs, and dependencies.
- Slices must declare their detachability level (FULLY_DETACHABLE, DETACHABLE_WITH_MIGRATION, DETACHABLE_WITH_NOTICE).
- No slice may create hidden dependencies that would prevent its removal.
- The cost of detaching a slice must be documented and bounded.
- Sales, licensing, and packaging decisions can operate at the slice level.

### Anti-Patterns
- **Monolithic integration.** A single integration that bundles 15 capabilities together with no way to enable or disable individual ones. Customers must take all or nothing.
- **Hidden cross-slice dependency.** Slice A secretly depends on Slice B, but this dependency is not declared. Disabling Slice B breaks Slice A without warning.
- **Detachment requires data loss.** Removing a slice deletes data that Construction OS core needs. The slice was storing core truth instead of reflecting external truth.
- **Capability without boundary.** A feature is added to a mirror without being declared as a slice. It has no identity, no dependency graph, no detachability assessment. It cannot be individually governed.

---

## Principle 3: Cooperate Without Entanglement

### Statement
Mirrors cooperate with Construction OS by reflecting compatible value, but they must never become entangled with core internals. Cooperation means contributing value across a governed boundary. Entanglement means creating dependencies that cannot be cleanly separated.

### Rationale
The construction industry runs on cooperation between many parties — general contractors, subcontractors, suppliers, architects, engineers, inspectors. Each party has their own systems, processes, and truth. Construction OS must cooperate with all of these parties and their systems without becoming dependent on any of them.

Entanglement is the enemy of longevity. When two systems are entangled, neither can evolve independently. Changes in one force changes in the other. Failures in one cascade to the other. The more entangled systems become, the more fragile the overall platform becomes.

Mirrors are the mechanism for cooperation without entanglement. A mirror can reflect value from an external system (cooperation) while maintaining a strict boundary that prevents the external system's internals from leaking into Construction OS core (no entanglement).

### Principles
- Reflections carry compatible truth, not identical truth. The mirror translates external concepts into Construction OS-compatible forms.
- Mirrors may not directly mutate Construction OS canonical core truth. Value flows inward through reflection; changes to core truth flow through governed promotion gates.
- The failure of an external system must not cause the failure of Construction OS core. Mirrors must handle external failures gracefully.
- Mirror removal must not leave Construction OS core in a broken state. Core must be complete and functional without any mirrors.

### Anti-Patterns
- **Mirror writes directly to core tables.** A mirror integration directly inserts or updates records in Construction OS core database tables. This bypasses all governance and creates hidden mutation paths.
- **Core depends on mirror for basic functionality.** Construction OS core cannot perform a basic operation (like creating a project) without a specific mirror being active. The mirror has become load-bearing for core.
- **Shared domain models.** The mirror and core share the same domain model classes. Changes to the model for mirror purposes now affect core behavior.
- **Cascading failure.** An external system goes down, and because the mirror is entangled with core, Construction OS core also becomes unavailable or degraded for unrelated features.
- **Truth confusion.** It becomes unclear whether a piece of data originated in Construction OS core or was reflected from an external system. Ownership is ambiguous, and conflicting updates create data corruption.

---

## Doctrine Application

### Decision Test

When evaluating any integration decision, apply the following test:

1. **Mirror test:** Is this connection going through a governed mirror boundary? If no, the decision violates the doctrine.
2. **Capability test:** Is this functionality exposed as a declared, detachable capability slice? If no, the decision violates the doctrine.
3. **Entanglement test:** Can this mirror be removed without breaking Construction OS core? If no, the decision violates the doctrine.

All three tests must pass. Passing two out of three is not sufficient.

### Precedence

The doctrine takes precedence over:
- Convenience ("It would be faster to connect directly")
- Cost ("A mirror boundary adds overhead")
- Vendor pressure ("The vendor's SDK is designed to be embedded")
- Customer urgency ("We need this integration by Friday")

The doctrine does not take precedence over:
- Safety (if a direct connection is required to prevent harm to people, the doctrine may be temporarily suspended with documented justification)
- Legal requirements (if a regulation requires a specific integration pattern, the doctrine must accommodate it within the closest compliant mirror structure)

### Enforcement

Doctrine violations are detected through:
- Mirror validity rules (12 rules documented in `mirror-validity-rules.md`)
- Forbidden pattern checks (10 patterns documented in `forbidden-patterns.md`)
- Parity fixture verification
- Dependency graph analysis
- Registry state audits

Doctrine violations are not warnings. They are blocking conditions that must be resolved before a mirror can reach or remain in ACTIVE state.
