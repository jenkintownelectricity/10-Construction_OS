# Interface Risk Map — Construction Assembly Kernel

## Purpose

Maps interface zones to their default risk levels, control layers at risk, and evidence expectations.

## Risk Matrix

| Interface Zone | Default Risk | Control Layers at Risk | Primary Failure Mode |
|---|---|---|---|
| roof_to_wall | Critical | bulk_water, air, thermal, vapor | Water intrusion at membrane-to-WRB transition |
| parapet_transition | Critical | bulk_water, air, thermal | Water intrusion at base, coping displacement by wind |
| penetration | High-Critical | bulk_water, air, thermal (density-dependent) | Seal failure at pipe boot or flashing |
| fenestration_edge | High | bulk_water, air | Flashing sequence error; sealant failure |
| below_grade_transition | High | bulk_water, capillary | Grade-line transition gap; backfill damage |
| expansion_joint | High | bulk_water, air, fire_smoke, movement | Joint cover failure; fire barrier discontinuity |
| deck_to_wall | High | bulk_water, drainage | Waterproofing turn-up failure under traffic |
| roof_edge | Medium-High | bulk_water, weathering_surface | Edge metal displacement by wind uplift |
| curb_transition | High | bulk_water, air | Three-dimensional intersection failure |
| drain_transition | Medium | bulk_water, drainage | Clamping ring seal failure; debris blockage |

## Risk Factors by Zone

### Roof-to-Wall (Critical)

- Change in plane: horizontal to vertical
- Change in assembly type: roof to wall
- Multiple control layers must transition simultaneously
- Different trades responsible for each side
- Difficult to inspect after cladding is installed
- Water concentrates at this junction

### Parapet Transition (Critical)

- Three-sided exposure: interior, exterior, top
- Thermal movement in coping (metal expands/contracts)
- Membrane must transition from horizontal to vertical
- Wind pressure differential across parapet
- Through-wall flashing coordination with multiple trades

### Penetration (High to Critical)

- Every penetration interrupts multiple control layers
- Density multiplies risk (more penetrations = higher probability of failure)
- Movement differential between penetrating element and assembly
- Material compatibility between sealant and membrane

## Evidence Expectations by Risk Level

| Risk Level | Evidence Expectation |
|---|---|
| Critical | Mock-up test results, enhanced field inspection, third-party review |
| High | Detailed submittal review, standard field inspection, documented seal verification |
| Medium | Standard inspection, manufacturer's installation verification |
| Low | Routine inspection |

## Risk Mitigation Hierarchy

1. **Eliminate**: Reduce number of penetrations; consolidate on curb platforms
2. **Simplify**: Use prefabricated transition assemblies where available
3. **Detail**: Provide explicit details for every interface condition
4. **Verify**: Inspect and test every critical and high-risk interface
5. **Document**: Record evidence of proper execution in kernel
