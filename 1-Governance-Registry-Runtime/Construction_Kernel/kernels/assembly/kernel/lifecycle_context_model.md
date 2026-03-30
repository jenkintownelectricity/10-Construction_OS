# Lifecycle Context Model — Construction Assembly Kernel

## Purpose

Defines how lifecycle stage context is recorded on assembly records. Assemblies exist across the full building lifecycle; the kernel records which stage each record reflects.

## Lifecycle Stages and Assembly Relevance

### design

Assembly is configured during design. The kernel records the intended layer stack, control-layer assignments, and interface details as specified in construction documents.

- Records created at this stage represent design intent
- Status is typically `draft` until validated by testing or field verification
- Climate and geometry context are established at design

### procurement

Components are being sourced against the designed assembly. Tested assembly configurations constrain acceptable substitutions.

- Assembly records may be revised if approved substitutions change layer composition
- Tested assembly records become critical: substitutions must match tested configurations

### installation

Assembly is being constructed in the field. Layer sequencing, attachment methods, and interface details are executed per the design.

- Field observations may create revised records reflecting as-built conditions
- Installation defects are documented as evidence linked to affected assembly records

### commissioning

Completed assembly is verified through testing and inspection. BECx (Building Enclosure Commissioning) activities validate control-layer performance.

- Air leakage testing (ASTM E2357) results link to assembly records
- Water penetration testing results link to transition and penetration conditions
- Visual inspection reports verify layer completeness and detailing

### operation

Assembly is in service under real climate and use conditions. Performance data may emerge over time.

- Sensor data (moisture, temperature) may validate or challenge assembly design assumptions
- Assembly records remain as-built reference documents

### maintenance

Periodic inspection and repair of assembly components. Sealant replacement, membrane repair, coating renewal.

- Maintenance activities may trigger assembly record review
- Component service life tracking references assembly configuration

### failure

Assembly or component failure has occurred. Forensic analysis documents root cause.

- Forensic reports link as evidence to the failed assembly record
- Failure may trigger creation of a revised assembly record with corrective configuration

### replacement

Assembly has reached end of service life or has failed beyond repair. Re-roofing, re-cladding, or system replacement.

- New assembly records are created for the replacement system
- Tie-in conditions document new-to-existing boundaries
- Old assembly record is deprecated with supersession reference to new record

## Recording Lifecycle Context

Lifecycle stage is recorded using the `lifecycle_stage` field from the shared taxonomy. It reflects the stage the record was created or last validated at, not the current stage of the physical assembly.

## Lifecycle-Sensitive Kernel Queries

- "Show all assemblies in draft status awaiting commissioning validation"
- "Find all tested assembly records older than 10 years that may need revalidation"
- "List all tie-in conditions of type repair_boundary created during maintenance"
