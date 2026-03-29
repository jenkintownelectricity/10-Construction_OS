/**
 * PMMA Product Registry — Canonical Product Truth Source
 *
 * L0-CMD-BARRETT-PMMA-GEN-005
 * Wave 1 — Product Registry Foundation
 *
 * Enforces chemistry truth boundaries for the Barrett PMMA Detail Generator.
 * All product lookups resolve through this registry.
 *
 * Classification branches:
 *   PMMA — In PMMA Generator
 *   Hybrid Polyurea/Polyurethane — Excluded From PMMA Generator
 *   Pending Review — Review Gate Required
 */

// ─── Chemistry Family ────────────────────────────────────────────

export type ChemistryFamily =
  | 'PMMA'
  | 'Hybrid Polyurea/Polyurethane'
  | 'Pending Review';

// ─── Product Class ───────────────────────────────────────────────

export type ProductClass =
  | 'Barrett PMMA'
  | 'PUMA PROOF'
  | 'Generic PMMA'
  | 'HIPPA COAT'
  | 'HyppoCoat 100'
  | 'HyppoCoat BC'
  | 'HyppoCoat TC'
  | 'HyppoCoat GC'
  | 'HyppoCoat 250';

// ─── Branch Status ───────────────────────────────────────────────

export type BranchStatus =
  | 'In PMMA Generator'
  | 'Excluded From PMMA Generator'
  | 'Review Gate Required';

// ─── Registry Entry ──────────────────────────────────────────────

export interface PMMAProductEntry {
  readonly canonical_name: string;
  readonly alias_names: readonly string[];
  readonly product_class: ProductClass;
  readonly chemistry_family: ChemistryFamily;
  readonly branch_status: BranchStatus;
}

// ─── Canonical Product Registry ──────────────────────────────────

export const PMMA_PRODUCT_REGISTRY: readonly PMMAProductEntry[] = [
  // ── PMMA Chemistry Family ──────────────────────────────────────
  {
    canonical_name: 'Barrett PMMA',
    alias_names: ['Barrett', 'Barrett Roofing PMMA', 'Barrett MMA'],
    product_class: 'Barrett PMMA',
    chemistry_family: 'PMMA',
    branch_status: 'In PMMA Generator',
  },
  {
    canonical_name: 'PUMA PROOF',
    alias_names: ['Puma Proof', 'PumaProof', 'PUMA', 'Puma proof'],
    product_class: 'PUMA PROOF',
    chemistry_family: 'PMMA',
    branch_status: 'In PMMA Generator',
  },
  {
    canonical_name: 'Generic PMMA',
    alias_names: ['PMMA', 'Generic MMA', 'MMA Resin'],
    product_class: 'Generic PMMA',
    chemistry_family: 'PMMA',
    branch_status: 'In PMMA Generator',
  },
  {
    canonical_name: 'HIPPA COAT',
    alias_names: ['Hippa Coat', 'HippaCoat', 'Hippacoat', 'HIPPA'],
    product_class: 'HIPPA COAT',
    chemistry_family: 'PMMA',
    branch_status: 'In PMMA Generator',
  },

  // ── Hybrid Polyurea/Polyurethane — EXCLUDED ────────────────────
  {
    canonical_name: 'HyppoCoat 100',
    alias_names: ['Hyppocoat 100', 'Hypocoat 100', 'HC100'],
    product_class: 'HyppoCoat 100',
    chemistry_family: 'Hybrid Polyurea/Polyurethane',
    branch_status: 'Excluded From PMMA Generator',
  },
  {
    canonical_name: 'HyppoCoat BC',
    alias_names: ['Hyppocoat BC', 'Hypocoat BC', 'HC-BC'],
    product_class: 'HyppoCoat BC',
    chemistry_family: 'Hybrid Polyurea/Polyurethane',
    branch_status: 'Excluded From PMMA Generator',
  },
  {
    canonical_name: 'HyppoCoat TC',
    alias_names: ['Hyppocoat TC', 'Hypocoat TC', 'HC-TC'],
    product_class: 'HyppoCoat TC',
    chemistry_family: 'Hybrid Polyurea/Polyurethane',
    branch_status: 'Excluded From PMMA Generator',
  },
  {
    canonical_name: 'HyppoCoat GC',
    alias_names: ['Hyppocoat GC', 'Hypocoat GC', 'HC-GC'],
    product_class: 'HyppoCoat GC',
    chemistry_family: 'Hybrid Polyurea/Polyurethane',
    branch_status: 'Excluded From PMMA Generator',
  },

  // ── Pending Review — GATED ─────────────────────────────────────
  {
    canonical_name: 'HyppoCoat 250',
    alias_names: ['Hyppocoat 250', 'Hypocoat 250', 'HC250'],
    product_class: 'HyppoCoat 250',
    chemistry_family: 'Pending Review',
    branch_status: 'Review Gate Required',
  },
] as const;

// ─── Lookup Helpers ──────────────────────────────────────────────

export function getProductByCanonicalName(name: string): PMMAProductEntry | undefined {
  return PMMA_PRODUCT_REGISTRY.find((p) => p.canonical_name === name);
}

export function getProductsByChemistryFamily(family: ChemistryFamily): readonly PMMAProductEntry[] {
  return PMMA_PRODUCT_REGISTRY.filter((p) => p.chemistry_family === family);
}

export function getProductsByBranchStatus(status: BranchStatus): readonly PMMAProductEntry[] {
  return PMMA_PRODUCT_REGISTRY.filter((p) => p.branch_status === status);
}

export function getPMMAGeneratorProducts(): readonly PMMAProductEntry[] {
  return PMMA_PRODUCT_REGISTRY.filter((p) => p.branch_status === 'In PMMA Generator');
}

export function isExcludedFromPMMAGenerator(canonicalName: string): boolean {
  const product = getProductByCanonicalName(canonicalName);
  return product !== undefined && product.branch_status === 'Excluded From PMMA Generator';
}

export function requiresReviewGate(canonicalName: string): boolean {
  const product = getProductByCanonicalName(canonicalName);
  return product !== undefined && product.branch_status === 'Review Gate Required';
}
