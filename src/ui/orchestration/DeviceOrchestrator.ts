/**
 * Construction OS — Device Orchestrator
 *
 * Governs panel layout adaptation across device classes.
 * Preserves capability, not layout sameness.
 */

import type { DeviceClass, PanelId } from '../contracts/events';

export interface DeviceLayout {
  deviceClass: DeviceClass;
  visiblePanels: PanelId[];
  primaryPanel: PanelId;
  companionPanel?: PanelId;
  maxVisiblePanels: number;
  layoutMode: 'full-cockpit' | 'split' | 'compact' | 'single-companion';
}

const DEVICE_LAYOUTS: Record<DeviceClass, DeviceLayout> = {
  ultrawide: {
    deviceClass: 'ultrawide',
    visiblePanels: ['explorer', 'work', 'reference', 'spatial', 'system'],
    primaryPanel: 'work',
    maxVisiblePanels: 6,
    layoutMode: 'full-cockpit',
  },
  desktop: {
    deviceClass: 'desktop',
    visiblePanels: ['explorer', 'work', 'reference', 'system'],
    primaryPanel: 'work',
    maxVisiblePanels: 4,
    layoutMode: 'full-cockpit',
  },
  laptop: {
    deviceClass: 'laptop',
    visiblePanels: ['explorer', 'work', 'reference'],
    primaryPanel: 'work',
    maxVisiblePanels: 3,
    layoutMode: 'split',
  },
  tablet: {
    deviceClass: 'tablet',
    visiblePanels: ['work', 'explorer'],
    primaryPanel: 'work',
    companionPanel: 'explorer',
    maxVisiblePanels: 2,
    layoutMode: 'compact',
  },
  phone: {
    deviceClass: 'phone',
    visiblePanels: ['work'],
    primaryPanel: 'work',
    companionPanel: 'explorer',
    maxVisiblePanels: 1,
    layoutMode: 'single-companion',
  },
};

export function detectDeviceClass(): DeviceClass {
  if (typeof window === 'undefined') return 'desktop';
  const w = window.innerWidth;
  if (w >= 2560) return 'ultrawide';
  if (w >= 1440) return 'desktop';
  if (w >= 1024) return 'laptop';
  if (w >= 768) return 'tablet';
  return 'phone';
}

export function getDeviceLayout(deviceClass: DeviceClass): DeviceLayout {
  return DEVICE_LAYOUTS[deviceClass];
}

export function shouldShowPanel(panelId: PanelId, deviceClass: DeviceClass): boolean {
  const layout = DEVICE_LAYOUTS[deviceClass];
  return layout.visiblePanels.includes(panelId);
}

export function getCompanionPanel(deviceClass: DeviceClass): PanelId | undefined {
  return DEVICE_LAYOUTS[deviceClass].companionPanel;
}

export const ALL_DEVICE_CLASSES: DeviceClass[] = ['ultrawide', 'desktop', 'laptop', 'tablet', 'phone'];
