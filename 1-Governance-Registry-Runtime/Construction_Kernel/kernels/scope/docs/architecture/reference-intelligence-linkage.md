# Reference Intelligence Linkage

## Purpose

Defines how the Scope Kernel references the Construction Reference Intelligence layer without owning or duplicating intelligence content.

## Linkage Principle

The Scope Kernel is a consumer of reference intelligence, not a producer. It links to intelligence artifacts through explicit pointers and never copies standards text, code provisions, or manufacturer data into scope records.

## Linked Intelligence Types

### 1. Standards References
Scope records reference ASTM, SPRI, FM, and UL standards by identifier for inspection and testing methods. The kernel does not store standards content.

### 2. Code References
Building code sections (IBC, IECC) may be referenced as the basis for scope requirements. The kernel does not interpret code provisions.

### 3. Control Layer Definitions
The shared control layer registry (maintained in Reference Intelligence) defines the functional layers. The Scope Kernel references control layers affected by scope items via `control_layers_affected`.

### 4. Interface Zone Definitions
The shared interface zone registry (maintained in Reference Intelligence) defines physical zones. The Scope Kernel references interface zones via `interface_zones`.

### 5. Division Posture
The shared Division 07 posture document (maintained in Reference Intelligence) defines the domain context. The Scope Kernel aligns its scope categories to this posture.

## Reference Pattern

```
Scope Record --> standard_ref --> "ASTM E2357"
                                    |
                    [Resolution by Reference Intelligence layer]
```

The Scope Kernel stores the reference identifier. Resolution of that identifier to actual content is the responsibility of the Reference Intelligence layer.

## What Is NOT Linked

- Manufacturer technical data (not scope truth)
- Product evaluation reports (not scope truth)
- Historical project data (not scope truth)
- Pricing databases (not scope truth)

## Shared Artifacts Consumed

| Artifact | Source | Use in Scope Kernel |
|---|---|---|
| `control_layers.json` | Reference Intelligence | `control_layers_affected` field values |
| `interface_zones.json` | Reference Intelligence | `interface_zones` field values |
| `division_07_posture.json` | Reference Intelligence | Domain alignment validation |
| `FAMILY_CONTEXT.md` | Reference Intelligence | Family architecture context |
