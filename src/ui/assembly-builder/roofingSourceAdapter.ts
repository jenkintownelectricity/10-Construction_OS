/**
 * Roofing Source Adapter
 *
 * Hydrates canonical assembly drafts from ShopDrawing_Compiler structures.
 * Uses the assembly_letter_parser extraction shape and detail_analysis_contract
 * to map roofing component stacks into Assembly Kernel assembly_system shape.
 *
 * Source: ShopDrawing_Compiler/compiler/intake/assembly_letter_parser.py
 * Source: ShopDrawing_Compiler/compiler/intake/detail_analysis_contract_seed.json
 *
 * Read-only consumption of ShopDrawing_Compiler structures.
 * Governance: VKGL04R — Ring 3 TOUCH-ALLOWED on ShopDrawing_Compiler (adapter only).
 */

import type {
  CanonicalAssemblyDraft,
  AssemblyLayer,
  ControlLayerId,
  AttachmentMethod,
  SourceLineage,
} from './types';

// ─── ShopDrawing_Compiler extraction shape (from assembly_letter_parser.py) ──

interface RoofingAssemblyExtraction {
  readonly manufacturer: string;
  readonly assembly_roof_area: string;
  readonly system: string;
  readonly membrane_1?: string;
  readonly membrane_1_attachment?: string;
  readonly coverboard_1?: string;
  readonly coverboard_1_attachment?: string;
  readonly coverboard_2?: string;
  readonly coverboard_2_attachment?: string;
  readonly insulation_layer_1?: string;
  readonly insulation_layer_1_attachment?: string;
  readonly insulation_layer_2?: string;
  readonly insulation_layer_2_attachment?: string;
  readonly vapor_barrier?: string;
  readonly vapor_barrier_attachment?: string;
  readonly deck_slope?: string;
  readonly deck_slope_attachment?: string;
}

// ─── Attachment method mapping ──────────────────────────────────────────

function mapAttachment(raw?: string): AttachmentMethod | undefined {
  if (!raw) return undefined;
  const lower = raw.toLowerCase();
  if (lower.includes('adhered') || lower.includes('adhesive')) return 'fully_adhered';
  if (lower.includes('mechanically') || lower.includes('fastened') || lower.includes('plates')) return 'mechanically_attached';
  if (lower.includes('torch')) return 'torch_applied';
  if (lower.includes('self-adhered') || lower.includes('self adhered') || lower.includes('peel')) return 'self_adhered';
  if (lower.includes('ballast')) return 'ballasted';
  if (lower.includes('hot mopped') || lower.includes('hot-mopped')) return 'hot_mopped';
  if (lower.includes('cold')) return 'cold_applied';
  if (lower.includes('standing seam')) return 'standing_seam';
  return 'mechanically_attached';
}

// ─── System type to material ref mapping ────────────────────────────────

function membraneRef(system?: string): string {
  if (!system) return 'MATL-MEMBRANE-GEN';
  const upper = system.toUpperCase();
  if (upper.includes('TPO')) return 'MATL-TPO-001';
  if (upper.includes('PVC')) return 'MATL-PVC-001';
  if (upper.includes('EPDM')) return 'MATL-EPDM-001';
  if (upper.includes('SBS')) return 'MATL-SBS-001';
  if (upper.includes('BUILT') || upper.includes('BUR')) return 'MATL-BUR-001';
  return 'MATL-MEMBRANE-GEN';
}

// ─── Sample roofing extraction (from ShopDrawing_Compiler patterns) ─────

/**
 * Example TPO roofing extraction representing a typical assembly letter
 * parsed by assembly_letter_parser.py. This mirrors the real output shape.
 */
export const SAMPLE_TPO_EXTRACTION: RoofingAssemblyExtraction = {
  manufacturer: 'Carlisle',
  assembly_roof_area: 'Main Store Roof',
  system: 'TPO',
  membrane_1: 'Carlisle Sure-Weld TPO 60 mil White',
  membrane_1_attachment: 'Fully Adhered with Carlisle Fast Adhesive',
  coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
  coverboard_1_attachment: 'Mechanically Attached',
  insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
  insulation_layer_1_attachment: 'Mechanically Attached with #14 FastenMaster Plates 12" o.c.',
  insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
  insulation_layer_2_attachment: 'Mechanically Attached with #14 FastenMaster Plates 12" o.c.',
  vapor_barrier: 'Carlisle VapAir 710 Self-Adhered',
  vapor_barrier_attachment: 'Self-Adhered',
  deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
  deck_slope_attachment: 'Welded to steel joists',
};

export const SAMPLE_TPO_LINEAGE: SourceLineage = {
  sourceAdapter: 'roofingSourceAdapter',
  sourceFile: 'ShopDrawing_Compiler/compiler/intake/assembly_letter_parser.py',
  sourceId: 'SDC-TPO-CARLISLE-001',
  hydratedAt: Date.now(),
};

