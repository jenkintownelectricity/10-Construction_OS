# Truth Model — Construction Assembly Kernel

## Definition of Assembly Truth

Assembly truth is a validated record of how building enclosure components are organized into layered systems with explicit control-layer assignments. An assembly truth record states: these layers, in this order, with these control-layer assignments, attached by these methods, produce a system that addresses these control functions.

## What Constitutes Truth in This Kernel

### Layer Stack Truth

A valid layer stack records:
- Ordered layers from exterior (position 1) to interior (position N)
- Each layer's control-layer assignment (which of the 11 control layers it serves)
- Each layer's material reference (pointer to Material Kernel entry)
- Each layer's attachment method to the layer below or above

A layer stack is not truth until all required fields are populated and the record passes schema validation.

### Control-Layer Assignment Truth

A valid control-layer assignment records:
- Which assembly contains the assignment
- Which control layer ID is assigned
- The continuity status: continuous, interrupted, terminated, or transitioned

Assignment truth is specific to an assembly. The same control layer may be continuous in one assembly and interrupted in another.

### Interface Condition Truth

Transitions, penetrations, edges, and tie-ins record how assemblies interact at boundaries. Interface truth states:
- Which assemblies are involved
- Which interface zone applies
- Which control layers are maintained, interrupted, or terminated at the interface
- What detail or method is used

### Tested Assembly Truth

A tested assembly record documents a specific configuration validated by a specific test under a specific standard. The truth is narrow: this exact configuration, tested this way, produced this result. No extrapolation.

### Continuity Requirement Truth

A continuity requirement states a rule: for a given control layer, under given conditions, the layer must be continuous, may be interrupted, must terminate, or must transition. Requirements are scope-bounded.

## Truth Validation Rules

1. **Schema compliance** — Every record must pass its JSON Schema validation.
2. **Required field completeness** — All required fields must be populated with valid values.
3. **Enum conformance** — All enum fields must use values from the shared registry or schema-defined enums.
4. **Reference validity** — Cross-kernel references (material_ref, spec_ref) must be syntactically valid identifiers.
5. **Status gating** — Records with missing data or flagged ambiguities must remain in `draft` status.

## Truth Does Not Include

- Inferred properties (material strength, chemical compatibility) — owned by sibling kernels
- Performance predictions — owned by engineering analysis tools
- Design recommendations — owned by the Reference Intelligence layer
- Cost or schedule data — outside kernel family scope
