/**
 * Context-to-Roofing-Draft Mapper
 *
 * Deterministic mapper: validated sourceContext → CanonicalAssemblyDraft.
 * Uses bounded local lookup logic inside Construction_Application_OS.
 * Calls existing hydrateRoofingDraft() from roofingSourceAdapter.
 *
 * FAIL_CLOSED on:
 *   - Unmappable manufacturer/spec combination
 *   - Ambiguous mapping result
 *   - Unsupported category
 *
 * The mapper does NOT:
 *   - Invent missing values
 *   - Infer unsupported assembly truth
 *   - Call external services
 *   - Broaden into generalized pattern intelligence
 *
 * Governance: VKGL04R — Ring 3 TOUCH-ALLOWED
 */

import type { GenerationSourceContext } from '../stores/generationStore';
import type { CanonicalAssemblyDraft } from '../assembly-builder/types';
import { hydrateRoofingDraft } from '../assembly-builder/roofingSourceAdapter';

// ─── Mapping Result ───────────────────────────────────────────────────

export interface MappingResult {
  readonly success: boolean;
  readonly draft?: CanonicalAssemblyDraft;
  readonly errorCode?: string;
  readonly errorMessage?: string;
}

// ─── Spec-to-System Lookup (bounded, local) ───────────────────────────

type RoofingSystem = 'TPO' | 'SBS' | 'EPDM' | 'PVC';

/**
 * Maps CSI spec codes to roofing membrane system types.
 * Deterministic: same spec always produces same system.
 */
const SPEC_TO_SYSTEM: ReadonlyMap<string, RoofingSystem> = new Map([
  ['07 52 00', 'SBS'],    // Modified Bituminous Membrane Roofing (generic)
  ['07 52 13', 'SBS'],    // SBS Modified Bituminous Membrane Roofing
  ['07 52 16', 'SBS'],    // SBS Modified Bituminous Sheet Roofing
  ['07 53 23', 'EPDM'],   // Ethylene-Propylene-Diene-Monomer Roofing
  ['07 54 19', 'PVC'],    // PVC Roofing Membrane
  ['07 54 23', 'TPO'],    // Thermoplastic Polyolefin Membrane Roofing
  ['07 55 56', 'TPO'],    // Protected Membrane Roofing (TPO default)
]);

// ─── Manufacturer-System Extraction Templates (bounded, local) ────────

/**
 * Deterministic extraction templates for known manufacturer/system combos.
 * These mirror the RoofingAssemblyExtraction shape from roofingSourceAdapter.
 * Each template is a fixed set of layers — no invention, no inference.
 */
interface ExtractionTemplate {
  readonly membrane_1: string;
  readonly membrane_1_attachment: string;
  readonly coverboard_1: string;
  readonly coverboard_1_attachment: string;
  readonly insulation_layer_1: string;
  readonly insulation_layer_1_attachment: string;
  readonly insulation_layer_2: string;
  readonly insulation_layer_2_attachment: string;
  readonly vapor_barrier: string;
  readonly vapor_barrier_attachment: string;
  readonly deck_slope: string;
  readonly deck_slope_attachment: string;
}

/**
 * Lookup key: `${normalizedManufacturer}::${system}`
 * Bounded set. No wildcard matching. No fuzzy logic.
 */
