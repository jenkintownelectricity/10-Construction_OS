# Chemistry Kernel Reference Intelligence Linkage

## Purpose

Defines how the Chemistry Kernel connects to the Construction Reference Intelligence layer and what data flows in each direction.

## Linkage Direction

**Chemistry Kernel → Reference Intelligence** (publish only)

This kernel publishes chemistry truth. Reference Intelligence consumes, synthesizes, and delivers cross-kernel insights. This kernel does not consume intelligence-layer outputs.

## What Chemistry Kernel Publishes

| Data Type | Format | Consumer Use |
|---|---|---|
| Incompatibility rules | JSON records with typed IDs | Risk identification at material transitions |
| Adhesion rules | JSON records with substrate + chemistry refs | Assembly feasibility validation |
| Cure mechanisms | JSON records with environmental ranges | Schedule and weather dependency analysis |
| Degradation mechanisms | JSON records with pathway + rate factors | Lifecycle risk assessment |
| Solvent systems | JSON records with VOC + flash point | Regulatory compliance checking |
| Chemical hazard records | JSON records with hazard type + precautions | Safety planning support |

## Shared Artifacts

Shared family artifacts are maintained in Construction_Reference_Intelligence:
- `shared/FAMILY_CONTEXT.md` — Family architecture
- `shared/control_layers.json` — Control layer registry
- `shared/interface_zones.json` — Interface zone registry
- `shared/division_07_posture.json` — Division 07 domain posture

This kernel references these artifacts but does not duplicate them.

## Cross-Kernel Reference Resolution

When Reference Intelligence synthesizes across kernels, it resolves chemistry references as follows:
1. Chemistry_ref IDs resolve to records in this kernel
2. Material_refs in chemistry records resolve to the Material Kernel
3. Evidence_refs resolve to evidence linkage records within this kernel

## Intelligence Layer Boundaries

Reference Intelligence may:
- Aggregate chemistry facts across multiple records
- Combine chemistry truth with material, assembly, and scope truth
- Generate risk assessments and recommendations

Reference Intelligence may NOT:
- Modify chemistry truth records
- Create chemistry records without kernel governance
- Override incompatibility rules based on field experience alone
