/**
 * Canonical Assembly Draft Validator — Fail-Closed
 *
 * Validates assembly drafts against Assembly Kernel schemas before save/preview.
 * Any invalid payload fails closed with explicit field-level diagnostics.
 *
 * Schema source: Construction_Assembly_Kernel/schemas/assembly_system.schema.json
 * No schema modifications. Validation is structural only.
 *
 * Governance: VKGL04R — Ring 2 commit gate item: "Invalid drafts fail closed."
 */

import type {
  CanonicalAssemblyDraft,
  AssemblyDraftFormState,
  FieldDiagnostic,
  ValidationOutcome,
  AssemblyType,
  ControlLayerId,
  AttachmentMethod,
  InterfaceZoneId,
  ExposureFlag,
  ExposureClass,
  GeometryContext,
  WarrantyPosture,
  ContinuityStatus,
} from './types';
import { CONTROL_LAYER_IDS } from './controlLayerData';
import { INTERFACE_ZONE_IDS } from './interfaceZoneData';

// ─── Valid enum sets (from schema) ──────────────────────────────────────

const VALID_ASSEMBLY_TYPES: readonly AssemblyType[] = [
  'roof_assembly', 'wall_assembly', 'below_grade_assembly',
  'plaza_assembly', 'vegetated_assembly', 'hybrid_assembly',
];

const VALID_ATTACHMENT_METHODS: readonly AttachmentMethod[] = [
  'mechanically_attached', 'fully_adhered', 'ballasted', 'torch_applied',
  'hot_mopped', 'cold_applied', 'spray_applied', 'self_adhered',
  'loose_laid', 'standing_seam', 'lapped', 'welded',
];

const VALID_CONTINUITY: readonly ContinuityStatus[] = [
  'continuous', 'interrupted', 'terminated', 'transitioned',
];

const VALID_EXPOSURE_FLAGS: readonly ExposureFlag[] = [
  'marine_exposure', 'high_uv', 'freeze_thaw', 'coastal_salt',
  'high_wind', 'high_humidity', 'severe_precipitation',
];

const VALID_EXPOSURE_CLASSES: readonly ExposureClass[] = [
  'sheltered', 'moderate', 'severe', 'extreme',
];

const VALID_GEOMETRY_CONTEXTS: readonly GeometryContext[] = [
  'low_slope_roof', 'steep_slope_roof', 'complex_roof_geometry',
  'large_parapet_run', 'multi_penetration_field', 'irregular_drainage_geometry',
  'tall_wall_field', 'podium_condition',
];

const VALID_WARRANTY_POSTURES: readonly WarrantyPosture[] = [
  'manufacturer_standard', 'manufacturer_extended', 'system_warranty',
  'no_dollar_limit', 'prorated', 'none', 'unknown',
];

// ─── Validator ──────────────────────────────────────────────────────────

/**
 * Validate a canonical assembly draft against Assembly Kernel schema.
 * Fail-closed: returns valid=false with diagnostics for any schema violation.
 */
