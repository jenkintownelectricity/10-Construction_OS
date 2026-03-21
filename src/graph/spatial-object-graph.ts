/**
 * Spatial Construction Object Graph
 *
 * Defines the canonical spatial object graph for Construction Atlas.
 * Objects exist within zones, have placements, and relate to each other
 * through adjacency and containment relationships.
 *
 * This module defines TYPES ONLY — no rendering, no UI, no execution.
 */

/** Unique identifier for a spatial object */
export type SpatialObjectId = string;

/** Unique identifier for a zone */
export type ZoneId = string;

/** A point in 2D or 3D construction space */
export interface SpatialPoint {
  x: number;
  y: number;
  z?: number;
}

/** Bounding region for spatial objects and zones */
export interface SpatialBounds {
  origin: SpatialPoint;
  extent: SpatialPoint;
}

/** Classification of spatial object types within the construction domain */
export type SpatialObjectType =
  | "assembly"
  | "element"
  | "detail"
  | "interface"
  | "zone"
  | "anchor"
  | "penetration"
  | "transition";

/** A node in the spatial construction object graph */
export interface SpatialObject {
  id: SpatialObjectId;
  type: SpatialObjectType;
  name: string;
  zoneId: ZoneId;
  placement: SpatialBounds;
  layer?: string;
  parentId?: SpatialObjectId;
  metadata?: Record<string, unknown>;
}

/** Relationship types between spatial objects */
export type AdjacencyType =
  | "adjacent_to"
  | "contained_in"
  | "interfaces_with"
  | "transitions_to"
  | "penetrates"
  | "overlaps";

/** An edge in the spatial object graph */
export interface SpatialEdge {
  sourceId: SpatialObjectId;
  targetId: SpatialObjectId;
  type: AdjacencyType;
  metadata?: Record<string, unknown>;
}

/** A spatial zone — a bounded region that contains objects */
export interface Zone {
  id: ZoneId;
  name: string;
  bounds: SpatialBounds;
  parentZoneId?: ZoneId;
  controlLayers?: string[];
}

/** The complete spatial object graph */
export interface SpatialObjectGraph {
  objects: SpatialObject[];
  edges: SpatialEdge[];
  zones: Zone[];
}
