# Truth Surface Map

## Purpose

Enumerates the truth surfaces the assistant may read from upstream systems. The assistant has no write access to any surface listed here.

## Layer 5: Construction_Kernel

| Surface | Kernel | Content |
|---|---|---|
| Governance truth surface | Governance Kernel | Rules, permissions, requirements, constraints governing construction activities. |
| Geometry truth surface | Geometry Kernel | Spatial definitions, dimensional requirements, geometric constraints. |
| Chemistry truth surface | Chemistry Kernel | Material compositions, chemical properties, compatibility rules. |
| Assembly truth surface | Assembly Kernel | Assembly definitions, component relationships, assembly sequences. |
| Reality truth surface | Reality Kernel | As-built conditions, field observations, reality state. |
| Deliverable truth surface | Deliverable Kernel | Deliverable definitions, submission requirements, package compositions. |
| Intelligence truth surface | Intelligence Kernel | Analytical outputs, pattern data, derived metrics from governed sources. |

## Layer 6: Construction_Runtime

| Surface | Content |
|---|---|
| Pipeline state surface | Current stage position within parse, normalize, validate, generate, audit pipeline. |
| Validation output surface | Pass/fail/warning results from runtime validation. |
| Execution state surface | Active/complete/pending status of runtime operations. |
| Audit trail surface | Audit records from the audit pipeline stage. |

## Layer 7: Construction_Application_OS

| Surface | Content |
|---|---|
| Assembly Parser state surface | Current state and output of Assembly Parser application. |
| Spec Intelligence state surface | Current state and output of Spec Intelligence application. |
| Workflow state surface | Current workflow position, next valid steps, completion status. |

## Access Constraints

1. All surfaces are read-only from the assistant's perspective.
2. No surface grants the assistant write, update, or delete capability.
3. Surface availability depends on upstream system state. If a surface is unavailable, the assistant emits an insufficiency emission.
4. Surface schema and content are owned by the upstream system. The assistant does not define or modify surface structure.
