/**
 * Construction OS — Truth Echo Tests
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { initTruthEcho, destroyTruthEcho } from './TruthEcho';
import { eventBus } from '../events/EventBus';
import { activeObjectStore } from '../stores/activeObjectStore';

describe('TruthEcho', () => {
  beforeEach(() => {
    eventBus.clear();
    activeObjectStore.reset();
    initTruthEcho();
  });

  afterEach(() => {
    destroyTruthEcho();
  });

  it('should propagate object selection from Explorer to other panels', async () => {
    const propagated = vi.fn();
    eventBus.on('truth-echo.propagated', propagated);

    eventBus.emit('object.selected', {
      object: { id: 'asm-001', type: 'assembly', name: 'Steel Assembly A1' },
      source: 'explorer',
      basis: 'mock',
    });

    // Wait for microtask chain (emit → TruthEcho handler → propagation)
    await new Promise((r) => setTimeout(r, 50));

    expect(activeObjectStore.getState().activeObject?.id).toBe('asm-001');
    expect(activeObjectStore.getState().sourcePanel).toBe('explorer');
    expect(propagated).toHaveBeenCalled();

    const payload = propagated.mock.calls[0][0];
    expect(payload.originPanel).toBe('explorer');
    expect(payload.subscribedPanels).not.toContain('explorer');
    expect(payload.subscribedPanels).toContain('work');
    expect(payload.subscribedPanels).toContain('reference');
    expect(payload.subscribedPanels).toContain('system');
  });

  it('should propagate object selection from Spatial to other panels', async () => {
    const propagated = vi.fn();
    eventBus.on('truth-echo.propagated', propagated);

    eventBus.emit('object.selected', {
      object: { id: 'elem-001', type: 'element', name: 'Column C-14' },
      source: 'spatial',
      basis: 'mock',
    });

    await new Promise((r) => setTimeout(r, 50));

    expect(activeObjectStore.getState().activeObject?.id).toBe('elem-001');
    expect(propagated).toHaveBeenCalled();

    const payload = propagated.mock.calls[0][0];
    expect(payload.originPanel).toBe('spatial');
    expect(payload.subscribedPanels).toContain('explorer');
    expect(payload.subscribedPanels).toContain('work');
    expect(payload.subscribedPanels).toContain('reference');
    expect(payload.subscribedPanels).toContain('system');
    expect(payload.subscribedPanels).not.toContain('spatial');
  });

  it('should propagate zone selection', async () => {
    const propagated = vi.fn();
    eventBus.on('truth-echo.propagated', propagated);

    eventBus.emit('zone.selected', {
      zoneId: 'zone-001',
      zoneName: 'Zone A',
      source: 'spatial',
      containedObjects: ['asm-001', 'asm-002'],
    });

    await new Promise((r) => setTimeout(r, 50));

    expect(activeObjectStore.getState().activeObject?.id).toBe('zone-001');
    expect(activeObjectStore.getState().activeObject?.type).toBe('zone');
    expect(propagated).toHaveBeenCalled();
  });

  it('should fail closed on ambiguous object (null)', async () => {
    const failed = vi.fn();
    eventBus.on('truth-echo.failed', failed);

    eventBus.emit('object.selected', {
      object: null as any,
      source: 'explorer',
      basis: 'mock',
    });

    await new Promise((r) => setTimeout(r, 50));

    expect(failed).toHaveBeenCalled();
    expect(failed.mock.calls[0][0].reason).toBe('ambiguous_object');
    expect(activeObjectStore.getState().activeObject).toBeNull();
  });

  it('should fail closed on object with empty id', async () => {
    const failed = vi.fn();
    eventBus.on('truth-echo.failed', failed);

    eventBus.emit('object.selected', {
      object: { id: '', type: 'element', name: 'Empty' },
      source: 'explorer',
      basis: 'mock',
    });

    await new Promise((r) => setTimeout(r, 50));

    expect(failed).toHaveBeenCalled();
    expect(failed.mock.calls[0][0].reason).toBe('ambiguous_object');
  });

  it('should fail closed on zone with empty id', async () => {
    const failed = vi.fn();
    eventBus.on('truth-echo.failed', failed);

    eventBus.emit('zone.selected', {
      zoneId: '',
      zoneName: '',
      source: 'spatial',
    });

    await new Promise((r) => setTimeout(r, 50));

    expect(failed).toHaveBeenCalled();
  });

  it('should exclude unfollowing panels from propagation', async () => {
    activeObjectStore.setPanelFollowing('work', false);

    const propagated = vi.fn();
    eventBus.on('truth-echo.propagated', propagated);

    eventBus.emit('object.selected', {
      object: { id: 'test-1', type: 'element', name: 'Test' },
      source: 'explorer',
      basis: 'mock',
    });

    await new Promise((r) => setTimeout(r, 50));

    expect(propagated).toHaveBeenCalled();
    const payload = propagated.mock.calls[0][0];
    expect(payload.subscribedPanels).not.toContain('work');
  });
});
