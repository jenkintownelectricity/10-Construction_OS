# IR Rendering Pipeline

## Purpose

Document the governed pipeline that transforms construction inputs into rendered drawing outputs through the Drawing Instruction IR.

---

## Governed Inputs

The pipeline consumes these governed inputs from Construction_Kernel:

| Input | Source |
|---|---|
| Assembly composition | Construction Assembly Composition Model |
| Material classes | Construction Material Taxonomy |
| Interface conditions | Interface and Adjacent Systems Model |
| Scope classifications | Scope Boundary Model |
| View intent | View Intent Model |
| Detail applicability | Detail Applicability Model |
| Detail schema | Construction Detail Schema |
| IR specification | Drawing Instruction IR |

---

## Pipeline Stages

### 1. Validation Stage

Validates presence and integrity of all required governed inputs. Checks:
- Condition identifier present
- Assembly type declared
- Interface type declared
- Material references use canonical classes
- View intent complete (type and depth)
- Parameters provided

Fail-closed: missing or ambiguous inputs stop execution.

### 2. Detail Resolution Stage

Selects the applicable canonical detail logic from governed applicability rules. The resolver:
- Matches condition pattern against applicability rules
- Selects highest-priority match
- Rejects ambiguous matches at equal priority
- Returns components, relationships, and parameter bindings

Fail-closed: no match or ambiguous match stops execution.

### 3. Parameterization Stage

Binds abstract parameters to concrete values:
- Material parameters resolved to canonical material classes
- Dimensional parameters bound from condition inputs
- Attachment and spacing parameters resolved

Fail-closed: unresolvable parameters stop execution.

### 4. IR Emission Stage

Emits Drawing Instruction IR from resolved detail logic:
- View boundary and depth instructions
- Component draw instructions with material references
- Relationship draw instructions
- Symbol placement (fasteners, anchors)
- Material tags, annotations, dimensions

All instructions are construction-semantic. No CAD commands.

Fail-closed: incomplete references stop emission.

### 5. Rendering Stage

Produces format-specific output from the IR:
- SVG renderer for preview and web display
- DXF renderer (stub) for CAD integration

All renderers consume the same IR. No renderer invents construction logic. Renderers make geometric decisions only.

### 6. Audit Logging Stage

Records the complete pipeline execution:
- Stage progression with timestamps
- Selected detail and parameters
- Instruction counts
- Success or failure with classified reason
- All errors and warnings

---

## Single-IR Rule

All renderers must consume the same IR. Preview output and production output derive from the same instruction set. No renderer may receive different instructions.

---

## Safety Note

- This document defines pipeline architecture documentation only
- No domain truth is created by the pipeline
