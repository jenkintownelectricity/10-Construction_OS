/**
 * Construction OS — Active Object Store Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { activeObjectStore } from './activeObjectStore';

describe('ActiveObjectStore', () => {
  beforeEach(() => {
    activeObjectStore.reset();
  });

  it('should start with null active object', () => {
    const state = activeObjectStore.getState();
    expect(state.activeObject).toBeNull();
    expect(state.sourcePanel).toBeNull();
  });

  it('should set active object and notify listeners', () => {
    const listener = vi.fn();
    activeObjectStore.subscribe(listener);

    const success = activeObjectStore.setActiveObject(
      { id: 'test-1', type: 'element', name: 'Test Element' },
      'explorer',
      'mock'
    );

    expect(success).toBe(true);
    expect(listener).toHaveBeenCalled();

    const state = activeObjectStore.getState();
    expect(state.activeObject?.id).toBe('test-1');
    expect(state.sourcePanel).toBe('explorer');
    expect(state.basis).toBe('mock');
  });

  it('should fail closed on null object', () => {
    const success = activeObjectStore.setActiveObject(null, 'explorer');
    expect(success).toBe(false);

    const state = activeObjectStore.getState();
    expect(state.activeObject).toBeNull();
    expect(state.echoFailure).toContain('ambiguous_object');
  });

  it('should fail closed on object without id', () => {
    const success = activeObjectStore.setActiveObject(
      { id: '', type: 'element', name: 'Empty' },
      'explorer'
    );
    expect(success).toBe(false);
  });

  it('should maintain active object identity across panel changes', () => {
    activeObjectStore.setActiveObject(
      { id: 'obj-1', type: 'element', name: 'First' },
      'explorer'
    );

    // Simulate a different panel selecting the same object
    activeObjectStore.setActiveObject(
      { id: 'obj-1', type: 'element', name: 'First' },
      'spatial'
    );

    const state = activeObjectStore.getState();
    expect(state.activeObject?.id).toBe('obj-1');
    expect(state.sourcePanel).toBe('spatial');
  });

  it('should track following panels', () => {
    const state = activeObjectStore.getState();
    expect(state.followingPanels.has('explorer')).toBe(true);

    activeObjectStore.setPanelFollowing('explorer', false);
    expect(activeObjectStore.getState().followingPanels.has('explorer')).toBe(false);

    activeObjectStore.setPanelFollowing('explorer', true);
    expect(activeObjectStore.getState().followingPanels.has('explorer')).toBe(true);
  });

  it('should handle workspace mode changes', () => {
    activeObjectStore.setWorkspaceMode('compare');
    expect(activeObjectStore.getState().workspaceMode).toBe('compare');
  });

  it('should handle pinned companion', () => {
    activeObjectStore.setPinnedCompanion('explorer');
    expect(activeObjectStore.getState().pinnedCompanion).toBe('explorer');
  });

  it('should clear echo failure on successful object set', () => {
    activeObjectStore.setActiveObject(null, 'explorer');
    expect(activeObjectStore.getState().echoFailure).toBeTruthy();

    activeObjectStore.setActiveObject(
      { id: 'good-1', type: 'element', name: 'Good' },
      'explorer'
    );
    expect(activeObjectStore.getState().echoFailure).toBeNull();
  });

  it('should unsubscribe correctly', () => {
    const listener = vi.fn();
    const unsub = activeObjectStore.subscribe(listener);

    activeObjectStore.setWorkspaceMode('focus');
    expect(listener).toHaveBeenCalledTimes(1);

    unsub();
    activeObjectStore.setWorkspaceMode('review');
    expect(listener).toHaveBeenCalledTimes(1); // Should not increase
  });
});