export function validateAssemblyDraft(draft: CanonicalAssemblyDraft): ValidationOutcome {
  const diagnostics: FieldDiagnostic[] = [];

  // Required: schema_version
  if (draft.schema_version !== 'v1') {
    diagnostics.push({
      field: 'schema_version',
      severity: 'error',
      message: `schema_version must be "v1", got "${draft.schema_version}"`,
      rule: 'schema_version_const',
    });
  }

  // Required: system_id
  if (!draft.system_id || draft.system_id.trim().length === 0) {
    diagnostics.push({
      field: 'system_id',
      severity: 'error',
      message: 'system_id is required and must not be empty',
      rule: 'required_field',
    });
  }

  // Required: title
  if (!draft.title || draft.title.trim().length === 0) {
    diagnostics.push({
      field: 'title',
      severity: 'error',
      message: 'title is required and must not be empty',
      rule: 'required_field',
    });
  }

  // Required: assembly_type (enum)
  if (!VALID_ASSEMBLY_TYPES.includes(draft.assembly_type)) {
    diagnostics.push({
      field: 'assembly_type',
      severity: 'error',
      message: `assembly_type "${draft.assembly_type}" is not valid. Must be one of: ${VALID_ASSEMBLY_TYPES.join(', ')}`,
      rule: 'enum_validation',
    });
  }

  // Required: status (enum)
  if (!['active', 'draft', 'deprecated'].includes(draft.status)) {
    diagnostics.push({
      field: 'status',
      severity: 'error',
      message: `status "${draft.status}" is not valid. Must be active, draft, or deprecated`,
      rule: 'enum_validation',
    });
  }

  // Layers validation
  if (draft.layers && draft.layers.length > 0) {
    const positions = new Set<number>();
    const layerIds = new Set<string>();

    for (let i = 0; i < draft.layers.length; i++) {
      const layer = draft.layers[i];
      const prefix = `layers[${i}]`;

      // Required: layer_id
      if (!layer.layer_id || layer.layer_id.trim().length === 0) {
        diagnostics.push({
          field: `${prefix}.layer_id`,
          severity: 'error',
          message: 'layer_id is required',
          rule: 'required_field',
        });
      } else if (layerIds.has(layer.layer_id)) {
        diagnostics.push({
          field: `${prefix}.layer_id`,
          severity: 'error',
          message: `Duplicate layer_id "${layer.layer_id}"`,
          rule: 'unique_layer_id',
        });
      } else {
        layerIds.add(layer.layer_id);
      }

      // Required: position (integer >= 1)
      if (typeof layer.position !== 'number' || layer.position < 1 || !Number.isInteger(layer.position)) {
        diagnostics.push({
          field: `${prefix}.position`,
          severity: 'error',
          message: `position must be an integer >= 1, got ${layer.position}`,
          rule: 'position_valid',
        });
      } else if (positions.has(layer.position)) {
        diagnostics.push({
          field: `${prefix}.position`,
          severity: 'warning',
          message: `Duplicate position ${layer.position} — positions should be unique`,
          rule: 'unique_position',
        });
      } else {
        positions.add(layer.position);
      }

      // Required: control_layer_id
      if (!CONTROL_LAYER_IDS.includes(layer.control_layer_id)) {
        diagnostics.push({
          field: `${prefix}.control_layer_id`,
          severity: 'error',
          message: `control_layer_id "${layer.control_layer_id}" not in CRI registry`,
          rule: 'control_layer_valid',
        });
      }

      // Required: material_ref
      if (!layer.material_ref || layer.material_ref.trim().length === 0) {
        diagnostics.push({
          field: `${prefix}.material_ref`,
          severity: 'error',
          message: 'material_ref is required',
          rule: 'required_field',
        });
      }

      // Optional: attachment_method (enum if present)
      if (layer.attachment_method && !VALID_ATTACHMENT_METHODS.includes(layer.attachment_method)) {
        diagnostics.push({
          field: `${prefix}.attachment_method`,
          severity: 'error',
          message: `attachment_method "${layer.attachment_method}" is not valid`,
          rule: 'enum_validation',
        });
      }
    }
  } else {
    diagnostics.push({
      field: 'layers',
      severity: 'warning',
      message: 'Assembly has no layers defined',
      rule: 'layers_present',
    });
  }

  // control_layer_continuity validation
  if (draft.control_layer_continuity) {
    for (const [key, value] of Object.entries(draft.control_layer_continuity)) {
      if (!CONTROL_LAYER_IDS.includes(key as ControlLayerId)) {
        diagnostics.push({
          field: `control_layer_continuity.${key}`,
          severity: 'error',
          message: `Control layer "${key}" not in CRI registry`,
          rule: 'control_layer_valid',
        });
      }
      if (!VALID_CONTINUITY.includes(value)) {
        diagnostics.push({
          field: `control_layer_continuity.${key}`,
          severity: 'error',
          message: `Continuity status "${value}" not valid`,
          rule: 'enum_validation',
        });
      }
    }
  }

  // interface_zones validation
  if (draft.interface_zones) {
    for (const zone of draft.interface_zones) {
      if (!INTERFACE_ZONE_IDS.includes(zone)) {
        diagnostics.push({
          field: 'interface_zones',
          severity: 'error',
          message: `Interface zone "${zone}" not in CRI registry`,
          rule: 'interface_zone_valid',
        });
      }
    }
  }

  // climate_context validation
  if (draft.climate_context) {
    if (draft.climate_context.exposure_flags) {
      for (const flag of draft.climate_context.exposure_flags) {
        if (!VALID_EXPOSURE_FLAGS.includes(flag)) {
          diagnostics.push({
            field: 'climate_context.exposure_flags',
            severity: 'error',
            message: `Exposure flag "${flag}" not valid`,
            rule: 'enum_validation',
          });
        }
      }
    }
    if (draft.climate_context.exposure_class && !VALID_EXPOSURE_CLASSES.includes(draft.climate_context.exposure_class)) {
      diagnostics.push({
        field: 'climate_context.exposure_class',
        severity: 'error',
        message: `Exposure class "${draft.climate_context.exposure_class}" not valid`,
        rule: 'enum_validation',
      });
    }
  }

  // geometry_context validation
  if (draft.geometry_context?.geometry_contexts) {
    for (const gc of draft.geometry_context.geometry_contexts) {
      if (!VALID_GEOMETRY_CONTEXTS.includes(gc)) {
        diagnostics.push({
          field: 'geometry_context.geometry_contexts',
          severity: 'error',
          message: `Geometry context "${gc}" not valid`,
          rule: 'enum_validation',
        });
      }
    }
  }

  // warranty_posture validation
  if (draft.warranty_posture && !VALID_WARRANTY_POSTURES.includes(draft.warranty_posture)) {
    diagnostics.push({
      field: 'warranty_posture',
      severity: 'error',
      message: `warranty_posture "${draft.warranty_posture}" not valid`,
      rule: 'enum_validation',
    });
  }

  // Fail-closed: any error = invalid
  const hasErrors = diagnostics.some((d) => d.severity === 'error');

  return {
    valid: !hasErrors,
    diagnostics,
    timestamp: Date.now(),
  };
}

