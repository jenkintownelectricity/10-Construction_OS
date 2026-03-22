/**
 * Read-only hydration of existing assembly examples from Construction_Assembly_Kernel.
 * Source files:
 *   - Construction_Assembly_Kernel/examples/tpo_roof_assembly.example.json
 *   - Construction_Assembly_Kernel/examples/fire_rated_assembly.example.json
 *
 * These are consumed read-only. No Assembly Kernel files are modified.
 * Governance: VKGL04R — Ring 3 read-only on Assembly Kernel.
 */

import type { CanonicalAssemblyDraft, SourceLineage } from './types';

/**
 * TPO Roof Assembly — existing active example from Assembly Kernel.
 * system_id: ASSY-ROOF-001
 */
export const TPO_ROOF_ASSEMBLY_EXAMPLE: CanonicalAssemblyDraft = {
  schema_version: 'v1',
  system_id: 'ASSY-ROOF-001',
  title: 'Fully Adhered TPO Roof Assembly — Steel Deck Substrate',
  assembly_type: 'roof_assembly',
  status: 'active',
  layers: [
    { layer_id: 'LYR-001', position: 1, control_layer_id: 'bulk_water_control', material_ref: 'MATL-TPO-001', attachment_method: 'fully_adhered' },
    { layer_id: 'LYR-002', position: 2, control_layer_id: 'protection_layer', material_ref: 'MATL-COVERBD-001', attachment_method: 'mechanically_attached' },
    { layer_id: 'LYR-003', position: 3, control_layer_id: 'thermal_control', material_ref: 'MATL-POLYISO-001', attachment_method: 'mechanically_attached' },
    { layer_id: 'LYR-004', position: 4, control_layer_id: 'vapor_control', material_ref: 'MATL-VR-001', attachment_method: 'self_adhered' },
    { layer_id: 'LYR-005', position: 5, control_layer_id: 'air_control', material_ref: 'MATL-AB-001', attachment_method: 'self_adhered' },
  ],
  control_layer_continuity: {
    bulk_water_control: 'continuous',
    thermal_control: 'continuous',
    vapor_control: 'continuous',
    air_control: 'continuous',
  },
  interface_zones: ['parapet_transition', 'penetration', 'roof_edge', 'curb_transition', 'drain_transition'],
  climate_context: {
    climate_zone: '5A',
    exposure_flags: ['freeze_thaw', 'high_wind'],
  },
  tested_assembly_refs: ['TEST-WU-001', 'TEST-FR-001'],
  standards_refs: ['ASHRAE_90_1', 'IBC'],
  warranty_posture: 'system_warranty',
  notes: 'Standard configuration for commercial low-slope roof. Vapor retarder position assumes heating-dominated climate.',
};

export const TPO_ROOF_LINEAGE: SourceLineage = {
  sourceAdapter: 'assemblyKernelExamples',
  sourceFile: 'Construction_Assembly_Kernel/examples/tpo_roof_assembly.example.json',
  sourceId: 'ASSY-ROOF-001',
  hydratedAt: Date.now(),
};

/**
 * Fire-Rated Assembly — existing tested_assembly_record from Assembly Kernel.
 * This is a test record, not a full assembly system. Used as reference evidence
 * for fireproofing assembly drafts.
 */
export interface TestedAssemblyRecord {
  readonly schema_version: 'v1';
  readonly record_id: string;
  readonly title: string;
  readonly test_type: string;
  readonly test_standard_ref: string;
  readonly result: string;
  readonly status: string;
  readonly assembly_ref: string;
  readonly test_date: string;
  readonly lab_ref: string;
  readonly evidence_ref: string;
  readonly notes: string;
}

export const FIRE_RATED_ASSEMBLY_EXAMPLE: TestedAssemblyRecord = {
  schema_version: 'v1',
  record_id: 'TEST-ASSY-FR-001',
  title: 'NFPA 285 Tested Wall Assembly — Metal Composite Panel with Mineral Wool CI',
  test_type: 'fire_rating',
  test_standard_ref: 'NFPA_285',
  result: 'pass',
  status: 'active',
  assembly_ref: 'ASSY-WALL-MCM-001',
  test_date: '2024-06-15',
  lab_ref: 'Southwest Research Institute',
  evidence_ref: 'EV-FR-001',
  notes: 'Assembly includes: aluminum composite panel (FR-core), 1-inch air cavity, 3-inch mineral wool continuous insulation, fluid-applied air/water barrier, glass-mat gypsum sheathing on steel studs. Passes NFPA 285 for buildings of any height. IBC Section 1402.5 compliance.',
};

export const FIRE_RATED_LINEAGE: SourceLineage = {
  sourceAdapter: 'assemblyKernelExamples',
  sourceFile: 'Construction_Assembly_Kernel/examples/fire_rated_assembly.example.json',
  sourceId: 'TEST-ASSY-FR-001',
  hydratedAt: Date.now(),
};

/** All available assembly examples for the builder UI */
export const ASSEMBLY_EXAMPLES = [
  { draft: TPO_ROOF_ASSEMBLY_EXAMPLE, lineage: TPO_ROOF_LINEAGE, category: 'roofing' as const },
  { draft: null, testedRecord: FIRE_RATED_ASSEMBLY_EXAMPLE, lineage: FIRE_RATED_LINEAGE, category: 'fireproofing' as const },
] as const;
