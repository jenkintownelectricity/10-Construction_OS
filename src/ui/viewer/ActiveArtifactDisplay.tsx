/**
 * Active Artifact Display — Current-generation-only SVG display module
 *
 * Holds exactly one successful SVG display payload for Viewer rendering.
 * NOT truth. NOT history. NOT persistence. NOT lineage authority.
 *
 * Lifecycle:
 *   - Set on successful roofing generation (from DetailViewerPanel)
 *   - Cleared on sourceContext.submittalId change
 *   - Cleared on generation failure
 *   - Cleared on explicit clear
 *
 * Display pattern informed by CADless_drawings:
 *   - renderers/utils.js createSVG / toString pattern
 *   - public/index.html modal viewer fullscreen SVG display
 *   - Responsive SVG via viewBox scaling
 *
 * Governance: VKGL04R — Ring 3 display seam only
 */

import { useEffect, useState } from 'react';
import { generationStore } from '../stores/generationStore';

// ─── Active Artifact Payload (current generation only) ───────────────

export interface ActiveArtifactPayload {
  /** SVG markup string from successful generation */
  readonly svgContent: string;
  /** Detail ID for display label */
  readonly detailId: string;
  /** Source submittal ID for identity binding */
  readonly sourceSubmittalId: string;
  /** Artifact type label */
  readonly artifactType: string;
  /** Filename label */
  readonly filename: string;
}

// ─── Module Implementation ───────────────────────────────────────────

type Listener = () => void;

class ActiveArtifactDisplayModule {
  private payload: ActiveArtifactPayload | null = null;
  private listeners = new Set<Listener>();
  private storeUnsub: (() => void) | null = null;
  private lastSubmittalId: string | null = null;

  constructor() {
    this.initStoreBinding();
  }

  /**
   * Bind to generationStore to auto-clear on:
   *   - sourceContext.submittalId change
   *   - generation failure (requestState.status === 'error')
   */
  private initStoreBinding(): void {
    this.storeUnsub = generationStore.subscribe(() => {
      const state = generationStore.getState();

      // Clear on submittalId change
      const currentSubmittalId = state.sourceContext?.submittalId ?? null;
      if (
        this.lastSubmittalId !== null &&
        currentSubmittalId !== null &&
        currentSubmittalId !== this.lastSubmittalId
      ) {
        this.clear();
      }
      this.lastSubmittalId = currentSubmittalId;

      // Clear on generation failure
      if (state.requestState.status === 'error') {
        this.clear();
      }
    });
  }

  /** Get current payload (null if no active artifact) */
  getPayload(): Readonly<ActiveArtifactPayload> | null {
    return this.payload;
  }

  /**
   * Set active artifact from successful generation.
   * Only accepts non-empty SVG content.
   */
  setPayload(payload: ActiveArtifactPayload): void {
    if (!payload.svgContent) {
      return;
    }
    this.payload = payload;
    this.lastSubmittalId = payload.sourceSubmittalId;
    this.notify();
  }

  /** Clear active artifact display */
  clear(): void {
    if (this.payload === null) return;
    this.payload = null;
    this.notify();
  }

  /** Subscribe to payload changes */
  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  /** Destroy binding (for testing) */
  destroy(): void {
    if (this.storeUnsub) {
      this.storeUnsub();
      this.storeUnsub = null;
    }
    this.payload = null;
    this.listeners.clear();
    this.lastSubmittalId = null;
  }

  /** Reset for testing */
  reset(): void {
    this.payload = null;
    this.lastSubmittalId = null;
    this.notify();
  }

  private notify(): void {
    queueMicrotask(() => {
      for (const listener of this.listeners) {
        try {
          listener();
        } catch (err) {
          console.error('[ActiveArtifactDisplay] Listener error:', err);
        }
      }
    });
  }
}

/** Singleton active artifact display module */
export const activeArtifactDisplay = new ActiveArtifactDisplayModule();

// ─── React Hook ──────────────────────────────────────────────────────

/** React hook to subscribe to active artifact payload */
export function useActiveArtifact(): ActiveArtifactPayload | null {
  const [payload, setPayload] = useState<ActiveArtifactPayload | null>(
    activeArtifactDisplay.getPayload(),
  );

  useEffect(() => {
    const sync = () => setPayload(activeArtifactDisplay.getPayload());
    sync();
    return activeArtifactDisplay.subscribe(sync);
  }, []);

  return payload;
}
