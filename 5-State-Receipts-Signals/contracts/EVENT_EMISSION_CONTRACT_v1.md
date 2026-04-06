# Construction OS Event Emission Contract v1

**Authority:** L0_ARMAND_LEFEBVRE
**Status:** DRAFT
**Date:** 2026-04-06

---

## EMITTED EVENT TYPES

| Event Type | Trigger |
|-----------|--------|
| kernel.condition_detected | Condition identified during intake/context |
| kernel.assembly_resolved | Assembly system mapped from kernel truth |
| kernel.validation_passed | All VR rules pass |
| kernel.validation_failed | One or more VR rules fail |
| kernel.detail_generated | WLVOS generates a governed detail |
| kernel.artifact_ready | Compiled artifact ready for delivery |
| kernel.receipt_recorded | Governance receipt produced |
| kernel.state_changed | Project state transition |

## EMISSION RULES

1. Registry-backed only: every event MUST reference at least one entity with valid registry_id. BLOCKED otherwise.
2. Domain execution origin only: no UI-originated truth claims.
3. No truth transfer: emission is notification, not authority.
4. Schema compliance: conform to schemas/events/kernel_event.schema.json. BLOCKED otherwise.
5. Idempotency key required.
6. Correlation tracking: related events SHOULD share correlation_id.

## FAIL-CLOSED

- No registry_id: BLOCK emission
- Schema validation fails: BLOCK emission
- VKBUS unavailable: buffer locally, retry per delivery spec
- Unknown event_type: BLOCK emission
- Missing required fields: BLOCK emission

---

**END OF CONTRACT**
