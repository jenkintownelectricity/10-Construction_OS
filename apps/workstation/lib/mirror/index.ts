export { MIRROR_STATES, BUILD_FEEDBACK, LENS_TYPES } from "./mirror-state";
export type {
  MirrorState,
  LensType,
  SessionContext,
  FeatureCatalogEntry,
  CapabilityMapEntry,
  MirrorNode,
  MirrorEdge,
} from "./mirror-state";

export { LensProvider, useLens } from "./lens-context";

export {
  subscribe,
  getSnapshot,
  selectNode,
  selectFeature,
  getFeatureCatalog,
  getCapabilityMap,
  getCapability,
  computeMirrorNodes,
  computeMirrorEdges,
  getActiveFeatureIds,
  getBuildFeedback,
} from "./feature-store";
