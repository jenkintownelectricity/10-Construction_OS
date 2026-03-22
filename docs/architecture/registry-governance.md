# Registry Governance Specification

## 1. Repository Topology Model

The registry maintains the authoritative map of all Construction OS repositories. This map includes:

- **Repository identity** — name, owner, and unique identifier for every repo in the system.
- **Classification** — each repository is classified by layer (infrastructure, cognitive, application) and by authority type (kernel, authority, non-authority).
- **Inter-dependencies** — the directed graph of which components depend on which, declared at registration time and validated continuously.

No other component in Construction OS holds a competing topology map. If the registry does not list a repository, that repository does not exist within the topology for governance purposes.

## 2. Dependency Mapping

The registry tracks dependency relationships between all registered components:

- **Declaration:** Each component declares its dependencies at registration time.
- **Validation:** The registry validates every dependency declaration against the current topology. A dependency on an unregistered component is invalid and will be rejected.
- **Graph integrity:** The registry maintains the full dependency graph and can detect cycles, orphaned nodes, and undeclared transitive dependencies.
- **Change propagation:** When a component's classification or status changes, the registry evaluates the impact on all dependents.

## 3. Registry Validation Rules

The registry enforces the following validation posture:

| Rule | Behavior |
|------|----------|
| Components must register | Any component that has not registered with the registry is unknown to the topology. |
| Topology changes must be validated | No structural change — new component, removed component, reclassification, dependency change — takes effect without registry validation. |
| Unregistered components are rejected | The registry operates **fail-closed**. An unregistered component is not partially trusted or provisionally accepted; it is rejected outright. |
| Dependency targets must exist | A declared dependency on a component not present in the registry is invalid. |
| Classification must be explicit | Every registered component must carry an explicit classification. Implicit or inherited classification is not permitted. |

**Fail-closed posture:** The default answer to any unvalidated topology question is rejection. The registry does not guess, infer, or assume. If validation cannot complete, the operation fails.

## 4. Component Registration Posture

All cognitive-layer repositories register with the registry following this protocol:

1. **Submission:** The component submits a registration declaration including its identity, classification, and dependency list.
2. **Validation:** The registry validates the declaration against existing topology — checking for naming conflicts, dependency validity, and classification correctness.
3. **Confirmation:** Upon successful validation, the registry confirms registration. The component is now part of the authoritative topology map.
4. **Boundary:** The registry does not govern internal component behavior. Once registered, a component's internal architecture, runtime decisions, and operational logic are its own concern. The registry cares about structural placement, not internal implementation.

## 5. Authoritative Relation to Cognitive-Layer Repositories

The registry classifies the following as cognitive-layer components with **non-authority** status:

| Component        | Classification        | Authority Status |
|------------------|-----------------------|------------------|
| CRI              | Cognitive layer       | Non-authority    |
| VKBUS            | Cognitive layer       | Non-authority    |
| Cognitive Bus    | Cognitive layer       | Non-authority    |
| Assistant        | Cognitive layer       | Non-authority    |
| Workers          | Cognitive layer       | Non-authority    |
| Awareness Cache  | Cognitive layer       | Non-authority    |

Non-authority status means these components do not originate doctrine, do not hold truth, and do not govern other components' classifications. They are registered participants in the topology, not authorities over it.

## 6. Classification of Non-Truth Cognitive Repos

All cognitive-layer repositories are classified as follows:

- **Non-authority.** No cognitive-layer repository holds authority status for doctrine or truth.
- **None are kernels.** Kernel status is reserved for repositories that originate and govern doctrine. No cognitive-layer repo qualifies.
- **None hold doctrine.** Doctrine is not stored in, originated by, or adjudicated within any cognitive-layer repository.

This classification is structural, not a commentary on the importance of these components. They perform critical cognitive functions; they simply do not hold doctrine authority.

## 7. Registry Authority Scope

The registry remains authoritative for Construction OS topology. This means:

- The registry is the single source of truth for what repositories exist.
- The registry is the single source of truth for how repositories are classified.
- The registry is the single source of truth for dependency relationships.
- No other component may maintain a competing or shadow topology.

## 8. Doctrine Boundary — Topology Authority Only

**The registry must not drift into doctrine ownership.**

This boundary is non-negotiable and load-bearing:

- **Topology authority** means the registry knows what exists, where it sits, and what depends on what.
- **Doctrine authority** means originating, storing, or adjudicating the truths that govern system behavior.
- The registry holds the first. It must never acquire the second.
- **Truth belongs to kernels.** If a question is about what is structurally true of the topology, the registry answers. If a question is about what is doctrinally true of the system's behavior or rules, a kernel answers.

Any observed drift toward doctrine ownership — the registry beginning to define behavioral rules, originate governing principles, or adjudicate truth claims — must be corrected immediately.

## 9. Non-Authority Guarantees, Fail-Closed Posture, and Lineage

### Non-Authority Guarantees (for Doctrine)

The registry guarantees that it will not:

- Originate doctrine under any circumstances.
- Store doctrine, even temporarily or as a cache.
- Adjudicate doctrinal disputes between components.
- Promote itself or any non-authority component to doctrine authority status.

These guarantees are structural, not aspirational. They are enforced by the classification system itself.

### Fail-Closed

The registry's default posture is fail-closed across all operations:

- **Unregistered components:** Rejected, not deferred.
- **Invalid dependencies:** Rejected, not warned.
- **Ambiguous classifications:** Rejected, not inferred.
- **Unvalidated topology changes:** Rejected, not queued.

If the registry cannot definitively validate an operation, the operation does not proceed. There is no soft-fail mode.

### Lineage

Every topology entry in the registry carries lineage metadata:

- **Registration timestamp:** When the component was registered.
- **Classification history:** All classification changes over time, with timestamps and rationale.
- **Dependency evolution:** The history of dependency declarations, additions, and removals.
- **Validation record:** A log of all validation decisions made about the component.

Lineage is immutable once recorded. It provides the audit trail necessary to verify that topology authority has been exercised correctly and that no drift toward doctrine ownership has occurred.
