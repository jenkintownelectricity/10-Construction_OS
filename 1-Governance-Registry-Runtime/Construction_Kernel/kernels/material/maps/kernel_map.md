# Kernel Map — Construction Material Kernel

## Purpose
Maps all objects, schemas, contracts, and relationships within this kernel.

## Object Types

| Object | Schema | Contract | Description |
|---|---|---|---|
| Material Class | material_class.schema.json | material_class_contract | Taxonomy classification |
| Material Form | material_form.schema.json | — | Physical delivery form |
| Material Property | material_property.schema.json | material_property_contract | Measured physical property |
| Material Performance | material_performance.schema.json | — | Aggregate performance record |
| Compatibility Record | material_compatibility_record.schema.json | material_compatibility_contract | Pairwise compatibility |
| Weathering Behavior | weathering_behavior.schema.json | weathering_behavior_contract | Environmental degradation |
| Hygrothermal Property | hygrothermal_property.schema.json | hygrothermal_property_contract | Moisture transport properties |
| Standards Reference | material_standard_reference.schema.json | — | Test method citation |
| Material Entry | material_entry.schema.json | — | General material fact |

## Relationship Map

```
Material Class ──(has forms)──> Material Form
Material Class ──(has properties)──> Material Property
Material Class ──(has compatibility)──> Compatibility Record
Material Class ──(has weathering)──> Weathering Behavior
Material Class ──(has hygrothermal)──> Hygrothermal Property
Material Property ──(tested by)──> Standards Reference
Material Class ──(has performance)──> Material Performance
```

## Model Coverage

| Model | File | Objects Governed |
|---|---|---|
| Material Model | kernel/material_model.md | Material Class, Material Form |
| Property Model | kernel/property_model.md | Material Property |
| Compatibility Model | kernel/compatibility_model.md | Compatibility Record |
| Weathering Model | kernel/weathering_model.md | Weathering Behavior |
| Hygrothermal Model | kernel/hygrothermal_model.md | Hygrothermal Property |
| Standards Model | kernel/standards_model.md | Standards Reference |
| Truth Model | kernel/truth_model.md | All objects (truth governance) |
| Taxonomy | kernel/taxonomy.md | Material Class enums |

## Governance Files

| File | Purpose |
|---|---|
| docs/doctrine/kernel-doctrine.md | Core principles |
| docs/doctrine/truth-boundary.md | Ownership boundaries |
| docs/doctrine/non-goals.md | Out-of-scope capabilities |
| docs/doctrine/interpretation-limitations.md | Data interpretation limits |
