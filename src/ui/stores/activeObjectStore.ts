/**
 * Construction OS — Active Object Store
 *
 * Canonical active object state. This is the single source of truth
 * for which object the cockpit is oriented around.
 *
 * State layers:
 * 1. canonical-source adapter state (from adapters)
 * 2. panel-local derived state (each panel manages internally)
 * 3. draft UI state (user edits not yet committed)
 * 4. compare state (when in compare mode)
 * 5. workspace/orchestration state (layout, mode)
 * 6. mailbox/task/proposal state (system panel)
 *
 * This store owns layer 1 (active object identity) and layer 5 (workspace state).
 */

import type {
  ActiveObjectIdentity,
  WorkspaceMode,
  DeviceClass,
  PanelId,
  SourceBasis,
} from '../contracts/events';

// ─── State Shape ────────────────────────────────────────────────────────────

export interface ActiveObjectState {
  /** Current active object — null means no selection (fail-closed) */
  activeObject: ActiveObjectIdentity | null;
  /** Source basis of the active object */
  basis: SourceBasis;
  /** Which panel last set the active object */
  sourcePanel: PanelId | null;
  /** Compare target (when in compare mode) */
  compareObject: ActiveObjectIdentity | null;
  /** Current workspace mode */
  workspaceMode: WorkspaceMode;
  /** Detected device class */
  deviceClass: DeviceClass;
  /** Pinned companion panel for phone-class */
  pinnedCompanion: PanelId | null;
  /** Panels currently following Truth Echo */
  followingPanels: Set<PanelId>;
  /** Last Truth Echo timestamp */
  lastEchoTimestamp: number;
  /** Truth Echo failure state */
  echoFailure: string | null;
}

type Listener = () => void;

// ─── Store Implementation ───────────────────────────────────────────────────

function createActiveObjectStore() {
  let state: ActiveObjectState = {
    activeObject: null,
    basis: 'mock',
    sourcePanel: null,
    compareObject: null,
    workspaceMode: 'default',
    deviceClass: 'desktop',
    pinnedCompanion: null,
    followingPanels: new Set(['explorer', 'work', 'reference', 'spatial', 'system']),
    lastEchoTimestamp: 0,
    echoFailure: null,
  };

  const listeners = new Set<Listener>();

  function notify() {
    for (const listener of listeners) {
      listener();
    }
  }

  return {
    getState(): ActiveObjectState {
      return state;
    },

    subscribe(listener: Listener): () => void {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },

    /**
     * Set the active object. Fails closed if object is null/undefined
     * or has no id. Returns true if successful, false if failed closed.
     */
    setActiveObject(
      object: ActiveObjectIdentity | null,
      sourcePanel: PanelId,
      basis: SourceBasis = 'mock'
    ): boolean {
      // Fail closed on ambiguous object
      if (!object || !object.id) {
        state = {
          ...state,
          echoFailure: 'ambiguous_object: attempted to set null or id-less object',
        };
        notify();
        return false;
      }

      state = {
        ...state,
        activeObject: object,
        basis,
        sourcePanel,
        echoFailure: null,
        lastEchoTimestamp: Date.now(),
      };
      notify();
      return true;
    },

    setCompareObject(object: ActiveObjectIdentity | null): void {
      state = { ...state, compareObject: object };
      notify();
    },

    setWorkspaceMode(mode: WorkspaceMode): void {
      const previousMode = state.workspaceMode;
      if (mode === previousMode) return;
      state = { ...state, workspaceMode: mode };
      notify();
    },

    setDeviceClass(deviceClass: DeviceClass): void {
      state = { ...state, deviceClass };
      notify();
    },

    setPinnedCompanion(panelId: PanelId | null): void {
      state = { ...state, pinnedCompanion: panelId };
      notify();
    },

    setPanelFollowing(panelId: PanelId, following: boolean): void {
      const next = new Set(state.followingPanels);
      if (following) {
        next.add(panelId);
      } else {
        next.delete(panelId);
      }
      state = { ...state, followingPanels: next };
      notify();
    },

    setEchoFailure(failure: string | null): void {
      state = { ...state, echoFailure: failure };
      notify();
    },

    /** Reset to initial state (for testing) */
    reset(): void {
      state = {
        activeObject: null,
        basis: 'mock',
        sourcePanel: null,
        compareObject: null,
        workspaceMode: 'default',
        deviceClass: 'desktop',
        pinnedCompanion: null,
        followingPanels: new Set(['explorer', 'work', 'reference', 'spatial', 'system']),
        lastEchoTimestamp: 0,
        echoFailure: null,
      };
      notify();
    },
  };
}

export const activeObjectStore = createActiveObjectStore();
