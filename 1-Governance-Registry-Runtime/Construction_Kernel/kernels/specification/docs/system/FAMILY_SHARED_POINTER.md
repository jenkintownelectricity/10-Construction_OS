# Family Shared Pointer — Construction Specification Kernel

## Canonical Source

All shared family artifacts are maintained in the Construction_Reference_Intelligence repository. This kernel consumes them by reference and never duplicates their content.

**Source repository:** `Construction_Reference_Intelligence`
**Shared artifacts path:** `Construction_Reference_Intelligence/shared/`

## Shared Artifacts Referenced

### Control Layers Registry
- **File:** `shared/control_layers.json`
- **Content:** 11 canonical control layers for Division 07 building envelope systems
- **Usage in this kernel:** `control_layers_served` field in specification sections and requirements
- **Layers:** bulk_water_control, capillary_control, air_control, vapor_control, thermal_control, fire_smoke_control, movement_control, weathering_surface, drainage_plane, protection_layer, vegetation_support_layer

### Interface Zones Registry
- **File:** `shared/interface_zones.json`
- **Content:** 10 canonical interface zones where control layer continuity is challenged
- **Usage in this kernel:** `interface_zones` field in requirements, interface risk mapping
- **Zones:** roof_to_wall, parapet_transition, penetration, fenestration_edge, below_grade_transition, expansion_joint, deck_to_wall, roof_edge, curb_transition, drain_transition

### Shared Enum Registry
- **File:** `shared/shared_enum_registry.json`
- **Content:** Canonical enum values for lifecycle stages, climate exposure flags, geometry contexts, confidence levels, risk levels, revision postures, evidence types, control layer IDs, interface zone IDs
- **Usage in this kernel:** Enum validation for climate_context, geometry_context, lifecycle_stage, and other shared fields

### Shared Standards Registry
- **File:** `shared/shared_standards_registry.json`
- **Content:** Standards citation registry (IBC, ASTM, AAMA, NFPA_285, ASHRAE_90_1, WBDG, UFGS, CSI_MASTERFORMAT, ISO_13788)
- **Usage in this kernel:** Standards reference validation, reference_standard entity alignment

### Shared Taxonomy
- **File:** `shared/shared_taxonomy.json`
- **Content:** Canonical taxonomy fields (csi_section_code, spec_family, subfamily, control_function, assembly_zone, interface_type, primary_material_class, chemistry_family, installation_method, performance_class)
- **Usage in this kernel:** Taxonomy field definitions for specification sections and requirements

### Division 07 Posture
- **File:** `shared/division_07_posture.json`
- **Content:** Domain posture for Division 07 building envelope systems
- **Usage in this kernel:** Domain alignment context

### Family Context
- **File:** `shared/FAMILY_CONTEXT.md`
- **Content:** Family architecture, coordination rules, kernel roles
- **Usage in this kernel:** Governance alignment

### Shared Evidence Registry
- **File:** `shared/shared_evidence_registry.json`
- **Content:** Evidence type definitions and linkage rules
- **Usage in this kernel:** Evidence linkage model alignment

### Shared Risk Registry
- **File:** `shared/shared_risk_registry.json`
- **Content:** Risk classification and interface risk definitions
- **Usage in this kernel:** Interface risk posture alignment

## Non-Duplication Rule

Shared artifacts are NEVER copied into this repository. All references use the canonical path in `Construction_Reference_Intelligence/shared/`. If a shared artifact is updated, this kernel's baseline must be re-evaluated.
