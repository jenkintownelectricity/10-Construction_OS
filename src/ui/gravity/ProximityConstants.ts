/**
 * Construction OS — Proximity Field Constants
 *
 * Configurable constants for deterministic proximity field behavior.
 * All values stored in UI scope only — no hidden inference, no random motion.
 *
 * FAIL_CLOSED: Invalid or missing proximity state results in idle layout.
 */

export const PROXIMITY = {
  // ─── Edge bands (pixels from viewport edge) ────────────────────────
  /** Trigger band: start sensing cursor intent */
  triggerBand: 80,
  /** Ramp band: expansion strength scales with distance to edge */
  rampBand: 40,
  /** Center safe zone: no edge expansion within this region */
  centerSafeZone: 200,

  // ─── Timing ────────────────────────────────────────────────────────
  /** Intent delay before expansion begins (ms) */
  intentDelay: 180,
  /** Expansion animation duration (ms) */
  expandDuration: 180,
  /** Collapse animation duration (ms) */
  collapseDuration: 200,
  /** Mouse polling interval (ms) */
  pollInterval: 16,

  // ─── Expansion sizes ──────────────────────────────────────────────
  /** Idle strip width for edge panels (px) */
  edgeIdleWidth: 4,
  /** Preview width for edge panels (px) */
  edgePreviewWidth: 320,
  /** Full expanded width for locked edge panels (px) */
  edgeLockedWidth: 380,
  /** Idle height for bottom dock (px) */
  dockIdleHeight: 28,
  /** Preview height for bottom dock (px) */
  dockPreviewHeight: 260,
  /** Full expanded height for bottom dock (px) */
  dockExpandedHeight: 380,

  // ─── Workspace bias ───────────────────────────────────────────────
  /** Bias step size per click (percentage points) */
  biasStep: 8,
  /** Minimum workspace share (%) */
  workspaceMinShare: 40,
  /** Maximum workspace share (%) */
  workspaceMaxShare: 90,
  /** Default workspace share (%) */
  workspaceDefaultShare: 65,

  // ─── Hover peek ───────────────────────────────────────────────────
  /** Hover peek delay before showing preview (ms) */
  peekDelay: 200,
  /** Peek panel share (50/50 split) */
  peekShare: 50,

  // ─── Deck fan-out ─────────────────────────────────────────────────
  /** Fan-out idle strip width (px) */
  fanIdleWidth: 6,
  /** Fan-out expanded width (px) */
  fanExpandedWidth: 280,
  /** Fan-out card height (px) */
  fanCardHeight: 64,
  /** Fan-out card gap (px) */
  fanCardGap: 4,

  // ─── Motion doctrine ──────────────────────────────────────────────
  /** Allowed easing function */
  easing: 'cubic-bezier(0.16, 1, 0.3, 1)' as const,
  /** Minimum animation duration (ms) */
  minDuration: 150,
  /** Maximum animation duration (ms) */
  maxDuration: 220,
} as const;

export type EdgeId = 'left' | 'right' | 'top' | 'bottom';
export type EdgeState = 'idle' | 'sensing' | 'expanding' | 'preview' | 'locked';

export interface EdgeFieldState {
  edge: EdgeId;
  proximity: number;  // 0 (far) to 1 (at edge)
  state: EdgeState;
  intentTimestamp: number | null;
  lockedAt: number | null;
}

export interface ProximityFieldSnapshot {
  left: EdgeFieldState;
  right: EdgeFieldState;
  top: EdgeFieldState;
  bottom: EdgeFieldState;
  dominantEdge: EdgeId | null;
  mouseX: number;
  mouseY: number;
  viewportWidth: number;
  viewportHeight: number;
}

export function createIdleFieldState(edge: EdgeId): EdgeFieldState {
  return {
    edge,
    proximity: 0,
    state: 'idle',
    intentTimestamp: null,
    lockedAt: null,
  };
}

export function createIdleSnapshot(): ProximityFieldSnapshot {
  return {
    left: createIdleFieldState('left'),
    right: createIdleFieldState('right'),
    top: createIdleFieldState('top'),
    bottom: createIdleFieldState('bottom'),
    dominantEdge: null,
    mouseX: -1,
    mouseY: -1,
    viewportWidth: window.innerWidth,
    viewportHeight: window.innerHeight,
  };
}
