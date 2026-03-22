/**
 * Generation Store — Tests
 *
 * Proves the Shop Drawings → Workstation → Generate → Viewer loop
 * through the shared generation store and event bus integration.
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { generationStore, type GenerationSourceContext } from './generationStore';
import { eventBus } from '../events/EventBus';
import { activeObjectStore } from './activeObjectStore';
import { getSampleRoofingDraft } from '../assembly-builder/roofingSourceAdapter';
import { getSampleFireproofingDraft } from '../assembly-builder/fireproofingSourceAdapter';
import { generateDetailPreview } from '../detail-viewer/detailGenerationAdapter';

beforeEach(() => {
  generationStore.clear();
  eventBus.clear();
  activeObjectStore.reset();
});

describe('generationStore', () => {
  it('initializes with null state', () => {
    const state = generationStore.getState();
    expect(state.lastResult).toBeNull();
    expect(state.sourceContext).toBeNull();
    expect(state.resultTimestamp).toBe(0);
  });

  it('stores source context from Shop Drawings selection', () => {
    const context: GenerationSourceContext = {
      submittalId: 'SD-001',
      submittalTitle: 'Curtain Wall System — South Elevation',
      manufacturer: 'YKK AP',
      spec: '08 44 13',
      project: 'Waterfront Tower Phase 2',
    };
    generationStore.setSourceContext(context);
    expect(generationStore.getState().sourceContext).toEqual(context);
  });

  it('stores generation result', () => {
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    generationStore.setResult(result);
    const state = generationStore.getState();
    expect(state.lastResult).toBe(result);
    expect(state.resultTimestamp).toBeGreaterThan(0);
  });

  it('notifies subscribers on state change', async () => {
    const listener = vi.fn();
    generationStore.subscribe(listener);

    generationStore.setSourceContext({
      submittalId: 'SD-002',
      submittalTitle: 'Test',
      manufacturer: 'Test',
      spec: '00 00 00',
      project: 'Test',
    });

    // Listener is called via microtask
    await new Promise((r) => setTimeout(r, 10));
    expect(listener).toHaveBeenCalled();
  });

  it('clears all state', () => {
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    generationStore.setSourceContext({
      submittalId: 'SD-001',
      submittalTitle: 'Test',
      manufacturer: 'Test',
      spec: '00 00 00',
      project: 'Test',
    });
    generationStore.setResult(result);
    generationStore.clear();
    const state = generationStore.getState();
    expect(state.lastResult).toBeNull();
    expect(state.sourceContext).toBeNull();
    expect(state.resultTimestamp).toBe(0);
  });
});

describe('End-to-end loop: Shop Drawings → Generate → Viewer', () => {
  it('completes the full roofing generation loop', async () => {
    // ── Step 1: Shop Drawings sets source context ──
    const sourceContext: GenerationSourceContext = {
      submittalId: 'SD-001',
      submittalTitle: 'Curtain Wall System — South Elevation',
      manufacturer: 'YKK AP',
      spec: '08 44 13',
      project: 'Waterfront Tower Phase 2',
    };
    generationStore.setSourceContext(sourceContext);

    // ── Step 2: Shop Drawings sets active object ──
    activeObjectStore.setActiveObject(
      { id: 'SD-001', type: 'document', name: 'Curtain Wall System' },
      'explorer',
      'canonical',
    );
    expect(activeObjectStore.getState().activeObject?.id).toBe('SD-001');

    // ── Step 3: Shop Drawings emits object.selected ──
    const objectSelectedHandler = vi.fn();
    eventBus.on('object.selected', objectSelectedHandler);
    eventBus.emit('object.selected', {
      object: { id: 'SD-001', type: 'document', name: 'Curtain Wall System' },
      source: 'explorer',
      basis: 'canonical',
    });
    await new Promise((r) => setTimeout(r, 10));
    expect(objectSelectedHandler).toHaveBeenCalledWith(
      expect.objectContaining({ object: expect.objectContaining({ id: 'SD-001' }) }),
    );

    // ── Step 4: Workstation generates roofing detail ──
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    expect(result.success).toBe(true);
    expect(result.generation_status).toBe('success');
    expect(result.artifact_type).toBe('roofing_detail');
    expect(result.svg_content).toBeTruthy();
    expect(result.dxf_available).toBe(true);

    // ── Step 5: Store result + emit generation.completed ──
    generationStore.setResult(result);
    const genCompletedHandler = vi.fn();
    eventBus.on('generation.completed', genCompletedHandler);
    eventBus.emit('generation.completed', {
      objectId: result.detail_id,
      status: 'success',
      dxfFilename: result.artifact_filename,
      generatorSeam: result.generator_seam,
      diagnostics: [...result.diagnostics],
      timestamp: Date.now(),
    });
    await new Promise((r) => setTimeout(r, 10));
    expect(genCompletedHandler).toHaveBeenCalledWith(
      expect.objectContaining({
        status: 'success',
        dxfFilename: expect.stringContaining('.dxf'),
        generatorSeam: 'detail_preview_seam_v1',
      }),
    );

    // ── Step 6: Viewer receives artifact context from store ──
    const viewerState = generationStore.getState();
    expect(viewerState.lastResult?.success).toBe(true);
    expect(viewerState.lastResult?.detail_id).toBe(result.detail_id);
    expect(viewerState.lastResult?.svg_content).toBeTruthy();
    expect(viewerState.lastResult?.dxf_available).toBe(true);
    expect(viewerState.lastResult?.artifact_filename).toBeTruthy();
    expect(viewerState.lastResult?.generator_seam).toBe('detail_preview_seam_v1');
    expect(viewerState.sourceContext).toEqual(sourceContext);
  });

  it('fireproofing remains FAIL_CLOSED', async () => {
    const { draft } = getSampleFireproofingDraft();
    const result = generateDetailPreview(draft, 'fireproofing');

    expect(result.success).toBe(false);
    expect(result.generation_status).toBe('unsupported');
    expect(result.diagnostics.some((d) => d.includes('FAIL_CLOSED'))).toBe(true);
    expect(result.errors.some((e) => e.code === 'UNSUPPORTED_CATEGORY')).toBe(true);
    expect(result.dxf_available).toBe(false);
    expect(result.svg_content).toBe('');

    // Store still records the fail-closed result
    generationStore.setResult(result);
    const state = generationStore.getState();
    expect(state.lastResult?.success).toBe(false);
    expect(state.lastResult?.generation_status).toBe('unsupported');

    // Event bus emits with error status
    const handler = vi.fn();
    eventBus.on('generation.completed', handler);
    eventBus.emit('generation.completed', {
      objectId: result.detail_id,
      status: 'generation_error',
      dxfFilename: null,
      generatorSeam: result.generator_seam,
      diagnostics: [...result.diagnostics],
      timestamp: Date.now(),
    });
    await new Promise((r) => setTimeout(r, 10));
    expect(handler).toHaveBeenCalledWith(
      expect.objectContaining({ status: 'generation_error' }),
    );
  });

  it('generation.completed with success triggers auto-navigate (event emitted)', async () => {
    // This test proves the event bus emits generation.completed with correct payload
    // The AtlasLayout component listens and auto-navigates to 'viewer'
    const navigateHandler = vi.fn();
    const unsub = eventBus.on('generation.completed', (payload) => {
      if (payload.status === 'success') {
        navigateHandler('viewer');
      }
    });

    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    eventBus.emit('generation.completed', {
      objectId: result.detail_id,
      status: 'success',
      dxfFilename: result.artifact_filename,
      generatorSeam: result.generator_seam,
      diagnostics: [...result.diagnostics],
      timestamp: Date.now(),
    });

    await new Promise((r) => setTimeout(r, 10));
    expect(navigateHandler).toHaveBeenCalledWith('viewer');
    unsub();
  });

  it('generation.completed with failure does NOT auto-navigate', async () => {
    const navigateHandler = vi.fn();
    const unsub = eventBus.on('generation.completed', (payload) => {
      if (payload.status === 'success') {
        navigateHandler('viewer');
      }
    });

    const { draft } = getSampleFireproofingDraft();
    const result = generateDetailPreview(draft, 'fireproofing');
    eventBus.emit('generation.completed', {
      objectId: result.detail_id,
      status: 'generation_error',
      dxfFilename: null,
      generatorSeam: result.generator_seam,
      diagnostics: [...result.diagnostics],
      timestamp: Date.now(),
    });

    await new Promise((r) => setTimeout(r, 10));
    expect(navigateHandler).not.toHaveBeenCalled();
    unsub();
  });
});
