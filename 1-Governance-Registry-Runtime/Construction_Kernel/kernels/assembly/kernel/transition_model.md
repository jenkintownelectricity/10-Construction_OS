# Transition Model — Construction Assembly Kernel

## Definition

A transition condition records how two assembly types connect at an interface zone. Transitions are where assemblies succeed or fail. The kernel models transitions as first-class objects with dedicated schemas, risk tracking, and evidence linkage.

## Transition Structure

| Property | Required | Description |
|---|---|---|
| transition_id | Yes | Unique identifier |
| title | Yes | Human-readable description |
| interface_zone | Yes | Interface zone ID from shared registry |
| from_assembly_ref | Yes | Source assembly system ID |
| to_assembly_ref | Yes | Target assembly system ID |
| status | Yes | active, draft, deprecated |
| control_layers_maintained | No | Control layers continuous across transition |
| detail_ref | No | Reference to detail drawing or specification |
| risk_level | No | critical, high, medium, low |
| evidence_refs | No | Test reports, mock-up results, inspection records |

## Common Transition Types

### Roof-to-Wall (interface_zone: roof_to_wall)

The most failure-prone transition in commercial construction. The horizontal roof membrane must connect to the vertical wall air/water barrier with continuity of water, air, and thermal control.

**Typical detail**: Roof membrane extends up wall minimum 8" above roof surface. Membrane is sealed to wall air barrier with compatible transition strip or sealant. Base flashing covers the transition. Counter-flashing sheds water over the base flashing.

**Control layers maintained**: bulk_water_control, air_control, thermal_control

### Parapet (interface_zone: parapet_transition)

Roof membrane transitions from horizontal to vertical (up parapet face) to horizontal (under coping). Three-sided exposure creates stress from thermal movement, wind pressure, and water.

**Typical detail**: Membrane extends up parapet face to top. Coping with drip edges covers the parapet top. Through-wall flashing at base of parapet directs water outward.

**Control layers maintained**: bulk_water_control, air_control

### Below-Grade (interface_zone: below_grade_transition)

Above-grade weather barrier transitions to below-grade waterproofing at or below the grade line.

**Typical detail**: Waterproofing membrane laps over or integrates with above-grade WRB at a defined transition height (typically 6-8" above finished grade). Protection board and drainage board begin at this transition.

**Control layers maintained**: bulk_water_control

## Risk Assessment

Transitions carry inherent risk because:
1. Two different assembly systems must achieve continuity despite different materials and configurations
2. Changes in plane (horizontal to vertical) create stress concentrations
3. Multiple trades typically work at transition zones, creating coordination risk
4. Transitions are difficult to inspect after construction is complete

Risk levels guide evidence requirements:
- **critical**: Mock-up testing recommended before full installation
- **high**: Detailed submittal review and enhanced field inspection
- **medium**: Standard inspection protocols
- **low**: Routine inspection

## Transition Completeness

A complete transition record includes:
1. Both assembly references (from and to)
2. The interface zone classification
3. The list of control layers that must be maintained
4. The detail reference describing how the transition is achieved
5. The risk level assessment
6. Evidence references supporting the transition design
