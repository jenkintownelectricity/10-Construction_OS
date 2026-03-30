# FROZEN_SEAMS — Construction_Runtime

## Frozen Seams

These seams are locked at v0.2 authority. They must not be casually redefined.

### Contract Schemas

Six JSON schemas frozen at v0.2: assembly_input, runtime_assembly, spec_input, runtime_spec, drawing_instruction, deliverable. These define the pipeline stage boundaries and are the authoritative interface between stages.

### Three-Stage Validation

Validation proceeds in fixed order: structural → domain → generation. No stage may be skipped, reordered, or bypassed. Fail-closed at every stage.

### Error Taxonomy

62 error codes across 11 categories. The taxonomy structure is frozen at the runtime level. New codes may be appended to existing categories; categories and existing codes must not be redefined. This is a runtime-level standard, not kernel-level canonical truth.

### DrawingInstructionSet

The governed intermediate representation for this runtime. DrawingInstructionSet is the sole input to both DXF and SVG generation. No generation path may accept input from any other source. Note: "governed" here means authoritative within the runtime's scope — it is not kernel-level canonical truth.

### Dual-Output Derivation

DXF and SVG derive from the identical DrawingInstructionSet. They must not derive from separate or divergent sources. This guarantees output equivalence.

### Audit Event Model

Append-only audit logging with cryptographic hashes and 9 event types. Audit records must never be mutated or deleted.

### Provenance and Authority Handling

Dimension authority statuses: EXPLICIT, DERIVED, INFERRED, UNAPPROVED. These status levels and their semantics are frozen.

### Layer Standards

10 governed A- layers with ACI color indices. Layer names and color assignments are frozen. This is a runtime-level standard, not kernel-level canonical truth.

### Deliverable Model Format

The deliverable model structure is frozen at v0.2.

## Boundary Rules

- Runtime executes applied construction truth from Construction_Kernel; it does not define construction ontology.
- Runtime does not originate universal truth.
- Runtime does not define governance rules.
- Apps in this repo are demos; application shell behavior belongs to Construction_Application_OS.

## Must Not Be Casually Redefined

- Contract schemas
- Validation stage order (structural → domain → generation)
- Error taxonomy structure
- DrawingInstructionSet as governed intermediate representation
- Dual-output derivation from single instruction set
- Audit append-only model
- Authority status levels (EXPLICIT / DERIVED / INFERRED / UNAPPROVED)
- Layer standard names and ACI color indices

## May Evolve

- Parser extraction logic and accuracy
- Geometry layout algorithms and rules parameters
- Engine internals (assembly, constraint, spec)
- Adapter implementations
- New entity types in DrawingInstructionSet (with schema versioning)
- New error codes (appended to existing categories only)
- Test fixtures and test coverage

## Invalid Drift

- Runtime defining construction truth (belongs to Construction_Kernel)
- Runtime bypassing validation stages
- Runtime generating DXF/SVG from separate sources (must share DrawingInstructionSet)
- Audit log mutation or deletion
- Silent validation failures (fail-closed is mandatory)

## Safe Changes

- Improving parser accuracy
- Adding geometry rules
- Extending DrawingInstructionSet entity types (with schema versioning)
- Appending error codes to existing categories
- Adding tests
- Improving adapter logic
