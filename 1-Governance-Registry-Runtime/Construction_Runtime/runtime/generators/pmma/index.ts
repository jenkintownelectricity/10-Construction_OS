/**
 * PMMA Generator Module — Barrel Export
 *
 * L0-CMD-BARRETT-PMMA-GEN-005
 * Public API surface for the Barrett PMMA Detail Generator.
 */

// Wave 1 — Product Registry
export {
  PMMA_PRODUCT_REGISTRY,
  getPMMAGeneratorProducts,
  getProductByCanonicalName,
  getProductsByBranchStatus,
  getProductsByChemistryFamily,
  isExcludedFromPMMAGenerator,
  requiresReviewGate,
  type BranchStatus,
  type ChemistryFamily,
  type PMMAProductEntry,
  type ProductClass,
} from './pmmaProductRegistry';

// Wave 2 — Alias Normalization
export {
  getAllAliases,
  isKnownProduct,
  normalizeProductName,
  resolveCanonicalName,
  resolveProductEntry,
  type NormalizationResult,
} from './aliasNormalizationMap';

// Wave 3 — Taxonomy
export {
  PMMA_TAXONOMY,
  getAllTaxonomyCodes,
  getTaxonomyFamily,
  isValidTaxonomyCode,
  type PMMATaxonomyCode,
  type PMMATaxonomyFamily,
} from './pmmaTaxonomy';

// Wave 4 — Assembly Library
export {
  PMMA_ASSEMBLY_LIBRARY,
  getAssembliesByProductClass,
  getAssembliesByTaxonomy,
  getAssembliesForSubstrate,
  getAssemblyById,
  type PMMAAssemblyLayer,
  type PMMAAssemblyRecord,
} from './pmmaAssemblyLibrary';

// Wave 5 — Generator Request Contract
export {
  VALID_BRANDS,
  VALID_CANT_CONDITIONS,
  VALID_CURB_TYPES,
  VALID_DRAIN_TYPES,
  VALID_EXPOSURES,
  VALID_JOINT_TYPES,
  VALID_PENETRATION_TYPES,
  VALID_REINFORCEMENTS,
  VALID_SUBSTRATES,
  VALID_WALL_TYPES,
  validateGeneratorRequest,
  type Brand,
  type CantCondition,
  type CurbType,
  type DrainType,
  type Exposure,
  type GeneratorDimensions,
  type JointType,
  type PMMAGeneratorRequest,
  type PenetrationType,
  type Reinforcement,
  type Substrate,
  type ValidationResult,
  type WallType,
} from './pmmaGeneratorRequest';

// Wave 6 — Detail Resolver
export {
  resolveDetail,
  type DetailManifest,
  type ResolverResult,
} from './pmmaDetailResolver';