// ─── Hydration: extraction → canonical assembly draft ───────────────────

/**
 * Hydrate a roofing assembly extraction into a canonical assembly draft.
 * Maps ShopDrawing_Compiler component layers to Assembly Kernel layer stack.
 */
export function hydrateRoofingDraft(
  extraction: RoofingAssemblyExtraction,
  draftId?: string,
): CanonicalAssemblyDraft {
  const layers: AssemblyLayer[] = [];
  let pos = 1;

  // Layer 1: Membrane → bulk_water_control
  if (extraction.membrane_1) {
    layers.push({
      layer_id: `LYR-R-${String(pos).padStart(3, '0')}`,
      position: pos++,
      control_layer_id: 'bulk_water_control',
      material_ref: membraneRef(extraction.system),
      attachment_method: mapAttachment(extraction.membrane_1_attachment),
      notes: extraction.membrane_1,
    });
  }

  // Layer 2: Coverboard 1 → protection_layer
  if (extraction.coverboard_1) {
    layers.push({
      layer_id: `LYR-R-${String(pos).padStart(3, '0')}`,
      position: pos++,
      control_layer_id: 'protection_layer',
      material_ref: 'MATL-COVERBD-001',
      attachment_method: mapAttachment(extraction.coverboard_1_attachment),
      notes: extraction.coverboard_1,
    });
  }

  // Layer 3: Coverboard 2 → protection_layer (if present)
  if (extraction.coverboard_2) {
    layers.push({
      layer_id: `LYR-R-${String(pos).padStart(3, '0')}`,
      position: pos++,
      control_layer_id: 'protection_layer',
      material_ref: 'MATL-COVERBD-002',
      attachment_method: mapAttachment(extraction.coverboard_2_attachment),
      notes: extraction.coverboard_2,
    });
  }

  // Layer 4: Insulation 1 → thermal_control
  if (extraction.insulation_layer_1) {
    layers.push({
      layer_id: `LYR-R-${String(pos).padStart(3, '0')}`,
      position: pos++,
      control_layer_id: 'thermal_control',
      material_ref: 'MATL-POLYISO-001',
      attachment_method: mapAttachment(extraction.insulation_layer_1_attachment),
      notes: extraction.insulation_layer_1,
    });
  }

  // Layer 5: Insulation 2 → thermal_control (if present)
  if (extraction.insulation_layer_2) {
    layers.push({
      layer_id: `LYR-R-${String(pos).padStart(3, '0')}`,
      position: pos++,
      control_layer_id: 'thermal_control',
      material_ref: 'MATL-POLYISO-002',
      attachment_method: mapAttachment(extraction.insulation_layer_2_attachment),
      notes: extraction.insulation_layer_2,
    });
  }

  // Layer 6: Vapor barrier → vapor_control
  if (extraction.vapor_barrier) {
    layers.push({
      layer_id: `LYR-R-${String(pos).padStart(3, '0')}`,
      position: pos++,
      control_layer_id: 'vapor_control',
      material_ref: 'MATL-VR-001',
      attachment_method: mapAttachment(extraction.vapor_barrier_attachment),
      notes: extraction.vapor_barrier,
    });
  }

  const id = draftId ?? `DRAFT-ROOF-${Date.now()}`;

  return {
    schema_version: 'v1',
    system_id: id,
    title: `${extraction.manufacturer} ${extraction.system} Roof Assembly — ${extraction.assembly_roof_area}`,
    assembly_type: 'roof_assembly',
    status: 'draft',
    layers,
    control_layer_continuity: {
      bulk_water_control: 'continuous',
      thermal_control: 'continuous',
      vapor_control: 'continuous',
    },
    interface_zones: ['parapet_transition', 'penetration', 'roof_edge', 'curb_transition', 'drain_transition'],
    climate_context: {
      climate_zone: '5A',
      exposure_flags: ['freeze_thaw', 'high_wind'],
    },
    geometry_context: {
      geometry_contexts: ['low_slope_roof'],
    },
    standards_refs: ['ASHRAE_90_1', 'IBC'],
    warranty_posture: 'system_warranty',
    notes: `Hydrated from ${extraction.manufacturer} assembly letter via ShopDrawing_Compiler extraction.`,
  };
}

/**
 * Get pre-hydrated roofing draft from sample data.
 */
export function getSampleRoofingDraft(): { draft: CanonicalAssemblyDraft; lineage: SourceLineage } {
  return {
    draft: hydrateRoofingDraft(SAMPLE_TPO_EXTRACTION, 'DRAFT-ROOF-SDC-001'),
    lineage: SAMPLE_TPO_LINEAGE,
  };
}
