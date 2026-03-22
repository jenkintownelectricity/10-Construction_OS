/**
 * Fireproofing Source Adapter
 *
 * Hydrates canonical assembly drafts from fire_proof_assistant ISOVER sequence data.
 * Maps one structured fireproofing DNA sequence into a canonical assembly draft
 * using Assembly Kernel assembly_system schema shape.
 *
 * Source: fire_proof_assistant/isover_master_db.json
 * Source structure: 20-layer DNA taxonomy from ISOVER FireProtect Handbook
 *
 * Read-only consumption of fire_proof_assistant data.
 * Governance: VKGL04R — Ring 3 NO-TOUCH on fire_proof_assistant.
 */

import type {
  CanonicalAssemblyDraft,
  AssemblyLayer,
  AttachmentMethod,
  SourceLineage,
} from './types';

// ─── ISOVER DNA Sequence shape (from fire_proof_assistant) ──────────────

interface ISOVERSequence {
  readonly id: string;
  readonly data: {
    readonly system?: string;
    readonly substrate?: string;
    readonly rating?: string;
    readonly crit_temp?: string;
    readonly thick_mm?: number;
    readonly max_av?: number | null;
    readonly note?: string;
    readonly fixing?: string;
  };
}

// ─── Fixing method mapping ──────────────────────────────────────────────

function mapFixing(seq: ISOVERSequence): AttachmentMethod {
  const id = seq.id.toUpperCase();
  const fixing = seq.data.fixing?.toUpperCase() ?? '';
  if (id.includes('-SCR-') || fixing.includes('SCR')) return 'mechanically_attached';
  if (id.includes('-PIN-') || fixing.includes('PIN')) return 'mechanically_attached';
  if (id.includes('-ADH-') || fixing.includes('ADH') || id.includes('-GLU-')) return 'fully_adhered';
  return 'mechanically_attached';
}

// ─── Sample ISOVER sequences (from isover_master_db.json) ───────────────

/**
 * Selected ISOVER FireProtect 150 sequence — R60 rated, 500C critical temp,
 * 40mm thickness, max section factor 272 m^-1.
 * Represents one real fireproofing product configuration.
 */
export const SAMPLE_ISOVER_SEQUENCE: ISOVERSequence = {
  id: 'EU-AEC-23-078100-SGO-ISO-FP-150-SW-STL-GEN-I-4S-MEC-EN13381-R60-500C-040-SCR-PG08',
  data: {
    system: 'FireProtect 150',
    substrate: 'Steel',
    rating: 'R60',
    crit_temp: '500C',
    thick_mm: 40,
    max_av: 272,
  },
};

/**
 * Additional ISOVER sequences available for browsing in UI.
 */
export const AVAILABLE_ISOVER_SEQUENCES: readonly ISOVERSequence[] = [
  {
    id: 'EU-AEC-23-078100-SGO-ISO-FP-150-SW-STL-GEN-I-4S-MEC-EN13381-R30-500C-020-SCR-PG08',
    data: { system: 'FireProtect 150', substrate: 'Steel', rating: 'R30', crit_temp: '500C', thick_mm: 20, max_av: 558 },
  },
  {
    id: 'EU-AEC-23-078100-SGO-ISO-FP-150-SW-STL-GEN-I-4S-MEC-EN13381-R30-600C-020-SCR-PG08',
    data: { system: 'FireProtect 150', substrate: 'Steel', rating: 'R30', crit_temp: '600C', thick_mm: 20, max_av: 645 },
  },
  SAMPLE_ISOVER_SEQUENCE,
  {
    id: 'EU-AEC-23-078100-SGO-ISO-FP-150-SW-STL-GEN-I-4S-MEC-EN13381-R90-500C-030-SCR-PG08',
    data: { system: 'FireProtect 150', substrate: 'Steel', rating: 'R90', crit_temp: '500C', thick_mm: 30, max_av: 106 },
  },
  {
    id: 'EU-AEC-23-078100-SGO-ISO-FP-150-SW-STL-GEN-I-4S-MEC-EN13381-R120-500C-040-SCR-PG08',
    data: { system: 'FireProtect 150', substrate: 'Steel', rating: 'R120', crit_temp: '500C', thick_mm: 40, max_av: 85 },
  },
  {
    id: 'EU-AEC-23-078100-SGO-ISO-FP-150-SW-STL-GEN-I-4S-MEC-EN13381-R180-500C-060-SCR-PG08',
    data: { system: 'FireProtect 150', substrate: 'Steel', rating: 'R180', crit_temp: '500C', thick_mm: 60, max_av: 61 },
  },
];

