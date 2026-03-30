# Dependency Map

## Upstream Dependencies

### Universal_Truth_Kernel (Layer 0)

- **Relationship:** Conceptual doctrinal reference.
- **What is consumed:** Root doctrine principles that bound all system behavior.
- **How consumed:** Referenced for alignment. Not consumed as code or data at runtime.
- **No code inheritance.**

### Construction_Kernel (Layer 5)

- **Relationship:** Domain truth source.
- **What is consumed:** Truth surfaces from 7 domain kernels (Governance, Geometry, Chemistry, Assembly, Reality, Deliverable, Intelligence).
- **How consumed:** Read-only query against exposed truth surfaces.
- **No code inheritance.**

### Construction_Runtime (Layer 6)

- **Relationship:** Execution state source.
- **What is consumed:** Pipeline state (parse, normalize, validate, generate, audit), validation results, execution status.
- **How consumed:** Read-only query against execution state surfaces.
- **No code inheritance.**

### Construction_Application_OS (Layer 7)

- **Relationship:** Application state source.
- **What is consumed:** Application state from Assembly Parser and Spec Intelligence, workflow positions.
- **How consumed:** Read-only query against application state surfaces.
- **No code inheritance.**

## Downstream Dependents

### Operator-Facing Query Responses

- **Relationship:** Output-only.
- **What is produced:** Bounded emissions classified as truth, uncertainty, insufficiency, or next valid action.
- **Who consumes:** Human operators and system consumers querying the assistant.

## Dependency Constraints

1. All upstream dependencies are read-only. No write path exists.
2. No code, schema, or artifact is inherited from upstream repos. The relationship is surface-based, not inheritance-based.
3. If an upstream surface becomes unavailable, the assistant emits an insufficiency emission. It does not cache or fabricate a substitute.
4. Upstream changes that alter truth surfaces require reaudit of this repo's maps and routing model.
