/**
 * Construction OS — Deterministic Proximity Field Model
 *
 * Implements proximity field logic for all reactive edges.
 * Rules:
 * - Each reactive edge has a trigger band and a ramp band
 * - Center safe zone = no edge expansion
 * - Only one edge may dominate at a time (strongest proximity wins)
 * - Locked panels override proximity collapse
 * - Transitions are smooth and predictable
 *
 * FAIL_CLOSED: Invalid mouse coordinates or state returns idle layout.
 */

import {
  PROXIMITY,
  type EdgeId,
  type EdgeState,
  type EdgeFieldState,
  type ProximityFieldSnapshot,
  createIdleSnapshot,
} from './ProximityConstants';

type Listener = (snapshot: ProximityFieldSnapshot) => void;

class ProximityFieldEngine {
  private snapshot: ProximityFieldSnapshot;
  private listeners = new Set<Listener>();
  private animFrame: number | null = null;
  private active = false;

  constructor() {
    this.snapshot = createIdleSnapshot();
  }

  start(): void {
    if (this.active) return;
    this.active = true;
    window.addEventListener('mousemove', this.handleMouseMove);
    window.addEventListener('click', this.handleClick);
    window.addEventListener('resize', this.handleResize);
    this.tick();
  }

  stop(): void {
    this.active = false;
    window.removeEventListener('mousemove', this.handleMouseMove);
    window.removeEventListener('click', this.handleClick);
    window.removeEventListener('resize', this.handleResize);
    if (this.animFrame != null) {
      cancelAnimationFrame(this.animFrame);
      this.animFrame = null;
    }
    this.snapshot = createIdleSnapshot();
    this.notify();
  }

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  getSnapshot(): ProximityFieldSnapshot {
    return this.snapshot;
  }

  /** Unlock a specific edge, returning it to proximity-driven behavior */
  unlockEdge(edge: EdgeId): void {
    const field = this.snapshot[edge];
    if (field.state === 'locked') {
      this.snapshot = {
        ...this.snapshot,
        [edge]: { ...field, state: 'idle', lockedAt: null },
      };
      this.notify();
    }
  }

  /** Lock a specific edge open */
  lockEdge(edge: EdgeId): void {
    const field = this.snapshot[edge];
    this.snapshot = {
      ...this.snapshot,
      [edge]: { ...field, state: 'locked', lockedAt: Date.now() },
    };
    this.notify();
  }

  // ─── Private ─────────────────────────────────────────────────────────

  private handleMouseMove = (e: MouseEvent): void => {
    this.snapshot = {
      ...this.snapshot,
      mouseX: e.clientX,
      mouseY: e.clientY,
    };
  };

  private handleClick = (_e: MouseEvent): void => {
    // Click locks the dominant edge if it's in preview state
    const dom = this.snapshot.dominantEdge;
    if (dom) {
      const field = this.snapshot[dom];
      if (field.state === 'preview' || field.state === 'expanding') {
        this.lockEdge(dom);
      }
    }
  };

  private handleResize = (): void => {
    this.snapshot = {
      ...this.snapshot,
      viewportWidth: window.innerWidth,
      viewportHeight: window.innerHeight,
    };
  };

  private tick = (): void => {
    if (!this.active) return;
    this.update();
    this.animFrame = requestAnimationFrame(this.tick);
  };

