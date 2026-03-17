# App-to-Kernel Map — Construction Application OS v0.1

## Assembly Parser App → Construction_Kernel

| App Need | Kernel | Kernel Role |
|----------|--------|-------------|
| Material properties, product data | Chemistry Kernel | Defines what the work is made of |
| Assembly composition, component structure | Assembly Kernel | Defines how work is composed into buildable conditions |
| Dimensions, plans, spatial relationships | Geometry Kernel | Defines what the work is shaped like |
| Shop drawings, issued deliverables | Deliverable Kernel | Defines what is formally produced and issued |

## Spec Intelligence App → Construction_Kernel

| App Need | Kernel | Kernel Role |
|----------|--------|-------------|
| Contracts, specifications, scope | Governance Kernel | Defines what governs the work |
| Product data, manufacturer documentation | Chemistry Kernel | Defines what the work is made of |
| Plans, dimensions, spatial references | Geometry Kernel | Defines what the work is shaped like |
| Opportunity detection, derived analysis | Intelligence Kernel | Defines what is derived from governed source truth |

## Truth Chain
Both apps consume kernel truth that is applied from Universal_Truth_Kernel through the Construction_Kernel layer. Apps do not access nucleus truth directly; they receive it transitively through the kernel and runtime layers.