export const SAMPLE_ISOVER_LINEAGE: SourceLineage = {
  sourceAdapter: 'fireproofingSourceAdapter',
  sourceFile: 'fire_proof_assistant/isover_master_db.json',
  sourceId: SAMPLE_ISOVER_SEQUENCE.id,
  hydratedAt: Date.now(),
};

// ─── Hydration: ISOVER sequence → canonical assembly draft ──────────────

/**
 * Hydrate an ISOVER fireproofing DNA sequence into a canonical assembly draft.
 * Maps fire protection product into Assembly Kernel assembly_system shape.
 *
 * The resulting assembly is a wall_assembly (fire-rated) since ISOVER FireProtect
 * is applied to structural steel elements as part of wall/structural assemblies.
 */
export function hydrateFireproofingDraft(
  seq: ISOVERSequence,
  draftId?: string,
): CanonicalAssemblyDraft {
  const layers: AssemblyLayer[] = [];
  const fixing = mapFixing(seq);

  // Primary fire protection layer
  layers.push({
    layer_id: 'LYR-FP-001',
    position: 1,
    control_layer_id: 'fire_smoke_control',
    material_ref: `MATL-ISOVER-FP150-${seq.data.thick_mm ?? 0}MM`,
    attachment_method: fixing,
    thickness: seq.data.thick_mm ? `${seq.data.thick_mm} mm` : undefined,
    notes: `${seq.data.system ?? 'ISOVER'} — ${seq.data.rating ?? 'N/A'} @ ${seq.data.crit_temp ?? 'N/A'}, max A/V ${seq.data.max_av ?? 'N/A'} m^-1`,
  });

  // Substrate layer (structural steel)
  layers.push({
    layer_id: 'LYR-FP-002',
    position: 2,
    control_layer_id: 'thermal_control',
    material_ref: 'MATL-STEEL-STRUCT-001',
    notes: `Substrate: ${seq.data.substrate ?? 'Structural Steel'}`,
  });

  const id = draftId ?? `DRAFT-FP-${Date.now()}`;

  return {
    schema_version: 'v1',
    system_id: id,
    title: `${seq.data.system ?? 'ISOVER'} Fire Protection Assembly — ${seq.data.rating ?? 'N/A'} (${seq.data.substrate ?? 'Steel'})`,
    assembly_type: 'wall_assembly',
    status: 'draft',
    layers,
    control_layer_continuity: {
      fire_smoke_control: 'continuous',
    },
    interface_zones: ['penetration'],
    tested_assembly_refs: ['TEST-ASSY-FR-001'],
    standards_refs: ['EN_13381_4', 'EN_13501_2'],
    warranty_posture: 'manufacturer_standard',
    notes: `Hydrated from ISOVER DNA sequence ${seq.id}. ${seq.data.note ?? ''}`.trim(),
  };
}

/**
 * Get pre-hydrated fireproofing draft from sample data.
 */
export function getSampleFireproofingDraft(): { draft: CanonicalAssemblyDraft; lineage: SourceLineage } {
  return {
    draft: hydrateFireproofingDraft(SAMPLE_ISOVER_SEQUENCE, 'DRAFT-FP-ISOVER-001'),
    lineage: SAMPLE_ISOVER_LINEAGE,
  };
}
