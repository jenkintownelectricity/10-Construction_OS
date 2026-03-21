/**
 * Construction OS — Device Orchestrator Tests
 */

import { describe, it, expect } from 'vitest';
import { getDeviceLayout, shouldShowPanel, getCompanionPanel, ALL_DEVICE_CLASSES } from './DeviceOrchestrator';

describe('DeviceOrchestrator', () => {
  it('should define all 5 device classes', () => {
    expect(ALL_DEVICE_CLASSES).toEqual(['ultrawide', 'desktop', 'laptop', 'tablet', 'phone']);
  });

  it('should have work as primary panel for all device classes', () => {
    for (const dc of ALL_DEVICE_CLASSES) {
      expect(getDeviceLayout(dc).primaryPanel).toBe('work');
    }
  });

  it('ultrawide should support 4-6 visible panels', () => {
    const layout = getDeviceLayout('ultrawide');
    expect(layout.maxVisiblePanels).toBeGreaterThanOrEqual(4);
    expect(layout.maxVisiblePanels).toBeLessThanOrEqual(6);
    expect(layout.visiblePanels.length).toBe(5);
  });

  it('desktop should support 3-4 visible panels', () => {
    const layout = getDeviceLayout('desktop');
    expect(layout.maxVisiblePanels).toBeGreaterThanOrEqual(3);
    expect(layout.maxVisiblePanels).toBeLessThanOrEqual(4);
  });

  it('laptop should support 2-3 visible panels', () => {
    const layout = getDeviceLayout('laptop');
    expect(layout.maxVisiblePanels).toBeGreaterThanOrEqual(2);
    expect(layout.maxVisiblePanels).toBeLessThanOrEqual(3);
  });

  it('tablet should show 2 panels', () => {
    const layout = getDeviceLayout('tablet');
    expect(layout.maxVisiblePanels).toBe(2);
  });

  it('phone should show 1 panel with companion', () => {
    const layout = getDeviceLayout('phone');
    expect(layout.maxVisiblePanels).toBe(1);
    expect(layout.companionPanel).toBeDefined();
    expect(layout.layoutMode).toBe('single-companion');
  });

  it('phone companion should be explorer', () => {
    expect(getCompanionPanel('phone')).toBe('explorer');
  });

  it('should correctly report panel visibility per device class', () => {
    expect(shouldShowPanel('spatial', 'ultrawide')).toBe(true);
    expect(shouldShowPanel('spatial', 'desktop')).toBe(false);
    expect(shouldShowPanel('work', 'phone')).toBe(true);
    expect(shouldShowPanel('spatial', 'phone')).toBe(false);
  });
});
