# Non-Goals

## Purpose

This document defines what the Construction Scope Kernel explicitly does not attempt to do. These boundaries are permanent and load-bearing.

## Non-Goals

### 1. Specification Authoring
The Scope Kernel does not write, interpret, or validate material or product specifications. It references CSI sections but does not define their content.

### 2. Assembly Instruction Generation
The Scope Kernel sequences operations but does not generate step-by-step installation procedures. Assembly truth belongs to the Assembly Kernel.

### 3. Material Selection or Evaluation
The Scope Kernel identifies materials within scope boundaries but does not evaluate suitability, compatibility, or performance characteristics.

### 4. Cost Estimation
Work operations have scope but not cost. The Scope Kernel does not estimate, track, or validate cost data.

### 5. Schedule Generation
The Scope Kernel defines sequencing dependencies and hold points but does not generate project schedules or Gantt charts. Duration estimates are advisory only.

### 6. Code Interpretation
The Scope Kernel references building codes and standards but does not interpret code requirements. Code compliance truth belongs to the Reference Intelligence domain.

### 7. Design Decision-Making
The Scope Kernel records scope as defined by design documents. It does not make or recommend design decisions.

### 8. Conflict Resolution
When scope gaps or overlaps are detected, the Scope Kernel flags them. It does not resolve conflicts autonomously. Resolution requires human review.

### 9. Contract Enforcement
The Scope Kernel models trade responsibilities but does not enforce contractual obligations. It is a truth record, not a contract management system.

### 10. Quality Judgment
Inspection and commissioning steps define verification procedures. The Scope Kernel does not judge whether work passes or fails -- it defines what must be checked.

## Rationale

Each non-goal exists because the truth it represents belongs to a different kernel or requires human judgment that cannot be safely automated in a fail-closed system.