  private update(): void {
    const { mouseX, mouseY, viewportWidth, viewportHeight } = this.snapshot;

    // FAIL_CLOSED: invalid coordinates → idle
    if (mouseX < 0 || mouseY < 0 || viewportWidth <= 0 || viewportHeight <= 0) {
      return;
    }

    const now = Date.now();

    // Calculate raw proximity for each edge (0 = far, 1 = at edge)
    const leftDist = mouseX;
    const rightDist = viewportWidth - mouseX;
    const topDist = mouseY;
    const bottomDist = viewportHeight - mouseY;

    // Check center safe zone
    const inCenterX = mouseX > PROXIMITY.centerSafeZone && mouseX < viewportWidth - PROXIMITY.centerSafeZone;
    const inCenterY = mouseY > PROXIMITY.centerSafeZone && mouseY < viewportHeight - PROXIMITY.centerSafeZone;
    const inCenter = inCenterX && inCenterY;

    // Calculate proximity values
    const leftProx = inCenter ? 0 : this.calcProximity(leftDist);
    const rightProx = inCenter ? 0 : this.calcProximity(rightDist);
    const topProx = inCenter ? 0 : this.calcProximity(topDist);
    const bottomProx = inCenter ? 0 : this.calcProximity(bottomDist);

    // Determine dominant edge (strongest proximity wins)
    const proximities: [EdgeId, number][] = [
      ['left', leftProx],
      ['right', rightProx],
      ['top', topProx],
      ['bottom', bottomProx],
    ];

    // Find strongest non-idle edge
    let dominantEdge: EdgeId | null = null;
    let maxProx = 0;
    for (const [edge, prox] of proximities) {
      if (prox > maxProx) {
        maxProx = prox;
        dominantEdge = edge;
      }
    }

    // Also consider locked edges — they stay dominant
    const edges: EdgeId[] = ['left', 'right', 'top', 'bottom'];
    for (const edge of edges) {
      if (this.snapshot[edge].state === 'locked') {
        // Locked edge persists regardless of proximity
      }
    }

    // Update each edge field
    const left = this.updateEdgeField(this.snapshot.left, leftProx, dominantEdge === 'left', now);
    const right = this.updateEdgeField(this.snapshot.right, rightProx, dominantEdge === 'right', now);
    const top = this.updateEdgeField(this.snapshot.top, topProx, dominantEdge === 'top', now);
    const bottom = this.updateEdgeField(this.snapshot.bottom, bottomProx, dominantEdge === 'bottom', now);

    const newSnapshot: ProximityFieldSnapshot = {
      left,
      right,
      top,
      bottom,
      dominantEdge: maxProx > 0 ? dominantEdge : null,
      mouseX,
      mouseY,
      viewportWidth,
      viewportHeight,
    };

    // Only notify if state actually changed
    if (this.hasChanged(newSnapshot)) {
      this.snapshot = newSnapshot;
      this.notify();
    }
  }

  private calcProximity(distFromEdge: number): number {
    const { triggerBand, rampBand } = PROXIMITY;
    if (distFromEdge > triggerBand) return 0;
    if (distFromEdge <= rampBand) return 1;
    // Linear ramp between trigger and ramp band
    return 1 - (distFromEdge - rampBand) / (triggerBand - rampBand);
  }

  private updateEdgeField(
    current: EdgeFieldState,
    proximity: number,
    isDominant: boolean,
    now: number
  ): EdgeFieldState {
    // Locked state ignores proximity collapse
    if (current.state === 'locked') {
      return { ...current, proximity };
    }

    if (proximity === 0) {
      // Far from edge → idle
      return {
        ...current,
        proximity: 0,
        state: 'idle',
        intentTimestamp: null,
      };
    }

    if (!isDominant) {
      // Not the dominant edge → sensing at most
      return {
        ...current,
        proximity,
        state: proximity > 0 ? 'sensing' : 'idle',
        intentTimestamp: null,
      };
    }

    // This is the dominant edge
    if (current.state === 'idle' || current.state === 'sensing') {
      // Start intent timer
      const intentTs = current.intentTimestamp ?? now;
      const elapsed = now - intentTs;
      if (elapsed >= PROXIMITY.intentDelay) {
        // Intent confirmed → expanding
        return {
          ...current,
          proximity,
          state: proximity >= 0.8 ? 'preview' : 'expanding',
          intentTimestamp: intentTs,
        };
      }
      return {
        ...current,
        proximity,
        state: 'sensing',
        intentTimestamp: intentTs,
      };
    }

    if (current.state === 'expanding') {
      if (proximity >= 0.8) {
        return { ...current, proximity, state: 'preview' };
      }
      return { ...current, proximity };
    }

    if (current.state === 'preview') {
      return { ...current, proximity };
    }

    return { ...current, proximity };
  }

  private hasChanged(next: ProximityFieldSnapshot): boolean {
    const prev = this.snapshot;
    return (
      prev.left.state !== next.left.state ||
      prev.right.state !== next.right.state ||
      prev.top.state !== next.top.state ||
      prev.bottom.state !== next.bottom.state ||
      prev.dominantEdge !== next.dominantEdge ||
      Math.abs(prev.left.proximity - next.left.proximity) > 0.01 ||
      Math.abs(prev.right.proximity - next.right.proximity) > 0.01 ||
      Math.abs(prev.top.proximity - next.top.proximity) > 0.01 ||
      Math.abs(prev.bottom.proximity - next.bottom.proximity) > 0.01
    );
  }

  private notify(): void {
    for (const listener of this.listeners) {
      listener(this.snapshot);
    }
  }
}

/** Singleton proximity field engine */
export const proximityField = new ProximityFieldEngine();
