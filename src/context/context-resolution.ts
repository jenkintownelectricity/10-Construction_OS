/**
 * Context Resolution
 *
 * Resolves spatial construction conditions given an object or zone.
 * Answers the four Atlas questions:
 *   1. What object exists?
 *   2. Where does it exist?
 *   3. What surrounds it?
 *   4. What rules apply?
 *
 * This module defines TYPES ONLY — no rendering, no UI, no execution.
 */

import type {
  SpatialObjectId,
  ZoneId,
  SpatialObject,
  SpatialEdge,
  Zone,
} from "../graph/spatial-object-graph";

/** Resolved context for a spatial object */
export interface ResolvedContext {
  /** The object itself */
  object: SpatialObject;

  /** The zone containing the object */
  zone: Zone;

  /** Adjacent objects and their relationship types */
  adjacencies: SpatialEdge[];

  /** Interface conditions that apply at this location */
  interfaceConditions: InterfaceCondition[];

  /** Control layers active in this zone */
  activeControlLayers: string[];
}

/** An interface condition at a spatial location */
export interface InterfaceCondition {
  id: string;
  name: string;
  type: InterfaceConditionType;
  involvedObjectIds: SpatialObjectId[];
  zoneId: ZoneId;
  riskLevel?: "low" | "medium" | "high" | "critical";
}

/** Classification of interface conditions */
export type InterfaceConditionType =
  | "roof_to_wall"
  | "parapet"
  | "penetration"
  | "fenestration"
  | "below_grade"
  | "expansion_joint"
  | "deck_to_wall"
  | "roof_edge"
  | "curb"
  | "drain"
  | "custom";

/** Query for context resolution */
export interface ContextQuery {
  objectId?: SpatialObjectId;
  zoneId?: ZoneId;
  includeAdjacencies?: boolean;
  includeInterfaceConditions?: boolean;
  maxDepth?: number;
}

/** Result of a context resolution query */
export interface ContextResolutionResult {
  resolved: boolean;
  context?: ResolvedContext;
  reason?: string;
}
