/**
 * PMMA Detail Resolver — Generator Decision Engine
 *
 * L0-CMD-BARRETT-PMMA-GEN-005
 * Wave 6 — Generator Decision Engine
 *
 * Responsibilities:
 *   1. Select assembly based on input conditions
 *   2. Enforce chemistry boundaries
 *   3. Trigger review gate when required
 *   4. Generate deterministic detail names
 *
 * Naming format: [System]-[FamilyCode]-[Condition]-[Variant]
 * Example: PMMA-DR-SCUPPER-BARRETT
 */

import type { PMMAGeneratorRequest } from './pmmaGeneratorRequest';
import { validateGeneratorRequest } from './pmmaGeneratorRequest';
import {
  getProductByCanonicalName,
  isExcludedFromPMMAGenerator,
  requiresReviewGate,
  type PMMAProductEntry,
} from './pmmaProductRegistry';
import { resolveProductEntry } from './aliasNormalizationMap';
import {
  PMMA_ASSEMBLY_LIBRARY,
  type PMMAAssemblyRecord,
} from './pmmaAssemblyLibrary';
import { isValidTaxonomyCode, type PMMATaxonomyCode } from './pmmaTaxonomy';

// ─── Resolution Result Types ────────────────────────────────────

export interface DetailManifest {
  readonly detail_name: string;
  readonly system: string;
  readonly family_code: PMMATaxonomyCode;
  readonly condition: string;
  readonly variant: string;
  readonly assembly: PMMAAssemblyRecord;
  readonly product: PMMAProductEntry;
  readonly request: PMMAGeneratorRequest;
  readonly render_formats: readonly ('DXF' | 'SVG' | 'PDF')[];
}

export type ResolverResult =
  | { success: true; manifest: DetailManifest }
  | { success: false; reason: string; review_gate?: boolean };

// ─── Condition-to-Taxonomy Mapping ───────────────────────────────

function deriveTaxonomyCode(request: PMMAGeneratorRequest): PMMATaxonomyCode {
  // Priority-based condition resolution
  if (request.drain_type !== 'none') return 'DR';
  if (request.penetration_type !== 'none') return 'PT';
  if (request.curb_type !== 'none') return 'CU';
  if (request.joint_type !== 'none') return 'EJ';
  if (request.cant_condition !== 'no cant') return 'CO';
  // Default to Assembly Sequence for field conditions
  return 'AS';
}

function deriveConditionCode(request: PMMAGeneratorRequest, taxonomyCode: PMMATaxonomyCode): string {
  switch (taxonomyCode) {
    case 'DR': return request.drain_type.toUpperCase().replace(/\s+/g, '-');
    case 'PT': return request.penetration_type.toUpperCase().replace(/\s+/g, '-');
    case 'CU': return request.curb_type.toUpperCase().replace(/\s+/g, '-');
    case 'EJ': return request.joint_type.toUpperCase().replace(/\s+/g, '-');
    case 'CO': return request.cant_condition.toUpperCase().replace(/\s+/g, '-');
    case 'AS': return 'FIELD';
    default: return 'STANDARD';
  }
}

function deriveVariant(product: PMMAProductEntry): string {
  // Use the product class as variant, uppercased and hyphenated
  return product.product_class.toUpperCase().replace(/\s+/g, '');
}

// ─── Deterministic Name Generator ────────────────────────────────

function generateDetailName(
  system: string,
  familyCode: PMMATaxonomyCode,
  condition: string,
  variant: string,
): string {
  return `${system}-${familyCode}-${condition}-${variant}`;
}

// ─── Assembly Selection ──────────────────────────────────────────

function selectAssembly(
  taxonomyCode: PMMATaxonomyCode,
  product: PMMAProductEntry,
  request: PMMAGeneratorRequest,
): PMMAAssemblyRecord | undefined {
  // Filter by taxonomy code and product class
  const candidates = PMMA_ASSEMBLY_LIBRARY.filter(
    (a) => a.taxonomy_code === taxonomyCode && a.product_class === product.product_class,
  );

  if (candidates.length === 0) return undefined;

  // Prefer assemblies matching the substrate
  const substrateMatch = candidates.find((a) =>
    a.applicable_substrates.some((s) => s.toLowerCase() === request.substrate.toLowerCase()),
  );

  return substrateMatch ?? candidates[0];
}

// ─── Main Resolver ───────────────────────────────────────────────

export function resolveDetail(request: PMMAGeneratorRequest): ResolverResult {
  // 1. Validate input contract (fail-closed)
  const validation = validateGeneratorRequest(request as unknown as Record<string, unknown>);
  if (!validation.valid) {
    return { success: false, reason: `Input validation failed: ${validation.errors.join('; ')}` };
  }

  // 2. Resolve product through alias normalization
  const product = resolveProductEntry(request.brand);
  if (!product) {
    return { success: false, reason: `Unknown brand: "${request.brand}"` };
  }

  // 3. Chemistry boundary enforcement — block excluded products
  if (isExcludedFromPMMAGenerator(product.canonical_name)) {
    return {
      success: false,
      reason: `Product "${product.canonical_name}" is excluded from PMMA generator (chemistry family: ${product.chemistry_family})`,
    };
  }

  // 4. Review gate enforcement — block gated products
  if (requiresReviewGate(product.canonical_name)) {
    return {
      success: false,
      reason: `Product "${product.canonical_name}" requires review gate approval before rendering through PMMA generator`,
      review_gate: true,
    };
  }

  // 5. Derive taxonomy code from conditions
  const taxonomyCode = deriveTaxonomyCode(request);

  // 6. Select assembly
  const assembly = selectAssembly(taxonomyCode, product, request);
  if (!assembly) {
    return {
      success: false,
      reason: `No assembly found for taxonomy ${taxonomyCode} with product ${product.canonical_name} on substrate ${request.substrate}`,
    };
  }

  // 7. Generate deterministic name
  const system = 'PMMA';
  const condition = deriveConditionCode(request, taxonomyCode);
  const variant = deriveVariant(product);
  const detailName = generateDetailName(system, taxonomyCode, condition, variant);

  // 8. Build manifest
  const manifest: DetailManifest = {
    detail_name: detailName,
    system,
    family_code: taxonomyCode,
    condition,
    variant,
    assembly,
    product,
    request,
    render_formats: ['DXF', 'SVG', 'PDF'],
  };

  return { success: true, manifest };
}
