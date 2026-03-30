# Kernel-to-Family Map — Construction Specification Kernel

## Family Position

This kernel is one of five truth kernels in the construction-kernel family, plus the intelligence layer.

## Family Members

| Kernel | Role | Truth Surface |
|---|---|---|
| **Construction_Specification_Kernel** (this) | specification-kernel | Specification documents, requirements, prohibitions, allowances, submittals, testing, warranties, qualifications |
| Construction_Assembly_Kernel | assembly-kernel | Assembly configurations, layer sequences, attachment methods |
| Construction_Material_Kernel | material-kernel | Material properties, physical characteristics, degradation behavior |
| Construction_Chemistry_Kernel | chemistry-kernel | Chemical interactions, adhesion mechanisms, cure behavior |
| Construction_Scope_Kernel | scope-kernel | Project scope boundaries, trade responsibilities, division of work |
| Construction_Reference_Intelligence | intelligence-layer | Pattern analysis, risk scoring, cross-kernel correlation |

## How This Kernel Fits

### Upstream Providers
- **Shared artifacts** from Construction_Reference_Intelligence/shared/ provide registries, enums, and taxonomy
- This kernel consumes shared artifacts by reference; it does not modify them

### Downstream Consumers
- **Construction_Reference_Intelligence** reads specification truth for pattern analysis and risk assessment
- **Sibling kernels** reference specification record IDs in their own records

### Peer Coordination
- **Assembly kernel** references spec requirements that mandate assembly types
- **Material kernel** references spec requirements that set performance thresholds
- **Chemistry kernel** references spec prohibitions on chemical contact
- **Scope kernel** references spec sections for scope delineation

## Non-Duplication Rule

Each truth surface is owned by exactly one kernel. This kernel does not duplicate assembly, material, chemistry, or scope truth. Cross-kernel coordination uses ID pointers, never embedded copies.

## Family Governance

All kernels are registered in ValidKernel_Registry. Schema versions are coordinated at baseline freezes. Shared artifacts are immutable within a baseline.
