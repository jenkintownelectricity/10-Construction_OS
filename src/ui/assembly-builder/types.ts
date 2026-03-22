/**
 * Assembly Builder — Canonical Types
 *
 * Aligned exactly to Construction_Assembly_Kernel/schemas/assembly_system.schema.json
 * No invented fields. No schema amendments.
 *
 * Governance: VKGL04R
 */

// ─── Assembly System (canonical shape from Assembly Kernel) ──────────────

export type AssemblyType =
  | 'roof_assembly'
  | 'wall_assembly'
  | 'below_grade_assembly'
  | 'plaza_assembly'
  | 'vegetated_assembly'
  | 'hybrid_assembly';

export type AssemblyStatus = 'active' | 'draft' | 'deprecated';

export type AttachmentMethod =
  | 'mechanically_attached'
  | 'fully_adhered'
  | 'ballasted'
  | 'torch_applied'
  | 'hot_mopped'
  | 'cold_applied'
  | 'spray_applied'
  | 'self_adhered'
  | 'loose_laid'
  | 'standing_seam'
  | 'lapped'
  | 'welded';

export type ContinuityStatus = 'continuous' | 'interrupted' | 'terminated' | 'transitioned';

export type ControlLayerId =
  | 'bulk_water_control'
  | 'capillary_control'
  | 'air_control'
  | 'vapor_control'
  | 'thermal_control'
  | 'fire_smoke_control'
  | 'movement_control'
  | 'weathering_surface'
  | 'drainage_plane'
  | 'protection_layer'
  | 'vegetation_support_layer';

export type InterfaceZoneId =
  | 'roof_to_wall'
  | 'parapet_transition'
  | 'penetration'
  | 'fenestration_edge'
  | 'below_grade_transition'
  | 'expansion_joint'
  | 'deck_to_wall'
  | 'roof_edge'
  | 'curb_transition'
  | 'drain_transition';

export type ExposureFlag =
  | 'marine_exposure'
  | 'high_uv'
  | 'freeze_thaw'
  | 'coastal_salt'
  | 'high_wind'
  | 'high_humidity'
  | 'severe_precipitation';

export type ExposureClass = 'sheltered' | 'moderate' | 'severe' | 'extreme';

export type GeometryContext =
  | 'low_slope_roof'
  | 'steep_slope_roof'
  | 'complex_roof_geometry'
  | 'large_parapet_run'
  | 'multi_penetration_field'
  | 'irregular_drainage_geometry'
  | 'tall_wall_field'
  | 'podium_condition';

export type WarrantyPosture =
  | 'manufacturer_standard'
  | 'manufacturer_extended'
  | 'system_warranty'
  | 'no_dollar_limit'
  | 'prorated'
  | 'none'
  | 'unknown';

// ─── Layer within an assembly ────────────────────────────────────────────

export interface AssemblyLayer {
  readonly layer_id: string;
  readonly position: number;
  readonly control_layer_id: ControlLayerId;
  readonly material_ref: string;
  readonly attachment_method?: AttachmentMethod;
  readonly thickness?: string;
  readonly notes?: string;
}

// ─── Climate Context ────────────────────────────────────────────────────

export interface ClimateContext {
  readonly climate_zone?: string;
  readonly exposure_flags?: readonly ExposureFlag[];
  readonly exposure_class?: ExposureClass;
}

// ─── Geometry Context ───────────────────────────────────────────────────

export interface GeometryContextObj {
  readonly geometry_contexts?: readonly GeometryContext[];
  readonly notes?: string;
}

// ─── Canonical Assembly Draft ───────────────────────────────────────────
// This is the shape the UI produces. Aligned to assembly_system.schema.json.

export interface CanonicalAssemblyDraft {
  readonly schema_version: 'v1';
  readonly system_id: string;
  readonly title: string;
  readonly assembly_type: AssemblyType;
  readonly status: AssemblyStatus;
  readonly layers?: readonly AssemblyLayer[];
  readonly control_layer_continuity?: Readonly<Record<string, ContinuityStatus>>;
  readonly interface_zones?: readonly InterfaceZoneId[];
  readonly climate_context?: ClimateContext;
  readonly geometry_context?: GeometryContextObj;
  readonly tested_assembly_refs?: readonly string[];
  readonly standards_refs?: readonly string[];
  readonly warranty_posture?: WarrantyPosture;
  readonly notes?: string;
}

// ─── Mutable draft form state (used by UI internally) ───────────────────

export interface AssemblyDraftFormState {
  system_id: string;
  title: string;
  assembly_type: AssemblyType;
  status: AssemblyStatus;
  layers: AssemblyLayer[];
  control_layer_continuity: Record<string, ContinuityStatus>;
  interface_zones: InterfaceZoneId[];
  climate_context: {
    climate_zone: string;
    exposure_flags: ExposureFlag[];
    exposure_class: ExposureClass;
  };
  geometry_context: {
    geometry_contexts: GeometryContext[];
    notes: string;
  };
  tested_assembly_refs: string[];
  standards_refs: string[];
  warranty_posture: WarrantyPosture;
  notes: string;
}

// ─── Validation ─────────────────────────────────────────────────────────

export interface FieldDiagnostic {
  readonly field: string;
  readonly severity: 'error' | 'warning';
  readonly message: string;
  readonly rule: string;
}

export interface ValidationOutcome {
  readonly valid: boolean;
  readonly diagnostics: readonly FieldDiagnostic[];
  readonly timestamp: number;
}

// ─── Source Lineage ─────────────────────────────────────────────────────

export interface SourceLineage {
  readonly sourceAdapter: string;
  readonly sourceFile: string;
  readonly sourceId: string;
  readonly hydratedAt: number;
}

// ─── Preview/Test Result ────────────────────────────────────────────────

export interface PreviewTestResult {
  readonly draftId: string;
  readonly status: 'pass' | 'fail' | 'error';
  readonly compilerAdapter: string;
  readonly diagnostics: readonly string[];
  readonly timestamp: number;
  readonly payload?: CanonicalAssemblyDraft;
}

// ─── CRI Shared Artifacts (read-only) ───────────────────────────────────

export interface ControlLayerDef {
  readonly id: ControlLayerId;
  readonly name: string;
  readonly description: string;
}

export interface InterfaceZoneDef {
  readonly id: InterfaceZoneId;
  readonly name: string;
  readonly description: string;
}
