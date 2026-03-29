import { MIRROR_STATES, BUILD_FEEDBACK, type MirrorState, type FeatureCatalogEntry, type MirrorNode, type MirrorEdge, type CapabilityMapEntry } from "./mirror-state";
import featureCatalogData from "../../features/platform/feature_catalog.json";
import capabilityMapData from "../../features/platform/capability_map.json";

/** Typed catalog and map accessors. */
const catalog: FeatureCatalogEntry[] = featureCatalogData.features as FeatureCatalogEntry[];
const capabilityMap: CapabilityMapEntry[] = capabilityMapData.capabilities as CapabilityMapEntry[];

/** Per-feature runtime state. */
interface FeatureRuntimeState {
  mirrorState: MirrorState;
  buildFeedback: string | null;
}

interface FeatureStoreState {
  featureStates: Record<string, FeatureRuntimeState>;
  selectedNodeId: string | null;
}

type Listener = () => void;

const listeners = new Set<Listener>();

/** Initialize all features to their catalog availability state. */
function initFeatureStates(): Record<string, FeatureRuntimeState> {
  const states: Record<string, FeatureRuntimeState> = {};
  for (const feature of catalog) {
    states[feature.feature_id] = {
      mirrorState: feature.availability_state,
      buildFeedback: null,
    };
  }
  return states;
}

let state: FeatureStoreState = {
  featureStates: initFeatureStates(),
  selectedNodeId: null,
};

function emit() {
  for (const listener of listeners) {
    listener();
  }
}

/** Subscribe to store changes (for useSyncExternalStore). */
export function subscribe(listener: Listener): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

/** Get current snapshot (for useSyncExternalStore). */
export function getSnapshot(): FeatureStoreState {
  return state;
}

/** Select a mirror node for inspection. */
export function selectNode(nodeId: string | null): void {
  state = { ...state, selectedNodeId: nodeId };
  emit();
}

/** Simulate the build sequence for a feature selection. */
export function selectFeature(featureId: string): void {
  const current = state.featureStates[featureId];
  if (!current) return;

  // If already ACTIVE or beyond AVAILABLE, deselect back to AVAILABLE
  if (current.mirrorState !== MIRROR_STATES.AVAILABLE) {
    state = {
      ...state,
      featureStates: {
        ...state.featureStates,
        [featureId]: { mirrorState: MIRROR_STATES.AVAILABLE, buildFeedback: null },
      },
    };
    emit();
    return;
  }

  // AVAILABLE → SELECTED
  updateFeatureState(featureId, MIRROR_STATES.SELECTED, BUILD_FEEDBACK.INITIALIZING);

  // SELECTED → BUILDING (after 400ms)
  setTimeout(() => {
    updateFeatureState(featureId, MIRROR_STATES.BUILDING, BUILD_FEEDBACK.BINDING);
  }, 400);

  // BUILDING → READY (after 800ms)
  setTimeout(() => {
    updateFeatureState(featureId, MIRROR_STATES.READY, BUILD_FEEDBACK.LINKING);
  }, 800);

  // READY → ACTIVE (after 1200ms)
  setTimeout(() => {
    updateFeatureState(featureId, MIRROR_STATES.ACTIVE, BUILD_FEEDBACK.READY);
  }, 1200);

  // Clear feedback (after 2000ms)
  setTimeout(() => {
    updateFeatureState(featureId, MIRROR_STATES.ACTIVE, null);
  }, 2000);
}

function updateFeatureState(featureId: string, mirrorState: MirrorState, buildFeedback: string | null): void {
  state = {
    ...state,
    featureStates: {
      ...state.featureStates,
      [featureId]: { mirrorState, buildFeedback },
    },
  };
  emit();
}

/** Get the full feature catalog. */
export function getFeatureCatalog(): FeatureCatalogEntry[] {
  return catalog;
}

/** Get the capability map. */
export function getCapabilityMap(): CapabilityMapEntry[] {
  return capabilityMap;
}

/** Look up a capability by ID. */
export function getCapability(capabilityId: string): CapabilityMapEntry | undefined {
  return capabilityMap.find((c) => c.capability_id === capabilityId);
}

/** Compute mirror nodes from catalog + current state for a given lens. */
export function computeMirrorNodes(lens: string): MirrorNode[] {
  const layerYPositions: Record<string, number> = {
    application: 60,
    intelligence: 180,
    infrastructure: 300,
  };

  const layerCounters: Record<string, number> = {
    application: 0,
    intelligence: 0,
    infrastructure: 0,
  };

  // Pre-count items per layer for spacing
  const layerCounts: Record<string, number> = { application: 0, intelligence: 0, infrastructure: 0 };
  for (const feature of catalog) {
    const cap = capabilityMap.find((c) => c.capability_id === feature.internal_capability_id);
    if (cap) layerCounts[cap.layer] = (layerCounts[cap.layer] || 0) + 1;
  }

  return catalog.map((feature) => {
    const cap = capabilityMap.find((c) => c.capability_id === feature.internal_capability_id);
    const layer = cap?.layer ?? "application";
    const count = layerCounters[layer]++;
    const total = layerCounts[layer] || 1;
    const spacing = 520 / (total + 1);

    let label = feature.buyer_label;
    if (lens === "investor") label = feature.investor_label;
    else if (lens === "engineering") label = feature.engineering_label;
    else if (lens === "admin") label = feature.admin_label ?? feature.buyer_label;

    const featureState = state.featureStates[feature.feature_id];

    return {
      id: feature.mirror_node_id,
      featureId: feature.feature_id,
      label,
      state: featureState?.mirrorState ?? MIRROR_STATES.AVAILABLE,
      layer: cap?.investor_layer ?? "Application Layer",
      x: spacing * (count + 1),
      y: layerYPositions[layer] ?? 180,
    };
  });
}

/** Compute mirror edges from capability dependencies and feature relationships. */
export function computeMirrorEdges(): MirrorEdge[] {
  const edges: MirrorEdge[] = [];
  const featureByCapId = new Map<string, string>();

  for (const feature of catalog) {
    featureByCapId.set(feature.internal_capability_id, feature.mirror_node_id);
  }

  // Dependency edges from capability map
  for (const cap of capabilityMap) {
    const fromNode = featureByCapId.get(cap.capability_id);
    if (!fromNode) continue;
    for (const dep of cap.dependencies) {
      const toNode = featureByCapId.get(dep);
      if (toNode) {
        edges.push({ from: fromNode, to: toNode, relationship: "dependency" });
      }
    }
  }

  // Related feature edges
  for (const feature of catalog) {
    for (const relatedId of feature.related_feature_ids) {
      const related = catalog.find((f) => f.feature_id === relatedId);
      if (related) {
        const exists = edges.some(
          (e) =>
            (e.from === feature.mirror_node_id && e.to === related.mirror_node_id) ||
            (e.from === related.mirror_node_id && e.to === feature.mirror_node_id)
        );
        if (!exists) {
          edges.push({ from: feature.mirror_node_id, to: related.mirror_node_id, relationship: "related" });
        }
      }
    }
  }

  return edges;
}

/** Get all currently active (selected) feature IDs. */
export function getActiveFeatureIds(): string[] {
  return Object.entries(state.featureStates)
    .filter(([, fs]) => fs.mirrorState !== MIRROR_STATES.AVAILABLE)
    .map(([id]) => id);
}

/** Get the build feedback message for a feature. */
export function getBuildFeedback(featureId: string): string | null {
  return state.featureStates[featureId]?.buildFeedback ?? null;
}
