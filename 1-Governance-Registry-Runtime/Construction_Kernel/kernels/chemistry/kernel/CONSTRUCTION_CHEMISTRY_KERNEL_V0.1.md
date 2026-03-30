# Construction Chemistry Kernel V0.1

## Version Manifest

| Field | Value |
|---|---|
| **Kernel ID** | KERN-CONST-CHEM |
| **Version** | 0.1 |
| **Status** | initialized |
| **Created** | 2026-03-17 |
| **Family** | construction-kernel |
| **Domain** | Chemistry-domain truth |
| **Focus** | CSI Division 07 — Building Envelope Systems |

## Object Types in This Version

| Object Type | Schema | ID Prefix | Status |
|---|---|---|---|
| Chemical System | chemical_system.schema.json | CSYS- | defined |
| Polymer Family | polymer_family.schema.json | PFAM- | defined |
| Additive | additive.schema.json | ADTV- | defined |
| Cure Mechanism | cure_mechanism.schema.json | CURE- | defined |
| Solvent System | solvent_system.schema.json | SOLV- | defined |
| Adhesion Rule | adhesion_rule.schema.json | ADHR- | defined |
| Incompatibility Rule | incompatibility_rule.schema.json | INCP- | defined |
| Degradation Mechanism | degradation_mechanism.schema.json | DEGR- | defined |
| Chemical Hazard Record | chemical_hazard_record.schema.json | HAZR- | defined |
| Chemistry Entry (general) | chemistry_entry.schema.json | CHEM- | defined |

## Chemistry Families (Shared Enum)

polyurethane, silicone, polysulfide, acrylic, epoxy, bituminous, polyolefin, pvc, epdm, butyl, sbs, app, pmma, polyurea, hybrid

## Governance Rules

1. All records require `schema_version`, typed ID, `title`, and `status`
2. Status lifecycle: draft → active → deprecated
3. Active records require at least one evidence reference
4. Deprecated records retain lineage; never deleted
5. Fail-closed: untested combinations are not assumed compatible
6. additionalProperties: false on all schemas

## Sibling Kernels

- Construction_Material_Kernel — physical properties
- Construction_Assembly_Kernel — assembly sequences
- Construction_Specification_Kernel — specification clauses
- Construction_Scope_Kernel — trade scope

## V0.2 Planned Additions

- Population of initial chemistry records for Division 07 sealant families
- Evidence linkage to ASTM C920, C794, C1135
- Adhesion rule population for common substrate types
