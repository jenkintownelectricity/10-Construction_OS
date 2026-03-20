# Mirror Activation Policy

**Command:** COMMAND I -- ACTIVATION GATE
**Status:** Normative
**Scope:** All mirrors in the Construction Kernel

---

## 1. Purpose

No mirror may transition to the ACTIVE lifecycle state without passing every
activation check defined in this document. The activation gate is the single
authority that governs whether a mirror is safe, complete, and structurally
sound enough to participate in live kernel operations.

A mirror that has not cleared the activation gate remains in the STAGED state.
There are no exceptions, overrides, or partial activations. A mirror is either
fully activated or it is not activated at all.

---

## 2. Fail-Closed Principle

The activation gate operates on a **fail-closed** model:

- If ANY single check fails, the entire activation is **denied**.
- If any check cannot be evaluated (missing data, schema unavailable, timeout),
  the result is treated as a **failure**.
- If the activation gate process itself encounters an unexpected error, the
  mirror remains STAGED.

The gate never defaults to "allow." Ambiguity is treated as failure. Silence is
treated as failure. The only path to ACTIVE is an explicit, recorded pass on
every condition.

---

## 3. Activation Conditions

A mirror must satisfy all eight of the following conditions. They are evaluated
in order. Evaluation stops at the first failure unless the gate is running in
`--full-report` mode, in which case all conditions are evaluated and every
failure is collected.

### Condition 1: Manifest Schema Validation

The mirror's manifest file must validate against the canonical schema
`mirror-manifest.schema.json` located in the `schemas/` directory.

- The manifest must be present at the expected path within the mirror directory.
- The manifest must be valid JSON.
- Every required field defined in the schema must be present and correctly typed.
- No additional properties are allowed unless the schema explicitly permits them.
- If the schema file itself is missing or unparseable, this condition fails.

**Failure reason:** `MANIFEST_SCHEMA_INVALID`

### Condition 2: Registry Entry Exists

The mirror must have a corresponding entry in the `mirrors-registry`. The
registry is the authoritative index of all known mirrors. A mirror that is not
registered cannot be activated regardless of its internal quality.

- The registry entry must reference the correct mirror identifier.
- The entry must not be marked as `deprecated` or `removed`.
- The entry's version field must match the manifest version.

**Failure reason:** `REGISTRY_ENTRY_MISSING`

### Condition 3: Trust Boundary Definition

The mirror must have a trust boundary definition that is present and complete.
Trust boundaries declare the security and integration perimeter of the mirror --
what it may access, what may access it, and what data may cross its edges.

- The trust boundary document must exist.
- All required sections must be populated (ingress rules, egress rules,
  data classification, dependency declarations).
- No section may be empty or contain only placeholder text.

**Failure reason:** `TRUST_BOUNDARY_INCOMPLETE`

### Condition 4: Slice Dependency Graph Validation

Every enabled slice within the mirror must validate against the kernel's
dependency graph. Slices are the functional subdivisions of a mirror, and their
dependencies must be explicitly declared and satisfiable.

- Each enabled slice must declare its dependencies.
- Every declared dependency must resolve to a known, non-deprecated entity.
- There must be no circular dependencies among the mirror's own slices.
- There must be no dependency on a slice or mirror that is itself not ACTIVE
  (unless the dependency is marked as `soft`).

**Failure reason:** `SLICE_DEPENDENCY_INVALID`

### Condition 5: Reflection Status Validation

Every reflection associated with the mirror must have a valid status entry.
Reflections are the traceability records that link a mirror's behavior to its
design intent.

- Each reflection must have a status of `pass`, `acknowledged`, or `deferred`.
- No reflection may have a status of `unknown`, `error`, or be missing entirely.
- Deferred reflections must include a justification and a target resolution date.

**Failure reason:** `REFLECTION_STATUS_INVALID`

### Condition 6: Minimum Fixture Set

The mirror must have a minimum number of parity fixtures for each active slice.
Fixtures are the concrete test cases that verify the mirror behaves correctly
under known conditions.

