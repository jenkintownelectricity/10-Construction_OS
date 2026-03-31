/**
 * Manufacturer Hub — Type Definitions
 * Wave 1 UI Surface Types
 *
 * OBSERVER-DERIVED: These types define the shape of UI projection data only.
 * They are NOT canonical truth. They represent a local observer-derived
 * projection of manufacturer truth for Construction OS UI consumption.
 * Canonical truth lives in 10-building-envelope-manufacturer-os.
 */

/** Validation state for observer-derived projections — presentational only */
export type ValidationState = 'certified' | 'unverified' | 'partial' | 'blocked';

/** Seed status of a manufacturer in the observer projection */
export type SeedStatus = 'seeded' | 'scaffold' | 'not-seeded';

/** Hub operational mode */
export type ManufacturerHubMode = 'work' | 'system';

/** Manufacturer summary for sidebar and overview */
export interface ManufacturerSummary {
  id: string;
  name: string;
  seedStatus: SeedStatus;
  productsCount: number;
  systemsCount: number;
  certificationsCount: number;
  description: string;
}

/** Product summary for product lists and stack visualization */
export interface ProductSummary {
  id: string;
  manufacturerId: string;
  name: string;
  type: string;
  role: string;
  description: string;
}

/** System summary for system inspector and certification panels */
export interface SystemSummary {
  id: string;
  manufacturerId: string;
  name: string;
  systemType: string;
  description: string;
  productIds: string[];
  certificationIds: string[];
  conditionIds: string[];
}

/** Certification summary — observer-derived status only */
export interface CertificationSummary {
  id: string;
  manufacturerId: string;
  systemId: string;
  name: string;
  status: ValidationState;
  requirementSummary: string;
}

/** Rule summary — known and deferred rules */
export interface RuleSummary {
  id: string;
  systemId: string;
  name: string;
  description: string;
  /** Whether a structured rule file has been materialized */
  materialized: boolean;
}

/** Condition summary — grounded conditions only */
export interface ConditionSummary {
  id: string;
  systemId: string;
  name: string;
  conditionType: string;
}

/** Governance status for the governance rail */
export interface GovernanceStatus {
  certificationState: ValidationState;
  projectionState: 'active' | 'stale' | 'scaffold';
  truthDebt: string[];
  seedStatus: SeedStatus;
}

/** Action item for the action rail */
export interface ActionItem {
  id: string;
  label: string;
  actionType: 'navigate' | 'inspect' | 'mode-switch' | 'future';
  targetMode?: ManufacturerHubMode;
  enabled: boolean;
}

/** UI signal — presentational state only, NOT bus emissions */
export type SignalType =
  | 'MANUFACTURER_SELECTED'
  | 'MODE_CHANGED'
  | 'SYSTEM_SELECTED'
  | 'CERTIFICATION_VIEWED'
  | 'PRODUCT_VIEWED';

export interface UISignal {
  type: SignalType;
  label: string;
  active: boolean;
}

/** Top-level projection shape for the entire Manufacturer Hub */
export interface ManufacturerHubProjection {
  manufacturers: ManufacturerSummary[];
  products: ProductSummary[];
  systems: SystemSummary[];
  certifications: CertificationSummary[];
  rulesSummary: RuleSummary[];
  conditionsSummary: ConditionSummary[];
  governanceStatus: Record<string, GovernanceStatus>;
  actions: ActionItem[];
}
