# Trust Boundary Model

## Definition

**Trust boundaries** are the isolation mechanisms between mirrors and Construction OS core. They define the exact perimeter where Construction OS governance ends and mirror/partner governance begins. Trust boundaries are not suggestions — they are enforced architectural constraints that determine what data can cross, what operations are permitted, and what guarantees each side provides.

Every mirror has exactly one trust boundary with Construction OS core. The boundary is defined at chartering time, documented in the mirror manifest, and enforced throughout the mirror's lifecycle.

---

## Why Trust Boundaries Exist

Without trust boundaries:
- A misbehaving mirror could corrupt core data
- Partner-specific logic could leak into core schemas
- Mirror failures could cascade into Construction OS service degradation
- Authentication and authorization contexts would become entangled
- Data classification violations would be undetectable
- Breakaway would be impossible to guarantee as non-destructive

Trust boundaries make the non-destructive guarantee enforceable. They make breakaway clean. They make promotion safe. They make transfer bounded.

---

## Trust Boundary Types

### 1. Data Boundary (Schema-Mediated)

The data boundary controls what information crosses between core and the mirror. All data exchange is mediated through explicit schemas — no raw, unstructured, or ad-hoc data transfer is permitted.

**Principles:**
- All data crossing the boundary must conform to a declared schema
- Schemas are versioned and governed by Construction OS
- The mirror receives reflections, never originals — core data is copied, not shared
- Data flowing from mirror to core (if permitted) passes through validation gates
- No schema field may be added at the boundary without governance approval

**Enforcement mechanisms:**
- Schema validation at ingress and egress points
- Data classification tags that prevent FORBIDDEN-class data from crossing
- Transformation layers that strip partner-specific fields before core ingestion
- Audit logging of all cross-boundary data transfers

**What CANNOT cross the data boundary:**
- Billing data (FORBIDDEN)
- Tenant UI configuration (FORBIDDEN)
- Authentication credentials (FORBIDDEN)
- Raw, unvalidated partner data
- Data without schema conformance

### 2. Control Boundary (No Direct Mutation)

The control boundary prevents mirrors from directly mutating Construction OS core state. Mirrors can observe, reflect, and request — but they cannot command.

**Principles:**
- Mirrors may not execute write operations against core data stores
- Mirrors may not trigger core workflows directly
- Mirrors may not modify core configuration
- All mirror-to-core requests pass through a governed request channel
- Core decides whether to honor mirror requests; mirrors do not assume acceptance

**Enforcement mechanisms:**
- Read-only access grants for mirror service accounts against core
- Request queues with governance-layer approval for state changes
- No shared database connections between mirror and core
- API gateways that enforce read-only patterns for mirror callers

**What the control boundary prevents:**
- A mirror updating a core detail record directly
- A mirror triggering a core billing event
- A mirror modifying core user permissions
- A mirror altering core schema definitions

### 3. Identity Boundary (Separate Auth)

The identity boundary ensures that mirrors and core maintain separate authentication and authorization contexts. A mirror's identity is not a core identity, and vice versa.

**Principles:**
- Mirrors authenticate with their own credentials, separate from core user credentials
- Mirror service accounts have explicitly scoped permissions — no ambient authority
- Partner users do not receive Construction OS core credentials through mirrors
- Token exchange between mirror and core (if needed) goes through a governed broker
- Identity lifecycle (creation, rotation, revocation) is managed independently

**Enforcement mechanisms:**
- Separate identity providers or isolated realms within a shared provider
- Mirror-specific service accounts with minimum-privilege scoping
- No credential sharing between mirror and core service accounts
- Automated credential rotation on governance-defined schedules
- Immediate revocation capability for breakaway scenarios

**What the identity boundary prevents:**
- A mirror operator gaining core admin access through the mirror
- A partner user authenticating as a Construction OS core user
- Credential leakage from mirror to partner or partner to core
- Privilege escalation through mirror-core token confusion

### 4. Failure Boundary (No Cascade to Core)

The failure boundary ensures that mirror failures — whether crashes, data corruption, resource exhaustion, or security incidents — cannot propagate to Construction OS core.

**Principles:**
- Mirror infrastructure is isolated from core infrastructure
- Mirror resource consumption is bounded and cannot starve core resources
- Mirror errors do not trigger core error handling or alerting (except through governed notification channels)
- If a mirror becomes unresponsive, core continues operating with zero degradation
- Mirror recovery is the mirror operator's responsibility; core does not auto-heal mirrors

**Enforcement mechanisms:**
- Separate compute, storage, and network resources for mirrors
- Resource quotas and rate limits on mirror-to-core communication
- Circuit breakers that cut mirror access to core if error rates exceed thresholds
- Health check independence — core health checks do not depend on mirror status
- Bulkhead patterns that isolate mirror interaction paths from core critical paths

**What the failure boundary prevents:**
- A mirror memory leak consuming core server resources
- A mirror infinite loop overwhelming core APIs
- A mirror database corruption spreading to core data stores
- A mirror security breach granting access to core infrastructure
- A mirror outage causing core service degradation

---

## Trust Boundary Lifecycle

### At Chartering
The trust boundary is defined when the mirror is chartered. The charter must specify:
- Which boundary types apply (all four are recommended; minimum is data + failure)
- The specific schemas that mediate the data boundary
- The access scope for mirror service accounts
- The resource limits for the failure boundary
- Any exceptions or special grants (which must be individually justified)

### During Active Operation
The trust boundary is continuously enforced:
- Automated monitoring detects boundary violations
- Periodic audits verify that actual behavior matches declared boundaries
- Boundary changes require governance approval and manifest updates
- Violations are logged and may trigger escalation or emergency breakaway

### At Breakaway
The trust boundary enables clean breakaway:
- Revoking mirror credentials severs the identity boundary
- Disabling mirror access points severs the data and control boundaries
- Stopping mirror infrastructure severs the failure boundary
- Core continues operating as if the mirror never existed

### At Promotion
When a capability is promoted from mirror to core:
- The promoted capability moves inside the trust boundary
- The boundary is updated to reflect the reduced mirror scope
- Any data that was reflected is now natively core-owned

---

## Trust Boundary Violations

A trust boundary violation is any event where the actual behavior of a mirror or core deviates from the declared boundary contract. Violations are classified by severity:

**Critical:** Immediate threat to core integrity. Examples: unauthorized write to core data store, credential leakage, data classification breach. Response: emergency freeze, potential emergency breakaway.

**Major:** Boundary contract broken but no immediate core damage. Examples: schema-nonconformant data transmitted, undeclared dependency discovered, resource quota exceeded. Response: mirror frozen until remediation is verified.

**Minor:** Boundary contract technically violated but with negligible impact. Examples: logging format deviation, minor schema version mismatch handled by compatibility layer. Response: documented, remediation scheduled, no freeze required.

All violations, regardless of severity, are recorded in the mirror's drift record and the governance audit log.

---

## Trust Boundary Documentation Requirements

Every mirror manifest must include a trust boundary section containing:

1. **Boundary type declarations** — which of the four boundary types are enforced
2. **Data schemas** — the specific schemas mediating the data boundary
3. **Access scope** — the permissions granted to mirror service accounts
4. **Resource limits** — quotas and rate limits for the failure boundary
5. **Exception grants** — any deviations from standard boundary policy, with justification
6. **Violation response plan** — how violations at each severity level will be handled
7. **Breakaway trust cut procedure** — the specific steps to sever all trust boundaries during breakaway