- Each active slice must have **at least 3 fixtures**.
- Fixtures must be parseable and structurally valid.
- Fixtures must reference the correct slice identifier.
- A slice with fewer than 3 fixtures is considered untested and blocks
  activation of the entire mirror.

**Failure reason:** `INSUFFICIENT_FIXTURES`

### Condition 7: Parity Baseline Report

A parity baseline report must exist for the mirror and must show no critical
failures. The parity baseline is the comparison between the mirror's current
behavior and the expected behavior defined by its reflections and fixtures.

- The report file must exist at the expected path.
- The report must have been generated within the current evaluation cycle (not
  stale).
- The report must contain zero entries with severity `critical`.
- Entries with severity `warning` are permitted but are logged for review.

**Failure reason:** `PARITY_BASELINE_CRITICAL`

### Condition 8: No Forbidden Patterns Detected (L0.9)

The mirror must be free of all forbidden patterns defined in the L0.9 rule set.
Forbidden patterns are structural or behavioral anti-patterns that compromise
kernel integrity, security, or maintainability. See Section 4 for the full list.

- The mirror's source, configuration, and manifest are scanned for each
  forbidden pattern.
- Detection of ANY forbidden pattern causes immediate failure.
- Each detected pattern is logged individually with its L0.9 identifier.

**Failure reason:** `FORBIDDEN_PATTERN_DETECTED`

---

## 4. L0.9 Forbidden Patterns

The following ten patterns are unconditionally forbidden in any mirror that
seeks ACTIVE status. These are not guidelines; they are hard constraints. A
mirror exhibiting any of these patterns cannot be activated.

| ID     | Pattern                                                        | Description |
|--------|----------------------------------------------------------------|-------------|
| L0.9-1 | Raw code sync between systems                                 | No mirror may synchronize source code directly between external systems. All code flow must pass through declared kernel interfaces. Raw sync creates hidden coupling and unauditable state. |
| L0.9-2 | Direct API coupling bypassing mirror                           | External systems must not call into or out of a mirror's internals without going through the mirror's declared API surface. Bypassing the mirror makes the trust boundary meaningless. |
| L0.9-3 | Mirror containing billing or tenant UI                         | Billing logic and tenant-facing user interface code must never reside inside a mirror. Mirrors are structural and operational; UI and billing belong in application layers. |
| L0.9-4 | Mirror importing application UX logic                          | A mirror must not import or depend on application-level UX code (components, stylesheets, interaction handlers). Mirrors operate below the UX layer. |
| L0.9-5 | ACTIVE slice with undeclared dependencies                      | Every dependency of an active slice must be explicitly declared. Implicit or discovered-at-runtime dependencies are forbidden because they cannot be validated by the dependency graph. |
| L0.9-6 | ACTIVE mirror without parity fixtures                          | An active mirror must have parity fixtures. This is also enforced by Condition 6, but L0.9-6 exists as a belt-and-suspenders rule to catch edge cases where fixture counts are manipulated. |
| L0.9-7 | Transfer-ready slice without detachment validation             | A slice marked as transfer-ready must have completed detachment validation proving it can operate independently. Without this, transfer could break the source mirror. |
| L0.9-8 | Mirror logic promoted into core without gate review            | Code or configuration from a mirror must not be promoted into the kernel core without passing a gate review. Unreviewed promotion can introduce untested or structurally unsound logic into the kernel. |
| L0.9-9 | Mirror treated as canonical core by accident                   | A mirror must not be referenced, depended on, or treated as if it were a core kernel component. Mirrors are by definition peripheral. If a mirror becomes load-bearing for core, it must be formally promoted through the gate. |
| L0.9-10| Undocumented fallback paths                                    | Every fallback path in a mirror (error recovery, degraded mode, default behavior) must be documented. Undocumented fallbacks create invisible control flow that cannot be audited or tested. |

---

## 5. Behavior on Failure

When the activation gate denies activation:

1. The mirror remains in the **STAGED** state. No partial activation occurs.
2. A failure report is generated containing:
   - The mirror identifier and version.
   - A timestamp of the evaluation.
   - The identity of the actor or system that triggered the evaluation.
   - Each failed condition, its failure reason code, and a human-readable
     explanation.
   - If `--full-report` mode was used, results for all conditions (including
     passes) are included.
