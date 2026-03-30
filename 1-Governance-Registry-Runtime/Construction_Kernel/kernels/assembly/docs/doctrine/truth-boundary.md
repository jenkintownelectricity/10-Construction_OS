# Truth Boundary — Construction Assembly Kernel

## What This Kernel Owns

The Construction Assembly Kernel owns **assembly-domain truth only**:

| Truth Surface | Description |
|---|---|
| Assembly systems | Ordered layer stacks with control-layer assignments |
| Assembly layers | Individual layers with position, material reference, and control-layer role |
| Assembly components | Discrete components within assemblies (membranes, insulation, fasteners, flashings) |
| Control-layer assignments | Which layers fulfill which control-layer functions |
| Transition conditions | How assemblies connect at interface zones (roof-to-wall, parapet, etc.) |
| Penetration conditions | How pipes, conduits, and structural members pass through enclosure assemblies |
| Edge conditions | How assemblies terminate at perimeters (fascia, coping, drip edge, termination bar) |
| Tie-in conditions | How new assemblies connect to existing or phased construction |
| Tested assembly records | Fire ratings, wind uplift, air leakage, and other test-validated configurations |
| Continuity requirements | Rules governing control-layer continuity across assembly boundaries |

## What This Kernel Does NOT Own

| Truth Surface | Owner |
|---|---|
| Material properties (tensile strength, elongation, chemical resistance) | Construction_Material_Kernel |
| Chemical behavior (compatibility, outgassing, plasticizer migration) | Construction_Chemistry_Kernel |
| Specification requirements (submittals, QA, installation tolerances) | Construction_Specification_Kernel |
| Scope of work (quantities, phasing, responsibility) | Construction_Scope_Kernel |
| Reference intelligence (cross-domain patterns, failure analysis) | Construction_Reference_Intelligence |

## Boundary Rules

1. This kernel references material entries by `material_ref` pointer. It does not store material properties.
2. This kernel references specification sections by `spec_ref` pointer. It does not store specification text.
3. When a question crosses the truth boundary, this kernel returns its assembly truth and directs the query to the owning kernel.
4. Shared enums (control layers, interface zones, lifecycle stages) come from the shared registry. This kernel consumes them; it does not define them.
5. The intelligence layer may read assembly truth to generate cross-domain insights. Assembly truth remains authoritative here.
