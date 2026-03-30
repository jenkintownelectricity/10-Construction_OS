# Kernel-to-Inspection Map — Construction Assembly Kernel

## Purpose

Maps how assembly kernel truth supports building enclosure inspection and commissioning workflows.

## Inspection-Relevant Kernel Objects

### Assembly Systems

Inspectors verify that the installed assembly matches the designed layer stack:
- Layer sequence matches the assembly_system record
- Materials match material_ref specifications
- Attachment methods match the recorded attachment_method

### Transition Conditions

Transitions are primary inspection targets:
- Roof-to-wall transitions verified against transition_condition records
- Control-layer continuity at transitions verified against control_layers_maintained
- Flashing details compared to detail_ref

### Penetration Conditions

Every penetration requires inspection:
- Seal method verified against penetration_condition record
- Control layers affected confirmed
- Penetration type classification confirmed

### Edge Conditions

Perimeter edge details inspected:
- Edge type matches edge_condition record
- Control layer termination verified
- Edge metal securement per SPRI ES-1 or FM requirements

### Tested Assembly Records

Inspectors verify installed configuration matches tested configuration:
- Component substitutions compared against tested assembly record
- Any deviation from tested configuration flagged

## Inspection Checkpoints by Lifecycle Stage

| Stage | Kernel Objects Verified |
|---|---|
| Substrate preparation | assembly_system (deck/substrate layer) |
| Vapor retarder installation | assembly_layer (vapor_control position) |
| Insulation installation | assembly_layer (thermal_control, attachment) |
| Membrane installation | assembly_layer (bulk_water_control, seam welds) |
| Transition detailing | transition_condition (control layers maintained) |
| Penetration sealing | penetration_condition (seal method, control layers) |
| Edge securement | edge_condition (edge type, termination) |
| Final commissioning | tested_assembly_record (configuration match), continuity_requirement (compliance) |

## Evidence Generation

Inspections generate evidence that links back to kernel objects:
- Inspection reports reference assembly_system IDs
- Test results reference tested_assembly_record IDs
- Deficiency reports reference specific kernel objects and fields

## Current State

Inspection workflow integration is documented conceptually. No automated inspection tools consume kernel data directly.
