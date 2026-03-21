/**
 * Construction OS — Event Bus Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { EventBusImpl } from './EventBus';
import type { ObjectSelectedPayload, TruthEchoFailedPayload } from '../contracts/events';

describe('EventBus', () => {
  let bus: EventBusImpl;

  beforeEach(() => {
    bus = new EventBusImpl({ debug: false });
  });

  it('should deliver events to subscribers', async () => {
    const handler = vi.fn();
    bus.on('object.selected', handler);

    const payload: ObjectSelectedPayload = {
      object: { id: 'test-1', type: 'element', name: 'Test Element' },
      source: 'explorer',
      basis: 'mock',
    };

    bus.emit('object.selected', payload);

    // Wait for microtask
    await new Promise<void>((r) => queueMicrotask(r));
    expect(handler).toHaveBeenCalledWith(payload);
  });

  it('should support unsubscribe', async () => {
    const handler = vi.fn();
    const unsub = bus.on('object.selected', handler);
    unsub();

    bus.emit('object.selected', {
      object: { id: 'test-1', type: 'element', name: 'Test' },
      source: 'explorer',
      basis: 'mock',
    });

    await new Promise<void>((r) => queueMicrotask(r));
    expect(handler).not.toHaveBeenCalled();
  });

  it('should not throw when emitting with no subscribers', () => {
    expect(() => {
      bus.emit('object.selected', {
        object: { id: 'test-1', type: 'element', name: 'Test' },
        source: 'explorer',
        basis: 'mock',
      });
    }).not.toThrow();
  });

  it('should track event log', () => {
    bus.emit('truth-echo.failed', {
      reason: 'ambiguous_object',
      details: 'test',
      timestamp: Date.now(),
    } as TruthEchoFailedPayload);

    const log = bus.getLog();
    expect(log.length).toBe(1);
    expect(log[0].event).toBe('truth-echo.failed');
  });

  it('should report listener count', () => {
    expect(bus.listenerCount('object.selected')).toBe(0);
    const unsub = bus.on('object.selected', () => {});
    expect(bus.listenerCount('object.selected')).toBe(1);
    unsub();
    expect(bus.listenerCount('object.selected')).toBe(0);
  });

  it('should clear all handlers', () => {
    bus.on('object.selected', () => {});
    bus.on('zone.selected', () => {});
    bus.clear();
    expect(bus.listenerCount('object.selected')).toBe(0);
    expect(bus.listenerCount('zone.selected')).toBe(0);
  });
});
