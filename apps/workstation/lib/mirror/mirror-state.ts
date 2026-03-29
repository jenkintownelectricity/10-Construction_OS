/**
 * Frozen mirror state enum.
 * These states must not change.
 */
export const MIRROR_STATES = {
  AVAILABLE: "AVAILABLE",
  SELECTED: "SELECTED",
  BUILDING: "BUILDING",
  READY: "READY",
  ACTIVE: "ACTIVE",
} as const;

export type MirrorState = (typeof MIRROR_STATES)[keyof typeof MIRROR_STATES];

/** Build feedback messages displayed during mirror state transitions. */
export const BUILD_FEEDBACK: Record<string, string> = {
  INITIALIZING: "Initializing mirror",
  BINDING: "Binding capability",
  LINKING: "Linking system node",
  READY: "Mirror ready",
};

/** Lens types available in the Multi-Lens Mirror Builder. */
export const LENS_TYPES = {
  BUYER: "buyer",
  INVESTOR: "investor",
  ENGINEERING: "engineering",
  ADMIN: "admin",
} as const;

export type LensType = (typeof LENS_TYPES)[keyof typeof LENS_TYPES];

/** User session role for admin gating. */
export interface SessionContext {
  role: "USER" | "ADMIN";
}

/** Feature entry as defined in feature_catalog.json */
export interface FeatureCatalogEntry {
  feature_id: string;
  feature_category: string;
  display_order: number;
  feature_status: string;
  pricing_key: string;
  internal_capability_id: string;
  mirror_node_id: string;
  availability_state: MirrorState;
  related_feature_ids: string[];

  buyer_label: string;
  investor_label: string;
  engineering_label: string;

  buyer_summary: string;
  investor_summary: string;
  engineering_summary: string;

  admin_label?: string;
  admin_summary?: string;
}

/** Capability entry as defined in capability_map.json */
export interface CapabilityMapEntry {
  capability_id: string;
  capability_label: string;
  module_class: string;
  layer: "application" | "intelligence" | "infrastructure";
  dependencies: string[];
  contract_class: string;
  investor_layer: string;
}

/** Mirror node used in graph rendering. */
export interface MirrorNode {
  id: string;
  featureId: string;
  label: string;
  state: MirrorState;
  layer: string;
  x: number;
  y: number;
}

/** Mirror edge connecting two nodes. */
export interface MirrorEdge {
  from: string;
  to: string;
  relationship: "dependency" | "related";
}
