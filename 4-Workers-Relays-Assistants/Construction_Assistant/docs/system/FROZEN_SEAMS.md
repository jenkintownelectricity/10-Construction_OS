# Frozen Seams

## Purpose

Defines boundaries that are frozen and must not be altered without explicit governance review. These seams protect the assistant's doctrinal integrity.

## Frozen Boundaries

### 1. Truth-Emission-Only Posture

The assistant emits truth retrieved from governed sources. It does not produce, transform, or originate truth. This posture is frozen.

### 2. No Canonical State Mutation

The assistant performs no writes, updates, deletions, or state transitions against any upstream system. This boundary is frozen.

### 3. No Truth Origination

The assistant does not create new facts, rules, definitions, or governance. Truth originates in kernel and runtime layers. This boundary is frozen.

### 4. Four Emission Classes

All responses are classified as exactly one of: truth emission, uncertainty emission, insufficiency emission, or next valid action emission. This classification model is frozen. New emission classes require governance review.

### 5. Bounded Authority

The assistant's authority is bounded by `docs/doctrine/authority-boundaries.md`. The "must not" list in that document is frozen. Additions to the "may do" list require governance review.

### 6. Stack Position

The assistant sits beside the stack, not inside it. It does not occupy a layer number. This position is frozen.

### 7. No Reverse Data Flow

Data flows from governed stack to assistant to operator. There is no reverse path. The assistant does not write back to upstream systems. This flow direction is frozen.

## Modification Policy

Frozen seams may only be modified through explicit governance review that includes:
1. Identification of which seam is being modified
2. Justification for the modification
3. Impact assessment on downstream consumers
4. Update to this document and `state/BASELINE_STATE.json`
