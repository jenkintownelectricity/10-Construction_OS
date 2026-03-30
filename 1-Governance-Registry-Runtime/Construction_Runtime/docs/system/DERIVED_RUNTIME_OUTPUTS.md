# Derived Runtime Outputs

## Purpose

Document the derived, non-canonical, recomputable output surfaces produced by the deterministic drawing runtime. These outputs support downstream app consumption, navigation, review, and issue tracking.

---

## Non-Canonical / Recomputable Rule

All derived outputs are:
- **Derived** — computed from governed truth plus runtime state
- **Non-canonical** — they are not sources of truth
- **Recomputable** — they can be regenerated from the same inputs at any time
- **Observational** — they summarize conditions; they do not declare design correctness

Derived outputs must never be stored or treated as canonical truth.

---

## Derived Issue Surface

Produces structured runtime issues for unresolved conditions:

| Issue Type | Description |
|---|---|
| `missing_required_input` | A governed input is absent |
| `unresolved_detail_applicability` | No detail matches the condition |
| `conflicting_detail_applicability` | Ambiguous detail match |
| `unknown_material_reference` | Material class not in canonical taxonomy |
| `unsupported_parameterization` | Parameter cannot be resolved |
| `incomplete_interface_context` | Required interface context missing |
| `unresolved_scope_condition` | Scope cannot be determined |

Issues are structured for indexing, filtering, and routing to review workflows.

---

## Derived Route Surface

Produces a dependency/blocking path from governed conditions to runtime success or failure:

```
condition
  → input validation (pass/fail)
  → detail resolution (pass/fail)
  → parameterization (pass/fail)
  → IR emission (pass/fail)
  → rendering (pass/fail)
```

Route discipline rule: Routes are derived strictly from existing domain relationships (composition, interface, scope, view intent, detail applicability) and runtime stage transitions. Runtime must not invent new relationship types.

---

## Derived Review Surface

Produces review-ready summaries for downstream consumption:
- Blocking conditions
- Coordination-required conditions
- Unresolved material conflicts
- Unresolved scope conflicts
- Completed pipeline stages

Review discipline rule: Review surfaces summarize unresolved, conflicting, or completed governed conditions and runtime outcomes. They must not declare design correctness, invent construction recommendations, or create new truth.

---

## Structured Output Rule

Derived surfaces produce structured outputs suitable for:
- Indexing and search
- Navigation overlays
- Issue aggregation dashboards
- Readiness dashboards
- Auto-RFI drafting (future)
- Constructability review (future)
- Execution sequencing support (future)

---

## Canonical Identity Reference Rule

Derived outputs must reference canonical object identities where available:
- `condition_id`
- `assembly_id`
- `component_id`
- `detail_id`
- Other governed references needed for graph navigability

---

## Future-Use Note

The derived outputs created here are intended to accelerate later work on:
- Construction Navigation Kernel
- Construction Execution Kernel
- Auto-RFI support
- Constructability review dashboards
- Condition-centric app navigation

These future capabilities are not implemented in this wave.

---

## Safety Note

- Derived outputs are non-canonical and recomputable
- No new construction truth is created
- No runtime behavior beyond documentation is modified in this section
