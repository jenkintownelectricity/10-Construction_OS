# Construction OS — Fabric Session Landing Contract v0.1

**Authority:** Armand Lefebvre — Lefebvre Design Solutions LLC
**Version:** v0.1
**Status:** LANDING_CONTRACT_LOCKED
**Classification:** DOMAIN_ENTRY_CONTRACT
**Target Repo:** Construction_Application_OS (write)
**Observer Repos:** Governed-Multi-Domain-OS-Fabric (read-only), Construction_OS_Registry (read-only)

---

## 1. Purpose

This document defines how Construction_Application_OS receives a Fabric session envelope and resolves the initial control-tower landing surface. The landing contract is an entry-point contract only. It does not grant Fabric authority over Construction OS truth, runtime execution, registry topology, atlas semantics, cognitive policies, or application internals.

---

## 2. Standalone Validity Clause

**Construction OS remains standalone-valid and may execute independently of Fabric.**

This clause is non-negotiable. No governance amendment, fabric update, or session envelope may weaken this invariant. Construction OS operates with or without a Fabric session envelope.

---

## 3. Landing Contract Role

The landing contract:

- Receives a Fabric session envelope
- Validates envelope schema and field constraints
- Resolves the initial control-tower surface from `initial_view`
- Preserves `return_route` as metadata for later Fabric return navigation
- Returns a bounded landing result in metadata form

The landing contract must **NOT**:

- Execute runtime actions
- Mutate topology
- Accept authority escalation fields
- Accept identity, auth tokens, secrets, or permission grants
- Import or invoke Fabric runtime code
- Depend on environment variables (`process.env`)
- Perform cross-repo writes

---

## 4. Accepted Envelope Fields

The landing contract may consume only these fields from the Fabric session envelope:

| Field | Purpose |
|---|---|
| `envelope_id` | Session tracking metadata |
| `domain_id` | Domain identity validation |
| `domain_key` | Domain key validation |
| `launch_origin` | Provenance label |
| `target_surface` | Landing surface reference |
| `initial_view` | View to resolve on landing |
| `observer_mode` | Must be true |
| `branding_ref` | Display metadata |
| `registry_ref` | Registry reference (read-only) |
| `launch_route` | Fabric-side route metadata |
| `return_route` | Fabric return navigation metadata |
| `session_scope` | Must be metadata_only |
| `readiness_state` | Fabric readiness assessment |
| `standalone_valid` | Must be true |
| `created_from` | Provenance label |
| `notes` | Governance notes |

All other fields are rejected.

---

## 5. Rejected Fields

The landing contract must reject any envelope containing:

- User identity fields
- Auth tokens or secrets
- Permission grants
- Runtime commands
- Topology mutation rights
- Kernel/atlas/cognitive authority fields
- Mutable application session state

---

## 6. Observer Mode Rule

If `observer_mode` is not `true`, the landing contract must **FAIL_CLOSED**.

Construction OS must not enter elevated execution mode via Fabric handoff.

---

## 7. Landing Surface Resolution

The `initial_view` field maps to allowed Construction Application OS surfaces:

| initial_view | Landing Surface |
|---|---|
| `workspace` | Control tower workspace surface |
| `dashboard` | Control tower dashboard surface |
| `atlas` | Atlas navigation surface |
| `inspector` | Inspector surface |

Any unknown `initial_view` value: **FAIL_CLOSED**.

---

## 8. Return Route Rule

The landing contract retains `return_route` as metadata only for later Fabric return navigation.

- No external routing logic
- No redirect execution
- No cross-repo handoff call
- The return route is preserved as a string reference, not an active navigation command

---

## 9. Fabric Boundary Rule

Construction_Application_OS may reference the Fabric session envelope schema as an **external contract definition only**.

Construction_Application_OS must **NOT**:

- Import Fabric runtime modules
- Import Fabric bridge implementations
- Import Fabric loaders, validators, or route handlers
- Depend on Fabric process state or environment variables

---

*This document is locked at v0.1. Changes require governance amendment under Construction OS authority.*
