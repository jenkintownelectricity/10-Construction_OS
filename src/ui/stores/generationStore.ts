/**
 * Construction OS — Generation Store
 *
 * Shared store for generation results and source context.
 * Enables the Shop Drawings → Workstation → Generate → Viewer loop.
 *
 * Pattern: matches activeObjectStore subscribe/getState API.
 * Single instance. Survives component unmounts.
 *
 * Governance: VKGL04R
 */

import type { DetailPreviewResult } from '../detail-viewer/types';

// ─── Source Context (from Shop Drawings page selection) ────────────────

export interface GenerationSourceContext {
  readonly submittalId: string;
  readonly submittalTitle: string;
  readonly manufacturer: string;
  readonly spec: string;
  readonly project: string;
}

// ─── Store State ──────────────────────────────────────────────────────

interface GenerationStoreState {
  /** Last generation result from DetailViewerPanel */
  lastResult: DetailPreviewResult | null;
  /** Source context from Shop Drawings selection */
  sourceContext: GenerationSourceContext | null;
  /** Timestamp of last result */
  resultTimestamp: number;
}

type Listener = () => void;

// ─── Store Implementation ─────────────────────────────────────────────

class GenerationStoreImpl {
  private state: GenerationStoreState = {
    lastResult: null,
    sourceContext: null,
    resultTimestamp: 0,
  };

  private listeners = new Set<Listener>();

  getState(): Readonly<GenerationStoreState> {
    return this.state;
  }

  /** Set source context from Shop Drawings page before launching Workstation */
  setSourceContext(context: GenerationSourceContext): void {
    this.state = { ...this.state, sourceContext: context };
    this.notify();
  }

  /** Store generation result after successful/failed generation */
  setResult(result: DetailPreviewResult): void {
    this.state = {
      ...this.state,
      lastResult: result,
      resultTimestamp: Date.now(),
    };
    this.notify();
  }

  /** Clear all state */
  clear(): void {
    this.state = {
      lastResult: null,
      sourceContext: null,
      resultTimestamp: 0,
    };
    this.notify();
  }

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notify(): void {
    queueMicrotask(() => {
      for (const listener of this.listeners) {
        try {
          listener();
        } catch (err) {
          console.error('[GenerationStore] Listener error:', err);
        }
      }
    });
  }
}

/** Singleton generation store */
export const generationStore = new GenerationStoreImpl();
