/**
 * Spatial Selectors and Anchors
 *
 * Defines selector types for identifying and navigating spatial objects.
 * Selectors are consumed by downstream systems (Construction_Application_OS
 * for UI rendering, Construction_Runtime for execution).
 *
 * This module defines TYPES ONLY — no rendering, no UI, no execution.
 */

import type {
  SpatialObjectId,
  ZoneId,
  SpatialObjectType,
  SpatialBounds,
} from "../graph/spatial-object-graph";

/** A selector that identifies spatial objects by criteria */
export interface SpatialSelector {
  /** Selector type determines how matching is performed */
  type: SpatialSelectorType;

  /** Human-readable label for downstream display */
  label: string;

  /** Selector-specific criteria */
  criteria: SelectorCriteria;
}

export type SpatialSelectorType =
  | "by_id"
  | "by_zone"
  | "by_type"
  | "by_bounds"
  | "by_adjacency"
  | "by_control_layer"
  | "by_interface_condition"
  | "compound";

/** Criteria for different selector types */
export type SelectorCriteria =
  | { kind: "by_id"; objectId: SpatialObjectId }
  | { kind: "by_zone"; zoneId: ZoneId }
  | { kind: "by_type"; objectType: SpatialObjectType }
  | { kind: "by_bounds"; bounds: SpatialBounds }
  | { kind: "by_adjacency"; objectId: SpatialObjectId; maxDepth: number }
  | { kind: "by_control_layer"; layerName: string }
  | { kind: "by_interface_condition"; conditionType: string }
  | { kind: "compound"; operator: "and" | "or"; selectors: SpatialSelector[] };

/** An anchor point — a stable reference location in spatial context */
export interface SpatialAnchor {
  id: string;
  name: string;
  objectId: SpatialObjectId;
  zoneId: ZoneId;
  description?: string;
}

/** A navigable object — an object exposed for downstream navigation */
export interface NavigableObject {
  objectId: SpatialObjectId;
  label: string;
  objectType: SpatialObjectType;
  zoneId: ZoneId;
  anchors: SpatialAnchor[];
  childNavigables?: NavigableObject[];
}
