/**
 * Generation Store — Tests
 *
 * Proves:
 *   - Locked schema enforcement (exactly 4 top-level keys)
 *   - sourceContext identity binding
 *   - requestState lifecycle: idle → validating → mapping → generating → success|error
 *   - latestResult cleared on sourceContext.submittalId change
 *   - navigationFlags behavior
 *   - Full Shop Drawings → Workstation → Generate → Viewer loop
 *   - Fireproofing FAIL_CLOSED
 *   - generationStore remains thin Ring 3 transport (no history, no caches)
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  generationStore,
  type GenerationSourceContext,
  type LatestResult,
} from './generationStore';
import { eventBus } from '../events/EventBus';
import { activeObjectStore } from './activeObjectStore';
import { validateSourceContext } from '../detail-viewer/validateSourceContext';
import { mapContextToRoofingDraft } from '../detail-viewer/contextToRoofingDraft';
import { generateDetailPreview } from '../detail-viewer/detailGenerationAdapter';
import { getSampleFireproofingDraft } from '../assembly-builder/fireproofingSourceAdapter';

beforeEach(() => {
  generationStore.clear();
  eventBus.clear();
  activeObjectStore.reset();
});

// ─── Source Context ───────────────────────────────────────────────────

const ROOFING_CONTEXT: GenerationSourceContext = {
  submittalId: 'SD-002',
  title: 'Roof Membrane Assembly — Full Plan',
  manufacturer: 'Carlisle SynTec',
  spec: '07 52 16',
  project: 'Heritage Plaza',
};

const NON_ROOFING_CONTEXT: GenerationSourceContext = {
  submittalId: 'SD-001',
  title: 'Curtain Wall System — South Elevation',
  manufacturer: 'YKK AP',
  spec: '08 44 13',
  project: 'Waterfront Tower Phase 2',
};

describe('generationStore — locked schema', () => {
  it('initializes with exactly 4 top-level keys', () => {
    const state = generationStore.getState();
    const keys = Object.keys(state).sort();
    expect(keys).toEqual(['latestResult', 'navigationFlags', 'requestState', 'sourceContext']);
  });

  it('initializes with null sourceContext', () => {
    expect(generationStore.getState().sourceContext).toBeNull();
  });

  it('initializes with idle requestState', () => {
    const rs = generationStore.getState().requestState;
    expect(rs.status).toBe('idle');
    expect(rs.requestId).toBe('');
    expect(rs.startedAt).toBe(0);
  });

  it('initializes with null latestResult', () => {
    expect(generationStore.getState().latestResult).toBeNull();
  });

  it('initializes with default navigationFlags', () => {
    const nf = generationStore.getState().navigationFlags;
    expect(nf.viewerAutoOpenPending).toBe(false);
    expect(nf.sourceContextChanged).toBe(false);
  });
});

describe('generationStore — sourceContext', () => {
  it('stores source context', () => {
    generationStore.setSourceContext(ROOFING_CONTEXT);
    expect(generationStore.getState().sourceContext).toEqual(ROOFING_CONTEXT);
  });

  it('sourceContextChanged=true when submittalId changes', () => {
    generationStore.setSourceContext(ROOFING_CONTEXT);
    generationStore.setSourceContext({ ...ROOFING_CONTEXT, submittalId: 'SD-099' });
    expect(generationStore.getState().navigationFlags.sourceContextChanged).toBe(true);
  });

  it('clears latestResult when submittalId changes', () => {
    generationStore.setSourceContext(ROOFING_CONTEXT);
    generationStore.completeSuccess({
      sourceSubmittalId: 'SD-002',
      detailId: 'DRAFT-ROOF-SD-002',
      artifactType: 'roofing_detail',
      filename: 'DRAFT-ROOF-SD-002.dxf',
      success: true,
      generationStatus: 'success',
      artifactIds: ['ART-1'],
    });
    expect(generationStore.getState().latestResult).not.toBeNull();

    // Change submittalId → latestResult cleared
    generationStore.setSourceContext({ ...ROOFING_CONTEXT, submittalId: 'SD-099' });
    expect(generationStore.getState().latestResult).toBeNull();
  });

  it('does NOT clear latestResult when submittalId stays the same', () => {
    generationStore.setSourceContext(ROOFING_CONTEXT);
    generationStore.completeSuccess({
      sourceSubmittalId: 'SD-002',
      detailId: 'D',
      artifactType: 'roofing_detail',
      filename: 'D.dxf',
      success: true,
      generationStatus: 'success',
    });
    // Re-set same context
    generationStore.setSourceContext(ROOFING_CONTEXT);
    expect(generationStore.getState().latestResult).not.toBeNull();
  });

  it('notifies subscribers on change', async () => {
    const listener = vi.fn();
    generationStore.subscribe(listener);
    generationStore.setSourceContext(ROOFING_CONTEXT);
    await new Promise((r) => setTimeout(r, 10));
    expect(listener).toHaveBeenCalled();
  });
});

describe('generationStore — requestState lifecycle', () => {
  it('follows locked lifecycle: idle → validating → mapping → generating → success', () => {
    expect(generationStore.getState().requestState.status).toBe('idle');

    const reqId = generationStore.beginRequest();
    expect(generationStore.getState().requestState.status).toBe('validating');
    expect(generationStore.getState().requestState.requestId).toBe(reqId);
    expect(generationStore.getState().requestState.startedAt).toBeGreaterThan(0);

    generationStore.advanceToMapping();
    expect(generationStore.getState().requestState.status).toBe('mapping');

    generationStore.advanceToGenerating();
    expect(generationStore.getState().requestState.status).toBe('generating');

    generationStore.completeSuccess({
      sourceSubmittalId: 'SD-002',
      detailId: 'D',
      artifactType: 'roofing_detail',
      filename: 'D.dxf',
      success: true,
      generationStatus: 'success',
    });
    expect(generationStore.getState().requestState.status).toBe('success');
    expect(generationStore.getState().requestState.completedAt).toBeGreaterThan(0);
  });

  it('follows locked lifecycle: idle → validating → error', () => {
    generationStore.beginRequest();
    generationStore.completeError('NO_SOURCE_CONTEXT', 'No context');
    const rs = generationStore.getState().requestState;
    expect(rs.status).toBe('error');
    expect(rs.completedAt).toBeGreaterThan(0);
    expect(rs.errorCode).toBe('NO_SOURCE_CONTEXT');
    expect(rs.errorMessage).toBe('No context');
  });

  it('requestId is unique per beginRequest call', () => {
    const id1 = generationStore.beginRequest();
    generationStore.clear();
    const id2 = generationStore.beginRequest();
    expect(id1).not.toBe(id2);
  });
});

describe('generationStore — navigationFlags', () => {
  it('viewerAutoOpenPending becomes true only on success', () => {
    generationStore.beginRequest();
    generationStore.advanceToMapping();
    generationStore.advanceToGenerating();
    generationStore.completeSuccess({
      sourceSubmittalId: 'SD-002',
      detailId: 'D',
      artifactType: 'roofing_detail',
      filename: 'D.dxf',
      success: true,
      generationStatus: 'success',
    });
    expect(generationStore.getState().navigationFlags.viewerAutoOpenPending).toBe(true);
  });

  it('viewerAutoOpenPending stays false on error', () => {
    generationStore.beginRequest();
    generationStore.completeError('ERR', 'fail');
    expect(generationStore.getState().navigationFlags.viewerAutoOpenPending).toBe(false);
  });

  it('viewerAutoOpenPending resets after resetViewerAutoOpen', () => {
    generationStore.beginRequest();
    generationStore.advanceToMapping();
    generationStore.advanceToGenerating();
    generationStore.completeSuccess({
      sourceSubmittalId: 'SD-002',
      detailId: 'D',
      artifactType: 'roofing_detail',
      filename: 'D.dxf',
      success: true,
      generationStatus: 'success',
    });
    expect(generationStore.getState().navigationFlags.viewerAutoOpenPending).toBe(true);
    generationStore.resetViewerAutoOpen();
    expect(generationStore.getState().navigationFlags.viewerAutoOpenPending).toBe(false);
  });

  it('sourceContextChanged clears on beginRequest', () => {
    generationStore.setSourceContext(ROOFING_CONTEXT);
    generationStore.setSourceContext({ ...ROOFING_CONTEXT, submittalId: 'SD-099' });
    expect(generationStore.getState().navigationFlags.sourceContextChanged).toBe(true);
    generationStore.beginRequest();
    expect(generationStore.getState().navigationFlags.sourceContextChanged).toBe(false);
  });
});

describe('generationStore — latestResult identity binding', () => {
  it('latestResult.sourceSubmittalId must match sourceContext.submittalId', () => {
    generationStore.setSourceContext(ROOFING_CONTEXT);
    const result: LatestResult = {
      sourceSubmittalId: 'SD-002',
      detailId: 'DRAFT-ROOF-SD-002',
      artifactType: 'roofing_detail',
      filename: 'DRAFT-ROOF-SD-002.dxf',
      success: true,
      generationStatus: 'success',
      artifactIds: ['ART-SVG-1', 'ART-DXF-1'],
    };
    generationStore.completeSuccess(result);
    const state = generationStore.getState();
    expect(state.latestResult!.sourceSubmittalId).toBe(state.sourceContext!.submittalId);
  });
});

describe('generationStore — boundary enforcement', () => {
  it('contains no history arrays', () => {
    const state = generationStore.getState();
    for (const value of Object.values(state)) {
      if (Array.isArray(value)) {
        throw new Error('generationStore must not contain arrays at top level');
      }
    }
  });

  it('clear() resets to initial state', () => {
    generationStore.setSourceContext(ROOFING_CONTEXT);
    generationStore.beginRequest();
    generationStore.advanceToMapping();
    generationStore.clear();
    const state = generationStore.getState();
    expect(state.sourceContext).toBeNull();
    expect(state.requestState.status).toBe('idle');
    expect(state.latestResult).toBeNull();
    expect(state.navigationFlags.viewerAutoOpenPending).toBe(false);
    expect(state.navigationFlags.sourceContextChanged).toBe(false);
  });
});

describe('End-to-end: Shop Drawings → Validate → Map → Generate → Viewer', () => {
  it('completes full context-driven roofing generation loop', async () => {
    // ── Step 1: Shop Drawings sets source context ──
    generationStore.setSourceContext(ROOFING_CONTEXT);
    activeObjectStore.setActiveObject(
      { id: 'SD-002', type: 'document', name: ROOFING_CONTEXT.title },
      'explorer',
      'canonical',
    );

    // ── Step 2: Begin request ──
    const reqId = generationStore.beginRequest();
    expect(reqId).toBeTruthy();

    // ── Step 3: Validate source context ──
    const validation = validateSourceContext(ROOFING_CONTEXT);
    expect(validation.valid).toBe(true);

    // ── Step 4: Map context to draft ──
    generationStore.advanceToMapping();
    const mapping = mapContextToRoofingDraft(ROOFING_CONTEXT);
    expect(mapping.success).toBe(true);
    expect(mapping.draft).toBeDefined();

    // ── Step 5: Generate roofing detail ──
    generationStore.advanceToGenerating();
    const genResult = generateDetailPreview(mapping.draft!, 'roofing');
    expect(genResult.success).toBe(true);
    expect(genResult.generation_status).toBe('success');
    expect(genResult.svg_content).toBeTruthy();
    expect(genResult.dxf_available).toBe(true);

    // ── Step 6: Store result ──
    const latestResult: LatestResult = {
      sourceSubmittalId: ROOFING_CONTEXT.submittalId,
      detailId: genResult.detail_id,
      artifactType: genResult.artifact_type,
      filename: genResult.artifact_filename,
      success: genResult.success,
      generationStatus: genResult.generation_status,
      artifactIds: [genResult.svg_artifact_id, genResult.dxf_artifact_id].filter(Boolean),
    };
    generationStore.completeSuccess(latestResult);

    // ── Step 7: Emit generation.completed ──
    const handler = vi.fn();
    eventBus.on('generation.completed', handler);
    eventBus.emit('generation.completed', {
      objectId: genResult.detail_id,
      status: 'success',
      dxfFilename: genResult.artifact_filename,
      generatorSeam: genResult.generator_seam,
      diagnostics: [...genResult.diagnostics],
      timestamp: Date.now(),
    });
    await new Promise((r) => setTimeout(r, 10));
    expect(handler).toHaveBeenCalledWith(
      expect.objectContaining({ status: 'success' }),
    );

    // ── Step 8: Verify store state ──
    const finalState = generationStore.getState();
    expect(finalState.requestState.status).toBe('success');
    expect(finalState.latestResult!.sourceSubmittalId).toBe('SD-002');
    expect(finalState.latestResult!.success).toBe(true);
    expect(finalState.navigationFlags.viewerAutoOpenPending).toBe(true);

    // ── Step 9: Viewer auto-open resets flag ──
    generationStore.resetViewerAutoOpen();
    expect(generationStore.getState().navigationFlags.viewerAutoOpenPending).toBe(false);
  });

  it('non-roofing source context FAIL_CLOSED at validation', () => {
    generationStore.setSourceContext(NON_ROOFING_CONTEXT);
    generationStore.beginRequest();

    const validation = validateSourceContext(NON_ROOFING_CONTEXT);
    expect(validation.valid).toBe(false);
    expect(validation.errorCode).toBe('NON_ROOFING_SPEC');

    generationStore.completeError(validation.errorCode!, validation.errorMessage!);
    const state = generationStore.getState();
    expect(state.requestState.status).toBe('error');
    expect(state.requestState.errorCode).toBe('NON_ROOFING_SPEC');
    expect(state.navigationFlags.viewerAutoOpenPending).toBe(false);
    expect(state.latestResult).toBeNull();
  });

  it('fireproofing remains FAIL_CLOSED via generation seam', () => {
    const { draft } = getSampleFireproofingDraft();
    const result = generateDetailPreview(draft, 'fireproofing');
    expect(result.success).toBe(false);
    expect(result.generation_status).toBe('unsupported');
    expect(result.diagnostics.some((d) => d.includes('FAIL_CLOSED'))).toBe(true);
    expect(result.errors.some((e) => e.code === 'UNSUPPORTED_CATEGORY')).toBe(true);
  });

  it('auto-navigate triggers only on success via eventBus', async () => {
    const navigateHandler = vi.fn();
    eventBus.on('generation.completed', (payload) => {
      if (payload.status === 'success') navigateHandler('viewer');
    });

    // Error case — no navigate
    eventBus.emit('generation.completed', {
      objectId: 'D',
      status: 'generation_error',
      dxfFilename: null,
      generatorSeam: 'detail_preview_seam_v1',
      diagnostics: [],
      timestamp: Date.now(),
    });
    await new Promise((r) => setTimeout(r, 10));
    expect(navigateHandler).not.toHaveBeenCalled();

    // Success case — navigate
    eventBus.emit('generation.completed', {
      objectId: 'D',
      status: 'success',
      dxfFilename: 'D.dxf',
      generatorSeam: 'detail_preview_seam_v1',
      diagnostics: [],
      timestamp: Date.now(),
    });
    await new Promise((r) => setTimeout(r, 10));
    expect(navigateHandler).toHaveBeenCalledWith('viewer');
  });
});
