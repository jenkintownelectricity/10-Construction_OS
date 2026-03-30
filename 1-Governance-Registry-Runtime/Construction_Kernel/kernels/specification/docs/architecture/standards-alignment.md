# Standards Alignment — Construction Specification Kernel

## Alignment Principle

This kernel references standards and codes by citation only, using the canonical `shared_standards_registry.json` maintained in `Construction_Reference_Intelligence/shared/`. No standards text is reproduced, summarized, or paraphrased.

## Referenced Standards Bodies

### International Building Code (IBC)

- Registry reference_id: `IBC`
- Governing relationship: `mandatory_compliance`
- Specification relevance: IBC requirements flow into project specifications as mandatory obligations. Chapter 15 (Roof Assemblies and Rooftop Structures) and Chapter 14 (Exterior Walls) generate Division 07 specification requirements for fire rating, weather protection, and structural attachment.

### ASTM International

- Registry reference_id: `ASTM`
- Governing relationship: `test_method_authority`
- Specification relevance: ASTM test methods are referenced in Division 07 specifications to define acceptance criteria. Common references include ASTM D4541 (adhesion testing), ASTM E2357 (air barrier), ASTM D903 (peel strength), ASTM E96 (vapor transmission), and ASTM E1105 (water penetration).

### American Architectural Manufacturers Association (AAMA)

- Registry reference_id: `AAMA`
- Governing relationship: `test_method_authority`
- Specification relevance: AAMA standards govern fenestration and curtain wall performance testing at interface zones where Division 07 enclosure systems meet openings.

### NFPA 285

- Registry reference_id: `NFPA_285`
- Governing relationship: `mandatory_compliance_where_applicable`
- Specification relevance: Fire propagation testing requirements for exterior wall assemblies. Specifications for combustible components in wall assemblies must reference NFPA 285 compliance where required by IBC.

### ASHRAE 90.1

- Registry reference_id: `ASHRAE_90_1`
- Governing relationship: `mandatory_compliance`
- Specification relevance: Energy code requirements driving thermal insulation values, air barrier performance criteria, and continuous insulation requirements in Division 07 specifications.

## Citation Protocol

When a specification requirement references a standard, the kernel records:

1. The `reference_id` from the shared standards registry
2. The specific section, table, or clause number within the standard (if stated in the spec)
3. The edition year (if stated in the spec)
4. The relationship to the requirement (e.g., test method, acceptance criterion, design basis)

The kernel never records what the standard says — only that the specification cites it.

## Standards Conflict Handling

When a specification cites conflicting editions or requirements from different standards, both citations are recorded. The conflict is flagged with `ambiguity_flag: true`. Resolution of standards conflicts is outside this kernel's scope.

## Shared Registry Dependency

All standards references in this kernel must use `reference_id` values that exist in `shared_standards_registry.json`. Standards not in the shared registry must be added to the shared registry first — this kernel does not maintain its own standards list.
