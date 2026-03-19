# Runtime Failure Taxonomy

## Purpose

Define the governed failure classes for the deterministic drawing runtime. Every runtime failure must be classified. Unclassified failures are governance violations.

---

## Failure Classes

| Failure Code | Stage | Description |
|---|---|---|
| `missing_required_input` | Input Validation | A required governed input is absent |
| `invalid_input_type` | Input Validation | Input data is not in expected format |
| `invalid_material_reference` | Input Validation | Material reference is empty or malformed |
| `incomplete_view_intent` | Input Validation | View intent missing required fields |
| `unresolved_detail_applicability` | Detail Resolution | No governed detail matches the condition |
| `conflicting_detail_applicability` | Detail Resolution | Multiple details match at equal priority |
| `unsupported_parameterization` | Parameterization | A required parameter cannot be resolved |
| `unknown_material_reference` | Parameterization | Material parameter references undefined class |
| `incomplete_interface_context` | Input Validation | Required interface context is missing |
| `unresolved_scope_condition` | Input Validation | Scope classification cannot be determined |
| `ir_emission_failure` | IR Emission | IR cannot be emitted from available inputs |
| `renderer_failure` | Rendering | Renderer cannot produce output from IR |

---

## Failure Posture

- Every failure must be classified by one of the above codes
- Every failure must be recorded in the audit log
- Every failure must stop pipeline execution at the failing stage
- No silent fallback or default behavior is permitted
- Derived issue surfaces must surface all failures for review

---

## Failure Resolution

Runtime failures are surfaced, not resolved, by the runtime. Resolution requires:
- Correcting the governed input (material, interface, scope, etc.)
- Adding a new governed applicability rule (if the condition is valid but unmatched)
- Adding a new canonical detail logic definition (if a true logic gap exists)

The runtime must not attempt automatic resolution.

---

## Safety Note

- This document defines failure taxonomy documentation only
- No runtime behavior beyond documentation is modified
