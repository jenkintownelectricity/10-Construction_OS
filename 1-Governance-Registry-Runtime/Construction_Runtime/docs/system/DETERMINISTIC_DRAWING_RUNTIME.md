# Deterministic Drawing Runtime

## Purpose

Define the runtime engine that consumes governed Construction OS models and emits deterministic drawing outputs. The runtime is an execution engine, not a source of construction truth.

---

## Runtime Role

The drawing runtime:
- Loads governed construction inputs (assemblies, materials, interfaces, scope, view intent, detail applicability)
- Validates required inputs before processing
- Resolves applicable canonical detail logic
- Parameterizes canonical detail logic with concrete values
- Emits Drawing Instruction IR
- Renders deterministic outputs from the IR
- Fails closed on unresolved conditions
- Logs all decisions for audit traceability
- Produces derived output surfaces for downstream app consumption

---

## Runtime Boundaries

The runtime must NOT:
- Define material classes, detail logic, view intent, or scope rules
- Infer construction logic not present in governed inputs
- Silently resolve unresolved conditions
- Create canonical execution or navigation logic
- Modify domain truth

The runtime MUST:
- Consume only governed canonical inputs
- Produce deterministic outputs from those inputs
- Fail closed on missing or ambiguous inputs
- Record all decisions in audit logs

---

## Execution Pipeline Stages

1. **Input Validation** — validate presence and integrity of all governed inputs
2. **Detail Resolution** — select canonical detail logic from applicability rules
3. **Parameterization** — bind parameters to concrete values
4. **IR Emission** — emit construction-semantic Drawing Instruction IR
5. **Rendering** — produce SVG/DXF from the IR
6. **Audit Logging** — record decisions and failures
7. **Derived Outputs** — produce issues, routes, reviews, condition packets

---

## Fail-Closed Posture

Every pipeline stage enforces fail-closed behavior. If any stage cannot complete with governed inputs:
- Execution stops at that stage
- The failure is classified and recorded
- Derived outputs surface the failure
- No partial or inferred output is produced

---

## Audit Logging Posture

Every pipeline run produces an audit log recording:
- Selected detail ID
- Parameter set used
- IR generation status
- Renderer status
- Failure reason (classified by failure taxonomy)
- Stage-by-stage progression

---

## Deterministic Output Rule

Given the same governed inputs, the runtime must produce identical:
- Detail resolution
- Parameterization result
- IR output
- Rendered output
- Derived issue outputs
- Derived route outputs
- Condition packet outputs

---

## Safety Note

- This document defines runtime architecture documentation only
- Runtime code changes are bounded to execution surfaces authorized in Wave 6
- No domain truth definitions are created by the runtime
