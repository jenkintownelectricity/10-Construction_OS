# Construction Application OS v0.1

## Identity

Construction_Application_OS is the application coordination layer (Layer 7) in the ValidKernel/Construction stack. It sits above Construction_Runtime and below user-facing construction applications.

## Purpose

Define and coordinate user-facing construction applications. This layer owns application specifications, workflows, role models, and app-to-runtime/kernel mappings. It does not own truth, governance, topology, or runtime execution.

## Current Applications

### 1. Assembly Parser App

- **Purpose**: Transform manufacturer assembly letters into structured assembly outputs and shop drawing preparation artifacts
- **Runtime Dependencies**: Contract schemas, structural validator, domain validator, geometry engine, DrawingInstructionSet generation, DXF writer, SVG writer, audit logger
- **Kernel Dependencies**: Chemistry, Assembly, Geometry, Deliverable
- **Upstream Truth Posture**: Consumes applied construction truth ultimately grounded in Universal_Truth_Kernel
- **Pipeline**: Raw input → Parse → Validate (structural + domain) → Assembly engine → Geometry engine → DrawingInstructionSet → DXF/SVG generation → DeliverableModel → Audit log

### 2. Spec Intelligence App

- **Purpose**: Transform specifications into structured product/system opportunity intelligence
- **Runtime Dependencies**: Contract schemas, structural validator, domain validator, spec parser/spec engine, validator surfaces, audit logger
- **Kernel Dependencies**: Governance, Chemistry, Geometry, Intelligence
- **Upstream Truth Posture**: Consumes applied construction truth ultimately grounded in Universal_Truth_Kernel
- **Pipeline**: Raw input → Parse → Validate (structural + domain) → Spec engine → Intelligence output → Audit log

## Workflows

- Assembly-to-shop-drawing workflow (Assembly Parser App)
- Spec-to-opportunity workflow (Spec Intelligence App)

## Roles

- **Project Manager**: Initiates workflows, reviews outputs
- **Estimator**: Consumes spec intelligence for opportunity evaluation
- **Detailer**: Reviews and finalizes shop drawing outputs
- **System**: Automated pipeline execution

## Boundaries

- This layer coordinates; it does not execute. Execution belongs to Construction_Runtime.
- This layer references kernel truth; it does not define it. Truth belongs to Construction_Kernel.
- This layer consumes governance; it does not define it. Governance belongs to ValidKernel-Governance.
