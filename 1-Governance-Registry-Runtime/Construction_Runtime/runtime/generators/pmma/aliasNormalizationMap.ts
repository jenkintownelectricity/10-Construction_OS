/**
 * Alias Normalization Engine — Spelling Variant Resolution
 *
 * L0-CMD-BARRETT-PMMA-GEN-005
 * Wave 2 — Alias Normalization Engine
 *
 * Normalizes product spelling variants to canonical names.
 * Cross-chemistry normalization is blocked: an alias in the
 * Hybrid Polyurea/Polyurethane branch cannot resolve to a PMMA product.
 */

import {
  PMMA_PRODUCT_REGISTRY,
  type PMMAProductEntry,
  type ChemistryFamily,
} from './pmmaProductRegistry';

// ─── Alias Index (built at module load) ─────────────────────────

interface AliasEntry {
  readonly canonical_name: string;
  readonly chemistry_family: ChemistryFamily;
}

const aliasIndex: ReadonlyMap<string, AliasEntry> = buildAliasIndex();

function buildAliasIndex(): Map<string, AliasEntry> {
  const index = new Map<string, AliasEntry>();

  for (const product of PMMA_PRODUCT_REGISTRY) {
    const entry: AliasEntry = {
      canonical_name: product.canonical_name,
      chemistry_family: product.chemistry_family,
    };

    // Index the canonical name itself
    index.set(normalizeKey(product.canonical_name), entry);

    // Index all aliases
    for (const alias of product.alias_names) {
      index.set(normalizeKey(alias), entry);
    }
  }

  return index;
}

function normalizeKey(input: string): string {
  return input.trim().toLowerCase().replace(/\s+/g, ' ');
}

// ─── Normalization Result ────────────────────────────────────────

export type NormalizationResult =
  | { resolved: true; canonical_name: string; chemistry_family: ChemistryFamily }
  | { resolved: false; reason: string };

// ─── Public API ──────────────────────────────────────────────────

/**
 * Resolve a product name or alias to its canonical form.
 * Returns the canonical name only if the alias belongs to the
 * same chemistry family as the expected context (if provided).
 */
export function normalizeProductName(
  input: string,
  expectedChemistry?: ChemistryFamily,
): NormalizationResult {
  const key = normalizeKey(input);
  const entry = aliasIndex.get(key);

  if (!entry) {
    return { resolved: false, reason: `Unknown product or alias: "${input}"` };
  }

  // Cross-chemistry boundary enforcement
  if (expectedChemistry && entry.chemistry_family !== expectedChemistry) {
    return {
      resolved: false,
      reason: `Cross-chemistry normalization blocked: "${input}" belongs to ${entry.chemistry_family}, expected ${expectedChemistry}`,
    };
  }

  return {
    resolved: true,
    canonical_name: entry.canonical_name,
    chemistry_family: entry.chemistry_family,
  };
}

/**
 * Resolve to canonical name or return undefined. No cross-chemistry guard.
 * Use normalizeProductName() for governed resolution.
 */
export function resolveCanonicalName(input: string): string | undefined {
  const key = normalizeKey(input);
  const entry = aliasIndex.get(key);
  return entry?.canonical_name;
}

/**
 * Get the full product entry for an alias.
 */
export function resolveProductEntry(input: string): PMMAProductEntry | undefined {
  const canonical = resolveCanonicalName(input);
  if (!canonical) return undefined;
  return PMMA_PRODUCT_REGISTRY.find((p) => p.canonical_name === canonical);
}

/**
 * Check whether a given string is a known alias or canonical name.
 */
export function isKnownProduct(input: string): boolean {
  return aliasIndex.has(normalizeKey(input));
}

/**
 * List all registered aliases (for UI autocomplete / search).
 */
export function getAllAliases(): readonly string[] {
  return Array.from(aliasIndex.keys());
}