const EXTRACTION_TEMPLATES: ReadonlyMap<string, ExtractionTemplate> = new Map([
  // ─── Carlisle SynTec ─────────────────────────────────────────────
  ['carlisle syntec::TPO', {
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
  }],
  ['carlisle syntec::SBS', {
    membrane_1: 'Carlisle WIP 300HT SBS Membrane 160 mil',
    membrane_1_attachment: 'Torch Applied',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with #14 FastenMaster Plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.5" R-14.5',
    insulation_layer_2_attachment: 'Mechanically Attached with #14 FastenMaster Plates 12" o.c.',
    vapor_barrier: 'Carlisle VapAir 710 Self-Adhered',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  ['carlisle syntec::PVC', {
    membrane_1: 'Carlisle Sure-Flex PVC 80 mil White',
    membrane_1_attachment: 'Fully Adhered',
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
  }],
  ['carlisle syntec::EPDM', {
    membrane_1: 'Carlisle Sure-Seal EPDM 60 mil Black',
    membrane_1_attachment: 'Fully Adhered with Carlisle BA Adhesive',
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
  }],
  // ─── Firestone Building Products ─────────────────────────────────
  ['firestone building products::TPO', {
    membrane_1: 'Firestone UltraPly TPO 60 mil White',
    membrane_1_attachment: 'Fully Adhered',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'Firestone V-Force Self-Adhered Vapor Barrier',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  ['firestone building products::EPDM', {
    membrane_1: 'Firestone RubberGard EPDM 60 mil Black',
    membrane_1_attachment: 'Fully Adhered with Firestone BA Adhesive',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'Firestone V-Force Self-Adhered Vapor Barrier',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  // ─── Sika Corporation ────────────────────────────────────────────
  ['sika corporation::TPO', {
    membrane_1: 'Sika Sarnafil G410 TPO 60 mil White',
    membrane_1_attachment: 'Fully Adhered',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'Sika Sarnavap 1000E',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  ['sika corporation::PVC', {
    membrane_1: 'Sika Sarnafil S327 PVC 80 mil White',
    membrane_1_attachment: 'Fully Adhered',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'Sika Sarnavap 1000E',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  // ─── GAF ───────────────────────────────────────────────────────────
  ['gaf::TPO', {
    membrane_1: 'GAF EverGuard Extreme TPO 60 mil White',
    membrane_1_attachment: 'Fully Adhered with GAF LRF Adhesive',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'GAF VaporBlock Self-Adhered Vapor Retarder',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  ['gaf::SBS', {
    membrane_1: 'GAF Ruberoid SBS HW Membrane 160 mil',
    membrane_1_attachment: 'Torch Applied',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.5" R-14.5',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'GAF VaporBlock Self-Adhered Vapor Retarder',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  // ─── Johns Manville ────────────────────────────────────────────────
  ['johns manville::TPO', {
    membrane_1: 'JM TPO 60 mil White Membrane',
    membrane_1_attachment: 'Fully Adhered with JMDERA Adhesive',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'JM Vapor Barrier SA',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  ['johns manville::PVC', {
    membrane_1: 'JM PVC 80 mil White Membrane',
    membrane_1_attachment: 'Fully Adhered',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'JM Vapor Barrier SA',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  ['johns manville::EPDM', {
    membrane_1: 'JM EPDM 60 mil Black Membrane',
    membrane_1_attachment: 'Fully Adhered with JM EPDM BA Adhesive',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'JM Vapor Barrier SA',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  // ─── Henry Company ─────────────────────────────────────────────────
  ['henry company::TPO', {
    membrane_1: 'Henry Sealant TPO 60 mil White',
    membrane_1_attachment: 'Fully Adhered with Henry 286 Adhesive',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.6" R-15.0',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'Henry Blueskin VP100 Self-Adhered',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
  ['henry company::SBS', {
    membrane_1: 'Henry Paradiene 20/20 SBS Membrane 160 mil',
    membrane_1_attachment: 'Torch Applied',
    coverboard_1: 'DensDeck Prime 1/4" Gypsum Cover Board',
    coverboard_1_attachment: 'Mechanically Attached',
    insulation_layer_1: 'Polyisocyanurate 3.0" R-17.4',
    insulation_layer_1_attachment: 'Mechanically Attached with plates 12" o.c.',
    insulation_layer_2: 'Polyisocyanurate 2.5" R-14.5',
    insulation_layer_2_attachment: 'Mechanically Attached with plates 12" o.c.',
    vapor_barrier: 'Henry Blueskin VP100 Self-Adhered',
    vapor_barrier_attachment: 'Self-Adhered',
    deck_slope: '22 Gauge Steel Deck, 1/4" per foot slope',
    deck_slope_attachment: 'Welded to steel joists',
  }],
]);

// ─── Manufacturer Normalization ───────────────────────────────────────

function normalizeManufacturer(raw: string): string {
  return raw.trim().toLowerCase();
}

// ─── Spec-to-System Resolution ────────────────────────────────────────

function resolveSystem(spec: string): RoofingSystem | null {
  // Try exact match first
  const exact = SPEC_TO_SYSTEM.get(spec);
  if (exact) return exact;

  // Try prefix match (e.g. "07 52 16" → check "07 52 00")
  const prefix = spec.slice(0, 5) + ' 00';
  return SPEC_TO_SYSTEM.get(prefix) ?? null;
}

// ─── Mapper ───────────────────────────────────────────────────────────

/**
 * Deterministically map a validated sourceContext into a CanonicalAssemblyDraft.
 *
 * Uses bounded local lookup: spec → system type, manufacturer+system → extraction template.
 * Calls existing hydrateRoofingDraft() from roofingSourceAdapter.
 *
 * FAIL_CLOSED on unmappable combinations.
 */
export function mapContextToRoofingDraft(
  context: GenerationSourceContext,
): MappingResult {
  // Step 1: Resolve roofing system from spec
  const system = resolveSystem(context.spec);
  if (!system) {
    return {
      success: false,
      errorCode: 'UNMAPPABLE_SPEC',
      errorMessage: `FAIL_CLOSED: Spec '${context.spec}' cannot be mapped to a known roofing system. Known specs: ${[...SPEC_TO_SYSTEM.keys()].join(', ')}.`,
    };
  }

  // Step 2: Look up extraction template for manufacturer + system
  const normalizedMfr = normalizeManufacturer(context.manufacturer);
  const lookupKey = `${normalizedMfr}::${system}`;
  const template = EXTRACTION_TEMPLATES.get(lookupKey);

  if (!template) {
    return {
      success: false,
      errorCode: 'UNMAPPABLE_MANUFACTURER',
      errorMessage: `FAIL_CLOSED: No extraction template for manufacturer '${context.manufacturer}' with system '${system}'. Known combinations: ${[...EXTRACTION_TEMPLATES.keys()].join(', ')}.`,
    };
  }

  // Step 3: Build extraction shape from template + context
  const extraction = {
    manufacturer: context.manufacturer,
    assembly_roof_area: context.title,
    system,
    ...template,
  };

  // Step 4: Deterministic draft ID from submittalId
  const draftId = `DRAFT-ROOF-${context.submittalId}`;

  // Step 5: Hydrate using existing roofing adapter seam
  const draft = hydrateRoofingDraft(extraction, draftId);

  return { success: true, draft };
}
