/**
 * PMMA Assembly Library — Canonical Assembly Records
 *
 * L0-CMD-BARRETT-PMMA-GEN-005
 * Wave 4 — PMMA Assembly Library
 *
 * Defines canonical assembly records for PMMA detail generation.
 * Each assembly maps to a taxonomy family code and a product class.
 * Assemblies are the atomic units that the generator resolver selects.
 */

import type { PMMATaxonomyCode } from './pmmaTaxonomy';
import type { ProductClass } from './pmmaProductRegistry';

// ─── Assembly Layer ──────────────────────────────────────────────

export interface PMMAAssemblyLayer {
  readonly order: number;
  readonly material: string;
  readonly description: string;
  readonly thickness_mm?: number;
}

// ─── Assembly Record ─────────────────────────────────────────────

export interface PMMAAssemblyRecord {
  readonly assembly_id: string;
  readonly name: string;
  readonly product_class: ProductClass;
  readonly taxonomy_code: PMMATaxonomyCode;
  readonly description: string;
  readonly layers: readonly PMMAAssemblyLayer[];
  readonly applicable_substrates: readonly string[];
  readonly notes?: string;
}

// ─── Canonical Assembly Library ──────────────────────────────────

export const PMMA_ASSEMBLY_LIBRARY: readonly PMMAAssemblyRecord[] = [
  // ── PUMA PROOF Standard Field Assembly ───────────────────────
  {
    assembly_id: 'PMMA-AS-FIELD-PUMAPROOF',
    name: 'PUMA PROOF Standard Field Assembly',
    product_class: 'PUMA PROOF',
    taxonomy_code: 'AS',
    description: 'Standard field membrane assembly for PUMA PROOF PMMA system. Full layup from primer through topcoat.',
    layers: [
      { order: 1, material: 'PUMA PROOF Primer', description: 'Substrate primer coat', thickness_mm: 0.3 },
      { order: 2, material: 'PUMA PROOF Base Resin', description: 'First resin application', thickness_mm: 1.0 },
      { order: 3, material: 'PUMA PROOF Reinforcement Fleece', description: 'Polyester reinforcement fleece embedded in resin' },
      { order: 4, material: 'PUMA PROOF Base Resin', description: 'Second resin application saturating fleece', thickness_mm: 1.0 },
      { order: 5, material: 'PUMA PROOF Topcoat', description: 'UV-stable finish topcoat', thickness_mm: 0.5 },
    ],
    applicable_substrates: ['concrete', 'plywood', 'metal deck', 'existing membrane'],
  },

  // ── PUMA PROOF Tile Underlayment ─────────────────────────────
  {
    assembly_id: 'PMMA-AS-TILE-PUMAPROOF',
    name: 'PUMA PROOF Tile Underlayment',
    product_class: 'PUMA PROOF',
    taxonomy_code: 'AS',
    description: 'Waterproofing underlayment assembly for tile or paver overlay using PUMA PROOF PMMA.',
    layers: [
      { order: 1, material: 'PUMA PROOF Primer', description: 'Substrate primer coat', thickness_mm: 0.3 },
      { order: 2, material: 'PUMA PROOF Base Resin', description: 'First resin application', thickness_mm: 1.0 },
      { order: 3, material: 'PUMA PROOF Reinforcement Fleece', description: 'Polyester reinforcement fleece embedded in resin' },
      { order: 4, material: 'PUMA PROOF Base Resin', description: 'Second resin application saturating fleece', thickness_mm: 1.0 },
      { order: 5, material: 'PUMA PROOF Wearing Surface', description: 'Aggregate or tile-ready wearing surface', thickness_mm: 0.8 },
    ],
    applicable_substrates: ['concrete', 'plywood'],
    notes: 'Topcoat omitted — tile or paver system provides UV protection and wearing surface.',
  },

  // ── Barrett Inside Corner Reinforcement ──────────────────────
  {
    assembly_id: 'PMMA-CO-INSIDE-BARRETT',
    name: 'Barrett Inside Corner Reinforcement Sequence',
    product_class: 'Barrett PMMA',
    taxonomy_code: 'CO',
    description: 'Inside corner reinforcement detail for Barrett PMMA system. Pre-formed cant with fleece wrap.',
    layers: [
      { order: 1, material: 'Barrett PMMA Primer', description: 'Corner area primer' },
      { order: 2, material: 'Pre-formed PMMA Cant Strip', description: 'Rigid cant providing transition geometry' },
      { order: 3, material: 'Barrett PMMA Resin', description: 'Resin application over cant', thickness_mm: 1.0 },
      { order: 4, material: 'Barrett Reinforcement Fleece', description: 'Fleece strip spanning corner and extending min 75mm each side' },
      { order: 5, material: 'Barrett PMMA Resin', description: 'Saturating resin over fleece', thickness_mm: 1.0 },
      { order: 6, material: 'Barrett PMMA Topcoat', description: 'Finish topcoat over corner reinforcement', thickness_mm: 0.5 },
    ],
    applicable_substrates: ['concrete', 'masonry', 'metal'],
  },

  // ── HIPPA COAT PMMA Topcoat Assembly ─────────────────────────
  {
    assembly_id: 'PMMA-AS-TOPCOAT-HIPPACOAT',
    name: 'HIPPA COAT PMMA Topcoat Assembly',
    product_class: 'HIPPA COAT',
    taxonomy_code: 'AS',
    description: 'HIPPA COAT PMMA topcoat assembly. Validated as PMMA chemistry variant for generator inclusion.',
    layers: [
      { order: 1, material: 'HIPPA COAT Primer', description: 'Substrate primer coat', thickness_mm: 0.3 },
      { order: 2, material: 'HIPPA COAT Base Resin', description: 'PMMA base resin application', thickness_mm: 1.2 },
      { order: 3, material: 'HIPPA COAT Reinforcement Fleece', description: 'Polyester reinforcement fleece' },
      { order: 4, material: 'HIPPA COAT Base Resin', description: 'Second resin saturation', thickness_mm: 1.2 },
      { order: 5, material: 'HIPPA COAT Topcoat', description: 'UV-stable PMMA topcoat finish', thickness_mm: 0.5 },
    ],
    applicable_substrates: ['concrete', 'plywood', 'metal deck'],
    notes: 'HIPPA COAT validated as PMMA variant. Included in generator per L0 directive.',
  },
] as const;

// ─── Lookup Helpers ──────────────────────────────────────────────

export function getAssemblyById(id: string): PMMAAssemblyRecord | undefined {
  return PMMA_ASSEMBLY_LIBRARY.find((a) => a.assembly_id === id);
}

export function getAssembliesByTaxonomy(code: PMMATaxonomyCode): readonly PMMAAssemblyRecord[] {
  return PMMA_ASSEMBLY_LIBRARY.filter((a) => a.taxonomy_code === code);
}

export function getAssembliesByProductClass(productClass: ProductClass): readonly PMMAAssemblyRecord[] {
  return PMMA_ASSEMBLY_LIBRARY.filter((a) => a.product_class === productClass);
}

export function getAssembliesForSubstrate(substrate: string): readonly PMMAAssemblyRecord[] {
  const normalized = substrate.trim().toLowerCase();
  return PMMA_ASSEMBLY_LIBRARY.filter((a) =>
    a.applicable_substrates.some((s) => s.toLowerCase() === normalized),
  );
}
