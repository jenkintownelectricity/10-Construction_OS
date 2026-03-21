/**
 * Construction Atlas — Spatial Context Layer
 *
 * Canonical spatial construction context layer binding geometry
 * and construction meaning.
 *
 * Exports spatial object graph types, context resolution types,
 * and spatial selector/anchor types for downstream consumers:
 *   - Construction_Runtime (execution)
 *   - Construction_Application_OS (UI rendering)
 *   - Construction_Reference_Intelligence (observation)
 */

export type {
  SpatialObjectId,
  ZoneId,
  SpatialPoint,
  SpatialBounds,
  SpatialObjectType,
  SpatialObject,
  AdjacencyType,
  SpatialEdge,
  Zone,
  SpatialObjectGraph,
} from "./graph/spatial-object-graph";

export type {
  ResolvedContext,
  InterfaceCondition,
  InterfaceConditionType,
  ContextQuery,
  ContextResolutionResult,
} from "./context/context-resolution";

export type {
  SpatialSelector,
  SpatialSelectorType,
  SelectorCriteria,
  SpatialAnchor,
  NavigableObject,
} from "./selectors/spatial-selectors";
