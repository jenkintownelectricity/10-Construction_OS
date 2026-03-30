/**
 * PMMA Taxonomy Model — Canonical Detail Family Codes
 *
 * L0-CMD-BARRETT-PMMA-GEN-005
 * Wave 3 — PMMA Taxonomy Model
 *
 * Defines the 12 canonical PMMA detail family codes used for
 * deterministic naming and assembly resolution. These codes align
 * to the SDIO taxonomy spine.
 */

// ─── Taxonomy Family Codes ───────────────────────────────────────

export type PMMATaxonomyCode =
  | 'AS'  // Assembly Sequence
  | 'PT'  // Penetration
  | 'CO'  // Corner
  | 'ED'  // Edge / Termination
  | 'DR'  // Drain
  | 'PE'  // Perimeter
  | 'CU'  // Curb
  | 'EJ'  // Expansion Joint
  | 'CN'  // Connection
  | 'ST'  // Substrate Transition
  | 'RP'  // Repair
  | 'TR'  // Transition;

// ─── Taxonomy Family Definition ─────────────────────────────────

export interface PMMATaxonomyFamily {
  readonly code: PMMATaxonomyCode;
  readonly name: string;
  readonly description: string;
}

// ─── Canonical Taxonomy Registry ────────────────────────────────

export const PMMA_TAXONOMY: readonly PMMATaxonomyFamily[] = [
  {
    code: 'AS',
    name: 'Assembly Sequence',
    description: 'Full field assembly layup sequences including primer, resin, fleece, and topcoat.',
  },
  {
    code: 'PT',
    name: 'Penetration',
    description: 'Pipe penetrations, mechanical curb penetrations, and conduit pass-throughs.',
  },
  {
    code: 'CO',
    name: 'Corner',
    description: 'Inside corners, outside corners, and corner reinforcement sequences.',
  },
  {
    code: 'ED',
    name: 'Edge / Termination',
    description: 'Drip edges, gravel stops, fascia terminations, and membrane edge details.',
  },
  {
    code: 'DR',
    name: 'Drain',
    description: 'Interior drains, scuppers, overflow drains, and gutter connections.',
  },
  {
    code: 'PE',
    name: 'Perimeter',
    description: 'Wall-to-deck transitions, base flashings, and perimeter termination bars.',
  },
  {
    code: 'CU',
    name: 'Curb',
    description: 'Mechanical curbs, skylight curbs, and raised curb assemblies.',
  },
  {
    code: 'EJ',
    name: 'Expansion Joint',
    description: 'Structural expansion joints, area dividers, and movement joints.',
  },
  {
    code: 'CN',
    name: 'Connection',
    description: 'System-to-system connections, tie-ins to existing membranes, and substrate bonds.',
  },
  {
    code: 'ST',
    name: 'Substrate Transition',
    description: 'Transitions between substrate types: concrete to metal, wood to concrete, etc.',
  },
  {
    code: 'RP',
    name: 'Repair',
    description: 'Localized repair details, blister repairs, and patching sequences.',
  },
  {
    code: 'TR',
    name: 'Transition',
    description: 'General transitions between roofing zones, heights, or material changes.',
  },
] as const;

// ─── Lookup Helpers ──────────────────────────────────────────────

const taxonomyByCode = new Map<PMMATaxonomyCode, PMMATaxonomyFamily>(
  PMMA_TAXONOMY.map((t) => [t.code, t]),
);

export function getTaxonomyFamily(code: PMMATaxonomyCode): PMMATaxonomyFamily | undefined {
  return taxonomyByCode.get(code);
}

export function isValidTaxonomyCode(code: string): code is PMMATaxonomyCode {
  return taxonomyByCode.has(code as PMMATaxonomyCode);
}

export function getAllTaxonomyCodes(): readonly PMMATaxonomyCode[] {
  return PMMA_TAXONOMY.map((t) => t.code);
}
