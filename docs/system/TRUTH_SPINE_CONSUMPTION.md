# Truth Spine Consumption Note

## 1. Purpose

This document defines the relationship between Construction_Runtime and the Construction Truth Spine.

---

## 2. Core Rule

Construction_Runtime consumes truth; it does not define it.

The Construction Truth Spine is defined by governance doctrine (`ValidKernel-Governance/docs/validkernel/construction-truth-spine-doctrine.md`) and architecturally specified in `Construction_Kernel/docs/system/CONSTRUCTION_TRUTH_SPINE.md`. Construction_Runtime operates against these definitions. It does not author, redefine, or override them.

---

## 3. Runtime Consumption Posture

Runtime validation and generation should later rely on Truth Spine state and event history. When the Truth Spine is implemented, runtime components will:

- Read truth state from the spine
- Validate against spine-recorded state transitions
- Generate outputs based on spine-verified truth conditions

---

## 4. Runtime Must Not Override Truth

Runtime must not silently override canonical truth history. If runtime detects a conflict between its internal state and Truth Spine records, runtime must surface the conflict — not resolve it by overwriting spine history.

---

## 5. Runtime Must Not Invent Continuity

Runtime must not invent object continuity where identity is unresolved. If an object's identity is provisional or unresolved in the Truth Spine, runtime must treat it as provisional. Runtime must not assume or assert durable object identity that the spine has not confirmed.

---

## 6. Comparison Capabilities

Runtime may compare truth states across the spine:

| Comparison | Purpose |
|------------|---------|
| proposed vs approved | Identify changes between intent and authorization |
| approved vs built | Identify departures from approved conditions |
| built vs observed | Identify discrepancies between claims and verification |
| observed vs documented | Identify gaps between verified conditions and formal records |

These comparisons depend on the Truth Spine providing reliable state history.

---

## 7. Scope of This Pass

Runtime behavior is not changed in this pass. This document establishes the architectural relationship only. No runtime code, schemas, validators, pipelines, or contracts are modified.

---

## Safety Note

- This document defines architectural consumption posture only.
- No runtime code, schemas, or implementations are modified.
- No existing contracts or frozen seams are changed.
