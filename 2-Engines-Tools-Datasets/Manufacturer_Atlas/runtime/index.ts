/**
 * Manufacturer Atlas Runtime — Export Surface
 *
 * Typed helpers for Construction_OS to consume upstream manufacturer
 * truth via the Manufacturer_Atlas bridge.
 *
 * This module does not own truth. It reads consumed upstream references
 * from truth-cache/ and exposes typed results for runtime use.
 *
 * Upstream authority: 10-building-envelope-manufacturer-os
 */

// Types
export type {
  RecordStatus,
  ManufacturerRecord,
  ProductRecord,
  SystemRecord,
  InstallationRuleRecord,
  CertificationRuleRecord,
  CompatibilityRecord,
  BarrettPmmaEvaluationResult,
  EvaluationStatus,
  LoaderFailure,
} from "./types";

// Loaders
export { loadManufacturers } from "./manufacturer-record-loader";
export { loadProducts } from "./manufacturer-product-loader";
export { loadSystems } from "./manufacturer-system-loader";
export { loadInstallationRules, loadCertificationRules } from "./manufacturer-rule-loader";
export { loadCompatibilityMatrix, filterUpstreamCompatibility, filterLegacyConstraints, filterLegacyConditions } from "./manufacturer-compatibility-loader";

// Evaluator
export { evaluateBarrettPmmaCompatibility } from "./barrett-pmma-compatibility-evaluator";
