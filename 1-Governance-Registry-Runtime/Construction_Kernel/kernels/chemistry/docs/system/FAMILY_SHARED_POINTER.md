# Family Shared Pointer

## Purpose

Points to shared family artifacts maintained in the Construction Reference Intelligence repository. This kernel does not duplicate shared artifacts.

## Family

**construction-kernel**

## Shared Artifact Registry

| Artifact | Canonical Location | Description |
|---|---|---|
| Family Context | `Construction_Reference_Intelligence/shared/FAMILY_CONTEXT.md` | Family architecture, coordination rules, kernel registry |
| Control Layers | `Construction_Reference_Intelligence/shared/control_layers.json` | 11 control layers for building envelope systems |
| Interface Zones | `Construction_Reference_Intelligence/shared/interface_zones.json` | 10 interface zones where assemblies meet |
| Division 07 Posture | `Construction_Reference_Intelligence/shared/division_07_posture.json` | Division 07 domain posture and section mapping |

## Shared Enums

The following enums are shared across the kernel family and must remain synchronized:

### chemistry_family
```
polyurethane, silicone, polysulfide, acrylic, epoxy, bituminous,
polyolefin, pvc, epdm, butyl, sbs, app, pmma, polyurea, hybrid
```

This enum is used in:
- `schemas/chemical_system.schema.json` → `chemistry_family`
- `schemas/polymer_family.schema.json` → `chemistry_family`
- Material Kernel schemas via cross-reference

### status
```
active, draft, deprecated
```

This enum is universal across all kernel schemas.

## Synchronization Rules

1. Shared artifacts are read-only from this kernel's perspective
2. Changes to shared enums require coordinated update across all kernels
3. This kernel validates its records against shared enum values
4. If a shared artifact is unavailable, this kernel operates on its last-known-good copy but flags the discrepancy