/**
 * Convert mutable form state to immutable canonical draft shape.
 */
export function formStateToDraft(form: AssemblyDraftFormState): CanonicalAssemblyDraft {
  return {
    schema_version: 'v1',
    system_id: form.system_id,
    title: form.title,
    assembly_type: form.assembly_type,
    status: form.status,
    layers: form.layers.length > 0 ? form.layers : undefined,
    control_layer_continuity: Object.keys(form.control_layer_continuity).length > 0
      ? form.control_layer_continuity
      : undefined,
    interface_zones: form.interface_zones.length > 0 ? form.interface_zones : undefined,
    climate_context: form.climate_context.climate_zone
      ? {
          climate_zone: form.climate_context.climate_zone,
          exposure_flags: form.climate_context.exposure_flags.length > 0 ? form.climate_context.exposure_flags : undefined,
          exposure_class: form.climate_context.exposure_class || undefined,
        }
      : undefined,
    geometry_context: form.geometry_context.geometry_contexts.length > 0
      ? {
          geometry_contexts: form.geometry_context.geometry_contexts,
          notes: form.geometry_context.notes || undefined,
        }
      : undefined,
    tested_assembly_refs: form.tested_assembly_refs.length > 0 ? form.tested_assembly_refs : undefined,
    standards_refs: form.standards_refs.length > 0 ? form.standards_refs : undefined,
    warranty_posture: form.warranty_posture || undefined,
    notes: form.notes || undefined,
  };
}
