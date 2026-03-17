# Assembly Parser App

## Purpose
Transform manufacturer assembly letters into structured assembly outputs and shop drawing preparation artifacts.

## Stack Alignment
- **Kernel**: Construction_Kernel (Chemistry, Assembly, Geometry, Deliverable kernels)
- **Runtime**: Construction_Runtime v0.2
- **Truth Posture**: Consumes applied construction truth ultimately grounded in Universal_Truth_Kernel

## Capabilities
- Parse and normalize raw assembly letter text
- Extract components, constraints, and assembly structure
- Validate structural and domain correctness
- Generate deterministic geometry via DrawingInstructionSet
- Produce dual-format deliverables (DXF + SVG)
- Emit append-only audit trail

## Status
Active — v0.1