3. The failure report is written to the mirror's state directory and to the
   kernel audit log.
4. No automatic retry is scheduled. Re-evaluation must be explicitly triggered
   after remediation.

---

## 6. Re-Evaluation After Remediation

A mirror that fails activation can be re-evaluated after the issues identified
in the failure report have been addressed.

- There is no limit on the number of re-evaluation attempts.
- Each re-evaluation is a full evaluation; there is no concept of "resuming"
  from a previous partial result.
- The re-evaluation must be explicitly triggered (see Section 7).
- Each re-evaluation produces its own independent report, which is appended to
  the audit trail. Previous failure reports are not overwritten or deleted.

---

## 7. Who Can Trigger Activation Evaluation

Activation evaluation can be triggered by:

1. **A kernel operator** running the activation gate command manually.
   Operators must have the `mirror:activate` permission.
2. **An automated pipeline** as part of a CI/CD or deployment workflow, provided
   the pipeline identity has the `mirror:activate` permission.
3. **The mirror itself** via a self-evaluation hook, but only if self-evaluation
   is enabled in the kernel configuration. Self-evaluation results are always
   flagged as `self-reported` in the audit trail.

Activation evaluation **cannot** be triggered by:

- Anonymous or unauthenticated actors.
- Actors with only read-level permissions on the mirror.
- External systems that are not registered in the kernel's identity registry.

---

## 8. Audit Trail Requirements

Every activation evaluation, whether it succeeds or fails, must produce an
audit record. The audit trail is append-only and must not be modified after
creation.

Each audit record must contain:

| Field                  | Description                                                |
|------------------------|------------------------------------------------------------|
| `evaluation_id`        | A unique identifier for this evaluation run.               |
| `mirror_id`            | The identifier of the mirror being evaluated.              |
| `mirror_version`       | The version of the mirror at evaluation time.              |
| `triggered_by`         | The identity of the actor or system that initiated the evaluation. |
| `trigger_method`       | How the evaluation was triggered (manual, pipeline, self). |
| `timestamp_start`      | When the evaluation began (UTC, ISO 8601).                 |
| `timestamp_end`        | When the evaluation completed (UTC, ISO 8601).             |
| `result`               | `ACTIVATED` or `DENIED`.                                   |
| `conditions_evaluated` | The number of conditions that were evaluated.              |
| `conditions_passed`    | The number of conditions that passed.                      |
| `conditions_failed`    | The number of conditions that failed.                      |
| `failure_reasons`      | A list of failure reason codes (empty if all passed).      |
| `failure_details`      | Human-readable details for each failure (empty if all passed). |
| `report_path`          | The file path to the full evaluation report.               |

Audit records are stored in the kernel's audit log at `state/audit/`. They are
never deleted. Retention policy is governed by the kernel's data governance
rules.

---

## 9. Relationship to Other Commands

- **COMMAND II (Registry Sync):** A mirror must have a registry entry
  (Condition 2) before it can be activated. Registry sync ensures the entry
  exists.
- **COMMAND III (Parity Evaluation):** The parity baseline report required by
  Condition 7 is produced by the parity evaluation process.
- **COMMAND IV (Slice Management):** Slice dependency validation (Condition 4)
  depends on accurate slice metadata maintained by slice management.
- **Runtime Implementation:** The Python implementation of the activation gate
  logic resides in `runtime/mirror_control/mirror_activation_gate.py`. This
  policy document is the authoritative specification; the implementation must
  conform to it.

---

## 10. Summary

The activation gate exists to enforce a single invariant: **no mirror becomes
ACTIVE unless it is fully validated**. This is achieved through eight mandatory
conditions, a fail-closed evaluation model, a prohibition on the ten L0.9
forbidden patterns, and an immutable audit trail. There are no shortcuts,
overrides, or grace periods. A mirror earns ACTIVE status by satisfying every
condition, or it remains STAGED until it does.
