# Non-Goals — Construction Assembly Kernel

## What This Kernel Is NOT

### Not a Runtime or Application

The kernel is a truth store, not a running application. It does not serve HTTP endpoints, render user interfaces, or execute business logic. Runtime systems consume kernel truth through defined contracts.

### Not a CAD System

The kernel does not store geometry, 3D models, or drawing files. It records assembly configurations in structured data. CAD and BIM systems may reference kernel assembly records, but geometric representation is outside this kernel's scope.

### Not a Cost Estimator

The kernel does not store pricing, labor rates, or cost models. Assembly records describe what an assembly is and how it performs, not what it costs. Cost estimation systems may consume assembly data but are not part of this kernel.

### Not a Product Database

The kernel records assembly configurations using material references, not product catalogs. It does not store manufacturer names, trade names, product numbers, or SKUs. Material identity is owned by the Material Kernel.

### Not a Specification Writer

The kernel does not generate specification sections, submittals, or contract language. Specification truth is owned by the Specification Kernel. This kernel provides the assembly facts that specifications reference.

### Not a Standards Repository

The kernel references standards by citation (IBC section, ASTM test number, NFPA clause). It does not reproduce standards text, interpret code intent, or track code adoption by jurisdiction.

### Not a Commissioning System

The kernel records tested assembly configurations and their test results. It does not manage commissioning workflows, punch lists, or field verification processes. Inspection and commissioning systems may reference kernel records.

### Not a Warranty Manager

The kernel may note warranty-relevant assembly constraints (e.g., maximum fastener spacing for wind warranty). It does not manage warranty terms, claims, or coverage periods.

## Why Non-Goals Matter

Excluding these functions keeps the kernel focused on its truth surface: assembly systems as layered, control-layer-organized configurations. Every excluded function has a proper home elsewhere in the family or in downstream systems.
