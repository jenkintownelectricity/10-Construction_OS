# Entity Relationship Map — Construction Material Kernel

## Core Entity Relationships

```
Material Class (1) ──has──> (N) Material Form
Material Class (1) ──has──> (N) Material Property
Material Class (1) ──has──> (N) Material Performance
Material Class (1) ──has──> (N) Hygrothermal Property
Material Class (1) ──has──> (N) Weathering Behavior
Material Class (N) ──participates in──> (N) Compatibility Record
Material Property (N) ──tested by──> (1) Standards Reference
Weathering Behavior (N) ──tested by──> (1) Standards Reference
Hygrothermal Property (N) ──tested by──> (1) Standards Reference
Compatibility Record (1) ──explains──> (0..1) Chemistry Kernel Record (external)
```

## Cardinality Rules

| Relationship | Cardinality | Description |
|---|---|---|
| Class to Form | 1:N | One class may have multiple forms |
| Class to Property | 1:N | One class has many measured properties |
| Class to Compatibility | N:N | A class participates in many compatibility pairs |
| Property to Standard | N:1 | Many properties reference one test method |
| Class to Weathering | 1:N | One class may have many weathering records |
| Class to Hygrothermal | 1:N | One class may have many hygrothermal properties |
| Performance to Class | N:1 | Many performance records for one class |

## Reference Integrity

- All `material_ref` fields must point to an existing material class or entry ID
- All `test_method_ref` fields must point to an existing standards reference ID
- All `material_a_ref` and `material_b_ref` in compatibility records must point to existing materials
- External references (`chemistry_ref`) are validated at the integration layer, not the kernel

## Cross-Kernel References

| This Kernel Entity | External Entity | Pointer Field |
|---|---|---|
| Compatibility Record | Chemistry Kernel mechanism | chemistry_ref |
| Material Class | Control Layer (shared) | control_layers_served |
| All entities | Shared enums | enum values from shared registry |

## Orphan Prevention

Records with broken references (pointing to non-existent IDs) are rejected at validation. Deprecated records that are referenced by active records may not be deleted. Lineage chains must remain unbroken.
