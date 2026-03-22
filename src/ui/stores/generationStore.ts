/**
 * Construction OS — Generation Store
 *
 * Thin Ring 3 UI transport seam for the Shop Drawings → Workstation →
 * Generate → Viewer loop. NOT truth. NOT history. NOT artifact cache.
 *
 * Top-level keys (locked):
 *   - sourceContext
 *   - requestState
 *   - latestResult
 *   - navigationFlags
 *
 * No additional top-level fields may exist.
 * No history arrays, diagnostics history, authoritative lineage truth,
 * resolved pattern truth, multi-artifact caches, retry queues,
 * background orchestration state, cross-session state, or persistent
 * localStorage-backed state.
 *
 * Governance: VKGL04R — Ring 3 transport seam only
 */

// ─── Source Context (locked schema) ───────────────────────────────────

export interface GenerationSourceContext {
  readonly submittalId: string;
  readonly title: string;
  readonly manufacturer: string;
  readonly spec: string;
  readonly project: string;
}

// ─── Request State (locked schema, locked lifecycle) ──────────────────

export type RequestStatus = 'idle' | 'validating' | 'mapping' | 'generating' | 'success' | 'error';

export interface RequestState {
  readonly status: RequestStatus;
  readonly requestId: string;
  readonly startedAt: number;
  readonly completedAt?: number;
  readonly errorCode?: string;
  readonly errorMessage?: string;
}

// ─── Latest Result (locked schema, identity-bound) ────────────────────

export interface LatestResult {
  readonly sourceSubmittalId: string;
  readonly detailId: string;
  readonly artifactType: string;
  readonly filename: string;
  readonly success: boolean;
  readonly generationStatus: string;
  readonly artifactIds?: readonly string[];
}

// ─── Navigation Flags (locked schema) ─────────────────────────────────

export interface NavigationFlags {
  readonly viewerAutoOpenPending: boolean;
  readonly sourceContextChanged: boolean;
}

// ─── Store State (exactly 4 top-level keys) ───────────────────────────

export interface GenerationStoreState {
  readonly sourceContext: GenerationSourceContext | null;
  readonly requestState: RequestState;
  readonly latestResult: LatestResult | null;
  readonly navigationFlags: NavigationFlags;
}

// ─── Defaults ─────────────────────────────────────────────────────────

const IDLE_REQUEST: RequestState = {
  status: 'idle',
  requestId: '',
  startedAt: 0,
};

const DEFAULT_NAV_FLAGS: NavigationFlags = {
  viewerAutoOpenPending: false,
  sourceContextChanged: false,
};

const INITIAL_STATE: GenerationStoreState = {
  sourceContext: null,
  requestState: IDLE_REQUEST,
  latestResult: null,
  navigationFlags: DEFAULT_NAV_FLAGS,
};

// ─── Store Implementation ─────────────────────────────────────────────

type Listener = () => void;

class GenerationStoreImpl {
  private state: GenerationStoreState = { ...INITIAL_STATE };
  private listeners = new Set<Listener>();

  getState(): Readonly<GenerationStoreState> {
    return this.state;
  }

  // ─── Source Context ───────────────────────────────────────────────

  /**
   * Set source context from Shop Drawings selection.
   * If submittalId changes from previous context:
   *   - sourceContextChanged flag is set to true
   *   - latestResult is cleared (identity mismatch)
   */
  setSourceContext(context: GenerationSourceContext): void {
    const prevId = this.state.sourceContext?.submittalId;
    const idChanged = prevId !== undefined && prevId !== context.submittalId;

    this.state = {
      ...this.state,
      sourceContext: context,
      latestResult: idChanged ? null : this.state.latestResult,
      navigationFlags: {
        ...this.state.navigationFlags,
        sourceContextChanged: idChanged,
      },
    };
    this.notify();
  }

  // ─── Request State Lifecycle ──────────────────────────────────────

  /**
   * Begin a new generation request.
   * Transitions: idle → validating
   * Generates requestId and sets startedAt.
   */
  beginRequest(): string {
    const requestId = `REQ-${Date.now().toString(16)}-${Math.random().toString(36).slice(2, 6)}`;
    this.state = {
      ...this.state,
      requestState: {
        status: 'validating',
        requestId,
        startedAt: Date.now(),
      },
      navigationFlags: {
        ...this.state.navigationFlags,
        sourceContextChanged: false,
      },
    };
    this.notify();
    return requestId;
  }

  /**
   * Advance request to mapping phase.
   * Transitions: validating → mapping
   */
  advanceToMapping(): void {
    this.state = {
      ...this.state,
      requestState: {
        ...this.state.requestState,
        status: 'mapping',
      },
    };
    this.notify();
  }

  /**
   * Advance request to generating phase.
   * Transitions: mapping → generating
   */
  advanceToGenerating(): void {
    this.state = {
      ...this.state,
      requestState: {
        ...this.state.requestState,
        status: 'generating',
      },
    };
    this.notify();
  }

  /**
   * Complete request with success.
   * Sets latestResult (identity-bound to sourceContext.submittalId).
   * Sets viewerAutoOpenPending to true.
   */
  completeSuccess(result: LatestResult): void {
    this.state = {
      ...this.state,
      requestState: {
        ...this.state.requestState,
        status: 'success',
        completedAt: Date.now(),
      },
      latestResult: result,
      navigationFlags: {
        ...this.state.navigationFlags,
        viewerAutoOpenPending: true,
      },
    };
    this.notify();
  }

  /**
   * Complete request with error.
   * Sets errorCode and errorMessage. Does NOT set viewerAutoOpenPending.
   */
  completeError(errorCode: string, errorMessage: string): void {
    this.state = {
      ...this.state,
      requestState: {
        ...this.state.requestState,
        status: 'error',
        completedAt: Date.now(),
        errorCode,
        errorMessage,
      },
      navigationFlags: {
        ...this.state.navigationFlags,
        viewerAutoOpenPending: false,
      },
    };
    this.notify();
  }

  // ─── Navigation Flags ─────────────────────────────────────────────

  /**
   * Reset viewerAutoOpenPending after viewer navigation occurs.
   */
  resetViewerAutoOpen(): void {
    this.state = {
      ...this.state,
      navigationFlags: {
        ...this.state.navigationFlags,
        viewerAutoOpenPending: false,
      },
    };
    this.notify();
  }

  // ─── Clear ────────────────────────────────────────────────────────

  /** Clear all state. For testing and full reset. */
  clear(): void {
    this.state = { ...INITIAL_STATE };
    this.notify();
  }

  // ─── Subscribe ────────────────────────────────────────────────────

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
