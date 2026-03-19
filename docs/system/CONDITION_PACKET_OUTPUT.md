# Condition Packet Output

## Purpose

Define the structure and boundaries of the condition packet — a single app-ready structured runtime packet produced per construction condition.

---

## Packet Boundaries

The condition packet is:
- **Derived** — assembled from governed truth plus runtime state
- **Non-canonical** — not a source of truth
- **Recomputable** — regenerable from the same inputs
- **Convenience output** — designed for downstream app consumption

The condition packet aggregates runtime state without redefining domain truth.

---

## Required Identity References

| Field | Description |
|---|---|
| `condition_id` | Governed condition identifier |
| `assembly_id` | Parent assembly identity |
| `component_ids` | Component identities within the condition |
| `detail_id` | Resolved canonical detail identifier |
| `view_intent_id` | View intent type reference |

---

## Required Status Surfaces

| Field | Description |
|---|---|
| `parameter_state` | resolved / unresolved |
| `issue_state` | clear / N_blocking / non_blocking |
| `route_state` | success / failed_at_stage |
| `render_state` | rendered / not_rendered |
| `readiness_state` | ready / incomplete / blocked |

---

## Readiness State Posture

| State | Meaning |
|---|---|
| `ready` | All stages passed, rendering complete, no blocking issues |
| `incomplete` | Some stages passed but gaps exist |
| `blocked` | Pipeline failed at a critical stage |

---

## Output Artifact References

The packet may reference output artifacts:
- `svg:{detail_id}` — rendered SVG output
- `dxf:{detail_id}` — rendered DXF output (when available)

---

## App-Consumption Note

The condition packet is designed for consumption by:
- Review dashboards
- Navigation interfaces
- Issue tracking surfaces
- Readiness indicators
- Package assembly workflows

Downstream apps consume the packet. They do not modify it or treat it as canonical truth.

---

## Fail-Closed Gap Reporting Rule

If the condition packet cannot be assembled from governed truth plus runtime state, the packet must surface explicit gaps rather than filling them by inference. The `gaps` field lists specific missing elements.

---

## Safety Note

- The condition packet is non-canonical and recomputable
- No new construction truth is created by the packet
